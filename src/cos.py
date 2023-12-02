import re
from bs4 import BeautifulSoup
from common import http
from common import dates
from common import endoflife

URL = "https://cloud.google.com/container-optimized-os/docs/release-notes/"
REGEX = r"^(cos-\d+-\d+-\d+-\d+)"


def list_milestones():
    response = http.fetch_url(URL)
    soup = BeautifulSoup(response.text, features="html5lib")
    milestones = soup.find_all('td', string=re.compile(r'COS \d+ LTS'))
    return [m.text.split(' ')[1] for m in milestones]


def fetch_milestones(milestones):
    urls = [f"{URL}m{channel}" for channel in milestones]
    return http.fetch_urls(urls)


def parse_date(date_str):
    date_str = date_str.strip().replace('Date: ', '')
    date_str = re.sub(r'Sep[a-zA-Z]+', 'Sep', date_str)
    return dates.parse_date(date_str).strftime('%Y-%m-%d')


def find_versions(text):
    """Takes soup, and returns a dictionary of versions and their release dates
    """
    versions = {}
    soup = BeautifulSoup(text, features="html5lib")
    for article in soup.find_all('article', class_='devsite-article'):
        # h2 contains the date, which we parse
        for heading in article.find_all(['h2', 'h3']):
            version = heading.get('data-text')
            m = re.match(REGEX, version)
            if m:
                version = m.group(1)
                try:
                    # 1st row is the header, so pick the first td in the 2nd row
                    d = heading.find_next('tr').find_next('tr').find_next('td').text
                except AttributeError:
                    # In some older releases, it is mentioned as Date: [Date]
                    d = heading.find_next('i').text
                try:
                    date = parse_date(d)
                except ValueError:
                    d = heading.find_previous('h2').get('data-text')
                    date = parse_date(d)
                versions[version] = date
                print(f"{version}: {date}")

    return versions


print("::group::cos")
versions = {}

for response in fetch_milestones(list_milestones()):
    versions |= find_versions(response.text)

endoflife.write_releases('cos', versions)
print("::endgroup::")
