import sys

from common import dates, endoflife, http, releasedata

METHOD = "npm"

p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product in endoflife.list_products(METHOD, p_filter):
    product_data = releasedata.Product(product.name)
    for config in product.get_auto_configs(METHOD):
        data = http.fetch_url(f"https://registry.npmjs.org/{config.url}").json()
        for version_str in data["versions"]:
            version_match = config.first_match(version_str)
            if version_match:
                version = config.render(version_match)
                date = dates.parse_datetime(data["time"][version_str])
                product_data.declare_version(version, date)

    product_data.write()
