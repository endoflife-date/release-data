from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime


PRODUCT = "ibm-aix"
URL = "https://www.ibm.com/support/pages/aix-support-lifecycle-information"


# Convert date from e.g. "November 2022" format to "2022-11-01"
def convert_date(date_str):
    return datetime.strptime(date_str, "%B %Y").strftime("%Y-%m-%d")


def fetch_releases():
    response = endoflife.fetch_url(URL)
    soup = BeautifulSoup(response, features="html5lib")

    releases = {}
    # for all release tables
    for release_table in soup.find("div", class_="ibm-container-body").find_all("table", class_="ibm-data-table ibm-grid"):
        # for all rows except the header one
        for row in release_table.find_all("tr")[1:]:
            cells = row.find_all("td")
            version = cells[0].text.strip("AIX ").replace(' TL', '.')
            date = convert_date(cells[1].text)
            print(f"{version} : {date}")
            releases[version] = date

    return releases


print(f"::group::{PRODUCT}")
versions = fetch_releases()
endoflife.write_releases(PRODUCT, versions)
print("::endgroup::")
