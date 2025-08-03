import logging
import re
from datetime import datetime
from re import Match

from bs4 import BeautifulSoup
from common import dates, endoflife, http
from common.releasedata import ProductData, config_from_argv
from liquid import Template

"""Fetch release-level data from an HTML table in a web page.

This script works based on a definition provided in the product's frontmatter to locate the table and extract the
necessary information. Available configuration options are:

- selector (mandatory, no default): A CSS selector used to locate one or more tables in the page.
- header_selector (mandatory, default = thead tr): A CSS selector used to locate the table's header row.
- rows_selector (mandatory, default = tbody tr): A CSS selector used to locate the table's rows.
- user_agent (optional, default = <endoflife.date-bot User-Agent>): A user agent string to use when fetching the page.
  Unused when render_javascript is true.
- render_javascript (optional, default = false): A boolean value indicating whether to render JavaScript on the page.
- render_javascript_wait_for (optional, default = None): Wait until the given selector appear on the page. Only use when
  render_javascript is true.
- render_javascript_wait_until (optional, default = None): Argument to pass to Playwright, one of "commit",
  "domcontentloaded", "load", or "networkidle". Only use when render_javascript is true and if the script fails without it.
- fields: A dictionary that maps release fields to the table's columns. Field definition include:
    - column (mandatory): The name or index (starts at 1) of the column in the table.
    - type (mandatory, default = string): The type of the field. Supported types are:
      - string: The raw string value.
      - identifier: A transformation of the raw string value so that it can be used as an identifier. The transformation
                    consists of putting the string in lower case, replacing spaces with dashes, and removing all
                    characters that are not alphanumeric, dashes, dots, plus signs, or underscores.
      - date  : A full or year-month date (supported patterns available in common.dates).
      - range : Convert a comma-separated list of values into a range, only keeping the first and last value.
                For example, "1.0, 1.1, 1.2" becomes "1.0 - 1.2".
      If the field is one of the known date fields, the type is automatically set to 'date' if not provided.
    - regex (mandatory, default = [DEFAULT_REGEX]): A regular expression, or a list of regular expressions, used to
      validate allowed values. Note that default value for the releaseCycle field is not DEFAULT_REGEX, but
      DEFAULT_RELEASE_REGEX.
    - regex_exclude (mandatory, default = []): A regular expression, or a list of regular expressions, used to exclude
      values even if they match any regular expression in 'regex'.
    - template (mandatory, default = DEFAULT_TEMPLATE): A liquid template used to clean up the value using the matched
      groups from a 'regex'.

Note that defining the column attribute directly instead of its full definition is allowed when
there the column name or index is the only attribute. For example, this:
```
fields:
  releaseCycle:
    column: "End of life"
```

can be replaced with this:
```
fields:
  releaseCycle: "End of life"
```

Supported CSS selectors are defined by BeautifulSoup and documented on its website. For more information, see
https://beautiful-soup-4.readthedocs.io/en/latest/index.html?highlight=selector#css-selectors."""

METHOD = "release_table"
SUPPORTED_TYPES = ["date", "string", "range", "identifier"]
STRING_TYPES = ["string", "identifier"]
STRING_FIELDS = ["releaseCycle", "releaseLabel"]
DATE_TYPES = ["date"]
DATE_FIELDS = ["releaseDate", "lts", "eoas", "eol", "eoes"]
DEFAULT_REGEX = r"^(?P<value>.+)$"
DEFAULT_TEMPLATE = "{{value}}"
DEFAULT_RELEASE_REGEX = r"^v?(?P<value>\d+(\.\d+)*)$"
RANGE_LIST_SEPARATOR_PATTERN = re.compile(r"\s*,\s*")


class Field:
    def __init__(self, name: str, definition: str | dict) -> None:
        # Directly specifying the column name or index instead of its full definition is allowed.
        # In this case we must convert it to a full definition.
        if isinstance(definition, (str, int)):
            definition = {"column": definition}

        self.name = name
        if self.name == "releaseCycle":
            definition["type"] = "string" if "type" not in definition else definition["type"]
            definition["regex"] = definition.get("regex", [DEFAULT_RELEASE_REGEX])
            definition["template"] = definition.get("template", DEFAULT_TEMPLATE)

        self.is_index = isinstance(definition["column"], int)
        if self.is_index:
            self.column = definition["column"] - 1  # convert to 0-based index
        else:
            self.column = definition["column"].lower()

        self.type = definition.get("type", "string")
        if self.name in DATE_FIELDS and self.type not in DATE_TYPES:
            self.type = "date"  # override type for known date fields
        elif self.name in STRING_FIELDS and self.type not in STRING_TYPES:
            self.type = "string"  # override type for known string fields
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

            return self.__process_value(match, raw_value)

        if self.name == "releaseCycle":
            return None  # skipping entire rows is allowed

        msg = f"field {self}'s value '{raw_value}' does not match any regex in {self.include_version_patterns}"
        raise ValueError(msg)

    def __process_value(self, match: Match[str], raw_value: str) -> str | datetime:
        str_value = self.template.render(**match.groupdict()) if self.template else raw_value

        if self.type == "date":
            try:
                return dates.parse_date(str_value)
            except ValueError:
                return dates.parse_month_year_date(str_value)

        elif self.type == "range":
            items = RANGE_LIST_SEPARATOR_PATTERN.split(str_value)
            return f"{items[0]} - {items[-1]}" if len(items) > 1 else str_value

        elif self.type == "identifier":
            return endoflife.to_identifier(str_value)

        return str_value

    def __repr__(self) -> str:
        return f"{self.name}({self.column})"


config = config_from_argv()
with ProductData(config.product) as product_data:
    user_agent = config.data.get("user_agent", http.ENDOFLIFE_BOT_USER_AGENT)
    render_js = config.data.get("render_javascript", False)
    render_js_wait_until = config.data.get("render_javascript_wait_until", None)
    render_js_wait_for = config.data.get("render_javascript_wait_for", None)
    render_js_click_selector = config.data.get("render_javascript_click_selector", None)
    header_row_selector = config.data.get("header_selector", "thead tr")
    rows_selector = config.data.get("rows_selector", "tbody tr")
    cells_selector = "td, th"
    release_cycle_field = Field("releaseCycle", config.data["fields"].pop("releaseCycle"))
    fields = [Field(name, definition) for name, definition in config.data["fields"].items()]

    if render_js:
        response_text = http.fetch_javascript_url(config.url, user_agent=user_agent, wait_until=render_js_wait_until,
                                                  wait_for=render_js_wait_for, click_selector=render_js_click_selector)
    else:
        response_text = http.fetch_url(config.url, user_agent=user_agent).text
    soup = BeautifulSoup(response_text, features="html5lib")

    for table in soup.select(config.data["selector"]):
        header_row = table.select_one(header_row_selector)
        if not header_row:
            logging.info(f"skipping table with attributes {table.attrs}: no header row found")
            continue

        headers = [th.get_text().strip().lower() for th in header_row.select(cells_selector)]
        logging.info(f"processing table with headers {headers}")

        try:
            fields_index = {"releaseCycle": headers.index(release_cycle_field.column)}
            for field in fields:
                fields_index[field.name] = field.column if field.is_index else headers.index(field.column)
            min_column_count = max(fields_index.values()) + 1

            for row in table.select(rows_selector):
                cells = [cell.get_text().strip() for cell in row.select(cells_selector)]
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

        except ValueError as e:
            logging.info(f"skipping table with headers {headers}: {e}")
