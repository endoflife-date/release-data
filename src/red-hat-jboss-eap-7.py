import logging

from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches RedHat JBoss EAP version data for JBoss 7"""

config = config_from_argv()
with ProductData(config.product) as product_data:
    html = http.fetch_html(config.url)

    for h4 in html.find_all("h4"):
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
            name = name_str.replace("GA", "Update 0").replace("Update ", release + ".")
            if not config.first_match(name):
                continue

            date_str = columns[1].text.strip()
            if date_str == "TBD" or date_str == "TDB": # Placeholder for a future release
                continue

            if date_str == "[July 21, 2021][d7400]":
                # Temporary fix for a typo in the source page
                date_str = "July 21 2021"


            date = dates.parse_date(date_str)
            product_data.declare_version(name, date)
