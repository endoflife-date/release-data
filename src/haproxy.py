import re

from common import dates, http
from common.releasedata import ProductData, config_from_argv

CYCLE_PATTERN = re.compile(r"^(\d+\.\d+)/$")
DATE_AND_VERSION_PATTERN = re.compile(r"^(\d{4})/(\d{2})/(\d{2})\s+:\s+(\d+\.\d+\.\d.?)$")  # https://regex101.com/r/1JCnFC/1

config = config_from_argv()
with ProductData(config.product) as product_data:
    # First, get all minor releases from the download page
    download_html = http.fetch_html(config.url)
    minor_versions = []
    for link in download_html.select("a"):
        minor_version_match = CYCLE_PATTERN.match(link.attrs["href"])
        if not minor_version_match:
            continue

        minor_version = minor_version_match.groups()[0]
        if minor_version != "1.0":  # No changelog in https://www.haproxy.org/download/1.0/src
            minor_versions.append(minor_version)

    # Then, fetches all versions from each changelog
    changelog_urls = [f"{config.url}{minor_version}/src/CHANGELOG" for minor_version in minor_versions]
    for changelog in http.fetch_urls(changelog_urls):
        for line in changelog.text.split('\n'):
            date_and_version_match = DATE_AND_VERSION_PATTERN.match(line)
            if date_and_version_match:
                year, month, day, version = date_and_version_match.groups()
                product_data.declare_version(version, dates.date(int(year), int(month), int(day)))
