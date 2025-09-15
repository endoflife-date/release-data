from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetch Tails versions from their announcement RSS feed.
"""

config = config_from_argv()
with ProductData(config.product) as product_data:
    rss = http.fetch_xml(config.url)

    for item in rss.getElementsByTagName("item"):
        title = item.getElementsByTagName("title").item(0).firstChild.nodeValue

        version_match = config.first_match(title)
        if not version_match:
            continue

        name = config.render(version_match)
        date = dates.parse_datetime(item.getElementsByTagName("pubDate").item(0).firstChild.nodeValue)
        product_data.declare_version(name, date)
