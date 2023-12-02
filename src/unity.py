from bs4 import BeautifulSoup
from common import http
from common import endoflife

# Fetches the Unity LTS releases from the Unity website. Non-LTS releases are not listed there,
# so this automation is only partial.
#
# This script iterates over all pages of the Unity LTS releases page, which is paginated.
# It keeps fetching the next page until there is no next page link.

PRODUCT = 'unity'
URL = 'https://unity.com/releases/editor/qa/lts-releases'


def fetch_releases(releases, url) -> str:
    print(url)
    response = http.fetch_url(url)
    soup = BeautifulSoup(response.text, features="html5lib")

    for release in soup.find_all('div', class_='component-releases-item__show__inner-header'):
        version = release.find('h4').find('span').text
        date = release.find('time').attrs['datetime'].split('T')[0]
        releases[version] = date
        print(f"{version}: {date}")

    next_link = soup.find('a', {"rel": "next"})
    if next_link:
        return URL + next_link.attrs['href']

    return None


print(f"::group::{PRODUCT}")
all_versions = {}
next_page_url = URL

# Do not try to fetch multiple pages in parallel: it is raising a lot of ChunkedEncodingErrors and
# make the overall process slower.
while next_page_url:
    next_page_url = fetch_releases(all_versions, next_page_url)

endoflife.write_releases(PRODUCT, all_versions)
print("::endgroup::")
