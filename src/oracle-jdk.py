from common import dates, endoflife
from requests_html import HTMLSession

"""Fetch Java versions from https://www.java.com/releases/.

This script is using requests-html because the page needs JavaScript to render correctly."""

product = endoflife.Product("oracle-jdk")
print(f"::group::{product.name}")
r = HTMLSession().get('https://www.java.com/releases/')
r.html.render(sleep=1, scrolldown=3)

previous_date = None
for row in r.html.find('#released tr'):
    version_cell = row.find('td.anchor', first=True)
    if version_cell:
        version = version_cell.attrs['id']
        date_str = row.find('td')[1].text
        date = dates.parse_date(date_str) if date_str else previous_date
        product.declare_version(version, date)
        previous_date = date

product.remove_version('1.0_alpha')  # the only version we don't want, a regex is not needed
product.write()
print("::endgroup::")
