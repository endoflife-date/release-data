import re
import urllib.parse
from itertools import islice

from bs4 import BeautifulSoup
from common import dates, http, releasedata

"""Fetch Firefox versions with their dates from https://www.mozilla.org/.

Versions lower than 10.0 are ignored because too difficult to parse."""


# Will be replaced by itertools.batched in Python 3.12+.
# See https://docs.python.org/3/library/itertools.html#itertools.batched.
def batched(iterable: iter, n: int) -> iter:
    if n < 1:
        msg = 'n must be at least one'
        raise ValueError(msg)
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


with releasedata.ProductData("firefox") as product_data:
    releases_page = http.fetch_url("https://www.mozilla.org/en-US/firefox/releases/")
    releases_soup = BeautifulSoup(releases_page.text, features="html5lib")
    releases_list = releases_soup.find_all("ol", class_="c-release-list")
    release_notes_urls = [urllib.parse.urljoin(releases_page.url, p.get("href")) for p in releases_list[0].find_all("a")]

    for batch_release_notes_urls in batched(release_notes_urls, 20):
        for release_notes in http.fetch_urls(batch_release_notes_urls):
            version = release_notes.url.split("/")[-3]

            release_notes_soup = BeautifulSoup(release_notes.text, features="html5lib")
            date_elt = release_notes_soup.find(class_="c-release-date")
            if date_elt:
                date = dates.parse_date(date_elt.get_text())
                product_data.declare_version(version, date)
                continue

            date_elt = release_notes_soup.find("small", string=re.compile("^.?First offered"))
            if date_elt:
                date = dates.parse_date(' '.join(date_elt.get_text().split(" ")[-3:]))  # get last 3 words
                product_data.declare_version(version, date)
            # versions < 10.0 are ignored
