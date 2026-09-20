import logging

from bs4.element import Tag

from src.common import http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.parsing import ValueExtractor
from src.common.releasedata import ProductData

"""Fetch versions and release dates from an XML document.
"""

class _Extractor(ValueExtractor[Tag]):
    def extract_raw_value(self, entry: Tag) -> str | None:
        selected = entry.select_one(self.selector)
        return selected.get_text(strip=True) if selected else None


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        document = http.fetch_html(config.url, features="xml")
        entries = document.select(config.data["selector"])
        version_extractor = _Extractor("name", config.data["name"])
        date_extractor = _Extractor("date", config.data["date"])

        for entry in entries:
            version = version_extractor.extract(entry)
            date = date_extractor.extract(entry)
            if version is None or date is None:
                continue

            logging.debug("Processing version: %s with date %s", version, date)
            product_data.declare_version(version, date)
