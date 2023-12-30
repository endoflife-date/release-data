import re

from bs4 import BeautifulSoup
from common import dates, endoflife, http

# https://regex101.com/r/c1ribd/1
VERSION_PATTERN = re.compile(r"^ROS (?P<name>(\w| )+)")

product = endoflife.Product("ros")
print(f"::group::{product.name}")
response = http.fetch_url("https://wiki.ros.org/Distributions")
soup = BeautifulSoup(response.text, features="html5lib")

for tr in soup.findAll("tr"):
    td_list = tr.findAll("td")
    if len(td_list) == 0:
        continue

    version_str = td_list[0].get_text().strip()
    if VERSION_PATTERN.match(version_str):
        # Get the "code" (such as noetic) instead of the display name (such as Noetic Ninjemys)
        version = td_list[0].findAll("a")[0]["href"][1:]
        try:
            date = dates.parse_date(td_list[1].get_text())
        except ValueError:  # The day has a suffix (such as May 23rd, 2020)
            x = td_list[1].get_text().split(",")
            date = dates.parse_date(x[0][:-2] + x[1])

        product.declare_version(version, date)

product.write()
print("::endgroup::")
