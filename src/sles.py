import logging

from bs4 import BeautifulSoup
from common import dates, endoflife, http

product = endoflife.Product("sles")
response = http.fetch_url("https://www.suse.com/lifecycle")
soup = BeautifulSoup(response.text, features="html5lib")

products_table = soup.find("tbody", id="productSupportLifecycle")
sles_header_rows = products_table.find_all("tr", class_="row", attrs={"data-productfilter": "SUSE Linux Enterprise Server"})

# Extract rows' IDs to find related sub-rows with details (normally hidden until a user expands a section)
for detail_id in [f"detail{row['id']}" for row in sles_header_rows]:
    detail_row = products_table.find("tr", id=detail_id)
    # There is a table with info about minor releases and after it, optionally, a table with info about modules
    minor_versions_table = detail_row.find_all("tbody")[0]

    # The first sub-row is a header, the rest contains info about the first release and later minor releases
    for row in minor_versions_table.find_all("tr")[1:]:
        # For each minor release there is an FCS date, general support end date and LTSS end date
        cells = row.find_all("td")
        version = cells[0].text.replace("SUSE Linux Enterprise Server ", '').replace(' SP', '.')
        date_str = cells[1].text

        try:
            date = dates.parse_date(date_str)
            product.declare_version(version, date)
        except ValueError:
            logging.info(f"Ignoring {version}: date '{date_str}' could not be parsed")

product.write()
