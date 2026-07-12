from collections.abc import Iterator
from urllib.parse import quote

from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches versions from GitLab tags using the REST API.
"""

GITLAB_API_URL = "https://gitlab.com/api/v4/projects"
PER_PAGE = 100


def fetch_tags(project_path: str) -> Iterator[dict]:
    project_path = quote(project_path, safe='')
    page = 1
    while True:
        url = f"{GITLAB_API_URL}/{project_path}/repository/tags?per_page={PER_PAGE}&page={page}"
        tags = http.fetch_json(url)
        if not tags:
            break
        yield from tags
        page += 1


config = config_from_argv()
with ProductData(config.product) as product_data:
    for tag in fetch_tags(config.url):
        version_str = tag['name']
        version_match = config.first_match(version_str)
        if version_match:
            version = config.render(version_match)
            date = dates.parse_datetime(tag['commit']['created_at'])
            product_data.declare_version(version, date)
