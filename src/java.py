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

PRODUCT = "java"
URL = "https://www.java.com/releases/"


def fetch_releases(releases):
    session = HTMLSession()
    r = session.get('https://www.java.com/releases/')
    r.html.render(sleep=1, scrolldown=3)

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


print(f"::group::{PRODUCT}")
releases = {}
fetch_releases(releases)
releases.pop('1.0_alpha') # that's the only version we do not want, regex not needed
endoflife.write_releases(PRODUCT, dict(
    # sort by date then version (desc)
    sorted(releases.items(), key=lambda x: (x[1], x[0]), reverse=True)
))
print("::endgroup::")
