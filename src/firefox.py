import re
import urllib.parse
from bs4 import BeautifulSoup
from common import http
from common import dates
from common import endoflife

"""Fetch Firefox versions with their dates from https://www.mozilla.org/"""

URL = "https://www.mozilla.org/en-US/firefox/releases/"
PRODUCT = "firefox"


def format_date(text: str) -> str:
    text = text.replace(')', '')
    return dates.parse_date(text).strftime("%Y-%m-%d")


print(f"::group::{PRODUCT}")
versions = {}

response = http.fetch_url(URL)
ff_releases = BeautifulSoup(response.text, features="html5lib").find_all("ol", class_="c-release-list")
urls = [urllib.parse.urljoin(URL, p.get("href")) for p in ff_releases[0].find_all("a")]

for response in http.fetch_urls(urls):
    soup = BeautifulSoup(response.text, features="html5lib")

    version = response.request.url.split("/")[-3]
    if soup.find("div", class_="c-release-version"):
        date = format_date(soup.find("p", class_="c-release-date").get_text())
        versions[version] = date
        print(f"{version}: {date}")
    elif soup.find("small", string=re.compile("^.?First offered")):
        element = soup.find("small", string=re.compile("^.?First offered"))
        date = format_date(' '.join(element.get_text().split(" ")[-3:]))  # get last 3 words
        versions[version] = date
        print(f"{version}: {date}")
    # we don't get version <= 10.0, not a big deal

endoflife.write_releases(PRODUCT, versions)
print("::endgroup::")
