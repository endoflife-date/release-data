import re
from bs4 import BeautifulSoup
from common import http
from common import endoflife

"""Fetch versions with their dates from access.redhat.com.

A few of the older versions, such as 'Satellite 6.1 GA Release (Build 6.1.1)',
were ignored because too hard to parse.
"""

URL = "https://access.redhat.com/articles/1365633"
# https://regex101.com/r/m8aWXG/1
regex = r"^Satellite (?P<version>\d+\.\d+\.\d+([.-]\d+)?) ([Uu]pdate|[Rr]elease)$"

print("::group::redhat-satellite")
response = http.fetch_url(URL)
soup = BeautifulSoup(response.text, features="html5lib")

versions = {}
for table in soup.findAll("tbody"):
    for tr in table.findAll("tr"):
        td_list = tr.findAll("td")

        # Versions x.y GA are transformed to x.y.0
        version = td_list[0].get_text().replace(' GA', '.0').strip()
        m = re.match(regex, version)
        if m:
            # Versions a.b.c-d are transformed to a.b.c.d
            version = m["version"].replace('-', '.')
            date = td_list[1].get_text().strip()
            versions[version] = date
            print(f"{version}: {date}")

endoflife.write_releases('redhat-satellite', versions)
print("::endgroup::")
