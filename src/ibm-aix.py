from bs4 import BeautifulSoup
from common import http
from common import dates
from common import endoflife

URLS = [
    "https://web.archive.org/web/20210123024247/https://www.ibm.com/support/pages/aix-support-lifecycle-information",
    "https://www.ibm.com/support/pages/aix-support-lifecycle-information",
]

product = endoflife.Product("ibm-aix")
print(f"::group::{product.name}")
for page in http.fetch_urls(URLS):
    page_soup = BeautifulSoup(page.text, features="html5lib")

    for release_table in page_soup.find("div", class_="ibm-container-body").find_all("table", class_="ibm-data-table ibm-grid"):
        for row in release_table.find_all("tr")[1:]:  # for all rows except the header
            cells = row.find_all("td")
            version = cells[0].text.strip("AIX ").replace(' TL', '.')
            date = dates.parse_month_year_date(cells[1].text)
            product.declare_version(version, date)

product.write()
print("::endgroup::")
