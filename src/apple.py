import logging
import re

from bs4 import BeautifulSoup
from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches and parses version and release date information from Apple's support website."""

URLS = [
    "https://support.apple.com/kb/HT201222",  # latest
    "https://support.apple.com/en-us/121012",  # 2022-2023
    "https://support.apple.com/en-us/120989",  # 2020-2021
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

config = config_from_argv()
with ProductData(config.product) as product_data:
    responses = http.fetch_urls(URLS)

    for response in responses:
        soup = BeautifulSoup(response.text, "html5lib")
        versions_table = soup.select_one("#tableWraper")
        versions_table = versions_table if versions_table else soup.select_one("table.gb-table")

        if not versions_table:
            message = f"no versions table found in {response.url}"
            raise ValueError(message)

        for row in versions_table.find_all("tr")[1:]:
            cells = row.find_all("td")
            version_text = cells[0].get_text(separator=" ").strip()
            date_text = cells[2].get_text(separator=" ").strip()

            date_match = DATE_PATTERN.search(date_text)
            if not date_match:
                logging.info(f"ignoring version {version_text} ({date_text}), date pattern don't match")
                continue

            date_str = date_match.group(0)
            date = dates.parse_date(date_str)
            for version_pattern in config.include_version_patterns:
                for version_str in version_pattern.findall(version_text):
                    version = product_data.get_version(version_str)
                    if not version or version.date() > date:
                        product_data.declare_version(version_str, date)
                    else:
                        logging.info(f"ignoring version {version_str} ({date}) for {product_data.name}")
