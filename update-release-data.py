import argparse
import concurrent.futures
import importlib
import json
import logging
import os
import signal
import sys
import threading
import time
from collections import defaultdict
from pathlib import Path

from deepdiff import DeepDiff

from src.common import proc
from src.common.endoflife import AutoConfig, ProductFrontmatter, list_products
from src.common.gha import GitHubOutput, GitHubStepSummary
from src.common.releasedata import DATA_DIR, SRC_DIR

SCRIPT_DIR = Path(__file__).resolve().parent

# Set by run_scripts() so that the SIGINT handler can shut down the executor (and thus stop
# submitting new work) in addition to killing already-running subprocesses.
_executor: concurrent.futures.ThreadPoolExecutor = None


def _handle_sigint(_signum: int, _frame: any) -> None:
    logging.warning("received interrupt, killing all subprocesses and exiting")

    if _executor is not None:
        _executor.shutdown(wait=False, cancel_futures=True)

    proc.kill_all()

    # Some worker threads may still be blocked on a call that ignores the killed subprocess (or
    # has none to kill), and non-daemon executor threads would otherwise prevent the interpreter
    # from exiting. Terminate immediately rather than waiting for them to notice.
    os._exit(130)

# Name of the product being updated in the current thread, so that every log line emitted while running its
# scripts (including those from shared modules like src/common/http.py) is prefixed with the product name.
# Stored in a thread-local because products are updated in parallel worker threads.
_product_context = threading.local()


class _ProductPrefixFormatter(logging.Formatter):
    """Formats log records, prefixing them with the product being updated in the current thread,
    or "main" for log lines emitted outside of any product's update (e.g. setup/summary steps)."""

    def format(self, record: logging.LogRecord) -> str:  # noqa: A003
        message = super().format(record)
        product = getattr(_product_context, "name", None) or "main"
        return f"[{product}] {message}"


# Default auto configs implicitly added around each product's own configs (see run_scripts below).
# These correspond to src/_copy_product_releases.py and src/_remove_invalid_releases.py.
COPY_PRODUCT_RELEASES_METHOD = "_copy_product_releases"
REMOVE_INVALID_RELEASES_METHOD = "_remove_invalid_releases"

# Number of products updated in parallel. Keep it modest: scripts may each launch a Playwright browser
# (src/common/http.py) and fan out to up to 16 concurrent HTTP requests, so a higher value would multiply
# the memory/connection usage. Parallelism is bounded by the number of products anyway.
MAX_WORKERS = 4


class ScriptExecutionSummary:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.success_by_product = defaultdict(lambda: True)
        self.success_by_script = defaultdict(lambda: True)
        self.durations_by_product = defaultdict(float)
        self.durations_by_script = defaultdict(float)
        self.scripts_by_product = defaultdict(list)
        self.products_by_script = defaultdict(list)

    def register(self, script: str, product: str, duration: float, success: bool) -> None:
        with self._lock:
            self.success_by_product[product] = self.success_by_product[product] and success
            self.success_by_script[script] = self.success_by_script[script] and success
            self.durations_by_product[product] += duration
            self.durations_by_script[script] += duration
            self.scripts_by_product[product].append(script)
            self.products_by_script[script].append(product)

    def print_summary(self, summary: GitHubStepSummary, min_duration: float = 3) -> None:
        summary.println("## Script execution summary\n")
        summary.println(f"Executions below {min_duration} seconds are hidden except in case of failure.\n")
        summary.println("### By products\n")
        summary.println("| Name | Duration | Scripts | Succeeded |")
        summary.println("|------|----------|---------|-----------|")
        for product, duration in sorted(self.durations_by_product.items(), key=lambda x: x[1], reverse=True):
            if duration >= min_duration or not self.success_by_product[product]:
                scripts = ', '.join(self.scripts_by_product[product])
                success = '✅' if self.success_by_product[product] else '❌'
                summary.println(f"| {product} | {duration:.2f}s | {scripts} | {success} |")

        summary.println("\n### By scripts\n")
        summary.println("| Name | Duration | #Products | Succeeded |")
        summary.println("|------|----------|-----------|-----------|")
        for script, duration in sorted(self.durations_by_script.items(), key=lambda x: x[1], reverse=True):
            if duration >= min_duration or not self.products_by_script[script]:
                product_count = len(self.products_by_script[script])
                success = '✅' if self.success_by_script[script] else '❌'
                summary.println(f"| {script} | {duration:.2f}s | {product_count} | {success} |")

        summary.println("")

    def any_failure(self) -> bool:
        return not all(self.success_by_product.values())


