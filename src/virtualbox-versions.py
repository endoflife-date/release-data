from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches versions from download.virtualbox.org."""

config = config_from_argv()
with ProductData(config.product) as product_data:
    html = http.fetch_html(config.url)

    for a in html.select("a"):
        href = a["href"]

        version_match = config.first_match(href)
        if version_match:
            version = config.render(version_match)
            date_str = a.next_sibling.strip().split(" ")[0]
            date = dates.parse_date(date_str)
            product_data.declare_version(version, date)
