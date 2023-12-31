import re
import urllib.parse

from bs4 import BeautifulSoup
from common import dates, endoflife, http

"""Fetch Firefox versions with their dates from https://www.mozilla.org/.

Versions lower than 10.0 are ignored because too difficult to parse."""

product = endoflife.Product("firefox")
releases_page = http.fetch_url("https://www.mozilla.org/en-US/firefox/releases/")
releases_soup = BeautifulSoup(releases_page.text, features="html5lib")
releases_list = releases_soup.find_all("ol", class_="c-release-list")
release_notes_urls = [urllib.parse.urljoin(releases_page.url, p.get("href")) for p in releases_list[0].find_all("a")]

for release_notes in http.fetch_urls(release_notes_urls):
    version = release_notes.url.split("/")[-3]

    release_notes_soup = BeautifulSoup(release_notes.text, features="html5lib")
    if release_notes_soup.find("div", class_="c-release-version"):
        date = dates.parse_date(release_notes_soup.find("p", class_="c-release-date").get_text())
        product.declare_version(version, date)

    elif release_notes_soup.find("small", string=re.compile("^.?First offered")):
        element = release_notes_soup.find("small", string=re.compile("^.?First offered"))
        date = dates.parse_date(' '.join(element.get_text().split(" ")[-3:]))  # get last 3 words
        product.declare_version(version, date)
    # versions < 10.0 are ignored

product.write()
