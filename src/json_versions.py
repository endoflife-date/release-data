import logging

from jsonpath_ng import parse

from src.common import http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.parsing import ValueExtractor
from src.common.releasedata import ProductData

"""Fetch versions and release dates from a JSON document."""


def _select(data: object, path: str) -> list[object]:
    return [match.value for match in parse(path).find(data)]


class _Extractor(ValueExtractor[object]):
    def extract_raw_value(self, entry: object) -> str | None:
        matches = _select(entry, self.selector)
        return str(matches[0]) if matches else None


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        document = http.fetch_json(config.url)
        entries = _select(document, config.data["selector"])

        version_extractor = _Extractor("name", config.data["name"])
        date_extractor = _Extractor("date", config.data["date"])

        for entry in entries:
            version = version_extractor.extract(entry)
            date = date_extractor.extract(entry)
            if version is None or date is None:
                continue

            logging.debug("Processing version: %s with date %s", version, date)
            product_data.declare_version(version, date)
