import logging

from jsonpath_ng.ext import parse

from src.common import http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.parsing import ValueExtractor
from src.common.releasedata import ProductData

"""Fetch release-level data from a JSON document.
"""

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
