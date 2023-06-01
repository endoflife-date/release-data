import json
import urllib.request

from bs4 import BeautifulSoup
from datetime import datetime


PRODUCT = "ibm-aix"
URL = "https://www.ibm.com/support/pages/aix-support-lifecycle-information"


def fetch_releases(url):
    headers = {"user-agent": "mozilla"}    
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=5) as response:
        return BeautifulSoup(response, features="html5lib")


def convert_date(date_str):
    return datetime.strptime(date_str, "%B %Y").strftime("%Y-%m-%d")


def strip_version(version_str):
    return version_str.strip("AIX ")


"""
Takes soup, and returns a dictionary of versions and their release dates
"""
def parse_soup_for_versions(soup):
    """ Parse the soup """
    versions = {}
    # Get the main page content div
    main_content = soup.find("div", class_="ibm-container-body")
    # Parse data tables
    for release_table in main_content.find_all("table", class_="ibm-data-table ibm-grid"):
        # Extract rows from the table
        rows = release_table.find_all("tr")
        # Skip the header row
        # Each row consists of five cells - first one is the version, the second one is the release date 
        for tr in rows[1:]:
            cells = tr.find_all("td")
            # Strip the version string from unneeded "AIX " prefix
            version = strip_version(cells[0].text)
            # Convert date from e.g. "November 2022" format to "2022-11-01"
            release_date = convert_date(cells[1].text)
            versions[version] = release_date
            print("%s: %s" % (version, release_date))
    return versions


def main():
    print(f"::group::{PRODUCT}")
    content = fetch_releases(URL)
    releases = parse_soup_for_versions(content)
    print("::endgroup::")

    with open(f"releases/{PRODUCT}.json", "w") as f:
        f.write(json.dumps(dict(
            # sort by version then date (asc)
            sorted(releases.items(), key=lambda x: (x[0], x[1]))
        ), indent=2))


if __name__ == "__main__":
    main()
