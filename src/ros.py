import datetime
import re
from bs4 import BeautifulSoup
from common import endoflife

URL = "https://wiki.ros.org/Distributions"
# https://regex101.com/r/c1ribd/1
regex = r"^ROS (?P<name>(\w| )+)"

print("::group::ros")
response = endoflife.fetch_url(URL)
soup = BeautifulSoup(response, features="html5lib")

versions = {}
for tr in soup.findAll("tr"):
    td_list = tr.findAll("td")
    if len(td_list) > 0:
        version = td_list[0].get_text()

        m = re.match(regex, version.strip())
        if m:
            version = td_list[0].findAll("a")[0]["href"][1:]
            try:
                date = datetime.datetime.strptime(
                    td_list[1].get_text().strip(), "%B %d, %Y"
                )
            # The date is a suffix (May 23rd, 2020)
            except Exception as e:
                x = td_list[1].get_text().split(",")
                date = datetime.datetime.strptime(x[0][:-2] + x[1], "%B %d %Y")
            abs_date = date.strftime("%Y-%m-%d")
            versions[version] = abs_date
            print("%s: %s" % (version, abs_date))

endoflife.write_releases('ros', versions)
print("::endgroup::")
