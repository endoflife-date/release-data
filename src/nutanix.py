from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetch Nutanix products versions from https://portal.nutanix.com/api/v1."""

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        data = http.fetch_json(f"https://portal.nutanix.com/api/v1/eol/find?type={config.url}")

        for version_data in data["contents"]:
            if 'GENERAL_AVAILABILITY' in version_data:
                version = version_data["version"]
                date = dates.parse_datetime(version_data["GENERAL_AVAILABILITY"]).replace(second=0)
                product_data.declare_version(version, date)
