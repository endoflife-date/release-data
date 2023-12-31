import logging
import re

from bs4 import BeautifulSoup
from common import dates, endoflife, http

"""Fetches and parses version and release date information from Apple's support website for macOS,
iOS, iPadOS, and watchOS. While all URLs are fetched once for performance reasons, the actual
parsing for each product is done in a separate loop for having easier-to-read logs."""

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

# If you are changing these, please use
# https://gist.githubusercontent.com/captn3m0/e7cb1f4fc3c07a5da0296ebda2b33e15/raw/5747e42ad611ec9ffdb7a2d1c0e3946bb87ab6d7/apple.txt
# as your corpus to validate your changes
VERSION_PATTERNS = {
    "macos": [
        # This covers Sierra and beyond
        re.compile(r"^macOS[\D]+(?P<version>\d+(?:\.\d+)*)", re.MULTILINE),
        # This covers Mavericks - El Capitan
        re.compile(r"OS\s+X\s[\w\s]+\sv?(?P<version>\d+(?:\.\d+)+)", re.MULTILINE),
        # This covers even older versions (OS X)
        re.compile(r"^Mac\s+OS\s+X\s[\w\s]+\sv?(?P<version>\d{2}(?:\.\d+)+)", re.MULTILINE),
    ],
    "ios": [
        re.compile(r"iOS\s+(?P<version>\d+)", re.MULTILINE),
        re.compile(r"iOS\s+(?P<version>\d+(?:\.\d+)+)", re.MULTILINE),
        re.compile(r"iPhone\s+v?(?P<version>\d+(?:\.\d+)+)", re.MULTILINE),
    ],
    "ipados": [
        re.compile(r"iPadOS\s+(?P<version>\d+)", re.MULTILINE),
        re.compile(r"iPadOS\s+(?P<version>\d+(?:\.\d+)+)", re.MULTILINE),
    ],
    "watchos": [
        re.compile(r"watchOS\s+(?P<version>\d+)", re.MULTILINE),
        re.compile(r"watchOS\s+(?P<version>\d+(?:\.\d+)+)", re.MULTILINE),
    ],
}

DATE_PATTERN = re.compile(r"\b\d+\s[A-Za-z]+\s\d+\b")

logging.info("::group::apple")
soups = [BeautifulSoup(response.text, features="html5lib") for response in http.fetch_urls(URLS)]
logging.info("::endgroup::")

for product_name in VERSION_PATTERNS:
    product = endoflife.Product(product_name)
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
            for version_pattern in VERSION_PATTERNS[product.name]:
                for version in version_pattern.findall(version_text):
                    if not product.has_version(version):
                        product.declare_version(version, date)
                    elif product.get_version_date(version) > date:
                        product.replace_version(version, date)
                    else:
                        logging.info(f"ignoring version {version} ({date}) for {product.name}")

    product.write()
