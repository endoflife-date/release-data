import re
from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime

# https://regex101.com/r/zPxBqT/1
REGEX = r"\d.\d+\.\d+-gke\.\d+"

def fetch_channel(channel):
    url = "https://cloud.google.com/kubernetes-engine/docs/release-notes-{}".format(channel)
    response = endoflife.fetch_url(url)
    return BeautifulSoup(response, features="html5lib")

"""
Takes soup, and returns a dictionary of versions and their release dates
"""
def parse_soup_for_versions(soup):
    """ Parse the soup """
    versions = {}
    for section in soup.find_all('section', class_='releases'):
        # h2 contains the date, which we parse
        for h2 in section.find_all('h2'):
            date = h2.get('data-text')
            date = datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d')
            # The div next to the h2 contains the notes about changes made on that date
            next_div = h2.find_next('div')
            # New releases are noted in a nested list, so we look for that
            # and parse it using the version regex
            for li in next_div.find_all('li'):
                # If the <li> text contains with "versions are now available:", get the <ul> inside the li
                if "versions are now available" in li.text:
                    ul = li.find('ul')
                    for version in re.findall(REGEX, ul.text):
                        versions[version] = date
                        print("%s: %s" % (version, date))
    return versions

CHANNELS = ['nochannel', 'stable', 'regular', 'rapid']

for channel in CHANNELS:
    soup = fetch_channel(channel)
    print("::group::GKE - {}".format(channel))
    versions = parse_soup_for_versions(soup)
    name = 'gke' if channel == 'nochannel' else 'gke-{}'.format(channel)
    endoflife.write_releases(name, versions)
    print("::endgroup::")
