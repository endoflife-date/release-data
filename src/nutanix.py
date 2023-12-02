from common import http
from common import endoflife

"""Fetch Nutanix products versions with their dates from https://portal.nutanix.com/api/v1.
"""

PRODUCTS = {
    'nutanix-aos': 'NOS',
    'nutanix-files': 'FILES',
    'nutanix-prism': 'PC',
}

BASE_URL = "https://portal.nutanix.com/api/v1/eol/find?type="


def fetch_releases(product_code):
    versions = {}
    url = BASE_URL + product_code
    print(url)
    response = http.fetch_url(url)
    data = response.json()

    for version_data in data["contents"]:
        if 'GENERAL_AVAILABILITY' in version_data:
            version = version_data["version"]
            date = version_data["GENERAL_AVAILABILITY"].split("T")[0]
            versions[version] = date
            print(f"{version}: {date}")

    return versions


for product_name, product_code in PRODUCTS.items():
    print(f"::group::{product_name}")
    all_versions = fetch_releases(product_code)
    endoflife.write_releases(product_name, all_versions)
    print("::endgroup::")
