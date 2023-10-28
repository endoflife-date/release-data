import json
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
    releases = {}
    url = BASE_URL + product_code
    print(url)
    response = endoflife.fetch_url(url)
    data = json.loads(response)

    for version_data in data["contents"]:
        if 'GENERAL_AVAILABILITY' in version_data:
            version = version_data["version"]
            date = version_data["GENERAL_AVAILABILITY"].split("T")[0]
            releases[version] = date
            print(f"{version}: {date}")

    return releases


for product_name, product_code in PRODUCTS.items():
    print(f"::group::{product_name}")
    all_releases = fetch_releases(product_code)
    endoflife.write_releases(product_name, dict(
        # sort by date then version (desc)
        sorted(all_releases.items(), key=lambda x: (x[1], x[0]), reverse=True)
    ))
    print("::endgroup::")
