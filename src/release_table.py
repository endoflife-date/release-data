import sys

from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

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

        index_by_target = {}
        headers = [th.get_text().strip().lower() for th in table.select(config.data["headers_selector"])]
        for target, column in config.data["mapping"].items():
            index_by_target[target] = headers.index(str(column).lower())

        min_column_count = max(index_by_target.values()) + 1
        release_cycle_index = index_by_target.pop("releaseCycle")
        for row in table.select(config.data["rows_selector"]):
            cells = row.findAll("td")
            if len(cells) < min_column_count:
                continue

            release_cycle = cells[release_cycle_index].get_text().strip()
            release_cycle_match = config.first_match(release_cycle)
            if not release_cycle_match:
                continue

            release = product_data.get_release(config.render(release_cycle_match))
            release.set_field("releaseCycle", release.name())
            for target, index in index_by_target.items():
                value_str = cells[index].get_text().strip()

                try:
                    value = dates.parse_date(value_str)
                except ValueError:
                    value = value_str

                release.set_field(target, value)
