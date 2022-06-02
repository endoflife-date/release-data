import json
import urllib.request
import datetime
from bs4 import BeautifulSoup
import re
from html.parser import HTMLParser

URLS = [
  "https://support.apple.com/en-us/HT201222", # latest
  "https://support.apple.com/kb/HT213078", # 2018-2019
  "https://support.apple.com/kb/HT213077", # 2016-2017
  "https://support.apple.com/kb/HT209441", # 2015
  "https://support.apple.com/kb/HT205762", # 2014
  "https://support.apple.com/kb/HT205759", # 2013
  "https://support.apple.com/kb/HT204611", # 2011 to 2012
  "https://support.apple.com/kb/HT5165", # 2010
  "https://support.apple.com/kb/HT4218", # 2008-2009
  "https://support.apple.com/kb/HT1263", # 2005-2007
]

# If you are changing these, please
# use https://www.toptal.com/developers/hastebin/mikahukube.txt as your corpus
# to validate your changes
CONFIG = {
  "macos": [
    # This covers Sierra and beyond
    r"macOS [\w ]+ (?P<version>\d{2}(?:\.\d+)+)",
    # This covers Mavericks - El Capitan
    r"OS X [\w ]+ v?(?P<version>\d{2}(?:\.\d+)+)",
    # This covers even older versions (OS X)
    r"^Mac OS X [\w ]+ v?(?P<version>\d{2}(?:\.\d+)+)",
  ],
  "ios": [
    r"iOS (?P<version>\d+(?:)(?:\.\d+)+)",
    r"iPhone v?(?P<version>\d+(?:)(?:\.\d+)+)"
  ],
  "ipados": [
    r"iPadOS (?P<version>\d+(?:)(?:\.\d+)+)"
  ],
  "watchos": [
    r"watchOS (?P<version>\d+(?:)(?:\.\d+)+)"
  ]
}

release_lists = {k: {} for k in CONFIG.keys()}
print("::group::apple")

for url in URLS:
  with urllib.request.urlopen(url, data=None, timeout=5) as response:
    soup = BeautifulSoup(response, features="html5lib")
    table = soup.find(id='tableWraper')
    for tr in reversed(table.findAll('tr')[1:]):
      td_list = tr.findAll('td')
      version_text = td_list[0].get_text()
      for key,regexes in CONFIG.items():
        for regex in regexes:
          matches = re.findall(regex, version_text, re.MULTILINE)
          if matches:
            for version in matches:
              try:
                abs_date = datetime.datetime.strptime(td_list[2].get_text(), "%d %b %Y")
                print_date = abs_date.strftime("%Y-%m-%d")
              except:
                next
              # Only update the date
              if version not in release_lists[key]:
                release_lists[key][version] = abs_date
                print("%s-%s: %s" % (key, version, print_date))
              elif release_lists[key][version] < abs_date:
                print("%s-%s: %s [IGNORED]" % (key, version, print_date))
              elif release_lists[key][version] > abs_date:
                # This is a lower date, so we mark it with a bang
                print("%s-%s: %s [UPDATED]" % (key, version, print_date))
                release_lists[key][version] = abs_date
              else:
                pass


for k in CONFIG.keys():
  with open("releases/%s.json" % k, 'w') as f:
    data = {v: d.strftime("%Y-%m-%d") for v,d in release_lists[k].items()}
    f.write(json.dumps(data, indent=2))

print("::endgroup::")
