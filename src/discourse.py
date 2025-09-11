import logging
import re

from bs4 import BeautifulSoup
from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetch versions from a discourse server."""

config = config_from_argv()
with ProductData(config.product) as product_data:
    html = BeautifulSoup(http.fetch_javascript_url(config.url))

    for topic in html.select("tr.topic-list-item"):
        title = topic.select_one("span.link-top-line").get_text(strip=True)
        versions = config.first_match(title)
        if not versions:
            logging.debug("Skipping %s: does not match regex", title)
            continue

        name = config.render(versions)
        print(topic)
        date_str = topic.select_one("td.activity").get("title").strip()
        date_match = re.search(r"Created:\s*([A-Za-z]+\s+\d{1,2},\s+\d{4}\s+\d{1,2}:\d{2}\s+[ap]m)", date_str)
        if not date_match:
            logging.debug("Skipping %s: no created date found", title)
            continue

        date = dates.parse_datetime(date_match.group(1))
        product_data.declare_version(name, date)
