from bs4 import BeautifulSoup
from common import http
from common import dates
from common import endoflife

URL = "https://docs.plesk.com/release-notes/obsidian/change-log"
PRODUCT = "plesk"


def make_bs_request(url):
    response = http.fetch_url(url)
    return BeautifulSoup(response.text, features="html5lib")


# Only 18.0.20.3 and later will be picked up :
# - format of the title for 18.0.20 and 18.0.19 are different,
# - there is not entry for GA of version 18.0.18 and older.
def fetch_releases():
    result = {}

    soup = make_bs_request(URL)
    releases = soup.find_all("div", class_="changelog-entry--obsidian")
    for release in releases:
        version = release.h2.text.strip()
        if not version.startswith('Plesk Obsidian 18'):
            continue

        version = version.replace(' Update ', '.').replace('Plesk Obsidian ', '')
        if ' ' in version:
            continue
        date = dates.parse_date(release.p.text).strftime("%Y-%m-%d")
        result[version] = date
        print(f"{version}: {date}")

    return result


print(f"::group::{PRODUCT}")
versions = fetch_releases()
endoflife.write_releases(PRODUCT, versions)
print("::endgroup::")
