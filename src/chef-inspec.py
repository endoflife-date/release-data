from bs4 import BeautifulSoup
from common import dates, github, http, releasedata

"""Fetch released versions from docs.chef.io and retrieve their date from GitHub.
docs.chef.io needs to be scraped because not all tagged versions are actually released.

More context on https://github.com/endoflife-date/endoflife.date/pull/4425#discussion_r1447932411.
"""

with releasedata.ProductData("chef-inspec") as product_data:
    rn_response = http.fetch_url("https://docs.chef.io/release_notes_inspec/")
    rn_soup = BeautifulSoup(rn_response.text, features="html5lib")
    released_versions = [h2.get('id') for h2 in rn_soup.find_all('h2', id=True) if h2.get('id')]

    for release in github.fetch_releases("inspec/inspec"):
        sanitized_version = release.tag_name.replace("v", "")
        if sanitized_version in released_versions:
            date = dates.parse_datetime(release.published_at)
            product_data.declare_version(sanitized_version, date)
