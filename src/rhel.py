import json
import urllib.request
from bs4 import BeautifulSoup
import re

URL = "https://access.redhat.com/articles/3078"
# https://regex101.com/r/877ibq/1
regex = r"RHEL (?P<major>\d)(\. ?(?P<minor>\d+))?(( Update (?P<minor2>\d))| GA)?"

list = {}
headers = {"user-agent": "mozilla"}
req = urllib.request.Request(URL, headers=headers)

with urllib.request.urlopen(req, timeout=5) as response:
    soup = BeautifulSoup(response, features="html5lib")
    for tr in soup.findAll("tr"):
        td_list = tr.findAll("td")
        if len(td_list) > 0:
            version = td_list[0].get_text()
            m = re.match(regex, version.strip()).groupdict()
            version = m["major"]
            if m["minor"]:
                version += ".%s" % m["minor"]
            if m["minor2"]:
                version += ".%s" % m["minor2"]
            list[version] = td_list[1].get_text()

with open("releases/redhat.json", "w") as f:
    f.write(json.dumps(list, indent=2))
