import re

from bs4 import BeautifulSoup
from common import dates, http, releasedata

"""Fetch Looker versions from the Google Cloud release notes RSS feed.
"""

ANNOUNCEMENT_PATTERN = re.compile(r"includes\s+the\s+following\s+changes", re.IGNORECASE)

for config in releasedata.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        rss = http.fetch_xml(config.url)

        for item in rss.getElementsByTagName("entry"):
            content = item.getElementsByTagName("content")[0].firstChild.nodeValue
            content_soup = BeautifulSoup(content, features="html5lib")

            announcement_match = content_soup.find(string=ANNOUNCEMENT_PATTERN)
            if not announcement_match:
                continue

            version_match = config.first_match(announcement_match.parent.get_text())
            if not version_match:
                continue
            version = config.render(version_match)

            date_str = item.getElementsByTagName("updated")[0].firstChild.nodeValue
            date = dates.parse_datetime(date_str)

            product_data.declare_version(version, date)
