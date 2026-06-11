import re

from common import dates
from common.git import Git
from common.releasedata import ProductData, config_from_argv

"""Fetches Red Hat OpenShift versions from the documentation's git repository"""

VERSION_AND_DATE_PATTERN = re.compile(
    r"{product-title}\s(?P<version>{product-version}\.\d+|\d+\.\d+\.\d+).*\n+Issued:\s(?P<date>\d\d?\s[a-zA-Z]+\s\d{4}|\d{4}-\d\d-\d\d)$",
    re.MULTILINE,
)

MODULE_INCLUDE_PATTERN = re.compile(r"^include::(?P<path>modules/zstream-[^]]+\.adoc)\[", re.MULTILINE)


def _read_text(path) -> str:
    with path.open("rb") as f:
        return f.read().decode("utf-8")


def _declare_versions_from_content(product_data: ProductData, content: str, branch_version: str) -> None:
    for version, date_str in VERSION_AND_DATE_PATTERN.findall(content):
        product_data.declare_version(
            version.replace("{product-version}", branch_version),
            dates.parse_date(date_str),
        )

config = config_from_argv()
with ProductData(config.product) as product_data:
    git = Git(config.url)
    git.setup()

    # only fetch v4+ branches, because the format was different in openshift v3
    for branch in git.list_branches("refs/heads/enterprise-[4-9]*"):
        if "-archive-" in branch:
            continue

        branch_version = branch.split("-")[1]
        file_version = branch_version.replace(".", "-")
        release_notes_filename = f"release_notes/ocp-{file_version}-release-notes.adoc"
        git.checkout(branch, file_list=[release_notes_filename])

        release_notes_file = git.repo_dir / release_notes_filename
        if not release_notes_file.exists():
            continue

        content = _read_text(release_notes_file)

        # Newer OpenShift release notes include z-stream entries from module files.
        module_files = MODULE_INCLUDE_PATTERN.findall(content)
        if module_files:
            git.checkout(branch, file_list=[release_notes_filename, *module_files])
            for module_file in module_files:
                module_path = git.repo_dir / module_file
                if not module_path.exists():
                    continue

                _declare_versions_from_content(product_data, _read_text(module_path), branch_version)

            continue

        # Fallback for older branches where release notes are still inline.
        _declare_versions_from_content(product_data, content, branch_version)
