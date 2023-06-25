import re
from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime

PRODUCT = "sles"
URL = "https://www.suse.com/lifecycle"
DATE_FORMAT = "%d %b %Y"


# Convert date from e.g. "16 Jul 2018" to "2018-07-16"
def convert_date(date_str):
    # If the date begins with a >3 letter month name, trim it to just 3 letters
    # Strip out the Date: section from the start
    d = re.sub(r'(\d{1,2}) (\w{3})(?:\w{1,4})? (\d{4})', r'\1 \2 \3', date_str)
    return datetime.strptime(d, DATE_FORMAT).strftime('%Y-%m-%d')


def strip_version(version_str):
    return version_str.strip("SUSE Linux Enterprise Server ").replace(' SP', '.')


def fetch_releases():
    response = endoflife.fetch_url(URL)
    soup = BeautifulSoup(response, features="html5lib")
    products_table = soup.find("tbody", id="productSupportLifecycle")
    # Get rows with SLES products
    sles_header_rows = products_table.find_all("tr", class_="row", attrs={"data-productfilter": "SUSE Linux Enterprise Server"})
    # Extract rows' IDs to find related sub-rows with details (normally hidden
    # until a user expands a section)
    sles_detail_ids = [f"detail{row['id']}" for row in sles_header_rows]

    versions = {}
    # for all release tables
    for detail_id in sles_detail_ids:
        detail_row = products_table.find("tr", id=detail_id)
        # There is a table with info about minor releases and after it
        # optionally a table with info about modules
        minor_versions_table = detail_row.find_all("tbody")[0]
        # The first sub-row is a header, the rest contains info about the first
        # release and later minor releases of a SLES product
        minor_version_rows = minor_versions_table.find_all("tr")[1:]
        for row in minor_version_rows:
            # For each minor release there is an FCS date, general support end
            # date and LTSS end date
            cells = row.find_all("td")
            version = strip_version(cells[0].text)
            release_date = convert_date(cells[1].text)
            versions[version] = release_date
            print(f"{version}: {release_date}")

    return versions


print(f"::group::{PRODUCT}")
releases = fetch_releases()
endoflife.write_releases(PRODUCT, dict(
    # sort by version then date (asc)
    sorted(releases.items(), key=lambda x: (x[0], x[1]))
))
print("::endgroup::")
