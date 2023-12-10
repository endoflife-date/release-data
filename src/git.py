import sys
from common import dates
from common import endoflife
from common.git import Git

"""Fetches versions from tags in a git repository. This replace the old update.rb script."""

METHOD = 'git'

p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product_name, configs in endoflife.list_products(METHOD, p_filter).items():
    print(f"::group::{product_name}")
    product = endoflife.Product(product_name, load_product_data=True)
    for config in product.get_auto_configs(METHOD):
        git = Git(config.url)
        git.setup(bare=True)

        tags = git.list_tags()
        for tag, date_str in tags:
            version_match = config.first_match(tag)
            if version_match:
                version = config.render(version_match)
                date = dates.parse_date(date_str)
                product.declare_version(version, date)

    product.write()
    print("::endgroup::")
