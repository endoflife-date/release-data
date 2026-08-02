from src.common import dates, github
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetches versions from GitHub releases using the GraphQL API and the GitHub CLI.

Note: GraphQL API and GitHub CLI are used because it's simpler: no need to manage pagination and authentication.
"""

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        for release in github.fetch_releases(config.url):
            if release.is_prerelease:
                continue

            version_str = release.tag_name
            if (version_match := config.first_match(version_str)):
                version = config.render(version_match)
                date = dates.parse_datetime(release.published_at)
                product_data.declare_version(version, date)
