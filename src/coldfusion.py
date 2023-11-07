import re
from bs4 import BeautifulSoup
from datetime import datetime
from common import endoflife

URLS = [
    "https://helpx.adobe.com/coldfusion/kb/coldfusion-10-updates.html",
    "https://helpx.adobe.com/coldfusion/kb/coldfusion-11-updates.html",
    "https://helpx.adobe.com/coldfusion/kb/coldfusion-2016-updates.html",
    "https://helpx.adobe.com/coldfusion/kb/coldfusion-2018-updates.html",
    "https://helpx.adobe.com/coldfusion/kb/coldfusion-2021-updates.html",
    "https://helpx.adobe.com/coldfusion/kb/coldfusion-2023-updates.html"
]

PRODUCT = "coldfusion"
regex = r"[r|R]elease [d|D]ate[,|:]? (.*?)\).*?Build Number: (.*?)$"

"""
Make a HEAD request to the URL
and parse the Last-Modified header
to return a YYYY-MM-DD string
"""
def parse_release_date(text):
    text = text.replace(",", "")
    date_formats = ['%d %b %Y', '%d %B %Y', '%b %d %Y', '%B %d %Y']

    for date_format in date_formats:
        try:
            return datetime.strptime(text, date_format).strftime("%Y-%m-%d")
        except ValueError:
            pass

    raise ValueError("Cannot parse date '" + text + "' with formats " + str(date_formats))

def parse(url, versions):
    response = endoflife.fetch_url(url)
    soup = BeautifulSoup(response, features="html5lib")
    for p in soup.findAll("div", class_="text"):
        text = p.get_text().strip().replace('\xa0', ' ')
        matches = re.findall(regex, text, re.DOTALL | re.MULTILINE)
        for m in matches:
            date = parse_release_date(m[0].strip())
            version = m[1].strip().replace(",",".")
            versions[version] = date
            print(f"{version}: {date}")

def fetch_releases():
    releases = {}
    for url in URLS:
        parse(url, releases)

    return releases

print(f"::group::{PRODUCT}")
releases = fetch_releases()
endoflife.write_releases(PRODUCT, dict(
    # sort by version (desc)
    sorted(releases.items(), key=lambda x: (x[0]), reverse=True)
))
print("::endgroup::")
