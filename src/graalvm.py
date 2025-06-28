import logging

from common import dates, endoflife, http, releasedata

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        html = http.fetch_html(config.url)
        table_selector = config.data.get("table_selector", "#previous-releases + table").strip()
        date_column = config.data.get("date_column", "Date").strip().lower()
        versions_column = config.data.get("versions_column").strip().lower()

        table = html.select_one(table_selector)
        if not table:
            logging.warning(f"Skipping config {config} as no table found with selector {table_selector}")
            continue

        headers = [th.get_text().strip().lower() for th in table.select("thead th")]
        if date_column not in headers or versions_column not in headers:
            logging.info(f"Skipping table with headers {headers} as it does not contain the required columns: {date_column}, {versions_column}")
            continue

        date_index = headers.index(date_column)
        versions_index = headers.index(versions_column)

        for row in table.select("tbody tr"):
            cells = row.select("td")
            if len(cells) <= max(date_index, versions_index):
                logging.warning(f"Skipping row {cells}: not enough cells")
                continue

            date_text = cells[date_index].get_text().strip()
            date = dates.parse_date(date_text)
            if date > dates.today():
                logging.info(f"Skipping future version {cells}")
                continue

            versions = cells[versions_index].get_text().strip()
            for version in versions.split(", "):
                if config.first_match(version):
                    product_data.declare_version(version.strip(), date)
