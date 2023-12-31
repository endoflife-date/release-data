import logging
import re

from bs4 import BeautifulSoup
from common import dates, endoflife, http

IDENTIFIERS_BY_PRODUCT = {
    "pan-os": "pan-os-panorama",
    "pan-gp": "globalprotect",
    "pan-cortex-xdr": "traps-esm-and-cortex",
}

# all products are on the same page, it's faster to fetch it only once
logging.info("::group::palo-alto-networks")
response = http.fetch_url("https://www.paloaltonetworks.com/services/support/end-of-life-announcements/end-of-life-summary")
soup = BeautifulSoup(response.text, features="html5lib")
logging.info("::endgroup::")

for product_name, identifier in IDENTIFIERS_BY_PRODUCT.items():
    product = endoflife.Product(product_name)
    table = soup.find(id=identifier)
    for tr in table.findAll("tr")[3:]:
        td_list = tr.findAll("td")
        if len(td_list) <= 1:
            continue

        version = td_list[0].get_text().strip().lower().replace(" ", "-").replace("*", "")
        version = version.removesuffix("-(cortex-xdr-agent)")
        version = version.removesuffix("-(vm-series-only)")
        version = version.removesuffix("-(panorama-only)")

        # A few dates have 1st, 2nd, 4th... Remove it.
        date_str = re.sub(r'(\w+) (\d{1,2})\w{2}, (\d{4})', r'\1 \2, \3', td_list[1].get_text())
        date = dates.parse_date(date_str)

        product.declare_version(version, date)

    product.write()
