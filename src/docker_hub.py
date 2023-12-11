import sys
from common import dates
from common import endoflife
from common import http

"""Fetches releases from the Docker Hub API.

Unfortunately images creation date cannot be retrieved, so we had to use the tag_last_pushed field instead."""

METHOD = "docker_hub"


def fetch_releases(product, config, url):
    data = http.fetch_url(url).json()

    for result in data["results"]:
        version_str = result["name"]
        if config.first_match(version_str):
            date = dates.parse_datetime(result["tag_last_pushed"])
            product.declare_version(version_str, date)

    if data["next"]:
        fetch_releases(product, config, data["next"])


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product_name, configs in endoflife.list_products(METHOD, p_filter).items():
    print(f"::group::{product_name}")
    product = endoflife.Product(product_name, load_product_data=True)

    for config in product.get_auto_configs(METHOD):
        url = f"https://hub.docker.com/v2/repositories/{config.url}/tags?page_size=100&page=1"
        fetch_releases(product, config, url)

    product.write()
    print("::endgroup::")