def install_playwright() -> None:
    logging.info("Installing Playwright")
    proc.run(['playwright', 'install', 'chromium'], timeout=120, check=True)
    logging.info("Playwright installed")


def __product_data_path(product: ProductFrontmatter) -> Path:
    return SCRIPT_DIR / DATA_DIR / f"{product.name}.json"


def __delete_data(product: ProductFrontmatter) -> None:
    release_data_path = __product_data_path(product)
    if not release_data_path.exists() or product.is_auto_update_cumulative():
        return

    release_data_path.unlink()
    logging.debug(f"deleted {release_data_path} before running scripts")


def __revert_data(product: ProductFrontmatter) -> None:
    release_data_path = __product_data_path(product)
    # check=False because the command fails if the file did not exist before
    proc.run(['git', 'checkout', 'HEAD', '--', str(release_data_path)], timeout=10, check=False, cwd=SCRIPT_DIR)
    logging.warning(f"reverted changes in {release_data_path}")


def __run_script(product: ProductFrontmatter, config: AutoConfig, summary: ScriptExecutionSummary) -> bool:
    script = SCRIPT_DIR / SRC_DIR / config.script

    logging.info(f"start running {script.name} for {config}")
    start = time.perf_counter()

    try:
        module = importlib.import_module(f"src.{config.method}")
        module.update(product, config)
        success = True
    except Exception:
        logging.exception(f"{script} for {config} failed")
        success = False

    elapsed_seconds = time.perf_counter() - start

    summary.register(script.stem, product.name, elapsed_seconds, success)
    logging.log(logging.ERROR if not success else logging.INFO,
                f"ran {script.name} for {config}, took {elapsed_seconds:.2f}s (success={success})")

    return success


def update_product(product: ProductFrontmatter, force: bool, exec_summary: ScriptExecutionSummary, git_lock: threading.Lock) -> None:
    # Add default configs
    configs = product.auto_configs()
    configs = [AutoConfig(product.name, {COPY_PRODUCT_RELEASES_METHOD: ""})] + configs
    configs = configs + [AutoConfig(product.name, {REMOVE_INVALID_RELEASES_METHOD: ""})]

    try:
        __delete_data(product)
        for config in configs:
            if config.is_disabled() and not force:
                logging.info(f"skipping script {config.script} as it is disabled")
                continue

            success = __run_script(product, config, exec_summary)
            if not success:
                # git checkout takes the index lock, so concurrent reverts must be serialized
                with git_lock:
                    __revert_data(product)
                break  # stop running scripts for this product

    except Exception:
        logging.exception("an error occurred while running the product's scripts")


def run_scripts(summary: GitHubStepSummary, products: list[ProductFrontmatter], force: bool = False) -> bool:
    global _executor

    exec_summary = ScriptExecutionSummary()
    git_lock = threading.Lock()

    def update_eligible_product(product: ProductFrontmatter) -> None:
        _product_context.name = product.name
        try:
            if not product.has_auto_configs():
                return  # skip products without auto configs

            if product.is_auto_update_disabled() and not force:
                logging.info("skipping as auto update is disabled")
                return

            update_product(product, force, exec_summary, git_lock)
        except Exception:
            logging.exception("an error occurred while running the product's scripts")
        finally:
            _product_context.name = None

    # Products are independent (each reads its own products/<name>.md and writes its own releases/<name>.json),
    # so they can safely be updated in parallel. Every log line emitted while a product is processed is prefixed
    # with its name (see _ProductPrefixFormatter).
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        _executor = executor
        try:
            list(executor.map(update_eligible_product, products))
        finally:
            _executor = None

    exec_summary.print_summary(summary)
    return exec_summary.any_failure()


def get_updated_products() -> list[Path]:
    proc.run(['git', 'add', '--all'], timeout=10, check=True, cwd=SCRIPT_DIR)  # to also get new files in git diff
    git_diff = proc.run(['git', 'diff', '--name-only', '--staged'], capture_output=True, timeout=10, check=True, cwd=SCRIPT_DIR)
    updated_files = [Path(file) for file in git_diff.stdout.decode('utf-8').split('\n') if file]
    return sorted([file for file in updated_files if file.parent == DATA_DIR])


