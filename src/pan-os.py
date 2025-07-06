from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches pan-os versions from https://github.com/mrjcap/panos-versions/."""

config = config_from_argv()
with ProductData(config.product) as product_data:
    versions = http.fetch_json(config.url)

    for version in versions:
        name = version['version']
        date = dates.parse_datetime(version['released-on'])
        product_data.declare_version(name, date)
