from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

"""Fetch Java versions from https://www.java.com/releases/.

This script is using requests-html because the page needs JavaScript to render correctly."""

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        content = http.fetch_javascript_url(config.url, wait_until='networkidle')
        soup = BeautifulSoup(content, 'html.parser')

        previous_date = None
        for row in soup.select('#released tr'):
            version_cell = row.select_one('td.anchor')
            if version_cell:
                version = version_cell.attrs['id']
                date_str = row.select('td')[1].text
                date = dates.parse_date(date_str) if date_str else previous_date
                product_data.declare_version(version, date)
                previous_date = date

        product_data.remove_version('1.0_alpha')  # the only version we don't want, a regex is not needed
