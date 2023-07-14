import re
import subprocess
from pathlib import Path
from common import endoflife
from hashlib import sha1
from os.path import exists
from subprocess import call
from typing import Union

"""
Fetch Red Hat OpenShift versions from the documentation git repository
"""

PRODUCT = "red-hat-openshift"
REPO_URL = "https://github.com/openshift/openshift-docs.git"


class Git:
    """
    Git cli wrapper
    """

    def __init__(self, url: str):
        self.url: str = url
        self._url_sha1: str = sha1(self.url.encode()).hexdigest()
        self.repo_dir: Path = Path(f"~/.cache/git/red-hat-openshift_{self._url_sha1}").expanduser()

    def run(self, cmd: str, return_output: bool = False) -> Union[bool, list]:
        """
        Run git command and return True on success or False on failure.
        Optionaly returns command result instead.
        """
        git_opts = f"--git-dir={self.repo_dir}/.git --work-tree={self.repo_dir}"

        if return_output:
            child = subprocess.Popen(
                f"git {git_opts} {cmd}",
                shell=True,
                stdout=subprocess.PIPE,
            )
            return child.communicate()[0].decode("utf-8").split("\n")

        return call(f"git {git_opts} {cmd}",
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL) == 0

    def clone(self):
        self.repo_dir.mkdir(parents=True, exist_ok=True)
        if not exists(f"{self.repo_dir}/.git"):
            self.run("init")
            self.run(f"remote add origin {self.url}")

    def list_branches(self):
        raw = self.run(
            # only list v4+ branches because the format in v3 is different
            "ls-remote origin 'refs/heads/enterprise-[4-9]*'",
            return_output=True,
        )
        return [line.split("\t")[1][11:] for line in raw if "\t" in line]

    def list_versions_from_branch(self, branch: str) -> dict:
        # convert "enterprise-4.9" to 4-9
        version = branch.split("-")[1].replace(".", "-")
        relative_notes_file = f"release_notes/ocp-{version}-release-notes.adoc"
        release_notes_file = self.repo_dir / relative_notes_file

        self.run(f"sparse-checkout set {relative_notes_file}")
        self.run(f"fetch --filter=blob:none --depth 1 origin {branch}")
        self.run(f"checkout {branch}")

        if not release_notes_file.exists():
            return {}

        with open(release_notes_file, "rb") as f:
            plain = f.read().decode("utf-8")

        return {
            version: date
            for (version, date) in re.findall(
                r"{product-title}\s(?P<version>\d+\.\d+\.\d+).*$\n+Issued:\s(?P<date>\d{4}-\d\d-\d\d)$",
                plain,
                re.MULTILINE,
            )
        }


g = Git(REPO_URL)
g.clone()
versions = {}
for branch in g.list_branches():
    versions = {**versions, **g.list_versions_from_branch(branch)}

print(f"::group::{PRODUCT}")
for version, date in versions.items():
    print(f"{version}: {date}")
print("::endgroup::")

endoflife.write_releases(
    PRODUCT,
    dict(
        # sort by date then version (desc)
        sorted(versions.items(), key=lambda x: (x[1], x[0]), reverse=True)
    ),
)
