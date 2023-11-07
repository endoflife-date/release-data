import re
from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime

"""Fetch versions with their dates from docs.couchbase.com.

Versions are fetched from the release notes of each minor version. Date is not
accurate (only month and year are provided) but it's already better than the
previous implementation which use dates of the images on Docker Hub. Because
of that lack of precision, all dates are set to the 15th of the month.

Notes:
- documentation for oldest versions is not available anymore on
  docs.couchbase.com, so this script is using the Wayback Machine to fetch them.
- dates are not available for some versions, those had to be set manually.
"""

PRODUCT = "couchbase-server"
REGEX = r"^Release (?P<version>\d+\.\d+(\.\d+)?) \((?P<date>.+)\)$"
URLS = [
    # Disabled, too much timed out.
    # "https://web.archive.org/web/20230519160357/https://docs.couchbase.com/server/",
    "https://docs.couchbase.com/server",
]
FIXED_VERSIONS = {
    "6.0.0": "2018-10-31",  # https://www.couchbase.com/blog/announcing-couchbase-6-0/
    "6.0.1": "2019-02-15",
    # https://web.archive.org/web/20190307191211/https://docs.couchbase.com/server/6.0/release-notes/relnotes.html
    "7.2.0": "2023-06-01",  # https://www.couchbase.com/blog/couchbase-capella-spring-release-72/
}

print(f"::group::{PRODUCT}")
versions = {}

for base_url in URLS:
    response = endoflife.fetch_url(f"{base_url}/current/install/install-intro.html")
    soup = BeautifulSoup(response, features="html5lib")
    for option in soup.find(class_="version_list").find_all("option"):
        minor = option.attrs["value"]
        versions[minor + '.0'] = 'N/A'  # there is no date available for x.y.0

        response = endoflife.fetch_url(f"{base_url}/{minor}/release-notes/relnotes.html")
        soup = BeautifulSoup(response, features="html5lib")
        for title in soup.find_all("h2"):
            versionAndDate = title.get_text().strip()
            m = re.match(REGEX, versionAndDate)
            if m:
                version = f"{m['version']}.0" if len(m['version'].split('.')) == 2 else m['version']
                date = datetime.strptime(m['date'], "%B %Y").strftime("%Y-%m-15")
                versions[version] = date
                print(f"{version}: {date}")

versions = versions | FIXED_VERSIONS
endoflife.write_releases(PRODUCT, dict(
    # sort by date then version (desc)
    sorted(versions.items(), key=lambda x: (x[1], x[0]), reverse=True)
))
print("::endgroup::")
