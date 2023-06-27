from common import endoflife
from datetime import datetime
from requests_html import HTMLSession

URL = "https://jfrog.com/help/r/jfrog-release-information/artifactory-end-of-life"
PRODUCT = "artifactory"


def parse_date(text):
    text = text.replace("Sept", "Sep").replace("_", "-")
    date_formats = ['%d-%b-%Y', '%d-%B-%Y']

    for date_format in date_formats:
        try:
            return datetime.strptime(text, date_format).strftime("%Y-%m-%d")
        except ValueError:
            pass

    raise ValueError("Cannot parse '" + text + "' with formats " + str(date_formats))


def fetch_releases():
    result = {}

    session = HTMLSession()
    r = session.get(URL)
    r.html.render(sleep=1, scrolldown=3)

    for row in r.html.find('.informaltable tbody tr'):
        cells = row.find("td")
        if len(cells) >= 2:
            version = cells[0].text.strip()
            date_text = cells[1].text.strip()
            if date_text:
                date = parse_date(date_text)
                result[version] = date
                print(f"{version}: {date}")

    return result


print(f"::group::{PRODUCT}")
releases = fetch_releases()
endoflife.write_releases(PRODUCT, dict(
    # sort by date then version (desc)
    sorted(releases.items(), key=lambda x: (x[1], x[0]), reverse=True)
))
print("::endgroup::")
