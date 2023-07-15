from subprocess import call, Popen, PIPE, DEVNULL
from typing import Union, List
from pathlib import Path
from hashlib import sha1

class Git:
    """
    Git cli wrapper
    used by debian.py and red-hat-openshift.py
    """

    def __init__(self, url: str):
        self.url: str = url
        self.repo_dir: Path = Path(
            f"~/.cache/git/{sha1(self.url.encode()).hexdigest()}"
        ).expanduser()

    def _run(self, cmd: str, return_output: bool = False) -> Union[bool, list]:
        """
        Run git command and return True on success or False on failure.
        Optionaly returns command result instead.
        """
        git_opts = f"--git-dir={self.repo_dir}/.git --work-tree={self.repo_dir}"

        if return_output:
            child = Popen(
                f"git {git_opts} {cmd}",
                shell=True,
                stdout=PIPE,
            )
            return child.communicate()[0].decode("utf-8").split("\n")

        return call(f"git {git_opts} {cmd}",
                    shell=True,
                    stdout=DEVNULL,
                    stderr=DEVNULL) == 0

    def setup(self):
        """
        Creates the repository path and runs:
        git init
        git remote add origin $url
        """
        self.repo_dir.mkdir(parents=True, exist_ok=True)
        if not Path(f"{self.repo_dir}/.git").exists():
            self._run("init")
            self._run(f"remote add origin {self.url}")

    def list_branches(self, pattern: str):
        """
        Uses ls-remote to fetch the branch names
        `pattern` uses fnmatch style globbing
        """
        raw = self._run(
            # only list v4+ branches because the format in v3 is different
            f"ls-remote origin '{pattern}'",
            return_output=True,
        )

        # this checks keeps the linter quiet, because _run returns a bool OR list
        # please dont remove
        if isinstance(raw, bool):
            return []

        return [line.split("\t")[1][11:] for line in raw if "\t" in line]

    def checkout(self, branch: str, file_list: List[str] = []):
        """
        Checks out a branch
        If `file_list` is given, sparse-checkout is used to save bandwith
        and only download the given files
        """
        if file_list:
            self._run(f"sparse-checkout set {' '.join(file_list)}")
        self._run(f"fetch --filter=blob:none --depth 1 origin {branch}")
        self._run(f"checkout {branch}")
