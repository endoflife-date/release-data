import re

import mwparserfromhell
from common import dates, endoflife, http, releasedata

DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        response = http.fetch_url(config.url)
        wikicode = mwparserfromhell.parse(response.text)

        for tr in wikicode.ifilter_tags(matches=lambda node: node.tag == "tr"):
            items = tr.contents.filter_tags(matches=lambda node: node.tag == "td")
            if len(items) < 2:
                continue

            version = items[0].__strip__()
            date_str = items[1].__strip__()
            if config.first_match(version) and DATE_PATTERN.match(date_str):
                date = dates.parse_date(date_str)
                product_data.declare_version(version, date)
