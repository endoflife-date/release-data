from bs4 import BeautifulSoup
from common import dates
from common import endoflife
import regex as re
import sys


"""Fetch versions with their dates from apache webserver hosted indexpage .

"""

METHOD = 'indexpage'
DEFAULT_VERSION_REGEX = "(\d+\.\d+\.\d+)"

def fetch_releases(product_name, url, regex):
    result = {}
    version_pattern = re.compile(regex)

    soup = make_bs_request(url)
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 2:
            link = cells[1].find('a')
            if link and product_name in link.text:
                version_match = version_pattern.search(link.text)
                date_text = cells[2].text.strip()

                if version_match and date_text:
                    version = version_match.group(1)  # Extract the version number
                    date = date_text.split(' ')[0]  # Extract the date
                    result[version] = date

    return result

def make_bs_request(url):
    response = endoflife.fetch_url(url)
    return BeautifulSoup(response, features="html5lib")

def update_product(product_name, configs):
    versions = {}

    for config in configs:
        regex = config.get("regex", DEFAULT_VERSION_REGEX)
        print(f"Fetching {METHOD} releases for {product_name} with regex {regex}")
        regex_product = r'{}{}'.format(product_name, regex)
        versions = versions | fetch_releases(product_name, config[METHOD], regex_product)

    endoflife.write_releases(product_name, versions)



p_filter = sys.argv[1] if len(sys.argv) > 1 else None
print(endoflife.list_products(METHOD, p_filter))
for product, configs in endoflife.list_products(METHOD, p_filter).items():
    print(f"::group::{product}")
    update_product(product, configs)
    print("::endgroup::")


