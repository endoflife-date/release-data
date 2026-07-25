from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        data = http.fetch_json(config.url)
        for v in data:
            if v['type'] == 'development':
                continue

            version = v["version"]
            date = dates.parse_datetime(v["date"], to_utc=False)  # utc kept for now for backwards compatibility
            product_data.declare_version(version, date)
