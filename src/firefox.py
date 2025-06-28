import urllib.parse

from bs4 import BeautifulSoup
from common import dates, http, releasedata

"""Fetch Firefox versions with their dates from https://www.mozilla.org/.

This script is cumulative: previously found versions are kept, and eventually updated if needed. It only considers the
first MAX_VERSIONS_COUNT versions on Firefox release page because:
- it is too long to fetch them all (at least a minute usually),
- this generates too many requests to the mozilla.org servers,
- and anyway oldest versions are never updated.

Note that it was assumed that:
- the script is ran regularly enough to keep the versions up to date (once a day or week looks enough),
- the versions are listed in descending order on the page,
- new versions are always added inside in the last MAX_VERSIONS_COUNT versions.

The script will need to be updated if someday those conditions are not met."""

MAX_VERSIONS_LIMIT = 100

for config in releasedata.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        releases_page = http.fetch_url(config.url)
        releases_soup = BeautifulSoup(releases_page.text, features="html5lib")
        releases_list = releases_soup.find_all("ol", class_="c-release-list")

        release_notes_urls = [urllib.parse.urljoin(releases_page.url, p.get("href")) for p in releases_list[0].find_all("a")]
        for release_notes in http.fetch_urls(release_notes_urls[:MAX_VERSIONS_LIMIT]):
            version = release_notes.url.split("/")[-3]
            release_notes_soup = BeautifulSoup(release_notes.text, features="html5lib")
            date_str = release_notes_soup.find(class_="c-release-date").get_text()  # note: only works for versions > 25
            product_data.declare_version(version, dates.parse_date(date_str))
