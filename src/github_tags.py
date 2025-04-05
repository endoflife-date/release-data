import sys

from common import dates, endoflife, github, releasedata

"""Fetches versions from GitHub tags using the GraphQL API and the GitHub CLI.

Note: GraphQL API and GitHub CLI are used because it's simpler: no need to manage pagination and authentication.
"""

METHOD = "github_tags"


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
m_filter = sys.argv[2] if len(sys.argv) > 2 else None
for config in endoflife.list_configs(p_filter, METHOD, m_filter):
    with releasedata.ProductData(config.product) as product_data:
        for tag in github.fetch_tags(config.url):
            version_str = tag.name
            version_match = config.first_match(version_str)
            if version_match:
                version = config.render(version_match)
                date = dates.parse_datetime(tag.commit_date)
                product_data.declare_version(version, date)
