import re
from bs4 import BeautifulSoup
from common import dates
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
REGEX = r"[r|R]elease [d|D]ate[,|:]? (.*?)\).*?Build Number: (.*?)$"

print(f"::group::{PRODUCT}")
versions = {}

for response in endoflife.fetch_urls(URLS):
    soup = BeautifulSoup(response.text, features="html5lib")
    for p in soup.findAll("div", class_="text"):
        text = p.get_text().strip().replace('\xa0', ' ')
        matches = re.findall(REGEX, text, re.DOTALL | re.MULTILINE)
        for m in matches:
            date = dates.parse_date(m[0]).strftime("%Y-%m-%d")
            version = m[1].strip().replace(",",".")
            versions[version] = date
            print(f"{version}: {date}")

endoflife.write_releases(PRODUCT, versions)
print("::endgroup::")
