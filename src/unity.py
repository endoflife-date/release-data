from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetches Unity versions from the Unity Editor Release API.

This script fetches stable releases from the Unity API, filtering out alpha, beta, and other pre-release versions.
The API provides paginated results with all Unity versions across different streams (TECH, LTS, BETA, ALPHA).
"""

def declare_releases(product_data: ProductData, data: dict) -> None:
    for release in data.get('results', []):
        version = release['version']

        # Skip pre-release versions (ALPHA, BETA, etc.)
        stream = release.get('stream', '')
        if stream in ('ALPHA', 'BETA'):
            continue

        date = dates.parse_datetime(release['releaseDate'])
        product_data.declare_version(version, date)


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        limit = 25

        # Fetch the first page to determine how many releases there are in total.
        data = http.fetch_json(f"{config.url}?limit={limit}&offset=0")
        total = data.get('total', 0)
        declare_releases(product_data, data)

        # Fetch the remaining pages in parallel.
        urls = [f"{config.url}?limit={limit}&offset={offset}" for offset in range(limit, total, limit)]
        for response in http.fetch_urls(urls):
            declare_releases(product_data, response.json())
