import re
from bs4 import BeautifulSoup
from common import dates
from common import endoflife

# https://regex101.com/r/zPxBqT/1
REGEX = r"\d.\d+\.\d+-gke\.\d+"
CHANNELS = ['nochannel', 'stable', 'regular', 'rapid']


def fetch_channel(channel):
    url = f"https://cloud.google.com/kubernetes-engine/docs/release-notes-{channel}"
    response = endoflife.fetch_url(url)
    return BeautifulSoup(response, features="html5lib")


def parse_soup_for_versions(soup):
    """Takes soup, and returns a dictionary of versions and their release dates
    """
    versions = {}
    for section in soup.find_all('section', class_='releases'):
        # h2 contains the date, which we parse
        for h2 in section.find_all('h2'):
            date = h2.get('data-text')
            date = dates.parse_date(date).strftime("%Y-%m-%d")
            # The div next to the h2 contains the notes about changes made
            # on that date
            next_div = h2.find_next('div')
            # New releases are noted in a nested list, so we look for that
            # and parse it using the version regex
            for li in next_div.find_all('li'):
                # If the <li> text contains with "versions are now available:",
                # get the <ul> inside the li
                if "versions are now available" in li.text:
                    ul = li.find('ul')
                    for version in re.findall(REGEX, ul.text):
                        versions[version] = date
                        print(f"{version}: {date}")
    return versions


for channel in CHANNELS:
    soup = fetch_channel(channel)
    print(f"::group::GKE - {channel}")
    versions = parse_soup_for_versions(soup)
    name = 'gke' if channel == 'nochannel' else f'gke-{channel}'
    endoflife.write_releases(name, versions)
    print("::endgroup::")
