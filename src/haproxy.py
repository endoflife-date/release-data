import json
import re
import urllib.request

URL = "https://www.haproxy.org/download/2.6/src/CHANGELOG"
REGEX = r'^(\d{4})\/(\d{2})\/(\d{2})\s+:\s+(\d+\.\d+\.\d.?)$'

list = {}
with urllib.request.urlopen(URL) as response:
  for line in response:
    m = re.match(REGEX, line.decode('utf-8'))
    if m:
      year,month,date,version = m.groups()
      abs_date = "%s-%s-%s" % (year, month, date)
      list[abs_date] = version

with open('releases/custom/haproxy.json', 'w') as f:
  f.write(json.dumps(list, indent=2))
