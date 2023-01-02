import json

from requests_html import HTMLSession

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
    for row in r.html.find('#released tr.shade'):
        version = row.find('td.anchor', first=True).attrs['id']
        date = row.find('td')[1].text
        date = previous_date if not date else date
        print(f"{version}: {date}")
        releases[version] = date
        previous_date = date


def main():
    print(f"::group::{PRODUCT}")
    releases = {}
    fetch_releases(releases)
    print("::endgroup::")

    with open(f"releases/{PRODUCT}.json", "w") as f:
        f.write(json.dumps(
            # sort by date desc
            dict(sorted(releases.items(), key=lambda e: e[1], reverse=True)),
            indent=2))


if __name__ == '__main__':
    main()
