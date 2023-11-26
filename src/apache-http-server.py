import re
from pathlib import Path
from common import dates
from common import endoflife
from common.git import Git

"""Fetch apache versions from its git repository.

Every branch formatted like 2.4.x has a STATUS file which contains a version
history. Not every version was released, the lines are filtered with
(?:Released|Announced) to get the released versions only (they were not
consistent in the past with the wording, it seems better now).
"""

PRODUCT = "apache-http-server"
REPO_URL = "https://github.com/apache/httpd.git"


def parse(date: str) -> str:
    date = date.replace("Feburary", "February")
    date = date.replace(". ", " ")
    return dates.parse_date(date).strftime("%Y-%m-%d")


def fetch_versions_from_file(release_notes_file: Path, versions: dict):
    if not release_notes_file.exists():
        return {}

    with open(release_notes_file, "rb") as f:
        plain = f.read().decode("utf-8", errors="ignore")

    # for most versions
    for (version, date_str) in re.findall(r"\s+(?P<version>\d+\.\d+\.\d+)\s*:.*(?:Released|Announced|Released and Retired)\s(?:on\s)?(?P<date>\w+\s\d\d?,\s\d{4})", plain):
        date = parse(date_str)
        versions[version] = date
        print(f"{version}: {date}")

    # for older 2.0.x versions (only GA versions are considered)
    for (version, date_str) in re.findall(r"\s+(?P<version>\d+\.\d+\.\d+)\s*:.*released\s(?P<date>\w+\s\d\d?,\s\d{4}) as GA", plain):
        date = parse(date_str)
        versions[version] = date
        print(f"{version}: {date}")

    # for older 1.3.x versions, we take the date of the tag and not the date of the release (too difficult to parse)
    for (version, date_str) in re.findall(r"\s+(?P<version>\d+\.\d+\.\d+)\s*:.*Tagged and [rR]olled\s(?:on\s)?(?P<date>\w+\.?\s\d\d?,\s\d{4})", plain):
        date = parse(date_str)
        versions[version] = date
        print(f"{version}: {date}")


git = Git(REPO_URL)
git.setup()
versions = {}

print(f"::group::{PRODUCT}")
for branch in git.list_branches("refs/heads/?.?.x"):
    status_file = "STATUS"
    git.checkout(branch, file_list=[status_file])
    fetch_versions_from_file(git.repo_dir / status_file, versions)
print("::endgroup::")

endoflife.write_releases(PRODUCT, versions)
