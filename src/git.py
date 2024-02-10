import sys

from common import dates, endoflife, releasedata
from common.git import Git

"""Fetches versions from tags in a git repository. This replace the old update.rb script."""

METHOD = 'git'

p_filter = sys.argv[1] if len(sys.argv) > 1 else None
m_filter = sys.argv[2] if len(sys.argv) > 2 else None
for config in endoflife.list_configs(p_filter, METHOD, m_filter):
    with releasedata.ProductData(config.product) as product_data:
        git = Git(config.url)
        git.setup(bare=True)

        tags = git.list_tags()
        for tag, date_str in tags:
            version_match = config.first_match(tag)
            if version_match:
                version = config.render(version_match)
                date = dates.parse_date(date_str)
                product_data.declare_version(version, date)
