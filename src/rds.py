import logging

from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

"""Fetches Amazon RDS versions from the version management pages on AWS docs.

Pages parsed by this script are expected to have version tables with a version in the first column and its release date
in the third column (usually named 'RDS release date').
"""

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        response = http.fetch_url(config.url)
        soup = BeautifulSoup(response.text, features="html5lib")

        for table in soup.find_all("table"):
            for row in table.find_all("tr"):
                columns = row.find_all("td")
                if len(columns) <= 3:
                    continue

                version_text = columns[0].text.strip()
                version_match = config.first_match(version_text)
                if not version_match:
                    logging.warning(f"Skipping {version_text}: does not match any version pattern")
                    continue

                version = config.render(version_match)
                date = dates.parse_date(columns[2].text)
                product_data.declare_version(version, date)
