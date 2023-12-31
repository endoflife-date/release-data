import sys

from bs4 import BeautifulSoup
from common import dates, endoflife, http

"""Fetches versions from repositories managed with cgit, such as the Linux kernel repository.
Ideally we would want to use the git repository directly, but cgit-managed repositories don't support partial clone."""

METHOD = "cgit"

p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product_name in endoflife.list_products(METHOD, p_filter):
    product = endoflife.Product(product_name)
    product_frontmatter = endoflife.ProductFrontmatter(product.name)
    for auto_config in product_frontmatter.get_auto_configs(METHOD):
        response = http.fetch_url(auto_config.url + '/refs/tags')
        soup = BeautifulSoup(response.text, features="html5lib")

        for table in soup.find_all("table", class_="list"):
            for row in table.find_all("tr"):
                columns = row.find_all("td")
                if len(columns) != 4:
                    continue

                version_str = columns[0].text.strip()
                version_match = auto_config.first_match(version_str)
                if not version_match:
                    continue

                datetime_td = columns[3].find_next("span")
                datetime_str = datetime_td.attrs["title"] if datetime_td else None
                if not datetime_str:
                    continue

                version = auto_config.render(version_match)
                date = dates.parse_datetime(datetime_str)
                product.declare_version(version, date)

    product.write()
