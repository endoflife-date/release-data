import re
from datetime import datetime

from bs4 import BeautifulSoup
from common import dates, endoflife, http

"""Fetches versions from Adobe ColdFusion release notes on helpx.adobe.com.

x.y.0 release dates are unfortunately not available in the release notes and have to updated them manually each time a
new minor version is released.
"""

URLS = [
    "https://helpx.adobe.com/coldfusion/kb/coldfusion-10-updates.html",
    "https://helpx.adobe.com/coldfusion/kb/coldfusion-11-updates.html",
    "https://helpx.adobe.com/coldfusion/kb/coldfusion-2016-updates.html",
    "https://helpx.adobe.com/coldfusion/kb/coldfusion-2018-updates.html",
    "https://helpx.adobe.com/coldfusion/kb/coldfusion-2021-updates.html",
    "https://helpx.adobe.com/coldfusion/kb/coldfusion-2023-updates.html"
]

VERSION_AND_DATE_PATTERN = re.compile(r"Release Date[,|:]? (.*?)\).*?Build Number: (.*?)$",
                                      re.DOTALL | re.MULTILINE | re.IGNORECASE)

# .0 release dates are not available in the release notes.
FIXED_VERSIONS = {
    "10.0.0": datetime(2012, 5, 15),  # https://en.wikipedia.org/wiki/Adobe_ColdFusion#Adobe_ColdFusion_10
    "11.0.0": datetime(2014, 4, 29),  # https://en.wikipedia.org/wiki/Adobe_ColdFusion#Adobe_ColdFusion_11
    "2016.0.0": datetime(2016, 2, 16),  # https://en.wikipedia.org/wiki/Adobe_ColdFusion#Adobe_ColdFusion_(2016_Release)
    "2018.0.0": datetime(2018, 7, 12),  # https://coldfusion.adobe.com/2018/07/new-coldfusion-release-adds-performance-monitoring-toolset-for-measuring-monitoring-and-managing-high-performing-web-apps/
    "2021.0.0": datetime(2020, 11, 11),  # https://community.adobe.com/t5/coldfusion-discussions/introducing-adobe-coldfusion-2021-release/m-p/11585468
    "2023.0.0": datetime(2022, 5, 16),  # https://coldfusion.adobe.com/2023/05/coldfusion2023-release/
}

product = endoflife.Product("coldfusion")
print(f"::group::{product.name}")

for changelog in http.fetch_urls(URLS):
    changelog_soup = BeautifulSoup(changelog.text, features="html5lib")

    for p in changelog_soup.findAll("div", class_="text"):
        version_and_date_str = p.get_text().strip().replace('\xa0', ' ')
        for (date_str, version_str) in VERSION_AND_DATE_PATTERN.findall(version_and_date_str):
            date = dates.parse_date(date_str)
            version = version_str.strip().replace(",", ".")  # 11,0,0,289974 -> 11.0.0.289974
            product.declare_version(version, date)

product.declare_versions(FIXED_VERSIONS)
product.write()
print("::endgroup::")
