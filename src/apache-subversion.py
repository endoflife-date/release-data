import logging
import re

from bs4 import BeautifulSoup
from common import dates, http, releasedata

# https://regex101.com/r/k4i7EO/1 only non beta versions
VERSION_PATTERN = re.compile(r"^Subversion\s(?P<version>[1-9]\d*.\d+\.\d+)$")
# https://regex101.com/r/GsimYd/2
DATE_PATTERN = re.compile(r"^\((?P<date>\w+,\s\d{1,2}\s\w+\s\d{4})")

with releasedata.ProductData("apache-subversion") as product_data:
    relnotes = http.fetch_url("https://subversion.apache.org/docs/release-notes/release-history.html")
    relnotes_soup = BeautifulSoup(relnotes.text, features="html5lib")

    ul = relnotes_soup.find("h2").find_next("ul")
    for li in ul.find_all("li"):
        b = li.find_next("b") # b contains the version
        version_text = b.get_text(strip=True)
        version_match = VERSION_PATTERN.match(version_text)
        if not version_match:
            logging.info(f"Skipping {version_text}, does not match version regex")
            continue

        remaining_part_str = b.next_sibling.get_text(strip=True)
        date_match = DATE_PATTERN.match(remaining_part_str)
        if not date_match:
            logging.info(f"Skipping {version_text}, no matching date in '{remaining_part_str}'")
            continue

        version = version_match.group("version")
        date = dates.parse_date(date_match.group("date"))
        product_data.declare_version(version, date)
