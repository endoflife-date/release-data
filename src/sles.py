import json
import urllib.request

from bs4 import BeautifulSoup
from datetime import datetime


PRODUCT = "sles"
URL = "https://www.suse.com/lifecycle"


def fetch_releases(url):
    headers = {"user-agent": "mozilla"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=5) as response:
        return BeautifulSoup(response, features="html5lib")


def convert_date(date_str):
    return datetime.strptime(date_str, "%d %b %Y").strftime("%Y-%m-%d")


def strip_version(version_str):
    return version_str.strip("SUSE Linux Enterprise Server ")


"""
Takes soup, and returns a dictionary of versions and their release dates
"""
def parse_soup_for_versions(soup):
    """ Parse the soup """
    versions = {}
    products_table = soup.find("tbody", id="productSupportLifecycle")
    # Get rows with SLES products
    sles_header_rows = products_table.find_all("tr", class_="row", attrs={"data-productfilter": "SUSE Linux Enterprise Server"})
    # Extract rows' IDs to find related subrows with details (normally hidden until a user expands a section)
    sles_detail_ids = [f"detail{row['id']}" for row in sles_header_rows]
    for detail_id in sles_detail_ids:
        detail_row = products_table.find("tr", id=detail_id)
        # There is a table with info about minor releases and after it optionally a table with info about modules
        minor_versions_table = detail_row.find_all("tbody")[0]
        # The first subrow is a header, the rest contain info about the first release and later minor releases of a SLES product
        minor_version_rows = minor_versions_table.find_all("tr")[1:]
        for row in minor_version_rows:
            # For each minor release there is an FCS date, general support end date and LTSS end date
            cells = row.find_all("td")
            # Remove unnecessary prefix
            version = strip_version(cells[0].text)
            # Convert date from e.g. "16 Jul 2018" to "2018-07-16"
            release_date = convert_date(cells[1].text)
            versions[version] = release_date
            print(f"{version}: {release_date}")
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
