from bs4 import BeautifulSoup
from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches Artifactory versions from https://jfrog.com, using requests_html because JavaScript is
needed to render the page."""

config = config_from_argv()
with ProductData(config.product) as product_data:
    content = http.fetch_javascript_url(config.url, wait_until = 'networkidle')
    soup = BeautifulSoup(content, 'html.parser')

    for row in soup.select('.informaltable tbody tr'):
        cells = row.select("td")
        if len(cells) >= 2:
            version = cells[0].text.strip()
            if version:
                date_str = cells[1].text.strip().replace("_", "-").replace("Sept-", "Sep-")
                product_data.declare_version(version, dates.parse_date(date_str))
