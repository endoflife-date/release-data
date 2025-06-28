from common import dates, releasedata
from common.git import Git

"""Fetches versions from tags in a git repository. This replace the old update.rb script."""

for config in releasedata.list_configs_from_argv():
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
