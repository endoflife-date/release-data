import logging
import re
import sys

from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

"""Fetches and parses version and release date information from Apple's support website."""

URLS = [
    "https://support.apple.com/en-us/100100",  # latest
    "https://support.apple.com/en-us/103179",  # 2018-2019
    "https://support.apple.com/en-us/103178",  # 2016-2017
    "https://support.apple.com/en-us/103813",  # 2015
    "https://support.apple.com/en-us/101445",  # 2014
    "https://support.apple.com/en-us/100502",  # 2013
    "https://support.apple.com/en-us/101444",  # 2011 to 2012
    "https://support.apple.com/en-us/104188",  # 2010
    "https://support.apple.com/en-us/104189",  # 15-Jan-2008 to 03-Dec-2009
    "https://support.apple.com/en-us/104190",  # 25-Jan-2005 to 21-Dec-2007
    "https://support.apple.com/en-us/101682",  # 03-Oct-2003 to 11-Jan-2005
    "https://support.apple.com/en-us/104191",  # August, 2003 to ~Jun 2001
]

DATE_PATTERN = re.compile(r"\b\d+\s[A-Za-z]+\s\d+\b")
METHOD = 'apple'

p_filter = sys.argv[1] if len(sys.argv) > 1 else None
m_filter = sys.argv[2] if len(sys.argv) > 2 else None
for config in endoflife.list_configs(p_filter, METHOD, m_filter):
    with releasedata.ProductData(config.product) as product_data:
        # URLs are cached to avoid rate limiting by support.apple.com.
        soups = [BeautifulSoup(response.text, features="html5lib") for response in http.fetch_urls(URLS, cache=True)]

        for soup in soups:
            versions_table = soup.find(id="tableWraper")
            versions_table = versions_table if versions_table else soup.find('table', class_="gb-table")

            if not versions_table:
                continue
            for row in versions_table.findAll("tr")[1:]:
                cells = row.findAll("td")
                version_text = cells[0].get_text().strip()
                date_text = cells[2].get_text().strip()

                date_match = DATE_PATTERN.search(date_text)
                if not date_match:
                    logging.info(f"ignoring version {version_text} ({date_text}), date pattern don't match")
                    continue

                date_str = date_match.group(0).replace("Sept ", "Sep ")
                date = dates.parse_date(date_str)
                for version_pattern in config.include_version_patterns:
                    for version_str in version_pattern.findall(version_text):
                        version = product_data.get_version(version_str)
                        if not version or version.date() > date:
                            product_data.declare_version(version_str, date)
                        else:
                            logging.info(f"ignoring version {version_str} ({date}) for {product_data.name}")
