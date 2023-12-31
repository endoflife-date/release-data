from common import dates, endoflife
from requests_html import HTMLSession

"""Fetches Jira versions from www.atlassian.com.

Note that requests_html is used because JavaScript is needed to render the page."""

product = endoflife.Product("jira")
r = HTMLSession().get("https://www.atlassian.com/software/jira/update")
r.html.render(sleep=1, scrolldown=3)

for version_block in r.html.find('.versions-list'):
    version = version_block.find('a.product-versions', first=True).attrs['data-version']
    date = dates.parse_date(version_block.find('.release-date', first=True).text)
    product.declare_version(version, date)

product.write()
