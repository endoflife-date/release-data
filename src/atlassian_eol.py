import logging

from bs4 import BeautifulSoup
from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches EOL dates from Atlassian EOL page.

This script takes a selector argument which is the product title identifier on the Atlassian EOL page, such as
`AtlassianSupportEndofLifePolicy-JiraSoftware`.
"""

config = config_from_argv()
with ProductData(config.product) as product_data:
    content = http.fetch_javascript_url(config.url)
    soup = BeautifulSoup(content, features="html5lib")

    # Find the section with the EOL dates
    for li in soup.select(f"#{config.data.get('selector')}+ul li"):
        match = config.first_match(li.get_text(strip=True))
        if not match:
            logging.warning(f"Skipping '{li.get_text(strip=True)}', no match found")
            continue

        release_name = match.group("release")
        date = dates.parse_date(match.group("date"))
        release = product_data.get_release(release_name)
        release.set_eol(date)
