import logging

from common import dates, http, releasedata

"""Fetches AWS lambda runtimes with their support / EOL dates from https://docs.aws.amazon.com."""

for config in releasedata.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        html = http.fetch_html(config.url)

        for i, table in enumerate(html.find_all("table")):
            headers = [th.get_text().strip().lower() for th in table.find("thead").find_all("tr")[0].find_all("th")]
            if "identifier" not in headers or "deprecation date" not in headers or "block function update" not in headers:
                logging.info(f"table with header '{headers}' does not contain all the expected headers")
                continue

            is_supported_table = i == 0  # first table is for supported runtimes, second for deprecated ones
            identifier_index = headers.index("identifier")
            deprecation_date_index = headers.index("deprecation date")
            block_function_update_index = headers.index("block function update")

            for row in table.find("tbody").find_all("tr"):
                cells = row.find_all("td")
                identifier = cells[identifier_index].get_text().strip()

                deprecation_date_str = cells[deprecation_date_index].get_text().strip()
                try:
                    deprecation_date = dates.parse_date(deprecation_date_str)
                except ValueError:
                    deprecation_date = None

                if identifier == "nodejs4.3-edge":
                    # there is a mistake in the data: block function update date cannot be before the deprecation date
                    block_function_update_str = "2020-04-30"
                else:
                    block_function_update_str = cells[block_function_update_index].get_text().strip()
                try:
                    block_function_update = dates.parse_date(block_function_update_str)
                except ValueError:
                    block_function_update = None

                release = product_data.get_release(identifier)
                # if no date is available, use False for supported runtimes and True for deprecated ones
                release.set_eoas(deprecation_date if deprecation_date else not is_supported_table)
                # if no date is available, use False for supported runtimes and True for deprecated ones
                release.set_eol(block_function_update if block_function_update else not is_supported_table)
