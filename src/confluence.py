from requests_html import HTMLSession
from common import dates
from common import endoflife

"""Fetch Confluence versions with their dates from the Atlassian Website.

This script is using requests-html (https://requests-html.kennethreitz.org/)
because the page needs JavaScript to render correctly.
"""

PRODUCT = 'confluence'
URL = 'https://www.atlassian.com/software/confluence/download-archives'

print(f"::group::{PRODUCT}")
session = HTMLSession()
r = session.get(URL)
r.html.render(sleep=1, scrolldown=3)

versions = {}
for version_block in r.html.find('.versions-list'):
    version = version_block.find('a.product-versions', first=True).attrs['data-version']
    date_text = version_block.find('.release-date', first=True).text
    date = dates.parse_date(date_text).strftime('%Y-%m-%d')
    print(f"{version}: {date}")
    versions[version] = date

endoflife.write_releases(PRODUCT, versions)
print("::endgroup::")
