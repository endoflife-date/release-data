import urllib.request
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime

# Keep updated against https://cloud.google.com/container-optimized-os/docs/release-notes/
REGEX = r"^(cos-\d+-\d+-\d+-\d+)"
MILESTONES = [69, 73, 77, 81, 85, 89, 93, 97, 101, 105]

def fetch_milestone(channel):
    url = "https://cloud.google.com/container-optimized-os/docs/release-notes/m{}".format(channel)
    # Google Docs website often returns SSL errors, retry the request in case of failures.
    for i in range(0,5):
        try:
            with urllib.request.urlopen(url, data=None, timeout=5) as response:
                return BeautifulSoup(response, features="html5lib")
        except Exception as e:
            print("Retrying Request")
            continue
    raise Exception("Failed to fetch COS milestone {}".format(channel))


"""
Takes soup, and returns a dictionary of versions and their release dates
"""
def parse_soup_for_versions(soup):
    """ Parse the soup """
    versions = {}
    for article in soup.find_all('article', class_='devsite-article'):
        # h2 contains the date, which we parse
        for heading in article.find_all(['h2', 'h3']):
            version = heading.get('data-text')
            m = re.match(REGEX, version)
            if m:
                version = m.group(1)
                date_format = '%b %d, %Y'
                try:
                    # The first row is the header, so we pick the first td in the second row
                    d = heading.find_next('tr').find_next('tr').find_next('td').text
                except:
                    # In some older releases, it is mentioned as Date: [Date] in the text
                    d = heading.find_next('i').text
                # If the date begins with a 4 letter month name, trim it to just 3 letters
                # Strip out the Date: section from the start
                d = re.sub(r'(?:Date\: )?(\w{3})(?:\w{1})? (\d{1,2}), (\d{4})', r'\1 \2, \3', d)
                date = datetime.strptime(d, date_format).strftime('%Y-%m-%d')
                versions[version] = date

    return versions

def get_all_versions():
    all_versions = {}
    for milestone in MILESTONES:
        soup = fetch_milestone(milestone)
        print("::group::COS - {}".format(milestone))
        versions = parse_soup_for_versions(soup)
        all_versions |= versions
        print("::endgroup::")

    return all_versions

if __name__ == '__main__':
    v = get_all_versions()
    with open('releases/cos.json', "w") as f:
        f.write(json.dumps(v, indent=2))
