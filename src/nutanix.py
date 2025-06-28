from common import dates, endoflife, http, releasedata

"""Fetch Nutanix products versions from https://portal.nutanix.com/api/v1."""

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        data = http.fetch_json(f"https://portal.nutanix.com/api/v1/eol/find?type={config.url}")

        for version_data in data["contents"]:
            release_name = '.'.join(version_data["version"].split(".")[:2])

            if 'GENERAL_AVAILABILITY' in version_data:
                version = version_data["version"]
                date = dates.parse_datetime(version_data["GENERAL_AVAILABILITY"]).replace(second=0)
                product_data.declare_version(version, date)
