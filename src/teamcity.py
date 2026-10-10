import logging
import re
from datetime import datetime

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetch TeamCity versions and support dates from the JetBrains releases feed.

The download page at https://www.jetbrains.com/teamcity/download/other/ is rendered client-side, but
the feed behind it is plain JSON and lists every release with its build number and date:

    https://data.services.jetbrains.com/products/releases?code=TC&latest=false&type=release

Per https://www.jetbrains.com/help/teamcity/teamcity-release-cycle.html , JetBrains ships two major
versions a year. A major version receives bugfix updates until End of Sale, which is when the next
major version is released, and reaches End of Support when the one after that is released. So eoas
and eol are the release dates of the following two major versions, and the two newest cycles are
left alone because the versions that would date them do not exist yet.

The feed does not list the 10.0 release itself, only 10.0.1 onwards, so taking the earliest version
in a cycle as its release date would be wrong there. A cycle is dated from the feed only when the
feed actually contains its base version; otherwise the date already in the product file is kept.

Version strings are used exactly as the feed reports them. That matters for 2022.04 through 2025.11,
where the second component is the release month and its leading zero is part of the name.
"""

CYCLE_PATTERN = re.compile(r"^(\d+\.\d+)")


def _cycle_of(version: str) -> str:
    return CYCLE_PATTERN.match(version).group(1)


def _documented_release_dates(product: ProductFrontmatter) -> dict[str, datetime]:
    """Return the release date the product file documents for each cycle."""
    documented = {}
    for release in product.get_releases() or []:
        if release_date := release.get("releaseDate"):
            documented[str(release.get("releaseCycle"))] = dates.to_datetime(release_date)
    return documented


def _releases_by_cycle(feed: dict, config: AutoConfig) -> dict[str, list[tuple[str, datetime]]]:
    """Group every release in the feed by the cycle it belongs to."""
    by_cycle = {}
    for releases in feed.values():
        for release in releases:
            version = release.get("version")
            date = release.get("date")
            if not version or not date or not CYCLE_PATTERN.match(version):
                logging.info(f"skipping {release}: no usable version or date")
                continue

            if config.is_excluded(version):
                continue

            by_cycle.setdefault(_cycle_of(version), []).append((version, dates.parse_date(date)))

    return by_cycle


def update(product: ProductFrontmatter, config: AutoConfig) -> None:
    by_cycle = _releases_by_cycle(http.fetch_json(config.url), config)
    documented = _documented_release_dates(product)

    with ProductData(config.product) as product_data:
        release_dates = {}

        for cycle, versions in by_cycle.items():
            for version, date in versions:
                product_data.declare_version(version, date)

            # The base version is the release the cycle is named after, and the only one whose date
            # can serve as the cycle's release date.
            base_version = next((date for version, date in versions if version == cycle), None)
            if base_version:
                product_data.get_release(cycle).set_release_date(base_version)
                release_dates[cycle] = base_version
            elif cycle in documented:
                logging.info(f"{cycle} is not in the feed, keeping its documented release date")
                release_dates[cycle] = documented[cycle]
            else:
                logging.warning(f"{cycle} has no release date: absent from both the feed and the product file")

        _update_support_dates(product_data, release_dates)


def _update_support_dates(product_data: ProductData, release_dates: dict[str, datetime]) -> None:
    """Date each cycle's End of Sale and End of Support from the two majors that follow it."""
    newest_first = sorted(release_dates.items(), key=lambda item: item[1], reverse=True)

    for position, (cycle, _) in enumerate(newest_first):
        # The two newest cycles cannot be dated: the releases that would end their support are still
        # unannounced.
        if position < 2:
            logging.debug(f"leaving {cycle} alone, nothing has superseded it yet")
            continue

        release = product_data.get_release(cycle)
        release.set_eoas(newest_first[position - 1][1])
        release.set_eol(newest_first[position - 2][1])
