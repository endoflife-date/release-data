import sys

from common import dates, endoflife, http, releasedata

"""Fetches releases from the Docker Hub API.

Unfortunately images creation date cannot be retrieved, so we had to use the tag_last_pushed field instead."""

METHOD = "docker_hub"


def fetch_releases(p: releasedata.ProductData, c: endoflife.AutoConfig, url: str) -> None:
    data = http.fetch_url(url).json()

    for result in data["results"]:
        version_str = result["name"]
        if c.first_match(version_str):
            date = dates.parse_datetime(result["tag_last_pushed"])
            p.declare_version(version_str, date)

    if data["next"]:
        fetch_releases(p, c, data["next"])


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
m_filter = sys.argv[2] if len(sys.argv) > 2 else None
for config in endoflife.list_configs(p_filter, METHOD, m_filter):
    with releasedata.ProductData(config.product) as product_data:
        fetch_releases(product_data, config, f"https://hub.docker.com/v2/repositories/{config.url}/tags?page_size=100&page=1")
