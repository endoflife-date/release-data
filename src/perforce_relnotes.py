import logging
import re

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetch Perforce patch versions from the plain text release notes.

Perforce publishes one release notes file covering p4d, p4, p4p and p4broker together, because they
are built and shipped as one train:

    https://help.perforce.com/helix-core/release-notes/current/relnotes.txt

Every release and patch is introduced by a heading carrying the full version and the date:

    Bugs fixed in 2025.2 Patch 2 (2025.2/2907753) (2026/03/09)

Versions are declared as Perforce writes them, release and change level separated by a slash, which
is what `p4d -V` reports and what the patch is referred to by.

Release cycle dates are left to perforce_lifecycle. The two disagree on purpose: the date in a
heading is when the build was cut, while the general availability Perforce anchors its end-of-life
dates to falls about a week later.

Note that the file only keeps the recent history. Headings for the first release of a cycle drop out
once it is old enough, so the earliest heading for a cycle is not necessarily its first release.

The `regex` and `regex_exclude` arguments are not honoured. Only stable releases reach this file, so
there is nothing to filter, and the default version regex would in any case reject every version
here because of the slash between the release and the change level.
"""

RELEASE_PATTERN = re.compile(
    r"^(?:Bugs fixed|Major new functionality|Minor new functionality|New functionality)"
    r" in \d{4}\.\d+(?: Patch \d+)?\s*"
    r"\((?P<version>\d{4}\.\d+/\d+)\)\s*"
    r"\((?P<date>\d{4}/\d{2}/\d{2})\)",
    re.MULTILINE)


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    relnotes = http.fetch_url(config.url).text

    with ProductData(config.product) as product_data:
        for match in RELEASE_PATTERN.finditer(relnotes):
            product_data.declare_version(match.group("version"), dates.parse_date(match.group("date")))

        if not product_data.versions:
            message = f"{config} found no version in the release notes"
            raise ValueError(message)

        logging.info(f"found {len(product_data.versions)} versions in the release notes")
