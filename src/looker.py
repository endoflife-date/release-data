import re
import xml.dom.minidom

from bs4 import BeautifulSoup
from common import dates, endoflife, http

"""Fetch Looker versions from the Google Cloud release notes RSS feed.
"""

ANNOUNCEMENT_PATTERN = re.compile(r"includes\s+the\s+following\s+changes", re.IGNORECASE)
VERSION_PATTERN = re.compile(r"Looker\s+(?P<version>\d+\.\d+)", re.IGNORECASE)

product = endoflife.Product("looker")
print(f"::group::{product.name}")
response = http.fetch_url("https://cloud.google.com/feeds/looker-release-notes.xml")
rss = xml.dom.minidom.parseString(response.text)

for item in rss.getElementsByTagName("entry"):
    content = item.getElementsByTagName("content")[0].firstChild.nodeValue
    content_soup = BeautifulSoup(content, features="html5lib")

    announcement_match = content_soup.find(string=ANNOUNCEMENT_PATTERN)
    if not announcement_match:
        continue

    version_match = VERSION_PATTERN.search(announcement_match.parent.get_text())
    if not version_match:
        continue

    version = version_match.group("version")
    date_str = item.getElementsByTagName("updated")[0].firstChild.nodeValue
    date = dates.parse_datetime(date_str)
    product.declare_version(version, date)

product.write()
print("::endgroup::")
