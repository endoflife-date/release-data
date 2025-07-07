import logging

from bs4 import BeautifulSoup
from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches versions from release notes of each minor version on docs.couchbase.com."""

config = config_from_argv()
with ProductData(config.product) as product_data:
    html = http.fetch_html(f"{config.url}/current/install/install-intro.html")

    minor_versions = [options.attrs["value"] for options in html.find(class_="version_list").find_all("option")]
    minor_version_urls = [f"{config.url}/{minor}/release-notes/relnotes.html" for minor in minor_versions]

    for minor_version in http.fetch_urls(minor_version_urls):
        minor_version_soup = BeautifulSoup(minor_version.text, features="html5lib")

        for title in minor_version_soup.find_all("h2"):
            match = config.first_match(title.get_text().strip())
            if not match:
                logging.info(f"Skipping {title}, does not match any regex")
                continue

            version = match["version"]
            version = f"{version}.0" if len(version.split(".")) == 2 else version
            date = dates.parse_month_year_date(match['date'])
            product_data.declare_version(version, date)
