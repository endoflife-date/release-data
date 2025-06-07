import logging

from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        response = http.fetch_url(config.url)
        soup = BeautifulSoup(response.text, features="html5lib")

        for tr in soup.findAll("tr"):
            td_list = tr.findAll("td")
            if len(td_list) == 0:
                continue

            version_str = td_list[0].get_text().strip()
            version_match = config.first_match(version_str)
            if not version_match:
                logging.warning(f"Skipping version '{version_str}': does not match the expected pattern")
                continue

            # Get the "code" (such as noetic) instead of the display name (such as Noetic Ninjemys)
            version = td_list[0].findAll("a")[0]["href"][1:]
            try:
                date = dates.parse_date(td_list[1].get_text())
            except ValueError:  # The day has a suffix (such as May 23rd, 2020)
                x = td_list[1].get_text().split(",")
                date = dates.parse_date(x[0][:-2] + x[1])

            product_data.declare_version(version, date)
