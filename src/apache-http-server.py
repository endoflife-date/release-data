import re

from common import dates, endoflife
from common.git import Git

"""Fetches Apache HTTP Server versions and release date from its git repository
by looking at the STATUS file of each <major>.<minor>.x branch."""

VERSION_AND_DATE_PATTERNS = [
    # for most versions
    re.compile(r"\s+(?P<version>\d+\.\d+\.\d+)\s*:.*(?:Released|Announced|Released and Retired)\s(?:on\s)?(?P<date>\w+\s\d\d?,\s\d{4})"),
    # for older 2.0.x versions (only GA versions are considered)
    re.compile(r"\s+(?P<version>\d+\.\d+\.\d+)\s*:.*released\s(?P<date>\w+\s\d\d?,\s\d{4}) as GA"),
    # for older 1.3.x versions, we take the date of the tag and not the date of the release (too difficult to parse)
    re.compile(r"\s+(?P<version>\d+\.\d+\.\d+)\s*:.*Tagged and [rR]olled\s(?:on\s)?(?P<date>\w+\.?\s\d\d?,\s\d{4})"),
]

product = endoflife.Product("apache-http-server")
print(f"::group::{product.name}")
git = Git("https://github.com/apache/httpd.git")
git.setup()

for branch in git.list_branches("refs/heads/?.?.x"):
    git.checkout(branch, file_list=["STATUS"])

    release_notes_file = git.repo_dir / "STATUS"
    if not release_notes_file.exists():
        continue

    with open(release_notes_file, "rb") as f:
        release_notes = f.read().decode("utf-8", errors="ignore")

    for pattern in VERSION_AND_DATE_PATTERNS:
        for (version, date_str) in pattern.findall(release_notes):
            product.declare_version(version, dates.parse_date(date_str))

product.write()
print("::endgroup::")
