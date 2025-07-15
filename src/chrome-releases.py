import re

from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches versions from https://chromiumdash.appspot.com API."""

FIRST_AVAILABLE_VERSION = 7
DATE_REGEX = re.compile(r'Stable release date:')

config = config_from_argv()
with ProductData(config.product) as product_data:
    latest_release = int(product_data.get_latest_release().name())
    n_available_releases = latest_release - FIRST_AVAILABLE_VERSION

    releases = http.fetch_json(f"{config.url}?offset=-{n_available_releases}&n={n_available_releases + 1}")
    for json_release in releases.get("mstones", []):
        release = product_data.get_release(str(json_release["mstone"]))
        release_date = dates.parse_datetime(json_release["stable_date"])
        release.set_release_date(release_date)
