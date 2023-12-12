from bs4 import BeautifulSoup
from common import http
from common import dates
from common import endoflife

# There is no build history for versions 2015 and below.
# This is not a big deal because there was no version for those release in a very long time.
URLS = [
    "https://learn.microsoft.com/en-us/visualstudio/releasenotes/vs2017-relnotes-history",
    "https://learn.microsoft.com/en-us/visualstudio/releases/2019/history",
    "https://learn.microsoft.com/en-us/visualstudio/releases/2022/release-history",
]

product = endoflife.Product("visualstudio")
print(f"::group::{product.name}")
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
            date = dates.parse_date(date)

            if date and version and endoflife.DEFAULT_VERSION_PATTERN.match(version):
                product.declare_version(version, date)

product.write()
print("::endgroup::")
