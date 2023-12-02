import re
from bs4 import BeautifulSoup
from common import http
from common import dates
from common import endoflife

# Release dates are not available in the release notes, so we have to set them manually.
RELEASE_DATES = {
    "10.0.0": "2012-05-15", # https://en.wikipedia.org/wiki/Adobe_ColdFusion#Adobe_ColdFusion_10
    "11.0.0": "2014-04-29", # https://en.wikipedia.org/wiki/Adobe_ColdFusion#Adobe_ColdFusion_11
    "2016.0.0": "2016-02-16", # https://en.wikipedia.org/wiki/Adobe_ColdFusion#Adobe_ColdFusion_(2016_Release)
    "2018.0.0": "2018-07-12", # https://coldfusion.adobe.com/2018/07/new-coldfusion-release-adds-performance-monitoring-toolset-for-measuring-monitoring-and-managing-high-performing-web-apps/
    "2021.0.0": "2020-11-11", # https://community.adobe.com/t5/coldfusion-discussions/introducing-adobe-coldfusion-2021-release/m-p/11585468
    "2023.0.0": "2022-05-16", # https://coldfusion.adobe.com/2023/05/coldfusion2023-release/
}

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
versions = RELEASE_DATES | {}

for response in http.fetch_urls(URLS):
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
