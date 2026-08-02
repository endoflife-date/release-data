import logging

from bs4 import BeautifulSoup

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetches EOL dates from Atlassian EOL page.

This script takes a selector argument which is the product title identifier on the Atlassian EOL page, such as
`AtlassianSupportEndofLifePolicy-JiraSoftware`.
"""

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        content = http.fetch_javascript_url(config.url, wait_until='networkidle')
        soup = BeautifulSoup(content, features="html5lib")

        # Find the section with the EOL dates
        for li in soup.select(f"#{config.data.get('selector')}+ul li"):
            if not (match := config.first_match(li.get_text(strip=True))):
                logging.warning(f"Skipping '{li.get_text(strip=True)}', no match found")
                continue

            release_name = match.group("release")
            date = dates.parse_date(match.group("date"))
            release = product_data.get_release(release_name)
            release.set_eol(date)
