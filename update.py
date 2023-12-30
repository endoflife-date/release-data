import json
import logging
import os
import subprocess
import sys
import time
from base64 import b64encode
from pathlib import Path

from deepdiff import DeepDiff


def github_output(name: str, value: str) -> None:
    if "GITHUB_OUTPUT" not in os.environ:
        logging.debug(f"GITHUB_OUTPUT does not exist, but would have written: {name}={value.strip()}")
        return

    if "\n" in value:
        # https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#multiline-strings
        delimiter = b64encode(os.urandom(16)).decode()
        value = f"{delimiter}\n{value}\n{delimiter}"
        command = f"{name}<<{value}"
    else:
        command = f"{name}={value}"

    with open(os.environ["GITHUB_OUTPUT"], 'a') as github_output_var:
        print(command, file=github_output_var)
        logging.debug(f"Wrote to GITHUB_OUTPUT: {name}={value.strip()}")


def add_summary_line(line: str) -> None:
    if "GITHUB_STEP_SUMMARY" not in os.environ:
        logging.debug(f"GITHUB_STEP_SUMMARY does not exist, but would have written: {line}")
        return

    with open(os.environ["GITHUB_STEP_SUMMARY"], 'a') as github_step_summary:
        print(line, file=github_step_summary)


SRC_DIR = 'src'
DATA_DIR = 'releases'

logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.INFO)

# Run scripts
scripts = sorted([os.path.join(SRC_DIR, file) for file in os.listdir(SRC_DIR) if file.endswith('.py')])
some_script_failed = False

add_summary_line("## Script execution summary\n")
add_summary_line("| Name | Duration | Succeeded |")
add_summary_line("|------|----------|-----------|")
for script in scripts:
    logging.info(f"start running {script}")

    start = time.perf_counter()
    child = subprocess.run([sys.executable, script], timeout=300)
    elapsed_seconds = time.perf_counter() - start

    if child.returncode != 0:
        some_script_failed = True
        add_summary_line(f"| {script} | {elapsed_seconds:.2f}s | ❌ |")
        logging.error(f"Error while running {script} after {elapsed_seconds:.2f}s, update will only be partial")
    else:
        logging.info(f"Finished running {script}, took {elapsed_seconds:.2f}s")
        add_summary_line(f"| {script} | {elapsed_seconds:.2f}s | ✅ |")

# Generate commit message
subprocess.run('git add --all', timeout=10, check=True, shell=True)  # to also get new files in git diff
git_diff = subprocess.run('git diff --name-only --staged', capture_output=True, timeout=10, check=True, shell=True)
updated_files = sorted([Path(file) for file in git_diff.stdout.decode('utf-8').split('\n') if file.startswith(DATA_DIR)])
logging.info(f"Updated files: {updated_files}")

add_summary_line("## Update summary\n")
if updated_files:
    # get modified files content
    new_files_content = {}
    for path in updated_files:
        with open(path) as file:
            new_files_content[path] = json.load(file)

    # get original files content
    old_files_content = {}
    subprocess.run('git stash --all --quiet', timeout=10, check=True, shell=True)
    for path in updated_files:
        if path.exists():
            with open(path) as file:
                old_files_content[path] = json.load(file)
        else:  # new file
            old_files_content[path] = {}
    subprocess.run('git stash pop --quiet', timeout=10, check=True, shell=True)

    # Generate commit message
    product_names = ', '.join([path.stem for path in updated_files])
    commit_message = f"🤖: {product_names}\n\n"
    add_summary_line(f"Updated {len(updated_files)} products: {product_names}.")

    for path in updated_files:
        add_summary_line(f"### {path.stem}\n")
        commit_message += f"{path.stem}:\n"

        diff = DeepDiff(old_files_content[path], new_files_content[path], ignore_order=True)
        for line in diff.pretty().split('\n'):
            add_summary_line(f"- {line}")
            commit_message += f"- {line}\n"
            logging.info(f"{path.stem}: {line}")

        commit_message += "\n"
        add_summary_line("")

    github_output('commit_message', commit_message)

else:
    add_summary_line("No update")

sys.exit(1 if some_script_failed else 0)
