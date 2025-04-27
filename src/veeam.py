import logging
import re
import sys

from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

"""Fetches Veeam products versions from https://www.veeam.com.

This script takes a single argument which is the url of the versions page on https://www.veeam.com/kb2680,
such as `https://www.veeam.com/kb2680`.
"""

p_filter = sys.argv[1] if len(sys.argv) > 1 else None
m_filter = sys.argv[2] if len(sys.argv) > 2 else None
for config in endoflife.list_configs(p_filter, "veeam", m_filter):
    with releasedata.ProductData(config.product) as product_data:
        response = http.fetch_url(config.url)
        soup = BeautifulSoup(response.text, features="html5lib")

        version_column = config.data.get("version_column", "Build Number").lower()
        date_column = config.data.get("date_column", "Release Date").lower()
        for table in soup.find_all("table"):
            headers = [header.get_text().strip().lower() for header in table.find("tr").find_all("td")]
            if version_column not in headers or date_column not in headers:
                logging.warning("Skipping table with headers %s as it does not contains '%s' or '%s'",
                                headers, version_column, date_column)
                continue

            version_index = headers.index(version_column)
            date_index = headers.index(date_column)
            for row in table.find_all("tr")[1:]:
                cells = row.find_all("td")
                if len(cells) <= max(version_index, date_index):
                    continue

                date_str = cells[date_index].get_text().strip()
                if not date_str or date_str == "-":
                    continue

                # whitespaces in version numbers are replaced with dashes
                version = re.sub(r'\s+', "-", cells[version_index].get_text().strip())
                date = dates.parse_date(date_str)
                product_data.declare_version(version, date)
