import re
import sys
from datetime import datetime

from bs4 import BeautifulSoup, PageElement
from common import dates, endoflife, http, releasedata
from liquid import Template

"""Fetch release-level data from an HTML table in a web page.

This script works based on a definition provided in the product's frontmatter to locate the table and extract the
necessary information. Available configuration options are:

- regex: A regular expression used to match release based on their names (aka releaseCycle).
  Releases not matching this expression are ignored. Default value is defined in endoflife.py (DEFAULT_VERSION_REGEX).
- regex_exclude: A regular expression used to exclude matching releases based on their names  (aka releaseCycle).
  Releases matching this expression are ignored, even if they match the above regex. This is empty by default.
- template: A liquid template used to render the release name. The template is rendered using the matched groups from
  the regex. Default value is defined in endoflife.py (DEFAULT_VERSION_TEMPLATE).
- selector: A CSS selector used to locate one or more tables in the page.
- headers_selector: A CSS selector used to locate the table's headers (column names).
- rows_selector: A CSS selector used to locate the table's rows.
- mapping: A dictionary that maps release fields to the table's columns names. All identifiers are case-insensitive.

Supported CSS selectors are defined by BeautifulSoup and documented on its website. For more information, see
https://beautiful-soup-4.readthedocs.io/en/latest/index.html?highlight=selector#css-selectors.

Column data types are auto-detected. The currently supported types are 'date' (parsed using the dates module) and
string."""

METHOD = "release_table"


class Field:
    SUPPORTED_TYPES = ["date", "month_year_date", "string"]
    DATE_TYPES = ["date", "month_year_date"]
    DATE_FIELDS = ["releaseDate", "support", "eol", "extendedSupport"]
    DEFAULT_REGEX = r"^(?P<value>.+)$"
    DEFAULT_TEMPLATE = "{{value}}"
    DEFAULT_RELEASE_REGEX = r"^v?(?P<value>\d+(\.\d+)?)$"

    def __init__(self, name: str, definition: str | dict, columns: list[str]) -> None:
        if isinstance(definition, str):
            definition = {"column": definition}

        self.name = name
        if self.name == "releaseCycle":
            definition["type"] = "string"
            definition["regex"] = definition.get("regex", [self.DEFAULT_RELEASE_REGEX])
            definition["template"] = definition.get("template", self.DEFAULT_TEMPLATE)

        self.column = definition["column"].lower()
        if self.column not in columns:
            msg = f"column {self.column} not found in {columns}"
            raise ValueError(msg)
        self.column_index = columns.index(self.column)

        self.type = definition.get("type", "string")
        if self.name in self.DATE_FIELDS and self.type not in self.DATE_TYPES:
            self.type = "date"  # override type for known date fields
        elif self.type not in self.SUPPORTED_TYPES:
            msg = f"unsupported type: {self.type} for field {self.name}"
            raise ValueError(msg)

        regex = definition.get("regex", [self.DEFAULT_REGEX])
        regex = regex if isinstance(regex, list) else [regex]
        self.include_version_patterns = [re.compile(r, re.MULTILINE) for r in regex]

        exclude_regex = definition.get("regex_exclude", [])
        exclude_regex = exclude_regex if isinstance(exclude_regex, list) else [exclude_regex]
        self.exclude_version_patterns = [re.compile(r, re.MULTILINE) for r in exclude_regex]

        self.template = Template(definition.get("template", self.DEFAULT_TEMPLATE)) \
            if "template" in definition or regex else None

    def extract_from(self, cells: list[PageElement]) -> str | datetime | None:
        raw_value = cells[self.column_index].get_text(strip=True)

        for exclude_pattern in self.exclude_version_patterns:
            if exclude_pattern.match(raw_value):
                return None

        for include_pattern in self.include_version_patterns:
            match = include_pattern.match(raw_value)
            if not match:
                continue

            str_value = self.template.render(**match.groupdict()) if self.template else raw_value
            if self.type == "date":
                return dates.parse_date(str_value)
            if self.type == "month_year_date":
                return dates.parse_month_year_date(str_value)
            return str_value

        if self.name == "releaseCycle":
            return None  # skipping entire rows is allowed

        msg = f"{raw_value} is not matching any regex in {self.include_version_patterns}"
        raise ValueError(msg)


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
m_filter = sys.argv[2] if len(sys.argv) > 2 else None
for config in endoflife.list_configs(p_filter, METHOD, m_filter):
    with releasedata.ProductData(config.product) as product_data:
        response = http.fetch_url(config.url)
        soup = BeautifulSoup(response.text, features="html5lib")
        table = soup.select_one(config.data["selector"])

        if not table:
            message = f"No table found for {config.product} with selector {config.data['selector']}"
            raise ValueError(message)

        headers = [th.get_text().strip().lower() for th in table.select(config.data["headers_selector"])]
        release_cycle_field = Field("releaseCycle", config.data["fields"].pop("releaseCycle"), headers)
        fields = [Field(name, definition, headers) for name, definition in config.data["fields"].items()]
        min_column_count = max([f.column_index for f in fields] + [release_cycle_field.column_index]) + 1

        for row in table.select(config.data["rows_selector"]):
            row_cells = row.findAll("td")
            if len(row_cells) < min_column_count:
                continue

            release_cycle = release_cycle_field.extract_from(row_cells)
            if not release_cycle:
                continue

            release = product_data.get_release(release_cycle)
            for field in fields:
                release.set_field(field.name, field.extract_from(row_cells))
