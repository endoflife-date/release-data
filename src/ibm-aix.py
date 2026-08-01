from bs4 import BeautifulSoup

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        html = BeautifulSoup(http.fetch_javascript_url(config.url, wait_for="table"), features="html5lib")

        for release_table in html.find_all("table"):
            for row in release_table.find_all("tr")[1:]:  # for all rows except the header
                cells = row.find_all("td")
                version = cells[0].text.strip("AIX ").replace(' TL', '.')
                date = dates.parse_month_year_date(cells[1].text)
                product_data.declare_version(version, date)
