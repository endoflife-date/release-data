from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime

URL = "https://docs.plesk.com/release-notes/obsidian/change-log"
PRODUCT = "plesk"


def make_bs_request(url):
    response = endoflife.fetch_url(url)
    return BeautifulSoup(response, features="html5lib")


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
        date = datetime.strptime(release.p.text.strip(), '%d %B %Y').strftime("%Y-%m-%d")
        result[version] = date
        print(f"{version}: {date}")

    return result


print(f"::group::{PRODUCT}")
releases = fetch_releases()
endoflife.write_releases(PRODUCT, dict(
    # sort by date then version (desc)
    sorted(releases.items(), key=lambda x: (x[1], x[0]), reverse=True)
))
print("::endgroup::")
