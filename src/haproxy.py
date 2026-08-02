import re

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

CYCLE_PATTERN = re.compile(r"^(\d+\.\d+)/$")
DATE_AND_VERSION_PATTERN = re.compile(r"^(\d{4})/(\d{2})/(\d{2})\s+:\s+(\d+\.\d+\.\d.?)$")  # https://regex101.com/r/1JCnFC/1

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        # First, get all minor releases from the download page
        download_html = http.fetch_html(config.url)
        minor_versions = [
            m.group(1)
            for link in download_html.select("a")
            if (m := CYCLE_PATTERN.match(link.attrs["href"])) and m.group(1) != "1.0"
        ]  # No changelog in https://www.haproxy.org/download/1.0/src

        # Then, fetches all versions from each changelog
        changelog_urls = [f"{config.url}{minor_version}/src/CHANGELOG" for minor_version in minor_versions]
        for changelog in http.fetch_urls(changelog_urls):
            for line in changelog.text.split('\n'):
                date_and_version_match = DATE_AND_VERSION_PATTERN.match(line)
                if date_and_version_match:
                    year, month, day, version = date_and_version_match.groups()
                    product_data.declare_version(version, dates.date(int(year), int(month), int(day)))
