from common import dates, http
from common.releasedata import ProductData, config_from_argv

config = config_from_argv()
with ProductData(config.product) as product_data:
    data = http.fetch_json(f"https://pypi.org/pypi/{config.url}/json")

    for version_str in data["releases"]:
        version_match = config.first_match(version_str)
        version_data = data["releases"][version_str]

        if version_match and version_data:
            version = config.render(version_match)
            date = dates.parse_datetime(version_data[0]["upload_time_iso_8601"])
            product_data.declare_version(version, date)
