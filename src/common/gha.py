import logging
import os
from base64 import b64encode

"""See https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions."""


class GitHubOutput:
    def __init__(self, name: str) -> None:
        self.name = name
        self.value = ""

    def __enter__(self) -> None:
        return None

    def println(self, value: str) -> None:
        self.value += value + "\n"

    def __exit__(self, exc_type: any, exc_value: any, traceback: any) -> None:
        var_exists = "GITHUB_OUTPUT" in os.environ
        delimiter = b64encode(os.urandom(16)).decode()
        value = f"{delimiter}\n{self.value}\n{delimiter}"
        command = f"{self.name}<<{value}"

        logging.info(f"GITHUB_OUTPUT (exists={var_exists}):\n{command}")
        if var_exists:
            with open(os.environ["GITHUB_OUTPUT"], 'a') as github_output_var:  # NOQA: PTH123
                print(command, file=github_output_var)


class GitHubStepSummary:
    def __init__(self) -> None:
        self.value = ""

    def __enter__(self) -> None:
        return None

    def println(self, value: str) -> None:
        self.value += value + "\n"

    def __exit__(self, exc_type: any, exc_value: any, traceback: any) -> None:
        var_exists = "GITHUB_STEP_SUMMARY" in os.environ

        logging.info(f"GITHUB_STEP_SUMMARY (exists={var_exists}):\n{self.value}")
        if var_exists:
            with open(os.environ["GITHUB_STEP_SUMMARY"], 'a') as github_step_summary:  # NOQA: PTH123
                print(self.value, file=github_step_summary)
