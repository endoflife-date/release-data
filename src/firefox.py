import concurrent.futures
import re
import requests
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime
from typing import Tuple

"""Fetch Firefox versions with their dates from https://www.mozilla.org/"""

URL = "https://www.mozilla.org/en-US/firefox/releases/"
PRODUCT = "firefox"

DATE_REGEX = r"(January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|October|Oct|November|Nov|December|Dec)\s+\d{1,2}(st|nd|rd|th)?,\s+\d{4}"
VERSION_REGEX = r"\d+(\.\d+)*"


class UnsupportedPageError(Exception):
    """Raised when a firefox release page is not supported"""
    pass


class InvalidPageVariantError(Exception):
    """Raised when an invalid variant is passed to get_version_and_date"""
    pass

class UnpublishedReleaseError(Exception):
    """Raised when a page is not yet published, but linked"""
    pass

def format_date(unformatted_date: str) -> str:
    """ Format date from July 11, 2002 to 2002-07-11 """
    date = re.sub(r'(\d)(st|nd|rd|th)', r'\1', unformatted_date)
    formats = ["%b %d, %Y", "%B %d, %Y"]
    for f in formats:
        try:
            return datetime.strptime(date, f).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return ""


def get_version_and_date_variant_1(soup: BeautifulSoup) -> Tuple[str, str]:
    """ Version matching for firefox versions >= 28.0 (usually) """
    # get version
    version = soup.find("div", class_="c-release-version").get_text()

    # get date
    unformatted_date = soup.find("p", class_="c-release-date").get_text()
    date = format_date(unformatted_date)

    return version, date


def get_version_and_date_variant_2(soup: BeautifulSoup) -> Tuple[str, str]:
    """ Version matching for firefox versions >= 10.0 (usually) """
    release_info = soup.find("h2").find("small").text

    # get version
    version_match = re.search(VERSION_REGEX, soup.select('div#nav-access a')[0].get("href"))
    if version_match is None:
        raise InvalidPageVariantError("Unable to find version")
    version = version_match.group()

    # get date
    unformatted_date_match = re.search(DATE_REGEX, release_info)
    if unformatted_date_match is None:
        raise InvalidPageVariantError("Unable to find date")
    unformatted_date = unformatted_date_match.group()
    date = format_date(unformatted_date)

    return version, date


def get_version_and_date_variant_3(soup: BeautifulSoup) -> Tuple[str, str]:
    """ Version matching for firefox versions >= 3.0 (usually) """
    release_info = soup.select('div#main-feature p em')[0].get_text()

    # get version
    version_match = re.search(VERSION_REGEX, release_info)
    if version_match is None:
        raise InvalidPageVariantError("Unable to find version")
    version = version_match.group()

    # get date
    unformatted_date_match = re.search(DATE_REGEX, release_info)
    if unformatted_date_match is None:
        raise InvalidPageVariantError("Unable to find date")
    unformatted_date = unformatted_date_match.group()
    date = format_date(unformatted_date)

    return version, date


def get_version_and_date(release_page: str, release_version: str) -> Tuple[str, str]:
    """ Get version and date from the given release page """
    major = int(release_version.split(".")[0])

    # firefox release pages for versions <3.0 don't include release dates, so we
    # can't match these versions for now.
    # example: https://www.mozilla.org/en-US/firefox/2.0/releasenotes/
    if major < 3:
        raise UnsupportedPageError(f"Unsupported release page: {release_page}")

    # Firefox release pages come in 3 different variants. Unfortunately, there
    # is no consistent way to determine which variant a page is (say, by version
    # number), so we have to try each variant until we find one that works.
    functions = [
        get_version_and_date_variant_1,
        get_version_and_date_variant_2,
        get_version_and_date_variant_3
    ]
    try:
        soup = make_bs_request(release_page)
    except(HTTPError) as e:
        if(e.code == 404):
            raise UnpublishedReleaseError(f"The release page is not yet published, got a 404: {release_page}")
        else:
            raise e

    for function in functions:
        try:
            return function(soup)
        except (InvalidPageVariantError, AttributeError, IndexError):
            pass

    raise UnsupportedPageError(f"Unable to find version and date from {release_page}")


def make_bs_request(url: str) -> BeautifulSoup:
    # requests to www.mozilla.org often time out, retry in case of failures
    response = endoflife.fetch_url(url, timeout=10, retry_count=5)
    return BeautifulSoup(response, features="html5lib")


def fetch_releases():
    releases = {}
    soup = make_bs_request(URL)

    ff_releases = soup.find_all("ol", class_="c-release-list")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {
            executor.submit(
                get_version_and_date,
                requests.compat.urljoin(URL, p.get("href")),
                p.get_text()): p.get("href") for p in ff_releases[0].find_all("a")
        }

        for future in concurrent.futures.as_completed(future_to_url):
            try:
                (version, date) = future.result()
                print(f"{version}: {date}")
                releases[version] = date
            except(UnsupportedPageError, UnpublishedReleaseError):
                print(f"Unsupported release page: {future_to_url[future]}")

    return releases


print(f"::group::{PRODUCT}")
releases = fetch_releases()
endoflife.write_releases(PRODUCT, dict(
    # sort by date then version (desc)
    sorted(releases.items(), key=lambda x: (x[1], x[0]), reverse=True)
))
print("::endgroup::")
