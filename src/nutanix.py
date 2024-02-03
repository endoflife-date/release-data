from common import dates, http, releasedata

"""Fetch Nutanix products versions from https://portal.nutanix.com/api/v1."""

PRODUCTS = {
    'nutanix-aos': 'https://portal.nutanix.com/api/v1/eol/find?type=NOS',
    'nutanix-files': 'https://portal.nutanix.com/api/v1/eol/find?type=FILES',
    'nutanix-prism': 'https://portal.nutanix.com/api/v1/eol/find?type=PC',
}

for product_name, url in PRODUCTS.items():
    with releasedata.ProductData(product_name) as product_data:
        data = http.fetch_url(url).json()
        for version_data in data["contents"]:
            if 'GENERAL_AVAILABILITY' in version_data:
                version = version_data["version"]
                date = dates.parse_datetime(version_data["GENERAL_AVAILABILITY"])
                product_data.declare_version(version, date)
