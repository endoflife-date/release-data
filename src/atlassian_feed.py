import logging
import re

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetch versions from an Atlassian download feed.

Atlassian publishes the data behind its download pages as plain JSON, one file per product and
channel:

    https://my.atlassian.com/download/feeds/current/<product>.json
    https://my.atlassian.com/download/feeds/archived/<product>.json

Pass the current feed as the method value. The archived one is derived from it by swapping the
channel, and is where nearly all the history lives: for Mesh the current feed holds 6 entries and
the archived one 235.

Prefer this over atlassian_versions where both work. The feed needs no browser, it reaches back
much further than the download pages do, and it keeps working for products whose pages have stopped
listing versions altogether, which is what happened to FishEye and Crucible after Atlassian
discontinued them.

Entries are skipped when the feed marks them type EAP or the version itself is labelled as a
pre-release. Both checks are needed: the dedicated eap feeds are empty for some products while their
archived feed still carries EAP entries mixed in, which is the case for FishEye and Crucible.
"""

CURRENT_CHANNEL = "/current/"
ARCHIVED_CHANNEL = "/archived/"

PRERELEASE_PATTERN = re.compile(r"-(?:rc|beta|alpha|eap|m|milestone)\d*$", re.IGNORECASE)

# Feeds date releases as "08-Sep-2026".
DATE_FORMATS = frozenset(["%d-%b-%Y", "%d-%B-%Y"])


def _is_prerelease(entry: dict) -> bool:
    return (entry.get("type") or "").upper() == "EAP" or bool(PRERELEASE_PATTERN.search(entry.get("version", "")))


def _feed_urls(url: str) -> list[str]:
    if CURRENT_CHANNEL not in url:
        message = f"expecting a {CURRENT_CHANNEL.strip('/')} feed url, got {url}"
        raise ValueError(message)
    return [url, url.replace(CURRENT_CHANNEL, ARCHIVED_CHANNEL)]


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        skipped = 0

        for feed_url in _feed_urls(config.url):
            for entry in http.fetch_json(feed_url):
                version = entry.get("version")
                released = entry.get("released")
                if not version or not released:
                    continue

                if _is_prerelease(entry):
                    skipped += 1
                    continue

                if config.is_excluded(version):
                    continue

                try:
                    date = dates.parse_date(released, DATE_FORMATS)
                except ValueError:
                    logging.warning(f"ignoring '{released}' for {version}: not a date")
                    continue

                product_data.declare_version(version, date)

        if not product_data.versions:
            message = f"{config} found no version in the feed"
            raise ValueError(message)

        logging.info(f"declared {len(product_data.versions)} versions, skipped {skipped} pre-release builds")
