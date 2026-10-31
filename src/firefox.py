from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetch Firefox version dates from whattrainisitnow.com's desktop and ESR APIs."""

FIREFOX_RELEASES_APIS = ["https://whattrainisitnow.com/api/esr/releases/", "https://whattrainisitnow.com/api/firefox/releases/"]

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        for api_url in FIREFOX_RELEASES_APIS:
            releases = http.fetch_json(api_url)
            for version, date_str in releases.items():
                product_data.declare_version(version, dates.parse_date(date_str))
