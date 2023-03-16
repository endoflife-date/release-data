import json
import urllib.request
import datetime
from bs4 import BeautifulSoup
import re

URLS = [
    "https://support.apple.com/en-us/HT201222",  # latest
    "https://support.apple.com/kb/HT213078",  # 2018-2019
    "https://support.apple.com/kb/HT213077",  # 2016-2017
    "https://support.apple.com/kb/HT209441",  # 2015
    "https://support.apple.com/kb/HT205762",  # 2014
    "https://support.apple.com/kb/HT205759",  # 2013
    "https://support.apple.com/kb/HT204611",  # 2011 to 2012
    "https://support.apple.com/kb/HT5165",  # 2010
    "https://support.apple.com/kb/HT4218",  # 2008-2009
    "https://support.apple.com/kb/HT1263",  # 2005-2007
]

# If you are changing these, please
# use https://gist.githubusercontent.com/captn3m0/e7cb1f4fc3c07a5da0296ebda2b33e15/raw/5747e42ad611ec9ffdb7a2d1c0e3946bb87ab6d7/apple.txt as your corpus
# to validate your changes
CONFIG = {
    "macos": [
        # This covers Sierra and beyond
        r"^macOS[\D]+(?P<version>\d+(?:\.\d+)*)",
        # This covers Mavericks - El Capitan
        r"OS\s+X\s[\w\s]+\sv?(?P<version>\d+(?:\.\d+)+)",
        # This covers even older versions (OS X)
        r"^Mac\s+OS\s+X\s[\w\s]+\sv?(?P<version>\d{2}(?:\.\d+)+)",
    ],
    "ios": [
        r"iOS\s+(?P<version>\d+)",
        r"iOS\s+(?P<version>\d+(?:)(?:\.\d+)+)",
        r"iPhone\s+v?(?P<version>\d+(?:)(?:\.\d+)+)",
    ],
    "ipados": [
        r"iPadOS\s+(?P<version>\d+)",
        r"iPadOS\s+(?P<version>\d+(?:)(?:\.\d+)+)"
    ],
    "watchos": [
        r"watchOS\s+(?P<version>\d+)",
        r"watchOS\s+(?P<version>\d+(?:)(?:\.\d+)+)"
    ],
}

release_lists = {k: {} for k in CONFIG.keys()}
print("::group::apple")


def parse_date(s):
    d, m, y = s.strip().split(" ")
    m = m[0:3].lower()
    return datetime.datetime.strptime("%s %s %s" % (d, m, y), "%d %b %Y")


for url in URLS:
    with urllib.request.urlopen(url, data=None, timeout=5) as response:
        soup = BeautifulSoup(response, features="html5lib")
        table = soup.find(id="tableWraper")
        for tr in reversed(table.findAll("tr")[1:]):
            td_list = tr.findAll("td")
            version_text = td_list[0].get_text()
            for key, regexes in CONFIG.items():
                for regex in regexes:
                    matches = re.findall(regex, version_text, re.MULTILINE)
                    if matches:
                        for version in matches:
                            abs_date = None
                            try:
                                print("== %s" % version_text.strip())
                                abs_date = parse_date(td_list[2].get_text())
                                print_date = abs_date.strftime("%Y-%m-%d")
                                # Only update the date if we are adding first time
                                # or if the date is lower
                                if version not in release_lists[key]:
                                    release_lists[key][version] = abs_date
                                    print("%s-%s: %s" % (key, version, print_date))
                                elif release_lists[key][version] < abs_date:
                                    print(
                                        "%s-%s: %s [IGNORED]"
                                        % (key, version, print_date)
                                    )
                                elif release_lists[key][version] > abs_date:
                                    # This is a lower date, so we mark it with a bang
                                    print(
                                        "%s-%s: %s [UPDATED]"
                                        % (key, version, print_date)
                                    )
                                    release_lists[key][version] = abs_date
                            except ValueError as e:
                                print(
                                    "%s-%s Failed to parse Date (%s)"
                                    % (key, version, td_list[2].get_text())
                                )
                                next


for k in CONFIG.keys():
    with open("releases/%s.json" % k, "w") as f:
        data = {v: d.strftime("%Y-%m-%d") for v, d in release_lists[k].items()}
        f.write(json.dumps(data, indent=2))

print("::endgroup::")
