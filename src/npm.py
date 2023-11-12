import json
import re
import sys
from common import endoflife

METHOD = "npm"
REGEX = r"^(?:(\d+\.(?:\d+\.)*\d+))$"


def fetch_releases(npm_id, regex):
    releases = {}

    if not isinstance(regex, list):
        regex = [regex]

    url = f"https://registry.npmjs.org/{npm_id}"
    response = endoflife.fetch_url(url)
    data = json.loads(response)
    for version in data["time"]:
        matches = False
        for r in regex:
            if re.match(r, version):
                matches = True

        release_datetime = data["time"][version]
        if matches and release_datetime:
            releases[version] = release_datetime.split("T")[0]
            print(f"{version}: {releases[version]}")

    return releases


def update_product(product_name, configs):
    versions = {}

    for config in configs:
        config = {"regex": REGEX} | config
        versions = versions | fetch_releases(config[METHOD], config["regex"])

    endoflife.write_releases(product_name, versions)


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product, configs in endoflife.list_products(METHOD, p_filter).items():
    print(f"::group::{product}")
    update_product(product, configs)
    print("::endgroup::")
