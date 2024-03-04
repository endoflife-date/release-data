import sys

from common import dates, endoflife, http, releasedata

"""Fetch Nutanix products versions from https://portal.nutanix.com/api/v1."""

METHOD = 'nutanix'

p_filter = sys.argv[1] if len(sys.argv) > 1 else None
m_filter = sys.argv[2] if len(sys.argv) > 2 else None
for config in endoflife.list_configs(p_filter, METHOD, m_filter):
    with releasedata.ProductData(config.product) as product_data:
        url = f"https://portal.nutanix.com/api/v1/eol/find?type={config.url}"
        data = http.fetch_url(url).json()
        for version_data in data["contents"]:
            release_name = '.'.join(version_data["version"].split(".")[:2])

            if 'GENERAL_AVAILABILITY' in version_data:
                version = version_data["version"]
                date = dates.parse_datetime(version_data["GENERAL_AVAILABILITY"]).replace(second=0)
                product_data.declare_version(version, date)
