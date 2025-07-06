from common import dates, http
from common.releasedata import ProductData, config_from_argv

config = config_from_argv()
with ProductData(config.product) as product_data:
    data = http.fetch_json(f"https://registry.npmjs.org/{config.url}")
    for version_str in data["versions"]:
        version_match = config.first_match(version_str)
        if version_match:
            version = config.render(version_match)
            date = dates.parse_datetime(data["time"][version_str])
            product_data.declare_version(version, date)
