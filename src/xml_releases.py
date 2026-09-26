import logging

from bs4.element import Tag

from src.common import http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.parsing import ValueExtractor
from src.common.releasedata import ProductData

"""Fetch release-level data from an XML document.
"""


class _Extractor(ValueExtractor[Tag]):
    def extract_raw_value(self, entry: Tag) -> str | None:
        selected = entry if self.selector == ":scope" else entry.select_one(self.selector)
        return selected.get_text(strip=True) if selected else None


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        document = http.fetch_html(config.url, features=config.data.get("features", "xml"))
        entries = document.select(config.data["selector"])

        extractors = {
            name: _Extractor(name, definition)
            for name, definition in config.data["fields"].items()
        }

        if "releaseCycle" not in extractors:
            message = "fields must define releaseCycle"
            raise ValueError(message)

        release_cycle_extractor = extractors.pop("releaseCycle")
        for entry in entries:
            release_name = release_cycle_extractor.extract(entry)
            if release_name is None:
                continue

            release = product_data.get_release(str(release_name))
            for name, extractor in extractors.items():
                try:
                    value = extractor.extract(entry)
                    if value is None:
                        continue
                except ValueError as error:
                    logging.debug("skipping field %s for %s: %s", name, release, error)
                    continue

                release.set_field(name, value)
