from common import dates, github
from common.releasedata import ProductData, config_from_argv

"""Fetches versions from GitHub releases using the GraphQL API and the GitHub CLI.

Note: GraphQL API and GitHub CLI are used because it's simpler: no need to manage pagination and authentication.
"""

config = config_from_argv()
with ProductData(config.product) as product_data:
    for release in github.fetch_releases(config.url):
        if release.is_prerelease:
            continue

        version_str = release.tag_name
        version_match = config.first_match(version_str)
        if version_match:
            version = config.render(version_match)
            date = dates.parse_datetime(release.published_at)
            product_data.declare_version(version, date)
