from bs4 import BeautifulSoup
from common import dates, http, releasedata

"""Fetches Artifactory versions from https://jfrog.com, using requests_html because JavaScript is
needed to render the page."""

for config in releasedata.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        content = http.fetch_javascript_url(config.url, wait_until = 'networkidle')
        soup = BeautifulSoup(content, 'html.parser')

        for row in soup.select('.informaltable tbody tr'):
            cells = row.select("td")
            if len(cells) >= 2:
                version = cells[0].text.strip()
                if version:
                    date_str = cells[1].text.strip().replace("_", "-").replace("Sept-", "Sep-")
                    product_data.declare_version(version, dates.parse_date(date_str))

        # 7.29.9 release date is wrong on https://jfrog.com/help/r/jfrog-release-information/artifactory-end-of-life.
        # Sent a mail to jfrog-help-center-feedback@jfrog.com to fix it, but in the meantime...
        product_data.declare_version('7.29.9', dates.date(2022, 1, 11))
