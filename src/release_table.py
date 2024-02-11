import sys

from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

"""Fetch release-level data from an HTML table in a web page.

This script works based on a definition provided in the product's frontmatter to locate the table and extract the
necessary information. Available configuration options are:

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

        for table in soup.select(config.data["selector"]):
            headers = [th.get_text().strip().lower() for th in table.select(config.data["headers_selector"])]

            index_by_target = {}
            for target, column in config.data["mapping"].items():
                index_by_target[target] = headers.index(str(column).lower())

            min_column_count = max(index_by_target.values()) + 1
            for row in table.select(config.data["rows_selector"]):
                cells = row.findAll("td")
                if len(cells) < min_column_count:
                    continue

                release_cycle = cells[index_by_target["releaseCycle"]].get_text().strip()
                release = product_data.get_release(release_cycle)
                for target, index in index_by_target.items():
                    value_str = cells[index].get_text().strip()

                    try:
                        value = dates.parse_date(value_str)
                    except ValueError:
                        value = value_str

                    release.set_field(target, value)
