import re
from datetime import datetime
from pathlib import Path
from common import endoflife
from common.git import Git

"""
Fetch apache versions from the git repository
"""

PRODUCT = "apache"
REPO_URL = "https://github.com/apache/httpd.git"


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

for branch in git.list_branches("refs/heads/?.?.x"):
    status_file = "STATUS"
    git.checkout(branch, file_list=[status_file])
    versions = {**versions, **get_versions_from_file(git.repo_dir / status_file)}

# convert the date format
converted = {}
for version, date in versions.items():
    try:
        d = datetime.strptime(date, "%B %d, %Y")
        converted[version] = d.strftime("%Y-%m-%d")
        continue
    except ValueError:
        pass

    try:
        d = datetime.strptime(date, "%b %d, %Y")
        converted[version] = d.strftime("%Y-%m-%d")
        continue
    except ValueError:
        pass

versions = converted

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
