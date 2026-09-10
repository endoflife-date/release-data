from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetch OpenSIPS release-cycle data from the OpenSIPS releases API."""


RELEASE_FIELDS = {"releaseDate", "lts", "eol", "latest", "latestReleaseDate"}


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        for release_name, release_data in http.fetch_json(config.url).get("releases", {}).items():
            release = product_data.get_release(release_data.get("name", release_name))
            for field, value in release_data.items():
                if field in RELEASE_FIELDS:
                    release.set_field(
                        field,
                        dates.parse_date(value) if isinstance(value, str) and (field.endswith("Date") or field == "eol") else value,
                    )
