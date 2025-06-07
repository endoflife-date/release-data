import logging

from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

"""Fetches LibreOffice versions from https://downloadarchive.documentfoundation.org/libreoffice/old/"""

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        response = http.fetch_url(config.url)
        soup = BeautifulSoup(response.text, features="html5lib")

        for table in soup.find_all("table"):
            for row in table.find_all("tr")[1:]:
                cells = row.find_all("td")
                if len(cells) < 4:
                    continue

                version_str = cells[1].get_text().strip()
                version_match = config.first_match(version_str)
                if not version_match:
                    logging.warning(f"Skipping version {version_str} as it does not match any known version pattern")
                    continue
                version = config.render(version_match)

                date_str = cells[2].get_text().strip()
                date = dates.parse_datetime(date_str)

                product_data.declare_version(version, date)
