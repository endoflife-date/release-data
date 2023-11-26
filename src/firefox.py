import re
import urllib.parse
from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime

"""Fetch Firefox versions with their dates from https://www.mozilla.org/"""

URL = "https://www.mozilla.org/en-US/firefox/releases/"
PRODUCT = "firefox"


def format_date(text: str) -> str:
    text = text.replace(')', '')
    formats = ["%b %d, %Y", "%B %d, %Y"]
    for f in formats:
        try:
            return datetime.strptime(text, f).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return ""


print(f"::group::{PRODUCT}")
versions = {}

response = endoflife.fetch_url(URL)
ff_releases = BeautifulSoup(response, features="html5lib").find_all("ol", class_="c-release-list")
urls = [urllib.parse.urljoin(URL, p.get("href")) for p in ff_releases[0].find_all("a")]

for response in endoflife.fetch_urls(urls):
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
