import logging

from bs4 import BeautifulSoup
from common import dates, http, releasedata

"""Fetches NetBSD versions and EOL information from https://www.netbsd.org/."""

with releasedata.ProductData('netbsd') as product_data:
    response = http.fetch_url('https://www.netbsd.org/releases/formal.html')
    soup = BeautifulSoup(response.text, features="html5lib")

    for row in soup.select('table tbody tr'):
        cells = [cell.get_text(strip=True) for cell in row.select('td')]

        version = cells[0]
        if not version.startswith('NetBSD'):
            logging.info(f"Skipping row {cells}, version does not start with 'NetBSD'")
            continue
        version = version.split(' ')[1]

        try:
            release_date = dates.parse_date(cells[1])
            product_data.declare_version(version, release_date)
        except ValueError:
            logging.warning(f"Skipping row {cells}, could not parse release date")

        eol_str = cells[2]
        if not eol_str:
            continue

        eol = dates.parse_date(eol_str)
        major_version = version.split('.')[0]
        product_data.get_release(major_version).set_eol(eol)
