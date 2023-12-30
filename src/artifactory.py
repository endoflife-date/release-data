
from common import dates, endoflife
from requests_html import HTMLSession

"""Fetches Artifactory versions from https://jfrog.com, using requests_html because JavaScript is
needed to render the page."""

product = endoflife.Product("artifactory")
print(f"::group::{product.name}")
r = HTMLSession().get("https://jfrog.com/help/r/jfrog-release-information/artifactory-end-of-life")
r.html.render(sleep=2, scrolldown=5)

for row in r.html.find('.informaltable tbody tr'):
    cells = row.find("td")
    if len(cells) >= 2:
        version = cells[0].text.strip()
        if version:
            date_str = cells[1].text.strip().replace("_", "-").replace("Sept-", "Sep-")
            product.declare_version(version, dates.parse_date(date_str))

# 7.29.9 release date is wrong on https://jfrog.com/help/r/jfrog-release-information/artifactory-end-of-life.
# Sent a mail to jfrog-help-center-feedback@jfrog.com to fix it, but in the meantime...
product.replace_version('7.29.9', dates.date(2022, 1, 11))

product.write()
print("::endgroup::")
