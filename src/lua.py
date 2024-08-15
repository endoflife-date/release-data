import re

from bs4 import BeautifulSoup
from common import dates, http, releasedata

"""Fetches Lua releases from lua.org."""

RELEASED_AT_PATTERN = re.compile(r"Lua\s*(?P<release>\d+\.\d+)\s*was\s*released\s*on\s*(?P<release_date>\d+\s*\w+\s*\d{4})")
VERSION_PATTERN = re.compile(r"(?P<version>\d+\.\d+\.\d+),\s*released\s*on\s*(?P<version_date>\d+\s*\w+\s*\d{4})")

with releasedata.ProductData("lua") as product_data:
    page = http.fetch_url("https://www.lua.org/versions.html")
    soup = BeautifulSoup(page.text, 'html.parser')
    page_text = soup.text # HTML is broken, no way to parse it with beautifulsoup

    for release_match in RELEASED_AT_PATTERN.finditer(page_text):
        release = release_match.group('release')
        release_date = dates.parse_date(release_match.group('release_date'))
        product_data.get_release(release).set_release_date(release_date)

    for version_match in VERSION_PATTERN.finditer(page_text):
        version = version_match.group('version')
        version_date = dates.parse_date(version_match.group('version_date'))
        product_data.declare_version(version, version_date)
