from bs4 import BeautifulSoup
from common import dates, http, releasedata

"""Fetches AWS lambda runtimes with their support / EOL dates from https://docs.aws.amazon.com."""

with releasedata.ProductData("aws-lambda") as product_data:
    response = http.fetch_url("https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html")
    soup = BeautifulSoup(response.text, features="html5lib")

    for table in soup.find_all("table"):
        table_name = table.find("thead").find_all("tr")[0].find("th").get_text().strip().lower()
        if table_name != "supported runtimes" and table_name != "deprecated runtimes":
            message = f"unexpected table '{table_name}'"
            raise ValueError(message)

        headers = [th.get_text().strip().lower() for th in table.find("thead").find_all("tr")[1].find_all("th")]
        if "identifier" not in headers or "deprecation date" not in headers or "block function update" not in headers:
            message = f"table '{table_name}' does not contain the expected headers"
            raise ValueError(message)

        is_supported_table = table_name == "supported runtimes"
        identifier_index = headers.index("identifier")
        deprecation_date_index = headers.index("deprecation date")
        block_function_update_index = headers.index("block function update")

        for row in table.find("tbody").find_all("tr"):
            cells = row.find_all("td")
            identifier = cells[identifier_index].get_text().strip()

            deprecation_date_str = cells[deprecation_date_index].get_text().strip()
            deprecation_date = dates.parse_date(deprecation_date_str) if deprecation_date_str else None

            if identifier == "nodejs4.3-edge":
                # there is a mistake in the data: block function update date cannot be before the deprecation date
                block_function_update_str = "2020-04-30"
            else:
                block_function_update_str = cells[block_function_update_index].get_text().strip()
            block_function_update = dates.parse_date(block_function_update_str) if block_function_update_str else None

            release = product_data.get_release(identifier)
            # if no date is available, use True for supported runtimes and False for deprecated ones
            release.set_support(deprecation_date if deprecation_date else is_supported_table)
            # if no date is available, use False for supported runtimes and True for deprecated ones
            release.set_eol(block_function_update if block_function_update else not is_supported_table)
