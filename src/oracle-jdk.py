from requests_html import HTMLSession
from common import endoflife

"""Fetch Java versions with their dates from https://www.java.com/releases/.

This script is using requests-html (https://requests-html.kennethreitz.org/)
because https://www.java.com/releases/ needs JavaScript to render correctly.

requests-html is using pyppeteer internally for executing javascript. And
pyppeteer is relying on Chromium, which is automatically downloaded  in
~/.local/share/pyppeteer by the library. This path can be overridden by
declaring a PYPPETEER_HOME environment variable. Unfortunately exporting this
variable in the python script does not work, so it has to be done before this
script execution.
"""

PRODUCT = "oracle-jdk"
URL = "https://www.java.com/releases/"


def fetch_releases():
    session = HTMLSession()
    r = session.get('https://www.java.com/releases/')
    r.html.render(sleep=1, scrolldown=3)

    releases = {}
    previous_date = None
    for row in r.html.find('#released tr'):
        version_cell = row.find('td.anchor', first=True)

        if version_cell:
            version = version_cell.attrs['id']
            date = row.find('td')[1].text
            date = previous_date if not date else date
            print(f"{version}: {date}")
            releases[version] = date
            previous_date = date

    return releases


print(f"::group::{PRODUCT}")
all_versions = fetch_releases()
all_versions.pop('1.0_alpha')  # only version we don't want, regex not needed
endoflife.write_releases(PRODUCT, all_versions)
print("::endgroup::")
