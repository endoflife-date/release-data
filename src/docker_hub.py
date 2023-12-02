import re
import sys
from common import http
from common import endoflife

METHOD = "docker_hub"


def fetch_releases(url, regex, releases):
    if not isinstance(regex, list):
        regex = [regex]

    response = http.fetch_url(url)
    data = response.json()
    for result in data["results"]:
        version = result["name"]

        matches = False
        for r in regex:
            if re.match(r, version):
                matches = True

        if matches:
            date = result['tag_last_pushed'].split("T")[0]
            releases[version] = date
            print(f"{version}: {date}")

    if data["next"]:
        fetch_releases(data["next"], regex, releases)


def update_product(product_name, configs):
    versions = {}

    for config in configs:
        url = f"https://hub.docker.com/v2/repositories/{config[METHOD]}/tags?page_size=100&page=1"
        config = {"regex": endoflife.DEFAULT_VERSION_REGEX} | config
        fetch_releases(url, config["regex"], versions)

    endoflife.write_releases(product_name, versions)


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product, configs in endoflife.list_products(METHOD, p_filter).items():
    print(f"::group::{product}")
    update_product(product, configs)
    print("::endgroup::")
