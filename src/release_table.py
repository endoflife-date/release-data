import logging
import re
import sys
from datetime import datetime

from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata
from liquid import Template

"""Fetch release-level data from an HTML table in a web page.

This script works based on a definition provided in the product's frontmatter to locate the table and extract the
necessary information. Available configuration options are:

- selector (mandatory, no default): A CSS selector used to locate one or more tables in the page.
- header_selector (mandatory, default = thead tr): A CSS selector used to locate the table's header row.
- rows_selector (mandatory, default = tbody tr): A CSS selector used to locate the table's rows.
- fields: A dictionary that maps release fields to the table's columns. Field definition include:
    - column (mandatory): The name of the column in the table. This is case-insensitive.
    - type (mandatory, default = string): The type of the field. Supported types are listed in SUPPORTED_TYPES. If the
      field is one of the known date fields (DATE_FIELDS), the type is automatically set to 'date' if not provided.
    - regex (mandatory, default = [DEFAULT_REGEX]): A regular expression, or a list of regular expressions, used to
      validate allowed values. Note that default value for the releaseCycle field is not DEFAULT_REGEX, but
      DEFAULT_RELEASE_REGEX.
    - regex_exclude (mandatory, default = []): A regular expression, or a list of regular expressions, used to exclude
      values even if they match any regular expression in 'regex'.
    - template (mandatory, default = DEFAULT_TEMPLATE): A liquid template used to clean up the value using the matched
      groups from a 'regex'.

Supported CSS selectors are defined by BeautifulSoup and documented on its website. For more information, see
https://beautiful-soup-4.readthedocs.io/en/latest/index.html?highlight=selector#css-selectors."""

METHOD = "release_table"
SUPPORTED_TYPES = ["date", "string"]
DATE_TYPES = ["date"]
DATE_FIELDS = ["releaseDate", "lts", "support", "eol", "extendedSupport"]
DEFAULT_REGEX = r"^(?P<value>.+)$"
DEFAULT_TEMPLATE = "{{value}}"
DEFAULT_RELEASE_REGEX = r"^v?(?P<value>\d+(\.\d+)*)$"


class Field:
    def __init__(self, name: str, definition: str | dict) -> None:
        if isinstance(definition, str):
            definition = {"column": definition}

        self.name = name
        if self.name == "releaseCycle":
            definition["type"] = "string"
            definition["regex"] = definition.get("regex", [DEFAULT_RELEASE_REGEX])
            definition["template"] = definition.get("template", DEFAULT_TEMPLATE)

        self.column = definition["column"].lower()
        self.type = definition.get("type", "string")
        if self.name in DATE_FIELDS and self.type not in DATE_TYPES:
            self.type = "date"  # override type for known date fields
        elif self.type not in SUPPORTED_TYPES:
            msg = f"unsupported type: {self.type} for field {self.name}"
            raise ValueError(msg)

        regex = definition.get("regex", [DEFAULT_REGEX])
        regex = regex if isinstance(regex, list) else [regex]
        self.include_version_patterns = [re.compile(r, re.MULTILINE) for r in regex]

        exclude_regex = definition.get("regex_exclude", [])
        exclude_regex = exclude_regex if isinstance(exclude_regex, list) else [exclude_regex]
        self.exclude_version_patterns = [re.compile(r, re.MULTILINE) for r in exclude_regex]

        self.template = Template(definition.get("template", DEFAULT_TEMPLATE)) \
            if "template" in definition or regex else None

    def extract_from(self, raw_value: str) -> str | datetime | None:
        for exclude_pattern in self.exclude_version_patterns:
            if exclude_pattern.match(raw_value):
                return None

        for include_pattern in self.include_version_patterns:
            match = include_pattern.match(raw_value)
            if not match:
                continue

            str_value = self.template.render(**match.groupdict()) if self.template else raw_value
            if self.type == "date":
                try:
                    return dates.parse_date(str_value)
                except ValueError:
                    return dates.parse_month_year_date(str_value)
            return str_value

        if self.name == "releaseCycle":
            return None  # skipping entire rows is allowed

        msg = f"field {self}'s value '{raw_value}' does not match any regex in {self.include_version_patterns}"
        raise ValueError(msg)

    def __repr__(self) -> str:
        return f"{self.name}({self.column})"


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
m_filter = sys.argv[2] if len(sys.argv) > 2 else None
for config in endoflife.list_configs(p_filter, METHOD, m_filter):
    with releasedata.ProductData(config.product) as product_data:
        response = http.fetch_url(config.url)
        soup = BeautifulSoup(response.text, features="html5lib")

        release_cycle_field = Field("releaseCycle", config.data["fields"].pop("releaseCycle"))
        fields = [Field(name, definition) for name, definition in config.data["fields"].items()]
        for table in soup.select(config.data["selector"]):
            header_row = table.select_one(config.data.get("header_selector", "thead tr"))
            if not header_row:
                logging.info(f"skipping table with attributes {table.attrs}: no header row found")
                continue

            headers = [th.get_text().strip().lower() for th in header_row.select("td, th")]

            try:
                fields_index = {"releaseCycle": headers.index(release_cycle_field.column)}
                for field in fields:
                    fields_index[field.name] = headers.index(field.column)
                min_column_count = max(fields_index.values()) + 1

                for row in table.select(config.data.get("rows_selector", "tbody tr")):
                    cells = [cell.get_text().strip() for cell in row.select("td, th")]
                    if len(cells) < min_column_count:
                        logging.info(f"skipping row {cells}: not enough columns")
                        continue

                    raw_release_name = cells[fields_index[release_cycle_field.name]]
                    release_name = release_cycle_field.extract_from(raw_release_name)
                    if not release_name:
                        logging.info(f"skipping row {cells}: invalid release cycle '{raw_release_name}', "
                                     f"should match one of {release_cycle_field.include_version_patterns} "
                                     f"and not match all of {release_cycle_field.exclude_version_patterns}")
                        continue

                    release = product_data.get_release(release_name)
                    for field in fields:
                        raw_field = cells[fields_index[field.name]]
                        try:
                            release.set_field(field.name, field.extract_from(raw_field))
                        except ValueError as e:
                            logging.info(f"skipping cell {raw_field} for {release}: {e}")

                    if config.data.get("ignore_empty_releases", False) and release.is_empty():
                        logging.info(f"removing empty release '{release}'")
                        product_data.remove_release(release_name)

            except ValueError as e:
                logging.info(f"skipping table with headers {headers}: {e}")
