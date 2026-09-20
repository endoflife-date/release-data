import logging
import re
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from liquid import Template

from src.common import dates

DEFAULT_VALUE_REGEX = r"^(?P<value>.+)$"
DEFAULT_VERSION_REGEX = r"^v?(?P<value>[1-9]\d*(\.\d+){0,3})$"
DEFAULT_TEMPLATE = "{{value}}"

DEFAULT_TYPES = {
    "name": "string",
    "date": "datetime",
    "releaseDate": "datetime",
    "lts": "boolean",
    "eoas": "datetime",
    "eol": "datetime",
    "eoes": "datetime",
    "latestReleaseDate": "datetime",
}

DEFAULT_REGEXES = {
    "name": DEFAULT_VERSION_REGEX,
    "date": DEFAULT_VALUE_REGEX,
}

Entry = TypeVar("Entry")


class ValueExtractor(Generic[Entry], ABC):
    def __init__(self, field: str, configuration: dict | str) -> None:
        if isinstance(configuration, str):
            configuration = {"selector": configuration}

        self.field = field
        self.selector = configuration["selector"]

        self.type = configuration.get("type", DEFAULT_TYPES.get(self.field, "string"))
        match self.type:
            case "datetime":
                self.type_resolver = dates.parse__datetime_or_date_or_month_year_date
            case "string":
                self.type_resolver = lambda value: value
            case "boolean":
                self.type_resolver = lambda value: {"true": True, "false": False}.get(value.lower())
            case _:
                message = f"unsupported type: {self.type}"
                raise ValueError(message)

        regexes = configuration.get("regex", DEFAULT_REGEXES.get(self.field, DEFAULT_VALUE_REGEX))
        regexes = regexes if isinstance(regexes, list) else [regexes]
        self.patterns = [re.compile(regex) for regex in regexes]

        regexes_exclude = configuration.get("regex_exclude", [])
        regexes_exclude = regexes_exclude if isinstance(regexes_exclude, list) else [regexes_exclude]
        self.exclude_patterns = [re.compile(regex) for regex in regexes_exclude]

        self.template = Template(configuration.get("template", DEFAULT_TEMPLATE))

    @abstractmethod
    def extract_raw_value(self, entry: Entry) -> str | None:
        pass

    def extract(self, entry: Entry) -> object | None:
        raw_value = self.extract_raw_value(entry)
        if raw_value is None:
            logging.debug("Skipping entry: no %s value found with selector '%s'",
                          self.field, self.selector)
            return None

        for pattern in self.exclude_patterns:
            if pattern.match(raw_value):
                logging.debug("Skipping entry: %s value, '%s', matches exclude regex '%s'",
                              self.field, raw_value, pattern.pattern)
                return None

        for pattern in self.patterns:
            match = pattern.match(raw_value)
            if match:
                logging.debug("%s value, '%s', matches regex '%s'",
                              self.field, raw_value, pattern.pattern)
                rendered = self.template.render(**match.groupdict())
                return self.type_resolver(rendered)

        logging.debug("Skipping entry: %s value, '%s', does not match any regex in %s",
                      self.field, raw_value, self.patterns)
        return None
