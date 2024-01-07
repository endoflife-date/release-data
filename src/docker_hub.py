import sys

from common import dates, endoflife, http, releasedata

"""Fetches releases from the Docker Hub API.

Unfortunately images creation date cannot be retrieved, so we had to use the tag_last_pushed field instead."""

METHOD = "docker_hub"


def fetch_releases(p: releasedata.Product, c: endoflife.AutoConfig, url: str) -> None:
    data = http.fetch_url(url).json()

    for result in data["results"]:
        version_str = result["name"]
        if c.first_match(version_str):
            date = dates.parse_datetime(result["tag_last_pushed"])
            p.declare_version(version_str, date)

    if data["next"]:
        fetch_releases(p, c, data["next"])


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product_name in endoflife.list_products(METHOD, p_filter):
    product = releasedata.Product(product_name)
    product_frontmatter = endoflife.ProductFrontmatter(product.name)
    for config in product_frontmatter.get_auto_configs(METHOD):
        fetch_releases(product, config, f"https://hub.docker.com/v2/repositories/{config.url}/tags?page_size=100&page=1")
    product.write()
