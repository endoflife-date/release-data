from common import dates, http
from common.git import Git
from common.releasedata import ProductData, config_from_argv

"""Fetch released versions from docs.chef.io and retrieve their date from GitHub.
docs.chef.io needs to be scraped because not all tagged versions are actually released.

More context on https://github.com/endoflife-date/endoflife.date/pull/4425#discussion_r1447932411.
"""

config = config_from_argv()
with ProductData(config.product) as product_data:
    html = http.fetch_html(config.url)
    released_versions = [h2.get('id') for h2 in html.find_all('h2', id=True) if h2.get('id')]

    git = Git(config.data.get('repository'))
    git.setup(bare=True)

    versions = git.list_tags()
    for version, date_str in versions:
        if version in released_versions:
            date = dates.parse_date(date_str)
            product_data.declare_version(version, date)
