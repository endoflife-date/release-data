from bs4 import BeautifulSoup
from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches versions from Atlassian download-archives pages.

This script takes a single argument which is the url of the product's download-archives URL, such as
`https://www.atlassian.com/software/confluence/download-archives`.
"""

config = config_from_argv()
with ProductData(config.product) as product_data:
    content = http.fetch_javascript_url(config.url, wait_until='networkidle')
    soup = BeautifulSoup(content, 'html5lib')

    for version_block in soup.select('.versions-list'):
        version = version_block.select_one('a.product-versions').attrs['data-version']
        date = dates.parse_date(version_block.select_one('.release-date').text)
        product_data.declare_version(version, date)
