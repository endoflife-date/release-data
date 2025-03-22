from bs4 import BeautifulSoup
from common import dates, http, releasedata

"""Fetches Bitbucket versions from www.atlassian.com.

Note that requests_html is used because JavaScript is needed to render the page."""

with releasedata.ProductData("bitbucket") as product_data:
    content = http.fetch_javascript_url("https://www.atlassian.com/software/bitbucket/download-archives")
    soup = BeautifulSoup(content, 'html.parser')

    for version_block in soup.select('.versions-list'):
        version = version_block.select_one('a.product-versions').attrs['data-version']
        date = dates.parse_date(version_block.select_one('.release-date').text)
        product_data.declare_version(version, date)
