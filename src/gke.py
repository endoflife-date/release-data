import re

from bs4 import BeautifulSoup
from common import dates, endoflife, http

# https://regex101.com/r/zPxBqT/1
VERSION_PATTERN = re.compile(r"\d.\d+\.\d+-gke\.\d+")
URL_BY_PRODUCT = {
    "gke": "https://cloud.google.com/kubernetes-engine/docs/release-notes-nochannel",
    "gke-stable": "https://cloud.google.com/kubernetes-engine/docs/release-notes-stable",
    "gke-regular": "https://cloud.google.com/kubernetes-engine/docs/release-notes-regular",
    "gke-rapid": "https://cloud.google.com/kubernetes-engine/docs/release-notes-rapid",
}

for product_name, url in URL_BY_PRODUCT.items():
    product = endoflife.Product(product_name)
    print(f"::group::{product.name}")
    relnotes = http.fetch_url(url)
    relnotes_soup = BeautifulSoup(relnotes.text, features="html5lib")

    for section in relnotes_soup.find_all('section', class_='releases'):
        for h2 in section.find_all('h2'):  # h2 contains the date
            date = dates.parse_date(h2.get('data-text'))

            next_div = h2.find_next('div')  # The div next to the h2 contains the notes about changes made on that date
            for li in next_div.find_all('li'):
                if "versions are now available" in li.text:
                    for version in VERSION_PATTERN.findall(li.find('ul').text):
                        product.declare_version(version, date)

    product.write()
    print("::endgroup::")
