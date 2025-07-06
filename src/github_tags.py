from common import dates, github
from common.releasedata import ProductData, config_from_argv

"""Fetches versions from GitHub tags using the GraphQL API and the GitHub CLI.

Note: GraphQL API and GitHub CLI are used because it's simpler: no need to manage pagination and authentication.
"""

config = config_from_argv()
with ProductData(config.product) as product_data:
    for tag in github.fetch_tags(config.url):
        version_str = tag.name
        version_match = config.first_match(version_str)
        if version_match:
            version = config.render(version_match)
            date = dates.parse_datetime(tag.commit_date)
            product_data.declare_version(version, date)
