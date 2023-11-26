from common import dates
from common import endoflife
from requests_html import HTMLSession

URL = "https://jfrog.com/help/r/jfrog-release-information/artifactory-end-of-life"
PRODUCT = "artifactory"


def parse_date(date_str):
    date_str = date_str.replace("Sept", "Sep").replace("_", "-")
    return dates.parse_date(date_str).strftime("%Y-%m-%d")


def fetch_releases():
    result = {}

    session = HTMLSession()
    r = session.get(URL)
    r.html.render(sleep=2, scrolldown=5)

    for row in r.html.find('.informaltable tbody tr'):
        cells = row.find("td")
        if len(cells) >= 2:
            version = cells[0].text.strip()
            date_text = cells[1].text.strip()
            if date_text:
                date = parse_date(date_text)
                result[version] = date
                print(f"{version}: {date}")

    # 7.29.9 release date is wrong on https://jfrog.com/help/r/jfrog-release-information/artifactory-end-of-life.
    # Sent a mail to jfrog-help-center-feedback@jfrog.com to fix it, but in the meantime...
    result['7.29.9'] = '2022-01-11'
    return result


print(f"::group::{PRODUCT}")
versions = fetch_releases()
endoflife.write_releases(PRODUCT, versions)
print("::endgroup::")
