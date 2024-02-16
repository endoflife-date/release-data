import json
import logging
import subprocess
import sys
import time
from pathlib import Path

from deepdiff import DeepDiff

from src.common.endoflife import AutoConfig, ProductFrontmatter, list_products
from src.common.gha import GitHubGroup, GitHubOutput, GitHubStepSummary

SRC_DIR = Path('src')
DATA_DIR = Path('releases')


class ScriptExecutionSummary:
    def __init__(self) -> None:
        self.success_by_product = {}
        self.success_by_script = {}
        self.durations_by_product = {}
        self.durations_by_script = {}
        self.scripts_by_product = {}
        self.products_by_script = {}

    def register(self, script: str, product: str, duration: float, success: bool) -> None:
        self.success_by_product[product] = self.success_by_product.get(product, True) and success
        self.success_by_script[script] = self.success_by_script.get(script, True) and success
        self.durations_by_product[product] = self.durations_by_product.get(product, 0) + duration
        self.durations_by_script[script] = self.durations_by_script.get(script, 0) + duration
        self.scripts_by_product[product] = self.scripts_by_product.get(product, []) + [script]
        self.products_by_script[script] = self.products_by_script.get(script, []) + [product]

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
    with GitHubGroup("Install Playwright"):
        logging.info("Installing Playwright")
        subprocess.run('playwright install chromium', timeout=120, check=True, shell=True)
        logging.info("Playwright installed")


def __delete_data(product: ProductFrontmatter) -> None:
    release_data_path = DATA_DIR / f"{product.name}.json"
    if not release_data_path.exists() or product.is_auto_update_cumulative():
        return

    release_data_path.unlink()
    logging.info(f"deleted {release_data_path} before running scripts")


def __revert_data(product: ProductFrontmatter) -> None:
    release_data_path = DATA_DIR / f"{product.name}.json"
    subprocess.run(f'git checkout HEAD -- {release_data_path}', timeout=10, check=True, shell=True)
    logging.warning(f"reverted changes in {release_data_path}")


def __run_script(product: ProductFrontmatter, config: AutoConfig, summary: ScriptExecutionSummary) -> bool:
    script = SRC_DIR / config.script

    logging.info(f"start running {script} for {config}")
    start = time.perf_counter()
    # timeout is handled in child scripts
    child = subprocess.run([sys.executable, script, config.product, str(config.url)])
    success = child.returncode == 0
    elapsed_seconds = time.perf_counter() - start

    summary.register(script.stem, product.name, elapsed_seconds, success)
    logging.log(logging.ERROR if not success else logging.INFO,
                f"ran {script} for {config}, took {elapsed_seconds:.2f}s (success={success})")

    return success


def run_scripts(summary: GitHubStepSummary, product_filter: str) -> bool:
    exec_summary = ScriptExecutionSummary()

    for product in list_products(product_filter):
        if not product.has_auto_configs():
            continue

        with GitHubGroup(product.name):
            __delete_data(product)
            for config in product.auto_configs():
                success = __run_script(product, config, exec_summary)
                if not success:
                    __revert_data(product)
                    break  # stop running scripts for this product

    exec_summary.print_summary(summary)
    return exec_summary.any_failure()


def get_updated_products() -> list[Path]:
    subprocess.run('git add --all', timeout=10, check=True, shell=True)  # to also get new files in git diff
    git_diff = subprocess.run('git diff --name-only --staged', capture_output=True, timeout=10, check=True, shell=True)
    updated_files = [Path(file) for file in git_diff.stdout.decode('utf-8').split('\n')]
    return sorted([file for file in updated_files if file.parent == DATA_DIR])


def load_products_json(updated_product_files: list[Path]) -> dict[Path, dict]:
    files_content = {}

    for path in updated_product_files:
        if path.exists():
            with path.open() as file:
                files_content[path] = json.load(file)
        else:  # new or deleted file
            files_content[path] = {}

    return files_content


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
            for line in diff.pretty().split('\n'):
                summary.println(f"- {line}")
                commit_message.println(f"- {line}")
                logging.info(f"{product_name}: {line}")

            commit_message.println("")
            summary.println("")


logging.basicConfig(format="%(message)s", level=logging.INFO)
p_filter = sys.argv[1] if len(sys.argv) > 1 else None


with GitHubStepSummary() as step_summary:
    install_playwright()
    some_script_failed = run_scripts(step_summary, p_filter)
    updated_products = get_updated_products()

    step_summary.println("## Update summary\n")
    if updated_products:
        new_files_content = load_products_json(updated_products)
        subprocess.run('git stash --all --quiet', timeout=10, check=True, shell=True)
        old_files_content = load_products_json(updated_products)
        subprocess.run('git stash pop --quiet', timeout=10, check=True, shell=True)
        generate_commit_message(old_files_content, new_files_content, step_summary)
    else:
        step_summary.println("No update")

sys.exit(1 if some_script_failed else 0)
