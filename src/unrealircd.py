import re

from common import dates, http, releasedata

DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")

for config in releasedata.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
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
