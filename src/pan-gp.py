import json
import urllib.request
from bs4 import BeautifulSoup

URL = "https://www.paloaltonetworks.com/services/support/end-of-life-announcements/end-of-life-summary"

list = {}
with urllib.request.urlopen(URL, data=None, timeout=5) as response:
  soup = BeautifulSoup(response, features="html5lib")
  table = soup.find(id='globalprotect')
  for tr in table.findAll('tr')[3:]:
    td_list = tr.findAll('td')
    version = td_list[0].get_text()
    month,date,year = td_list[1].get_text().split('/')
    abs_date = f"{year}-{month:0>2}-{date:0>2}"
    list[version] = abs_date

with open('releases/pan-gp.json', 'w') as f:
  f.write(json.dumps(list, indent=2))
