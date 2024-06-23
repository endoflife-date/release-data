import re

from bs4 import BeautifulSoup
from common import dates, http, releasedata

"""Fetches LibreOffice versions from https://downloadarchive.documentfoundation.org/libreoffice/old/"""

VERSION_PATTERN = re.compile(r"^(?P<version>\d+(\.\d+)*)\/$")

with releasedata.ProductData("libreoffice") as product_data:
    response = http.fetch_url("https://downloadarchive.documentfoundation.org/libreoffice/old/")
    soup = BeautifulSoup(response.text, features="html5lib")

    for table in soup.find_all("table"):
        for row in table.find_all("tr")[1:]:
            cells = row.find_all("td")
            if len(cells) < 4:
                continue

            version_str = cells[1].get_text().strip()
            date_str = cells[2].get_text().strip()
            version_match = VERSION_PATTERN.match(version_str)

            if version_match:
                version = version_match["version"]
                date = dates.parse_datetime(date_str)
                product_data.declare_version(version, date)
