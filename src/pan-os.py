from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetches pan-os versions from https://github.com/mrjcap/panos-versions/."""

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        versions = http.fetch_json(config.url)

        for version in versions:
            name = version['version']
            date = dates.parse_datetime(version['released-on'])
            product_data.declare_version(name, date)
