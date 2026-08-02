import logging

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetches versions from Google Kubernetes Engine release notes.

This script does not work for versions prior to March 29, 2021, as the release note format was different before that date.
"""

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        html = http.fetch_html(config.url)

        for section in html.find_all('section', class_='releases'):
            for h2 in section.find_all('h2'):  # h2 contains the date
                date = dates.parse_date(h2.get('data-text'))

                for li in h2.find_next('div').find_all('li'):
                    if "versions are now available" not in li.text:
                        logging.debug(f"Skipping {li.text}: does not contain new versions")
                        continue

                    for sub_li in li.find_all('li', recursive=True):
                        if (match := config.first_match(sub_li.text.strip())):
                            product_data.declare_version(config.render(match), date)
