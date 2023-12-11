import re
import sys
from common import http
from common import endoflife

METHOD = "npm"


def fetch_releases(npm_id, regex):
    releases = {}

    if not isinstance(regex, list):
        regex = [regex]

    url = f"https://registry.npmjs.org/{npm_id}"
    response = http.fetch_url(url)
    data = response.json()
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
        config = {"regex": endoflife.DEFAULT_VERSION_REGEX} | config
        versions = versions | fetch_releases(config[METHOD], config["regex"])

    endoflife.write_releases(product_name, versions)


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product, configs in endoflife.list_products(METHOD, p_filter).items():
    print(f"::group::{product}")
    update_product(product, configs)
    print("::endgroup::")
