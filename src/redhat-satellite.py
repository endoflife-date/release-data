import re
from bs4 import BeautifulSoup
from common import dates
from common import endoflife
from common import http

"""Fetches Satellite versions from access.redhat.com.

A few of the older versions, such as 'Satellite 6.1 GA Release (Build 6.1.1)', were ignored because too hard to parse."""

# https://regex101.com/r/m8aWXG/1
VERSION_PATTERN = re.compile(r"^Satellite (?P<version>\d+\.\d+\.\d+([.-]\d+)?) ([Uu]pdate|[Rr]elease)$")

product = endoflife.Product("redhat-satellite")
print(f"::group::{product.name}")
response = http.fetch_url("https://access.redhat.com/articles/1365633")
soup = BeautifulSoup(response.text, features="html5lib")

for table in soup.findAll("tbody"):
    for tr in table.findAll("tr"):
        td_list = tr.findAll("td")

        version_str = td_list[0].get_text().replace(' GA', '.0').strip()  # x.y GA => x.y.0
        version_match = VERSION_PATTERN.match(version_str)
        if version_match:
            version = version_match["version"].replace('-', '.')  # a.b.c-d => a.b.c.d
            date = dates.parse_date(td_list[1].get_text().strip())
            product.declare_version(version, date)

product.write()
print("::endgroup::")
