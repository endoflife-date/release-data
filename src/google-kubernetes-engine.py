import logging

from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches versions from Google Kubernetes Engine release notes.

This script does not work for versions prior to March 29, 2021, as the release note format was different before that date.
"""

config = config_from_argv()
with ProductData(config.product) as product_data:
    html = http.fetch_html(config.url)
    regex = config.data.get('regex')

    for section in html.find_all('section', class_='releases'):
        for h2 in section.find_all('h2'):  # h2 contains the date
            date = dates.parse_date(h2.get('data-text'))

            for li in h2.find_next('div').find_all('li'):
                if "versions are now available" not in li.text:
                    logging.debug(f"Skipping {li.text}: does not contain new versions")
                    continue

                for sub_li in li.find_all('li', recursive=True):
                    match = config.first_match(sub_li.text.strip())
                    if match:
                        product_data.declare_version(config.render(match), date)
