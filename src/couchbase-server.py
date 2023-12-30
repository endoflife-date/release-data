import re
from datetime import datetime

from bs4 import BeautifulSoup
from common import dates, endoflife, http

"""Fetches versions from release notes of each minor version on docs.couchbase.com.

Dates are not available for all versions, so they must be set manually in some cases.
Moreover dates are not accurate (only month and year are provided), so they are set to the last day of the month.
"""

URLS = "https://docs.couchbase.com/server"
VERSION_AND_DATE_PATTERN = re.compile(r"^Release (?P<version>\d+\.\d+(\.\d+)?) \((?P<date>.+)\)$")
MANUAL_VERSIONS = {
    "6.0.0": datetime(2018, 10, 31),  # https://www.couchbase.com/blog/announcing-couchbase-6-0/
    "6.0.1": datetime(2019, 2, 15),  # https://web.archive.org/web/20190307191211/https://docs.couchbase.com/server/6.0/release-notes/relnotes.html
    "6.6.0": datetime(2020, 8, 12),  # https://www.couchbase.com/blog/whats-new-and-improved-in-couchbase-server-6-6/
    "7.2.0": datetime(2023, 6, 1),  # https://www.couchbase.com/blog/couchbase-capella-spring-release-72/
}

product = endoflife.Product("couchbase-server")
print(f"::group::{product.name}")
main = http.fetch_url(f"{URLS}/current/install/install-intro.html")
main_soup = BeautifulSoup(main.text, features="html5lib")

minor_versions = [options.attrs["value"] for options in main_soup.find(class_="version_list").find_all("option")]
minor_version_urls = [f"{URLS}/{minor}/release-notes/relnotes.html" for minor in minor_versions]

for minor_version in http.fetch_urls(minor_version_urls):
    minor_version_soup = BeautifulSoup(minor_version.text, features="html5lib")

    for title in minor_version_soup.find_all("h2"):
        match = VERSION_AND_DATE_PATTERN.match(title.get_text().strip())
        if match:
            version = match["version"]
            version = f"{version}.0" if len(version.split(".")) == 2 else version
            date = dates.parse_month_year_date(match['date'])
            product.declare_version(version, date)

product.declare_versions(MANUAL_VERSIONS)
product.write()
print("::endgroup::")
