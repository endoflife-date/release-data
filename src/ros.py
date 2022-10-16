import json
import urllib.request
import datetime
from bs4 import BeautifulSoup
import re

URL = "https://wiki.ros.org/Distributions"
# https://regex101.com/r/c1ribd/1
regex = r"^ROS (?P<name>(\w| )+)"

list = {}

with urllib.request.urlopen(URL, timeout=5) as response:
    soup = BeautifulSoup(response, features="html5lib")
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
                list[version] = abs_date
                print("%s: %s" % (version, abs_date))

with open("releases/ros.json", "w") as f:
    f.write(json.dumps(list, indent=2))
