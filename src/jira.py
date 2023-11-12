from requests_html import HTMLSession
from common import endoflife
from datetime import datetime

"""Fetch Jira versions with their dates from the Atlassian Website.

This script is using requests-html (https://requests-html.kennethreitz.org/)
because the page needs JavaScript to render correctly.
"""

PRODUCT = 'jira'
URL = 'https://www.atlassian.com/software/jira/update'


def parse_date(text):
    return datetime.strptime(text, "%d-%b-%Y").strftime("%Y-%m-%d")


print(f"::group::{PRODUCT}")

session = HTMLSession()
r = session.get(URL)
r.html.render(sleep=1, scrolldown=3)

versions = {}
for version_block in r.html.find('.versions-list'):
    version = version_block.find('a.product-versions', first=True).attrs['data-version']
    date = parse_date(version_block.find('.release-date', first=True).text)
    print(f"{version}: {date}")
    versions[version] = date

endoflife.write_releases(PRODUCT, versions)
print("::endgroup::")
