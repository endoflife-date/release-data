import re

from bs4 import BeautifulSoup
from common import dates, http, releasedata

"""Fetches Satellite versions from access.redhat.com.

A few of the older versions, such as 'Satellite 6.1 GA Release (Build 6.1.1)', were ignored because too hard to parse."""

# https://regex101.com/r/m8aWXG/1
VERSION_PATTERN = re.compile(r"^Satellite (?P<version>\d+\.\d+\.\d+([.-]\d+)?) ([Uu]pdate|[Rr]elease)$")

with releasedata.ProductData("redhat-satellite") as product_data:
    response = http.fetch_url("https://access.redhat.com/articles/1365633")
    soup = BeautifulSoup(response.text, features="html5lib")

    for table in soup.findAll("tbody"):
        for tr in table.findAll("tr"):
            td_list = tr.findAll("td")

            version_str = td_list[0].get_text().replace(' GA', '.0').strip()  # x.y GA => x.y.0
            version_match = VERSION_PATTERN.match(version_str)
            if version_match:
                version = version_match["version"].replace('-', '.')  # a.b.c-d => a.b.c.d
                date_str = td_list[1].get_text().strip()
                date_str = '2024-12-04' if date_str == '2024-12-041' else date_str  # there is a typo for 6.15.5
                date = dates.parse_date(date_str)
                product_data.declare_version(version, date)
