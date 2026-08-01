from bs4 import BeautifulSoup

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetches versions from Atlassian download-archives pages.

This script takes a single argument which is the url of the product's download-archives URL, such as
`https://www.atlassian.com/software/confluence/download-archives`.
"""

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        content = http.fetch_javascript_url(config.url, wait_until='networkidle')
        soup = BeautifulSoup(content, features='html5lib')

        for version_block in soup.select('.versions-list'):
            version = version_block.select_one('a.product-versions')['data-version']
            date = dates.parse_date(version_block.select_one('.release-date').text)
            product_data.declare_version(version, date)
