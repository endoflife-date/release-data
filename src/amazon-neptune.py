import logging

from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches Amazon Neptune versions from its RSS feed on docs.aws.amazon.com."""

config = config_from_argv()
with ProductData(config.product) as product_data:
    rss = http.fetch_xml(config.url)

    for entry in rss.getElementsByTagName("item"):
        version_str = entry.getElementsByTagName("title")[0].firstChild.nodeValue
        date_str = entry.getElementsByTagName("pubDate")[0].firstChild.nodeValue

        version_match = config.first_match(version_str)
        if not version_match:
            logging.warning(f"Skipping entry with malformed version: {version_str}")
            continue

        version = config.render(version_match)
        date = dates.parse_datetime(date_str)
        product_data.declare_version(version, date)
