import logging

from src.common import http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.parsing import ValueExtractor
from src.common.releasedata import ProductData

"""Fetch versions and release dates from a JSON document.

The ``selector``, ``name`` and ``date`` configuration values use dot-separated
paths. List indexes can be used as path components, for example
``releases.0.version``. The name and date values also support ``regex``,
``regex_exclude`` and ``template`` options, matching ``xml_versions.py``.
"""

def select(data: object, path: str) -> object | None:
    """Return the value at a dot-separated path in a JSON value."""
    if not path:
        return data

    value = data
    for component in path.split("."):
        if isinstance(value, dict):
            if component not in value:
                return None
            value = value[component]
        elif isinstance(value, list) and component.isdigit():
            index = int(component)
            if index >= len(value):
                return None
            value = value[index]
        else:
            return None

    return value


class _Extractor(ValueExtractor[object]):
    def extract_raw_value(self, entry: object) -> str | None:
        selected = select(entry, self.selector)
        return str(selected) if selected else None


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        document = http.fetch_json(config.url)
        entries = select(document, config.data["selector"])
        if not isinstance(entries, list):
            entries = [entries]

        version_extractor = _Extractor("name", config.data["name"])
        date_extractor = _Extractor("date", config.data["date"])

        for entry in entries:
            version = version_extractor.extract(entry)
            date = date_extractor.extract(entry)
            if version is None or date is None:
                continue

            logging.debug("Processing version: %s with date %s", version, date)
            product_data.declare_version(version, date)
