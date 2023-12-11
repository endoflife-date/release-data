import re
from bs4 import BeautifulSoup
from common import http
from common import dates
from common import endoflife

PRODUCT = "visualstudio"

# There is no build history for versions 2015 and below.
# This is not a big deal because there was no version for those release in a very long time.
URLS = [
    "https://learn.microsoft.com/en-us/visualstudio/releasenotes/vs2017-relnotes-history",
    "https://learn.microsoft.com/en-us/visualstudio/releases/2019/history",
    "https://learn.microsoft.com/en-us/visualstudio/releases/2022/release-history",
]

print(f"::group::{PRODUCT}")
versions = {}

for response in http.fetch_urls(URLS):
    soup = BeautifulSoup(response.text, features="html5lib")
    for table in soup.find_all("table"):
        headers = [th.get_text().strip().lower() for th in table.find_all("th")]
        if "version" not in headers or "release date" not in headers:
            continue

        version_index = headers.index("version")
        date_index = headers.index("release date")
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            if len(cells) < (max(version_index, date_index) + 1):
                continue

            version = cells[version_index].get_text().strip()
            date = cells[date_index].get_text().strip()
            date = dates.parse_date(date).strftime("%Y-%m-%d")

            if date and version and re.match(endoflife.DEFAULT_VERSION_REGEX, version):
                versions[version] = date
                print(f"{version}: {date}")


endoflife.write_releases(PRODUCT, versions)
print("::endgroup::")
