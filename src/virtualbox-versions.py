from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetches versions from download.virtualbox.org."""

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        html = http.fetch_html(config.url)

        for a in html.select("a"):
            href = a["href"]

            if (version_match := config.first_match(href)):
                version = config.render(version_match)
                date_str = a.next_sibling.strip().split(" ")[0]
                date = dates.parse_date(date_str)
                product_data.declare_version(version, date)
