import logging

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        response = http.fetch_url(config.url)
        for line in response.text.strip().split('\n'):
            items = line.split('|')
            if len(items) >= 5 and config.first_match(items[1].strip()):
                version = items[1].strip()
                try:
                    date = dates.parse_date(items[3])
                    product_data.declare_version(version, date)
                except Exception as e:
                    logging.exception(f"Could not process release {version} for {config.product}: {e}")
