import logging

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        html = http.fetch_html(config.url)

        ul = html.find("h2").find_next("ul")
        for li in ul.find_all("li"):
            text = li.get_text(strip=True)
            if not (match := config.first_match(text)):
                logging.info(f"Skipping {text}, does not match any regex")
                continue

            version = match.group("version")
            date = dates.parse_date(match.group("date"))
            product_data.declare_version(version, date)
