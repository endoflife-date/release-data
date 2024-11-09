import re

from bs4 import BeautifulSoup
from common import dates, http, releasedata

"""Fetches Veeam versions from https://www.veeam.com."""

with releasedata.ProductData("veeam-backup-and-replication") as product_data:
    response = http.fetch_url("https://www.veeam.com/kb2680")
    soup = BeautifulSoup(response.text, features="html5lib")

    for table in soup.find_all("table"):
        headers = [header.get_text().strip().lower() for header in table.find("tr").find_all("td")]
        if "build number" not in headers or "release date" not in headers:
            continue

        version_index = headers.index("build number")
        date_index = headers.index("release date")
        for row in table.find_all("tr")[1:]:
            cells = row.find_all("td")
            if len(cells) <= max(version_index, date_index):
                continue

            date_str = cells[date_index].get_text().strip()
            if date_str and date_str != "-":
                # whitespaces in version numbers are replaced with dashes
                version = re.sub(r'\s+', "-", cells[version_index].get_text().strip())
                date = dates.parse_date(date_str)
                product_data.declare_version(version, date)
