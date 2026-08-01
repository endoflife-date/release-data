import re

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetches Amazon Neptune versions from its RSS feed on docs.aws.amazon.com."""

REGEX = r"(Maintenance r|R)elease:? (?P<version>.+) \((?P<date>\d+-\d+-\d+)\)"

def parse(data: dict, product: ProductData) -> None:
    if "title" in data:
        title = data["title"]
        print(title)
        match = re.search(REGEX, title)
        if match:
            name = match.group("version")
            date = dates.parse_date(match.group("date"))
            product.declare_version(name, date)

    for item in data.get("contents", []):
        parse(item, product)

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        json = http.fetch_json(config.url)
        parse(json, product_data)
