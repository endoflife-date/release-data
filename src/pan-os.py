from common import dates, endoflife, http, releasedata

"""Fetches pan-os versions from https://github.com/mrjcap/panos-versions/."""

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        versions = http.fetch_json(config.url)

        for version in versions:
            name = version['version']
            date = dates.parse_datetime(version['released-on'])
            product_data.declare_version(name, date)
