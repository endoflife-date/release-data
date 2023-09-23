import re
from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime

# Parse Atlassian product release notes to get the release date of each version.
#
# For each product, we get the list of minor releases from a set of main release notes page,
# then we get the release date either from that page or from the version's dedicated page.
#
# Unfortunately, the structure of the release notes pages is not consistent across versions,
# and there are some typos in the text, so we have to use a few heuristics to parse the data
# and not all versions can be retrieved.

BASE_URL = 'https://confluence.atlassian.com'
# 'unpublished' versions were never published due to various technical reasons
PRODUCTS = {
    'confluence': {
        'main_urls': [
            f"{BASE_URL}/doc/confluence-release-notes-327.html",
            f"{BASE_URL}/doc/confluence-7-releases-1115677314.html",
            f"{BASE_URL}/doc/confluence-6-releases-976776014.html",
            # 5 and lower pages don't have the same structure
        ],
        'unpublished': [],
    },
    'jira': {
        'main_urls': [
            f"{BASE_URL}/jiracore/jira-core-release-notes-781386726.html"
            # 7.1 and lower pages don't have the same structure
        ],
        'unpublished': ['7.2.5', '7.13.10', '7.13.7'],
    },
}

RELNOTES_PATTERN = re.compile(r'release notes', re.IGNORECASE)
RESOLVED_IN_PATTERN = re.compile(r'(Issues resolved in|Resolved issues in)', re.IGNORECASE)
# a in released is optional because of a typo for Jira 8.20.26
DATE_PATTERN = re.compile(r'Rele?ased( on)? (?P<date>\d+ \w+ \d+)', re.IGNORECASE)


def parse_date(text):
    m = re.match(DATE_PATTERN, text)
    if not m:
        raise ValueError("Cannot find date in '" + text + "'")

    date_formats = ['%d %B %Y', '%d %b %Y']
    for date_format in date_formats:
        try:
            return datetime.strptime(m['date'], date_format).strftime("%Y-%m-%d")
        except ValueError:
            pass

    raise ValueError("Cannot parse '" + text + "' with formats " + str(date_formats))


def get_date_from_dedicated_page(release_title) -> str:
    page_url = BASE_URL + release_title.find('a').get('href')
    page = BeautifulSoup(endoflife.fetch_url(page_url), features="html5lib")

    date = page.find('time')
    if date:
        return date.get('datetime')

    try:
        return parse_date(page.find('p', string=DATE_PATTERN).text)
    except ValueError:
        raise ValueError(f"cannot find date on dedicated page {page_url}")


def fetch_releases_from_relnotes(link, unpublished_versions):
    versions = {}
    relnotes_url = BASE_URL + link.get('href')
    relnotes = BeautifulSoup(endoflife.fetch_url(relnotes_url), features="html5lib")

    for release_title in relnotes.find_all(['h3', 'p'], string=RESOLVED_IN_PATTERN):
        version = release_title.text.split(' ')[-1]
        date_paragraph = release_title.find_next('p')
        date_text = date_paragraph.text.strip() if date_paragraph else ''

        try:
            date = parse_date(date_text)
            versions[version] = date
            print(f"{version}: {date}")
        except ValueError as ex:
            if version not in unpublished_versions:
                try:
                    date = get_date_from_dedicated_page(release_title)
                    versions[version] = date
                    print(f"{version}: {date}")
                except ValueError as ex:
                    print(f"Error parsing date for {version}: {ex}")

    return versions


def fetch_releases(main_urls, unpublished_versions):
    versions = {}

    for main_url in main_urls:
        main = BeautifulSoup(endoflife.fetch_url(main_url), features="html5lib")
        releases_div = main.find('div', class_='sidepanel-in-this-section')

        for link in releases_div.find_all('a', string=RELNOTES_PATTERN):
            versions = versions | fetch_releases_from_relnotes(link, unpublished_versions)

    return versions


for product in PRODUCTS.keys():
    print(f"::group::{product}")
    all_versions = fetch_releases(PRODUCTS[product]['main_urls'], PRODUCTS[product]['unpublished'])
    endoflife.write_releases(product, dict(
        # sort by date then version (asc)
        sorted(all_versions.items(), key=lambda x: (x[1], x[0]))
    ))
    print("::endgroup::")
