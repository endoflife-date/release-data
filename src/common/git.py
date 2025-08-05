import logging
from hashlib import sha1
from pathlib import Path
from subprocess import run

from . import http


class Git:
    """Git cli wrapper
    """

    def __init__(self, url: str) -> None:
        self.url: str = url
        self.repo_dir: Path = Path(f"~/.cache/git/{sha1(url.encode()).hexdigest()}").expanduser()

    def _run(self, cmd: str) -> list:
        """Run git command and return command result as a list of lines.
        """
        try:
            logging.info(f"Running 'git {cmd}' on {self.url}")
            child = run(f"git {cmd}", capture_output=True, timeout=300, check=True, shell=True, cwd=self.repo_dir)
            return child.stdout.decode("utf-8").strip().split("\n")
        except ChildProcessError as ex:
            msg = f"Failed to run '{cmd}': {ex}"
            raise RuntimeError(msg) from ex

    def setup(self, bare: bool = False) -> None:
        """Creates the repository path and runs:
        git init
        git remote add origin $url
        """
        if not Path(f"{self.repo_dir}").exists():
            self.repo_dir.mkdir(parents=True, exist_ok=True)
            bare = "--bare" if bare else ""
            self._run(f"init {bare}")
            self._run(f"remote add origin {self.url}")

    # See https://stackoverflow.com/a/65746233/374236
    def list_tags(self) -> list[tuple[str, str]]:
        """Fetch and return tags matching the given`pattern`"""
        # See https://stackoverflow.com/a/65746233/374236
        self._run("config --local extensions.partialClone true")
        self._run(f"config --local http.userAgent '{http.ENDOFLIFE_BOT_USER_AGENT}'")
        # Using --force to avoid error like "would clobber existing tag".
        # See https://stackoverflow.com/questions/58031165/how-to-get-rid-of-would-clobber-existing-tag.
        self._run("fetch --force --tags --filter=blob:none --depth=1 origin")
        tags_with_date = self._run("tag --list --format='%(refname:strip=2) %(creatordate:short)'")
        return [tag_with_date.split(" ") for tag_with_date in tags_with_date]

    def list_branches(self, pattern: str) -> list[str]:
        """Uses ls-remote to fetch the branch names
        `pattern` uses fnmatch style globbing
        """
        lines = self._run(f"ls-remote origin '{pattern}'")

        # this checks keeps the linter quiet, because _run returns a bool OR list
        if isinstance(lines, bool):
            return []

        return [line.split("\t")[1][11:] for line in lines if "\t" in line]

    def checkout(self, branch: str, file_list: list[str] = None) -> None:
        """Checks out a branch
        If `file_list` is given, sparse-checkout is used to save bandwidth
        and only download the given files
        """
        if file_list:
            # --skip-checks needed to avoid error when file_list contains a file
            self._run(f"sparse-checkout set --skip-checks {' '.join(file_list)}")
        self._run(f"fetch --filter=blob:none --depth 1 origin {branch}")
        self._run(f"checkout {branch}")
