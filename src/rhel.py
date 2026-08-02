import re

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

# https://regex101.com/r/877ibq/1
VERSION_PATTERN = re.compile(r"RHEL (?P<major>\d)(\. ?(?P<minor>\d+))?(( Update (?P<minor2>\d))| GA)?")

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        html = http.fetch_html(config.url)

        for tr in html.findAll("tr"):
            td_list = tr.findAll("td")
            if len(td_list) == 0:
                continue

            version_str = td_list[0].get_text().strip()
            version_match = VERSION_PATTERN.match(version_str).groupdict()
            version = ".".join(v for v in version_match.values() if v)
            date = dates.parse_date(td_list[1].get_text())
            product_data.declare_version(version, date)