def load_products_json(updated_product_files: list[Path]) -> dict[Path, dict]:
    files_content = {}

    for path in updated_product_files:
        absolute_path = SCRIPT_DIR / path
        if absolute_path.exists():
            with absolute_path.open() as file:
                files_content[path] = json.load(file)
        else:  # new or deleted file
            files_content[path] = {}

    return files_content


# GitHub step summaries and outputs are truncated by GitHub past a certain size (docs mention 1MiB for step
# summaries), so cap the number of diff lines we emit per product to avoid silently losing later products'
# summaries or blowing past the limit entirely.
MAX_DIFF_LINES_PER_PRODUCT = 200


def generate_commit_message(old_content: dict[Path, dict], new_content: dict[Path, dict], summary: GitHubStepSummary) -> None:
    product_names = ', '.join([path.stem for path in old_content])
    summary.println(f"Updated {len(old_content)} products: {product_names}.\n")

    commit_message = GitHubOutput('commit_message')
    with commit_message:
        commit_message.println(f"🤖: {product_names}\n")

        for path in old_content:
            product_name = path.stem
            summary.println(f"### {product_name}\n")
            commit_message.println(f"{product_name}:")

            diff = DeepDiff(old_content[path], new_content[path], ignore_order=True, verbose_level=2)
            diff_lines = diff.pretty().split('\n')
            total_line_count = len(diff_lines)

            truncated = total_line_count > MAX_DIFF_LINES_PER_PRODUCT
            if truncated:
                logging.warning(f"{product_name}: diff has {total_line_count} lines, "
                                 f"truncating to {MAX_DIFF_LINES_PER_PRODUCT} in summary/commit message")
                diff_lines = diff_lines[:MAX_DIFF_LINES_PER_PRODUCT]

            for line in diff_lines:
                summary.println(f"- {line}")
                commit_message.println(f"- {line}")
                logging.info(f"{product_name}: {line}")

            if truncated:
                omitted = total_line_count - MAX_DIFF_LINES_PER_PRODUCT
                summary.println(f"- ... {omitted} more line(s) omitted, see logs for full diff ...")
                commit_message.println(f"- ... {omitted} more line(s) omitted, see logs for full diff ...")

            commit_message.println("")
            summary.println("")


if __name__ == "__main__":
    # Kill any subprocess (git, playwright/chromium, ...) started by this program, in any thread,
    # as soon as the user presses Ctrl-C, instead of leaving them running in the background while
    # we wait for the (possibly still busy) worker threads to notice and unwind.
    signal.signal(signal.SIGINT, _handle_sigint)

    parser = argparse.ArgumentParser(description='Update product releases.')
    parser.add_argument('product', nargs='?', help='restrict update to the given product')
    parser.add_argument('-p', '--product-dir', required=True, help='path to the product directory')
    parser.add_argument('-f', '--force', action='store_true', help='force update even if auto update is disabled')
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=os.environ.get('ACTIONS_STEP_DEBUG') == 'true',
                        help='enable verbose logging (automatically enabled when ACTIONS_STEP_DEBUG is set)')
    args = parser.parse_args()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_ProductPrefixFormatter(logging.BASIC_FORMAT))
    logging.basicConfig(handlers=[handler], level=(logging.DEBUG if args.verbose else logging.INFO))
    install_playwright()

    products_dir = Path(args.product_dir)
    products_list = list_products(products_dir, args.product)

    with GitHubStepSummary() as step_summary:
        some_script_failed = run_scripts(step_summary, products_list, force=args.force)
        updated_products = get_updated_products()

        step_summary.println("## Update summary\n")
        if updated_products:
            new_files_content = load_products_json(updated_products)
            proc.run(['git', 'stash', '--all', '--quiet'], timeout=10, check=True, cwd=SCRIPT_DIR)
            try:
                old_files_content = load_products_json(updated_products)
            finally:
                # Always try to restore the stash, even if reading the old content failed above, so we never
                # leave the working tree in a half-stashed state.
                proc.run(['git', 'stash', 'pop', '--quiet'], timeout=10, check=True, cwd=SCRIPT_DIR)
            generate_commit_message(old_files_content, new_files_content, step_summary)
        else:
            step_summary.println("No update")

    sys.exit(1 if some_script_failed else 0)
