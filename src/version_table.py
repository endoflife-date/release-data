import logging

from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetch version-level data from an HTML table in a web page.

This script works based on a definition provided in the product's frontmatter to locate the table and extract the
necessary information. Available configuration options are:

- selector (optional, default = table): A CSS selector used to locate one or more tables in the page.
- header_selector (optional, default = thead tr): A CSS selector used to locate the table's header row.
- rows_selector (optional, default = tbody tr): A CSS selector used to locate the table's rows.
- name_column (mandatory): The name of the column containing the version names.
- date_column (mandatory): The name of the column containing the version dates.

Supported CSS selectors are defined by BeautifulSoup and documented on its website. For more information, see
https://beautiful-soup-4.readthedocs.io/en/latest/index.html?highlight=selector#css-selectors.
"""

config = config_from_argv()
with ProductData(config.product) as product_data:
    table_selector: str = config.data.get("selector", "table")
    header_row_selector: str = config.data.get("header_selector", "thead tr")
    rows_selector: str = config.data.get("rows_selector", "tbody tr")
    cells_selector: str = "td, th"

    version_name_column = config.data["name_column"].strip().lower()
    version_date_column = config.data["date_column"].strip().lower()

    html = http.fetch_html(config.url)

    for table in html.select(table_selector):
        header_row = table.select_one(header_row_selector)
        if not header_row:
            logging.info(f"skipping table with attributes {table.attrs}: no header row found")
            continue

        headers = [th.get_text().strip().lower() for th in header_row.select(cells_selector)]
        logging.info(f"processing table with headers {headers}")

        try:
            version_name_index = headers.index(version_name_column)
            version_date_index = headers.index(version_date_column)
            min_columns_count = max([version_name_index, version_date_index]) + 1

            for row in table.select(rows_selector):
                cells = [cell.get_text().strip() for cell in row.select(cells_selector)]
                if len(cells) < min_columns_count:
                    logging.debug(f"skipping row {cells}: not enough columns")
                    continue

                raw_version_name = cells[version_name_index]
                version_match = config.first_match(raw_version_name)
                if not version_match:
                    logging.debug(f"skipping row {cells}: invalid release cycle '{raw_version_name}', "
                                  f"should match one of {config.include_version_patterns} "
                                  f"and not match all of {config.exclude_version_patterns}")
                    continue

                version_name = config.render(version_match)
                version_date = dates.parse_datetime(cells[version_date_index])
                product_data.declare_version(version_name, version_date)

        except ValueError as e:
            logging.info(f"skipping table with headers {headers}: {e}")
