from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        # Fetch major versions
        latest_by_major = http.fetch_url(config.url).json()
        major_version_urls = [f"{config.url}&version={major_version}" for major_version in latest_by_major]

        # Fetch all versions for major versions
        for major_versions_response in http.fetch_urls(major_version_urls):
            major_versions_data = major_versions_response.json()
            for version in major_versions_data:
                if config.first_match(version):  # exclude versions such as "3.0.x (latest)"
                    date = dates.parse_date(major_versions_data[version]["date"])
                    product_data.declare_version(version, date)
