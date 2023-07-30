import datetime
import re
from bs4 import BeautifulSoup
from common import endoflife

"""Fetch versions with their dates from the RSS feed of
https://docs.aws.amazon.com/neptune/latest/userguide/engine-releases.html.
"""

PRODUCT = "aws-lambda"
URL = 'https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html'

def parse_date(s):
    s = s.strip()
    if s == '':
        return None
    return datetime.datetime.strptime(s, '%b %d, %Y')

print(f"::group::{PRODUCT}")

response = endoflife.fetch_url(URL)
soup = BeautifulSoup(response, features="html5lib")
table_headers = soup.findAll('th', {'class':'table-header'})

runtimes = {}

for table_header in table_headers[0:1]:
    print(table_header)
    table = table_header.parent.parent.parent
    for tr in table.findAll('tr'):
        td_list = tr.findAll("td")
        if not td_list:
            continue
        print(td_list)
        runtime = td_list[1].find('code').text
        r = {
            'name': td_list[0].text.strip(),
            'deprecation': None,
            'endoflife': None,
            }
        deprecation = td_list[5].text
        if deprecation:
            r['deprecation'] = parse_date(deprecation)
        runtimes[runtime] = r

for table_header in table_headers[1:]:
    table = table_header.parent.parent.parent
    for tr in table.findAll('tr'):
        td_list = tr.findAll("td")
        if not td_list:
            continue
        for td in td_list:
            print(td)
        runtime = td_list[1].find('code').text
        r = {
            'name': td_list[0].text.strip(),
            'deprecation': parse_date(td_list[3].text),
            'endoflife': parse_date(td_list[4].text),
            }
        runtimes[runtime] = r

print(runtimes)
