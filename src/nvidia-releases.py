import logging
import re
from urllib.parse import urlparse

from src.common import http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

WINDOWS_VERSION_REGEX = re.compile(r'Version .+\(Linux\)/(?P<version>.+)\(Windows\)')

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        data = http.fetch_json(config.url)
        for release_name in data:
            release_data = data[release_name]
            latest_version_data = release_data.get('driver_info')[0]
            latest = latest_version_data['release_version']
            latest_release_data = latest_version_data['release_date']
            link = latest_version_data['release_notes']

            # Only linux releases are documented in the JSON document.
            release = product_data.get_release(f"r{release_name}-linux")
            release.set_field('latest', latest)
            release.set_field('latestReleaseDate', latest_release_data)
            release.set_field('link', link)

            # Windows releases are documented in the release notes.
            if urlparse(link).hostname != 'docs.nvidia.com':
                logging.debug("Skipping windows release %s, link %s is not from docs.nvidia.com", release_name, link)
                continue

            release_note_html = http.fetch_html(link)
            release_note_title = release_note_html.select_one('h2.title.topictitle1')
            if not release_note_title:
                logging.warning("Skipping windows release %s, could not find release note title in '%s'", release_name, link)
                continue

            windows_version_match = WINDOWS_VERSION_REGEX.search(release_note_title.text)
            if not windows_version_match:
                logging.warning("Skipping windows release %s, could not find version in release note title '%s'", release_name, release_note_title.text)
                continue

            release = product_data.get_release(f"r{release_name}-windows")
            release.set_field('latest', windows_version_match.group('version'))
            release.set_field('latestReleaseDate', latest_release_data)
            release.set_field('link', link)
