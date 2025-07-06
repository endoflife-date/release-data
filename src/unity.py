from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches the Unity LTS releases from the Unity website. Non-LTS releases are not listed there, so this automation
is only partial.

This script is cumulative, only the first page is fetched (e.g. the first ten versions). This is because:
- it is too long to fetch all (at least 30s, usually more than a minute),
- this generates too many requests to the unity.com servers,
- fetching multiple pages in parallel is raising a lot of errors and makes the overall process slower (this was tested
  during https://github.com/endoflife-date/release-data/pull/194),
- and anyway oldest versions are never updated.

Note that it was assumed that:
- the script is ran regularly enough to keep the versions up to date (once a day or week looks enough),
- there is never more than 10 new LTS versions at a time.

The script will need to be updated if someday those conditions are not met."""

config = config_from_argv()
with ProductData(config.product) as product_data:
    html = http.fetch_html(config.url)

    for release in html.find_all('div', class_='component-releases-item__show__inner-header'):
        version = release.find('h4').find('span').text
        date = dates.parse_datetime(release.find('time').attrs['datetime'])
        product_data.declare_version(version, date)
