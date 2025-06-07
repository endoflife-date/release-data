import logging

from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

"""Fetches RedHat JBoss EAP version data for JBoss 7"""

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        response = http.fetch_url(config.url)
        soup = BeautifulSoup(response.text, features="html5lib")

        for h4 in soup.find_all("h4"):
            title = h4.get_text(strip=True)
            if not title.startswith("7."):
                continue

            release = title[:3]
            version_table = h4.find_next("table")
            if not version_table:
                logging.warning(f"Version table not found for {title}")
                continue

            for (i, row) in enumerate(version_table.find_all("tr")):
                if i == 0:  # Skip the first row (header)
                    continue

                columns = row.find_all("td")
                # Get the version name without the content of the <sup> tag, if present
                name_str = ''.join([content for content in columns[0].contents if isinstance(content, str)]).strip()
                date_str = columns[1].text.strip()

                if date_str == "TBD" or date_str == "TDB": # Placeholder for a future release
                    continue

                if date_str == "[July 21, 2021][d7400]":
                    # Temporary fix for a typo in the source page
                    date_str = "July 21 2021"

                name = name_str.replace("GA", "Update 0").replace("Update ", release + ".")
                date = dates.parse_date(date_str)
                product_data.declare_version(name, date)
