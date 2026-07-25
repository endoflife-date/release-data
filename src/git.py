from src.common import dates
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.git import Git
from src.common.releasedata import ProductData

"""Fetches versions from tags in a git repository. This replace the old update.rb script."""

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        git = Git(config.url)
        git.setup(bare=True)

        tags = git.list_tags()
        for tag, date_str in tags:
            version_match = config.first_match(tag)
            if version_match:
                version = config.render(version_match)
                date = dates.parse_date(date_str)
                product_data.declare_version(version, date)
