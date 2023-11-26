import re
from bs4 import BeautifulSoup
from common import dates
from common import endoflife

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
URLS = "https://docs.couchbase.com/server"
FIXED_VERSIONS = {
    "6.0.0": "2018-10-31",  # https://www.couchbase.com/blog/announcing-couchbase-6-0/
    "6.0.1": "2019-02-15",  # https://web.archive.org/web/20190307191211/https://docs.couchbase.com/server/6.0/release-notes/relnotes.html
    "6.6.0": "2020-08-12",  # https://www.couchbase.com/blog/whats-new-and-improved-in-couchbase-server-6-6/
    "7.2.0": "2023-06-01",  # https://www.couchbase.com/blog/couchbase-capella-spring-release-72/
}

print(f"::group::{PRODUCT}")
versions = {}

response = endoflife.fetch_url(f"{URLS}/current/install/install-intro.html")
soup = BeautifulSoup(response, features="html5lib")

minor_versions = [options.attrs["value"] for options in soup.find(class_="version_list").find_all("option")]

# there is no date available for x.y.0
for minor in minor_versions:
    versions[minor + '.0'] = 'N/A'

minor_version_urls = [f"{URLS}/{minor}/release-notes/relnotes.html" for minor in minor_versions]
for response in endoflife.fetch_urls(minor_version_urls):
    soup = BeautifulSoup(response.text, features="html5lib")
    for title in soup.find_all("h2"):
        versionAndDate = title.get_text().strip()
        m = re.match(REGEX, versionAndDate)
        if m:
            version = f"{m['version']}.0" if len(m['version'].split('.')) == 2 else m['version']
            date = dates.parse_month_year_date(m['date']).strftime("%Y-%m-%d")
            versions[version] = date
            print(f"{version}: {date}")

versions = versions | FIXED_VERSIONS
endoflife.write_releases(PRODUCT, versions)
print("::endgroup::")
