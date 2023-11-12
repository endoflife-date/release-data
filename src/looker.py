import re

from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime, timezone
from xml.dom.minidom import parseString

"""Fetch Looker versions with their dates from the Google Cloud release notes RSS feed.
"""

PRODUCT = "looker"
URL = "https://cloud.google.com/feeds/looker-release-notes.xml"
ANNOUNCEMENT_PATTERN = re.compile(r"includes\s+the\s+following\s+changes", re.IGNORECASE)
VERSION_PATTERN = re.compile(r"Looker\s+(?P<version>\d+\.\d+)", re.IGNORECASE)


def parse_date(date_str):
    return datetime.fromisoformat(date_str).astimezone(timezone.utc).strftime("%Y-%m-%d")

print(f"::group::{PRODUCT}")
versions = {}

response = endoflife.fetch_url(URL)
rss = parseString(response)
for item in rss.getElementsByTagName("entry"):
    date = parse_date(item.getElementsByTagName("updated")[0].firstChild.nodeValue)
    content = item.getElementsByTagName("content")[0].firstChild.nodeValue
    soup = BeautifulSoup(content, features="html5lib")

    announcement = soup.find(string=ANNOUNCEMENT_PATTERN)
    if announcement:
        m = re.search(VERSION_PATTERN, announcement.parent.get_text())
        if m:
            version = m.group("version")
            versions[version] = date
            print(f"{version}: {date}")

endoflife.write_releases(PRODUCT, versions)
print("::endgroup::")
