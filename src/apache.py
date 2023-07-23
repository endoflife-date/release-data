import re
from datetime import datetime
from pathlib import Path
from common import endoflife
from common.git import Git

"""Fetch apache versions from its git repository.

Every branch formatted like 2.4.x has a STATUS file which contains a version
history. Not every version was released, the lines are filtered with
(?:Released|Announced) to get the released versions only (they were not
consistent in the past with the wording, it seems better now).
"""

PRODUCT = "apache"
REPO_URL = "https://github.com/apache/httpd.git"


def parse(date: str) -> str:
    for format in ["%B %d, %Y", "%b %d, %Y"]:
        try:
            return datetime.strptime(date, format).strftime("%Y-%m-%d")
        except ValueError:
            pass

    raise ValueError(f"Unknown date format for '{date}'")


def get_versions_from_file(release_notes_file: Path) -> dict:
    if not release_notes_file.exists():
        return {}

    with open(release_notes_file, "rb") as f:
        plain = f.read().decode("utf-8", errors="ignore")

    return {
        version: date
        for (version, date) in re.findall(
            r"\s+(?P<version>\d+\.\d+\.\d+)\s*:.*(?:Released|Announced)\s(?:on\s)?(?P<date>\w+\s\d\d?,\s\d{4})",
            plain,
        )
    }


git = Git(REPO_URL)
git.setup()
versions = {}

print(f"::group::{PRODUCT}")
for branch in git.list_branches("refs/heads/?.?.x"):
    status_file = "STATUS"
    git.checkout(branch, file_list=[status_file])
    for version, date_str in get_versions_from_file(git.repo_dir / status_file).items():
        date = parse(date_str)
        versions[version] = date
        print(f"{version}: {date}")
print("::endgroup::")

endoflife.write_releases(
    PRODUCT,
    dict(
        # sort by date then version (desc)
        sorted(versions.items(), key=lambda x: (x[1], x[0]), reverse=True)
    ),
)
