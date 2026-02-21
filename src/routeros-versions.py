import logging
import re

from bs4 import BeautifulSoup
from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches versions from MikroTik RouterOS release notes page.

This script only considers stable and long-term versions, and ignores testing and development versions.
"""

config = config_from_argv()
with ProductData(config.product) as product_data:
    content = http.fetch_javascript_url(config.url)
    soup = BeautifulSoup(content, features="html5lib")

    for release_line in soup.select("div.grow"):
        text = re.sub(r'\s+', ' ', release_line.get_text()).strip()
        parts = text.split(' ')
        if len(parts) != 3:
            logging.debug(f"Skipping '{text}', not in expected format")
            continue

        version = parts[0]
        channel = parts[1].lower()
        release_date = dates.parse_date(parts[2])
        if channel in ["stable", "long-term"]:
            product_data.declare_version(version, release_date)
