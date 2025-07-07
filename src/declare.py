from datetime import datetime

from common.releasedata import ProductData, config_from_argv

"""Manually declare missing or erroneous versions."""

config = config_from_argv()
with ProductData(config.product) as product_data:
    for version in config.data.get("versions", []):
        product_data.declare_version(version['name'], version['date'])

    releases: list[dict[str, str | bool | datetime]] = config.data.get("releases", [])
    for release in releases:
        release_data = product_data.get_release(release.pop("name"))
        for key, value in release.items():
            release_data.set_field(key, value)
