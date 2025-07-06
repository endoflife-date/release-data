import re

from common import dates, http
from common.releasedata import ProductData, config_from_argv

DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")

config = config_from_argv()
with ProductData(config.product) as product_data:
    wikicode = http.fetch_markdown(config.url)

    for tr in wikicode.ifilter_tags(matches=lambda node: node.tag == "tr"):
        items = tr.contents.filter_tags(matches=lambda node: node.tag == "td")
        if len(items) < 2:
            continue

        version = items[0].__strip__()
        date_str = items[1].__strip__()
        if config.first_match(version) and DATE_PATTERN.match(date_str):
            date = dates.parse_date(date_str)
            product_data.declare_version(version, date)
