import re
from pathlib import Path

from src.common import dates
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.git import Git
from src.common.releasedata import ProductData

"""Fetches Red Hat OpenShift versions from the documentation's git repository"""

VERSION_AND_DATE_PATTERN = re.compile(
    r"{product-title}\s(?P<version>{product-version}\.\d+|\d+\.\d+\.\d+).*\n+"
    r"(?:\[role=.*?\]\s*\n+)?"  # some module files have a "[role=...]" line before "Issued:"
    r"Issued:\s(?P<date>\d\d?\s[a-zA-Z]+\s\d{4}|\d{4}-\d\d-\d\d)$",
    re.MULTILINE,
)

# Only match module files that can contain a version/date (either the bare
# "zstream-<version>.adoc" or the older "zstream-<version>-about.adoc" split
# style). This excludes companion files like "-bug-fixes.adoc", "-fixed-issues.adoc"
# and "-updating.adoc", which never match VERSION_AND_DATE_PATTERN and would
# otherwise be fetched for nothing.
MODULE_INCLUDE_PATTERN = re.compile(r"^include::(?P<path>modules/zstream-[\d-]+(?:-about)?\.adoc)\[", re.MULTILINE)


def _read_text(path: Path) -> str:
    with path.open("rb") as f:
        return f.read().decode("utf-8")


def _declare_versions_from_content(product_data: ProductData, content: str, branch_version: str) -> None:
    for version, date_str in VERSION_AND_DATE_PATTERN.findall(content):
        product_data.declare_version(
            version.replace("{product-version}", branch_version),
            dates.parse_date(date_str),
        )

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        git = Git(config.url)
        git.setup()

        # only consider v4+ branches, because the format was different in openshift v3
        branches = [
            branch
            for branch in git.list_branches("refs/heads/enterprise-[4-9]*")
            if "-archive-" not in branch
        ]

        # Fetch every branch in a single round-trip instead of one fetch per branch.
        git.fetch_branches(branches)

        for branch in branches:
            branch_version = branch.split("-")[1]
            file_version = branch_version.replace(".", "-")
            release_notes_filename = f"release_notes/ocp-{file_version}-release-notes.adoc"
            git.checkout(branch, file_list=[release_notes_filename])

            release_notes_file = git.repo_dir / release_notes_filename
            if not release_notes_file.exists():
                continue

            content = _read_text(release_notes_file)

            # Older releases are declared inline in the main release notes file, while
            # newer z-stream entries are pulled in from separate module files. A single
            # branch can contain both, so both need to be parsed.
            _declare_versions_from_content(product_data, content, branch_version)

            module_files = MODULE_INCLUDE_PATTERN.findall(content)
            if module_files:
                git.checkout(branch, file_list=[release_notes_filename, *module_files])
                for module_file in module_files:
                    module_path = git.repo_dir / module_file
                    if not module_path.exists():
                        continue

                    _declare_versions_from_content(product_data, _read_text(module_path), branch_version)
