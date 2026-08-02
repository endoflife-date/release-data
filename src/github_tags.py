from src.common import dates, github
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetches versions from GitHub tags using the GraphQL API and the GitHub CLI.

Note: GraphQL API and GitHub CLI are used because it's simpler: no need to manage pagination and authentication.
"""

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        for tag in github.fetch_tags(config.url):
            version_str = tag.name
            if (version_match := config.first_match(version_str)):
                version = config.render(version_match)
                date = dates.parse_datetime(tag.commit_date)
                product_data.declare_version(version, date)
