from bs4 import BeautifulSoup
from common import dates
from common import endoflife
from common import http

# Fetches the Unity LTS releases from the Unity website. Non-LTS releases are not listed there,
# so this automation is only partial.
#
# This script iterates over all pages of the Unity LTS releases page, which is paginated.
# It keeps fetching the next page until there is no next page link.

BASE_URL = "https://unity.com/releases/editor/qa/lts-releases"

product = endoflife.Product("unity")
print(f"::group::{product.name}")
next_page_url = BASE_URL

# Do not try to fetch multiple pages in parallel: it is raising a lot of errors and make the overall process slower.
while next_page_url:
    response = http.fetch_url(next_page_url)
    soup = BeautifulSoup(response.text, features="html5lib")

    for release in soup.find_all('div', class_='component-releases-item__show__inner-header'):
        version = release.find('h4').find('span').text
        date = dates.parse_datetime(release.find('time').attrs['datetime'])
        product.declare_version(version, date)

    next_link = soup.find('a', {"rel": "next"})
    next_page_url = BASE_URL + next_link.attrs['href'] if next_link else None

product.write()
print("::endgroup::")
