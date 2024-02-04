import sys

from common import dates, endoflife, http, releasedata

METHOD = "pypi"

p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product in endoflife.list_products(METHOD, p_filter):
    with releasedata.ProductData(product.name) as product_data:
        for config in product.get_auto_configs(METHOD):
            data = http.fetch_url(f"https://pypi.org/pypi/{config.url}/json").json()

            for version_str in data["releases"]:
                version_match = config.first_match(version_str)
                version_data = data["releases"][version_str]

                if version_match and version_data:
                    version = config.render(version_match)
                    date = dates.parse_datetime(version_data[0]["upload_time_iso_8601"])
                    product_data.declare_version(version, date)
