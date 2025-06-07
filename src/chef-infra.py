from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata
from common.git import Git

"""Fetch released versions from docs.chef.io and retrieve their date from GitHub.
docs.chef.io needs to be scraped because not all tagged versions are actually released.

More context on https://github.com/endoflife-date/endoflife.date/pull/4425#discussion_r1447932411.
"""

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        rn_response = http.fetch_url(config.url)
        rn_soup = BeautifulSoup(rn_response.text, features="html5lib")
        released_versions = [h2.get('id') for h2 in rn_soup.find_all('h2', id=True) if h2.get('id')]

        git = Git(config.data.get('repository'))
        git.setup(bare=True)

        versions = git.list_tags()
        for version, date_str in versions:
            if version in released_versions:
                date = dates.parse_date(date_str)
                product_data.declare_version(version, date)
