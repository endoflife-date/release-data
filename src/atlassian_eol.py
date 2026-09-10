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

        # Find the section with the EOL dates. The list is not always the heading's immediate
        # sibling: the Jira Service Management section puts a paragraph in between, which an
        # adjacent sibling selector would step over.
        heading = soup.find(id=config.data.get('selector'))
        if not heading:
            message = f"{config} found no section with id '{config.data.get('selector')}'"
            raise ValueError(message)

        version_list = heading.find_next('ul')
        if not version_list:
            message = f"{config} found no version list under '{config.data.get('selector')}'"
            raise ValueError(message)

        for li in version_list.find_all('li'):
            if not (match := config.first_match(li.get_text(strip=True))):
                logging.warning(f"Skipping '{li.get_text(strip=True)}', no match found")
                continue

            release_name = match.group("release")
            date = dates.parse_date(match.group("date"))
            release = product_data.get_release(release_name)
            release.set_eol(date)
