import logging
import re

from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

"""Fetches and parses version and release date information from Apple's support website."""

URLS = [
    "https://support.apple.com/en-us/HT201222",  # latest
    "https://support.apple.com/kb/HT213078",  # 2018-2019
    "https://support.apple.com/kb/HT213077",  # 2016-2017
    "https://support.apple.com/kb/HT209441",  # 2015
    "https://support.apple.com/kb/HT205762",  # 2014
    "https://support.apple.com/kb/HT205759",  # 2013
    "https://support.apple.com/kb/HT204611",  # 2011 to 2012
    # Apple still links to the following articles, but they are 404:
    "http://web.archive.org/web/20230404214605_/https://support.apple.com/en-us/HT5165",  # 2010
    "http://web.archive.org/web/20230327200842_/https://support.apple.com/en-us/HT4218",  # 2008-2009
    "http://web.archive.org/web/20230204234533_/https://support.apple.com/en-us/HT1263",  # 2005-2007
]

DATE_PATTERN = re.compile(r"\b\d+\s[A-Za-z]+\s\d+\b")

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        # URLs are cached to avoid rate limiting by support.apple.com.
        soups = [BeautifulSoup(response.text, features="html5lib") for response in http.fetch_urls(URLS)]

        for soup in soups:
            versions_table = soup.find(id="tableWraper")
            versions_table = versions_table if versions_table else soup.find('table', class_="gb-table")

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
