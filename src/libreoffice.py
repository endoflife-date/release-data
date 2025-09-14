import logging

from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches LibreOffice versions from https://downloadarchive.documentfoundation.org/libreoffice/old/"""


def fetch_prereleases(url: str, text_to_match: str) -> list[str]:
    """Get all prereleases from the LibreOffice download page.
    Note that prereleases are version numbers without the patch number, e.g. "25.8.0" and not "25.8.0.1".
    See https://github.com/endoflife-date/release-data/issues/511."""
    prereleases_html = http.fetch_html(url)
    prereleases_paragraph = next(
        (p for p in prereleases_html.find_all("p")
         if text_to_match in p.get_text()),
        None,
    )

    if not prereleases_paragraph:
        message = "Could not find the prerelease paragraph on the LibreOffice download page"
        raise ValueError(message)

    prereleases = []
    for prerelease in prereleases_paragraph.find_next("ul").find_all("li"):
        prereleases.append(prerelease.get_text().strip())

    return prereleases


config = config_from_argv()
with ProductData(config.product) as product_data:
    prereleases_url = config.data.get("prereleases_url", "https://www.libreoffice.org/download/download-libreoffice/")
    prereleases_text = config.data.get("prereleases_text", "LibreOffice is available in the following prerelease versions:")
    prerelease_prefixes = fetch_prereleases(prereleases_url, prereleases_text)

    html = http.fetch_html(config.url)
    for table in html.find_all("table"):
        for row in table.find_all("tr")[1:]:
            cells = row.find_all("td")
            if len(cells) < 4:
                continue

            version_str = cells[1].get_text().strip()
            version_match = config.first_match(version_str)
            if not version_match:
                logging.warning(f"Skipping version {version_str} as it does not match any known version pattern")
                continue
            version = config.render(version_match)

            if any(prerelease_prefix in version for prerelease_prefix in prerelease_prefixes):
                logging.info(f"Skipping prerelease version {version}")
                continue

            date_str = cells[2].get_text().strip()
            date = dates.parse_datetime(date_str)

            product_data.declare_version(version, date)
