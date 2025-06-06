from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        page = http.fetch_url(config.url)
        page_soup = BeautifulSoup(page.text, features="html5lib")

        for release_table in page_soup.find("div", class_="ibm-container-body").find_all("table", class_="ibm-data-table ibm-grid"):
            for row in release_table.find_all("tr")[1:]:  # for all rows except the header
                cells = row.find_all("td")
                version = cells[0].text.strip("AIX ").replace(' TL', '.')
                date = dates.parse_month_year_date(cells[1].text)
                product_data.declare_version(version, date)
