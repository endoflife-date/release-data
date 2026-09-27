import logging

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetches EOL dates from Atlassian EOL page.

This script takes a selector argument which is the product title identifier on the Atlassian EOL page, such as
`AtlassianSupportEndofLifePolicy-JiraSoftware`.
"""

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        html = http.fetch_html_js(config.url, wait_until='networkidle')

        heading = html.select_one(f"#{config.data.get('selector')}")
        if not heading:
            message = f"{config} found no section with id '{config.data.get('selector')}'"
            raise ValueError(message)

        version_list = heading.find_next('ul')
        if not version_list:
            message = f"{config} found no version list under '{config.data.get('selector')}'"
            raise ValueError(message)

        for li in version_list.select('li'):
            if not (match := config.first_match(li.get_text(strip=True))):
                logging.warning(f"Skipping '{li.get_text(strip=True)}', no match found")
                continue

            release_name = match.group("release")
            date = dates.parse_date(match.group("date"))
            release = product_data.get_release(release_name)
            release.set_eol(date)
