import json
import re
from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime

REGEX = r"^(cos-\d+-\d+-\d+-\d+)"


def fetch_all_milestones():
    url = "https://cloud.google.com/container-optimized-os/docs/release-notes/"
    # Retry as Google Docs often returns SSL errors.
    response = endoflife.fetch_url(url, retry_count=10)
    soup = BeautifulSoup(response, features="html5lib")
    milestones = soup.find_all('td', text=re.compile(r'COS \d+ LTS'))
    return [m.text.split(' ')[1] for m in milestones]


def fetch_milestone(channel):
    url = "https://cloud.google.com/container-optimized-os/docs/release-notes/m{}".format(channel)
    # Retry as Google Docs often returns SSL errors.
    response = endoflife.fetch_url(url, retry_count=10)
    return BeautifulSoup(response, features="html5lib")


def parse_soup_for_versions(soup):
    """Takes soup, and returns a dictionary of versions and their release dates
    """
    versions = {}
    for article in soup.find_all('article', class_='devsite-article'):
        def parse_date(d):
            # If the date begins with a >3 letter month name, trim it to just 3 letters
            # Strip out the Date: section from the start
            d = re.sub(r'(?:Date\: )?(\w{3})(?:\w{1,4})? (\d{1,2}), (\d{4})', r'\1 \2, \3', d)
            return datetime.strptime(d, date_format).strftime('%Y-%m-%d')
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
                try:
                    date = parse_date(d)
                except ValueError:
                    d = heading.find_previous('h2').get('data-text')
                    date = parse_date(d)
                versions[version] = date
                print("%s: %s" % (version, date))

    return versions


def get_all_versions():
    all_versions = {}
    all_milestones = fetch_all_milestones()
    print("::group::cos")
    for milestone in all_milestones:
        soup = fetch_milestone(milestone)
        versions = parse_soup_for_versions(soup)
        all_versions |= versions
    print("::endgroup::")
    return all_versions


if __name__ == '__main__':
    v = get_all_versions()
    with open('releases/cos.json', "w") as f:
        f.write(json.dumps(v, indent=2))
