import logging

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetches EOL dates from Citrix Virtual Apps and Desktops Download Updates RSS feed."""

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        rss = http.fetch_xml(config.url)

        for entry in rss.getElementsByTagName("item"):
            version_str = entry.getElementsByTagName("title")[0].firstChild.nodeValue
            date_str = entry.getElementsByTagName("pubDate")[0].firstChild.nodeValue

            if not (version_match := config.first_match(version_str)):
                logging.info(f"Skipping unmatched entry: {version_str}")
                continue

            logging.debug(f"Processing version: {version_str} with date {date_str}")
            version = config.render(version_match)
            date = dates.parse_datetime(date_str)
            product_data.declare_version(version, date)
