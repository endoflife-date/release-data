import sys

from common import dates, endoflife, releasedata
from common.git import Git

"""Fetches versions from tags in a git repository. This replace the old update.rb script."""

METHOD = 'git'

p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product in endoflife.list_products(METHOD, p_filter):
    with releasedata.ProductData(product.name) as product_data:
        for config in product.get_auto_configs(METHOD):
            git = Git(config.url)
            git.setup(bare=True)

            tags = git.list_tags()
            for tag, date_str in tags:
                version_match = config.first_match(tag)
                if version_match:
                    version = config.render(version_match)
                    date = dates.parse_date(date_str)
                    product_data.declare_version(version, date)
