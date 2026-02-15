from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches Unity versions from the Unity Editor Release API.

This script fetches stable releases from the Unity API, filtering out alpha, beta, and other pre-release versions.
The API provides paginated results with all Unity versions across different streams (TECH, LTS, BETA, ALPHA).
"""

config = config_from_argv()
with ProductData(config.product) as product_data:
    offset = 0
    limit = 25

    while True:
        url = f"{config.url}?limit={limit}&offset={offset}"
        data = http.fetch_json(url)

        if 'results' not in data:
            break

        for release in data['results']:
            version = release['version']

            # Skip pre-release versions (ALPHA, BETA, etc.)
            stream = release.get('stream', '')
            if stream in ('ALPHA', 'BETA'):
                continue

            date = dates.parse_datetime(release['releaseDate'])
            product_data.declare_version(version, date)

        # Check if we've reached the end
        total = data.get('total', 0)
        offset += limit
        if offset >= total:
            break
