from bs4 import BeautifulSoup
from common import dates, http
from common.releasedata import ProductData, config_from_argv

config = config_from_argv()
with ProductData(config.product) as product_data:
    html = BeautifulSoup(http.fetch_javascript_url(config.url, wait_for="table"), "html5lib")

    for release_table in html.find_all("table"):
        for row in release_table.find_all("tr")[1:]:  # for all rows except the header
            cells = row.find_all("td")
            version = cells[0].text.strip("AIX ").replace(' TL', '.')
            date = dates.parse_month_year_date(cells[1].text)
            product_data.declare_version(version, date)
