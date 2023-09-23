import re
from bs4 import BeautifulSoup
from common import endoflife

PRODUCT = 'unity'
URL = 'https://unity.com/releases/editor/qa/lts-releases'


def fetch_releases(releases, url) -> str:
    print(url)
    response = endoflife.fetch_url(url)
    soup = BeautifulSoup(response, features="html5lib")

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
releases = {}
next_page_url = URL

while next_page_url:
    next_page_url = fetch_releases(releases, next_page_url)

endoflife.write_releases(PRODUCT, dict(
    # sort by version then date (asc)
    sorted(releases.items(), key=lambda x: (x[0], x[1]))
))
print("::endgroup::")
