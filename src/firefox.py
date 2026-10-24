from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetch Firefox version dates from whattrainisitnow.com's desktop and ESR APIs.

Versions with a major number below 100 are skipped. Existing versions are retained, and their dates are refreshed
when the API reports a different date."""

FIREFOX_RELEASES_APIS = ["https://whattrainisitnow.com/api/esr/releases/", "https://whattrainisitnow.com/api/firefox/releases/"]
# Avoid adding the large historical version range while retaining existing data for older versions.
MIN_FIREFOX_MAJOR_VERSION = 100

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        for api_url in FIREFOX_RELEASES_APIS:
            releases = http.fetch_json(api_url)
            for version, date_str in releases.items():
                major_version = int(version.split(".", maxsplit=1)[0])
                if major_version < MIN_FIREFOX_MAJOR_VERSION:
                    continue

                product_data.declare_version(version, dates.parse_date(date_str))
