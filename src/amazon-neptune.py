import logging

from common import dates, http, releasedata

"""Fetches Amazon Neptune versions from its RSS feed on docs.aws.amazon.com."""

for config in releasedata.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        rss = http.fetch_xml(config.url)

        for entry in rss.getElementsByTagName("item"):
            version_str = entry.getElementsByTagName("title")[0].firstChild.nodeValue
            date_str = entry.getElementsByTagName("pubDate")[0].firstChild.nodeValue

            version_match = config.first_match(version_str)
            if not version_match:
                logging.warning(f"Skipping entry with malformed version: {entry}")
                continue

            version = config.render(version_match)
            date = dates.parse_datetime(date_str)
            product_data.declare_version(version, date)
