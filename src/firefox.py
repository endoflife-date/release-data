import re
import urllib.parse
from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests_futures.sessions import FuturesSession
from requests.exceptions import ChunkedEncodingError
from concurrent.futures import as_completed

"""Fetch Firefox versions with their dates from https://www.mozilla.org/"""

URL = "https://www.mozilla.org/en-US/firefox/releases/"
PRODUCT = "firefox"

DATE_REGEX = r"(January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|October|Oct|November|Nov|December|Dec)\s+\d{1,2}(st|nd|rd|th)?,\s+\d{4}"
VERSION_REGEX = r"\d+(\.\d+)*"


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
ff_urls = [urllib.parse.urljoin(URL, p.get("href")) for p in ff_releases[0].find_all("a")]

session = FuturesSession()
session.mount('https://', HTTPAdapter(max_retries=Retry(total=5, backoff_factor=0.2)))
futures = [session.get(url, timeout=30) for url in ff_urls]
for future in as_completed(futures):
    try:
        response = future.result()
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
    except ChunkedEncodingError:
        # This may happen sometimes and will be ignored to not make the script fail,
        # see https://stackoverflow.com/a/71899731/374236.
        print(f"Error fetching {response.request.url}: ChunkedEncodingError")

endoflife.write_releases(PRODUCT, versions)
print("::endgroup::")
