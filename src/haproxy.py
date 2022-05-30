import json
import re
import urllib.request

# https://regex101.com/r/1JCnFC/1
REGEX = r'^(\d{4})\/(\d{2})\/(\d{2})\s+:\s+(\d+\.\d+\.\d.?)$'

list = {}

for i in range(17, 27):
  url = "https://www.haproxy.org/download/%s/src/CHANGELOG" % (i/10)
  with urllib.request.urlopen(url) as response:
    for line in response:
      m = re.match(REGEX, line.decode('utf-8'))
      if m:
        year,month,date,version = m.groups()
        abs_date = "%s-%s-%s" % (year, month, date)
        list[version] = abs_date

with open('releases/haproxy.json', 'w') as f:
  f.write(json.dumps(list, indent=2))
