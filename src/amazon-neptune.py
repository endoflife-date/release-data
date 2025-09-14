import re

from common import dates, http
from common.releasedata import ProductData, config_from_argv

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

config = config_from_argv()
with ProductData(config.product) as product_data:
    json = http.fetch_json(config.url)
    parse(json, product_data)
