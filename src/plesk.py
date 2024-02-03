from bs4 import BeautifulSoup
from common import dates, http, releasedata

"""Fetches versions from Plesk's change log.

Only 18.0.20.3 and later will be picked up, as the format of the change log for 18.0.20 and 18.0.19 are different and
there is no entry for GA of version 18.0.18 and older."""

with releasedata.ProductData("plesk") as product_data:
    response = http.fetch_url("https://docs.plesk.com/release-notes/obsidian/change-log")
    soup = BeautifulSoup(response.text, features="html5lib")

    for release in soup.find_all("div", class_="changelog-entry--obsidian"):
        version = release.h2.text.strip()
        if not version.startswith('Plesk Obsidian 18'):
            continue

        version = version.replace(' Update ', '.').replace('Plesk Obsidian ', '')
        if ' ' in version:
            continue

        date = dates.parse_date(release.p.text)
        product_data.declare_version(version, date)
