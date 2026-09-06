import logging
import re

from bs4 import BeautifulSoup
from bs4.element import Tag
from liquid import Template

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetch versions and release dates from an XML document.
"""

DEFAULT_VALUE_REGEX = r"^(?P<value>.+)$"
DEFAULT_VALUE_TEMPLATE = "{{value}}"


class BeautifulSoupValueExtractor:
    def __init__(self, field: str, configuration: dict | str) -> None:
        self.field = field
        if isinstance(configuration, str):
            configuration = {"selector": configuration}

        self.selector = configuration["selector"]

        regexes_exclude = configuration.get("regex_exclude", [])
        regexes_exclude = regexes_exclude if isinstance(regexes_exclude, list) else [regexes_exclude]
        self.exclude_patterns = [re.compile(regex) for regex in regexes_exclude]

        regexes = configuration.get("regex", DEFAULT_VALUE_REGEX)
        regexes = regexes if isinstance(regexes, list) else [regexes]
        self.patterns = [re.compile(regex) for regex in regexes]
        self.template = Template(configuration.get("template", DEFAULT_VALUE_TEMPLATE))

    def extract(self, entry: Tag) -> str | None:
        selected = entry.select_one(self.selector)
        if selected is None:
            logging.debug("Skipping entry: no %s element found with selector '%s'", self.field, self.selector)
            return None

        value = selected.get_text(strip=True)
        for pattern in self.exclude_patterns:
            if pattern.match(value):
                logging.debug("Skipping entry: %s element value, '%s', matches exclude regex '%s'", self.field,
                              value, pattern.pattern)
                return None

        for pattern in self.patterns:
            match = pattern.match(value)
            if match:
                return self.template.render(**match.groupdict())

        logging.debug("Skipping entry: %s element value, '%s', does not match any regex in %s", self.field, value,
                      self.patterns)
        return None


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        response = http.fetch_url(config.url)
        document = BeautifulSoup(response.text, features="xml")
        entries = document.select(config.data["selector"])
        version_extractor = BeautifulSoupValueExtractor("name", config.data["name"])
        date_extractor = BeautifulSoupValueExtractor("date", config.data["date"])

        for entry in entries:
            version = version_extractor.extract(entry)
            date_str = date_extractor.extract(entry)
            if version is None or date_str is None:
                continue

            logging.debug("Processing version: %s with date %s", version, date_str)
            product_data.declare_version(version, dates.parse__datetime_or_date_or_month_year_date(date_str))
