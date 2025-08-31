from common import dates, endoflife, http
from common.releasedata import ProductData, config_from_argv

"""Fetches releases from the Docker Hub API.

Unfortunately images creation date cannot be retrieved, so we had to use the tag_last_pushed field instead."""

def fetch_releases(p: ProductData, c: endoflife.AutoConfig, url: str) -> None:
    data = http.fetch_json(url)

    for result in data["results"]:
        version_str = c.first_match(result["name"])
        if version_str:
            version = c.render(version_str)
            date = dates.parse_datetime(result["tag_last_pushed"])
            p.declare_version(version, date)

    if data["next"]:
        fetch_releases(p, c, data["next"])


config = config_from_argv()
with ProductData(config.product) as product_data:
    fetch_releases(product_data, config, f"https://hub.docker.com/v2/repositories/{config.url}/tags?page_size=100&page=1")
