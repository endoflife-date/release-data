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

    def _run(self, args: list[str]) -> list:
        """Run git command and return command result as a list of lines.
        """
        try:
            logging.info(f"Running 'git {' '.join(args)}' on {self.url}")
            child = run(["git", *args], capture_output=True, timeout=300, check=True, cwd=self.repo_dir)
            return child.stdout.decode("utf-8").strip().split("\n")
        except ChildProcessError as ex:
            msg = f"Failed to run '{' '.join(args)}': {ex}"
            raise RuntimeError(msg) from ex

    def setup(self, bare: bool = False) -> None:
        """Creates the repository path and runs:
        git init
        git remote add origin $url
        """
        if not Path(f"{self.repo_dir}").exists():
            self.repo_dir.mkdir(parents=True, exist_ok=True)
            init_args = ["init", "--bare"] if bare else ["init"]
            self._run(init_args)
            self._run(["remote", "add", "origin", self.url])

    # See https://stackoverflow.com/a/65746233/374236
    def list_tags(self) -> list[tuple[str, str]]:
        """Fetch and return tags matching the given`pattern`"""
        # See https://stackoverflow.com/a/65746233/374236
        # The extensions.partialClone and http.userAgent settings only need to apply to this
        # fetch, so they're passed as one-off `-c` overrides instead of persisted `git config`
        # calls, saving two extra subprocess invocations.
        # Using --force to avoid error like "would clobber existing tag".
        # See https://stackoverflow.com/questions/58031165/how-to-get-rid-of-would-clobber-existing-tag.
        self._run([
            "-c", "extensions.partialClone=true",
            "-c", f"http.userAgent={http.ENDOFLIFE_BOT_USER_AGENT}",
            "fetch", "--force", "--tags", "--filter=blob:none", "--depth=1", "origin",
        ])
        tags_with_date = self._run(["tag", "--list", "--format=%(refname:strip=2) %(creatordate:short)"])
        return [tag_with_date.split(" ") for tag_with_date in tags_with_date]

    def list_branches(self, pattern: str) -> list[str]:
        """Uses ls-remote to fetch the branch names
        `pattern` uses fnmatch style globbing
        """
        lines = self._run(["ls-remote", "origin", pattern])

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
            self._run(["sparse-checkout", "set", "--skip-checks", *file_list])
        self._run(["fetch", "--filter=blob:none", "--depth", "1", "origin", branch])
        self._run(["checkout", branch])
