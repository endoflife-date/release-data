import argparse
import json
import logging
import subprocess
import sys
import time
from pathlib import Path

from deepdiff import DeepDiff

from src.common.endoflife import AutoConfig, ProductFrontmatter, list_products
from src.common.gha import GitHubGroup, GitHubOutput, GitHubStepSummary
from src.common.releasedata import DATA_DIR, SRC_DIR


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
    release_data_path = Path(__file__).resolve().parent / DATA_DIR / f"{product.name}.json"
    if not release_data_path.exists() or product.is_auto_update_cumulative():
        return

    release_data_path.unlink()
    logging.info(f"deleted {release_data_path} before running scripts")


def __revert_data(product: ProductFrontmatter) -> None:
    release_data_path = Path(__file__).resolve().parent / DATA_DIR / f"{product.name}.json"
    # check=False because the command fails if the file did not exist before
    subprocess.run(f'git checkout HEAD -- {release_data_path}', timeout=10, check=False, shell=True)
    logging.warning(f"reverted changes in {release_data_path}")


def __run_script(product: ProductFrontmatter, config: AutoConfig, summary: ScriptExecutionSummary) -> bool:
    script = Path(__file__).resolve().parent / SRC_DIR / config.script

    logging.info(f"start running {script} for {config}")
    start = time.perf_counter()

    # timeout is handled in child scripts
    script_args = [sys.executable, script, "-p", product.path, "-m", str(config.method), "-u", str(config.url)]
    script_args = script_args + ["-v"] if logging.getLogger().isEnabledFor(logging.DEBUG) else script_args
    child = subprocess.run(script_args)

    success = child.returncode == 0
    elapsed_seconds = time.perf_counter() - start

    summary.register(script.stem, product.name, elapsed_seconds, success)
    logging.log(logging.ERROR if not success else logging.INFO,
                f"ran {script} for {config}, took {elapsed_seconds:.2f}s (success={success})")

    return success


def run_scripts(summary: GitHubStepSummary, products: list[ProductFrontmatter]) -> bool:
    exec_summary = ScriptExecutionSummary()

    for product in products:
        configs = product.auto_configs()

        if not configs:
            continue # skip products without auto configs

        # Add default configs
        configs = [AutoConfig(product.name, {"_copy_product_releases": ""})] + configs
        configs = configs + [AutoConfig(product.name, {"_remove_invalid_releases": ""})]

        with GitHubGroup(product.name):
            try:
                __delete_data(product)
                for config in configs:
                    success = __run_script(product, config, exec_summary)
                    if not success:
                        __revert_data(product)
                        break  # stop running scripts for this product

            except BaseException:
                logging.exception(f"Skipping {product.name}, there was an error while running its scripts")

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update product releases.')
    parser.add_argument('product', nargs='?', help='restrict update to the given product')
    parser.add_argument('-p', '--product-dir', required=True, help='path to the product directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose logging')
    args = parser.parse_args()

    logging.basicConfig(format=logging.BASIC_FORMAT, level=(logging.DEBUG if args.verbose else logging.INFO))
    install_playwright()

    products_dir = Path(args.product_dir)
    products_list = list_products(products_dir, args.product)

    with GitHubStepSummary() as step_summary:
        some_script_failed = run_scripts(step_summary, products_list)
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
