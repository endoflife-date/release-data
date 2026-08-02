import logging

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.git import Git
from src.common.releasedata import ProductData

"""Fetch released versions from docs.chef.io and retrieve their date from GitHub.
docs.chef.io needs to be scraped because not all tagged versions are actually released.

More context on https://github.com/endoflife-date/endoflife.date/pull/4425#discussion_r1447932411.
"""

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        html = http.fetch_html(config.url)

        released_versions = []
        for h2 in html.find_all('h2'):
            title = h2.get_text(strip=True)
            match = config.first_match(title)
            if not match:
                logging.warning(f"Skipping '{title}', no match found")
                continue
            released_versions.append(config.render(match))

        git = Git(config.data.get('repository'))
        git.setup(bare=True)
        versions = git.list_tags()
        for version, date_str in versions:
            version = version.removeprefix("v")  # Remove 'v' prefix if present
            if version in released_versions:
                date = dates.parse_date(date_str)
                product_data.declare_version(version, date)
