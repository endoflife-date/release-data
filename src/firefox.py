import json
from typing import Tuple
from datetime import datetime
import re
import requests
import urllib.request
from bs4 import BeautifulSoup

"""Fetch Firefox versions with their dates from https://www.mozilla.org/en-US/firefox/releases/"""
URL = "https://www.mozilla.org/en-US/firefox/releases/"
PRODUCT = "firefox"

DATE_REGEX = r"(January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|October|Oct|November|Nov|December|Dec)\s+\d{1,2}(st|nd|rd|th)?,\s+\d{4}"
VERSION_REGEX = r"\d+(\.\d+)*"

class UnsupportedReleasePageError(Exception):
    "Raised when a firefox release page is not supported"
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

def get_version_and_date_gt_28(rp_soup) -> Tuple[str, str]:
    """ Version matching for firefox versions >= 28.0 """

    # get version
    version = rp_soup.find("div", class_="c-release-version").get_text()

    # get date
    unformatted_date = rp_soup.find("p", class_="c-release-date").get_text()
    date = format_date(unformatted_date)

    return (version, date)

def get_version_and_date_gt_10(rp_soup) -> Tuple[str, str]:
    """ Version matching for firefox versions >= 10.0 """
    release_info = rp_soup.find("h2").find("small").text

    # get version
    version_match = re.search(VERSION_REGEX, rp_soup.select('div#nav-access a')[0].get("href"))
    if version_match is None:
        raise UnsupportedReleasePageError("Unable to find version")
    version = version_match.group()

    # get date
    unformatted_date_match = re.search(DATE_REGEX, release_info)
    if unformatted_date_match is None:
        raise UnsupportedReleasePageError("Unable to find date")
    unformatted_date = unformatted_date_match.group()
    date = format_date(unformatted_date)

    return (version, date)

def get_version_and_date_gt_3(rp_soup) -> Tuple[str, str]:
    """ Version matching for firefox versions >= 3.0 """
    release_info = rp_soup.select('div#main-feature p em')[0].get_text()

    # get version
    version_match = re.search(VERSION_REGEX, release_info)
    if version_match is None:
        raise UnsupportedReleasePageError("Unable to find version")
    version = version_match.group()

    # get date
    unformatted_date_match = re.search(DATE_REGEX, release_info)
    if unformatted_date_match is None:
        raise UnsupportedReleasePageError("Unable to find date")
    unformatted_date = unformatted_date_match.group()
    date = format_date(unformatted_date)

    return (version, date)

def get_version_and_date(soup: BeautifulSoup, release_page: str) -> Tuple[str, str]:
    functions = [get_version_and_date_gt_28, get_version_and_date_gt_10, get_version_and_date_gt_3]
    for function in functions:
        try:
            return function(soup)
        except (UnsupportedReleasePageError, AttributeError, IndexError):
            pass

    raise UnsupportedReleasePageError("Unable to find version and date for %s" % release_page)

def make_bs_request(url: str) -> BeautifulSoup:
    """ Make a request to the given url and return a BeautifulSoup object """
    headers = {"user-agent": "mozilla"}
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req, timeout=5)
    return BeautifulSoup(res.read(), features="html5lib")

def fetch_releases():
    releases = {}
    soup = make_bs_request(URL)

    ff_releases = soup.find_all("ol", class_="c-release-list")
    for p in ff_releases[0].find_all("a")[::-1]:
        release_page = requests.compat.urljoin(URL, p.get("href"))
        rp_soup = make_bs_request(release_page)

        try:
            (version, date) = get_version_and_date(rp_soup, release_page)
            print("%s: %s" % (version, date))
            releases[version] = date
        except UnsupportedReleasePageError:
            print("Unsupported release page: %s" % release_page)

    return releases

def main():
    print(f"::group::{PRODUCT}")

    releases = fetch_releases()
    with open(f"releases/{PRODUCT}.json", "w") as f:
        f.write(json.dumps(
            # sort by date desc
            dict(sorted(releases.items(), key=lambda e: e[1], reverse=True)),
            indent=2))

    print("::endgroup::")


if __name__ == '__main__':
    main()
