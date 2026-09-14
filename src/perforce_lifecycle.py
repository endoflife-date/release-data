import logging
import re
from datetime import datetime

from bs4 import BeautifulSoup

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetch general availability and end-of-life dates from a Perforce lifecycle article.

The lifecycle articles on portal.perforce.com are a Salesforce Experience Cloud site that renders
client-side, so a plain request returns nothing but the loading shell. The public knowledge endpoint
serves the article body without authentication instead:

    https://portal.perforce.com/services/data/v59.0/support/knowledgeArticles/<urlName>

Salesforce rejects that call unless a language is named in an Accept-Language header, and offers no
query parameter to do it instead, so the request carries one.

Pass the URL as the method value. The article body is in the Information__c layout item and holds
one table per product, each introduced by a heading such as "P4 Server (P4D)" or "P4 Code Review".
The `selector` argument names the heading to read, so a single article can feed several products:
the Helix Core article carries P4D, P4Broker and P4Proxy in one page, with identical dates, since
they are released as one train.

Perforce documents three milestones. From general availability to End of Maintenance a release gets
bug fixes and security updates. Between End of Maintenance and End of Maintenance and Support those
fixes are sold separately while technical support continues normally, and after that support drops
to basic troubleshooting. eoas is therefore mapped to EOM and eol to EOMS.

Only the release cycles are set here. Patch versions are not in these tables, so they come from
another method: perforce_relnotes for the server family, docker_hub for Swarm.
"""

# Cells read "P4D 2025.2", "P4Proxy 2025.2" or "P4 Code Review 2026.3".
CYCLE_PATTERN = re.compile(r"(\d{4}\.\d+)\s*$")

# Cells read "18-Nov-25", "7-Nov-24" or "02-Apr-25".
DATE_FORMATS = frozenset(["%d-%b-%y", "%d-%b-%Y"])

HEADING_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")

ARTICLE_HEADERS = {"Accept-Language": "en-US"}


def _find_table(soup: BeautifulSoup, selector: str) -> BeautifulSoup | None:
    """Return the table introduced by the heading matching the selector."""
    for heading in soup.find_all(HEADING_TAGS):
        if heading.get_text(strip=True) == selector:
            return heading.find_next("table")
    return None


def _parse_date(text: str) -> datetime | None:
    """Parse a lifecycle date, or return None for the placeholders Perforce uses instead."""
    if not text:
        return None

    try:
        return dates.parse_date(text, DATE_FORMATS)
    except ValueError:
        # Cells such as "Current Version (under maintenance)" stand in for a date that has not been
        # decided yet, and are left to the product file.
        logging.info(f"ignoring '{text}': not a date")
        return None


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    selector = config.data.get("selector")
    if not selector:
        message = f"{config} is missing the selector argument naming the table to read"
        raise ValueError(message)

    article = http.fetch_json(config.url, extra_headers=ARTICLE_HEADERS)
    body = next((item["value"] for item in article["layoutItems"] if item["name"] == "Information__c"), None)
    if not body:
        message = f"{config} returned an article with no body"
        raise ValueError(message)

    table = _find_table(BeautifulSoup(body, features="html5lib"), selector)
    if not table:
        message = f"{config} has no table under a '{selector}' heading"
        raise ValueError(message)

    with ProductData(config.product) as product_data:
        for row in table.find_all("tr"):
            cells = [cell.get_text(strip=True) for cell in row.find_all("td")]
            if len(cells) < 2:
                continue

            cycle_match = CYCLE_PATTERN.search(cells[0])
            if not cycle_match:
                continue  # The header row, which names the columns rather than a version.

            release = product_data.get_release(cycle_match.group(1))

            if general_availability := _parse_date(cells[1]):
                release.set_release_date(general_availability)

            if end_of_maintenance := _parse_date(cells[2] if len(cells) > 2 else ""):
                release.set_eoas(end_of_maintenance)

            if end_of_support := _parse_date(cells[3] if len(cells) > 3 else ""):
                release.set_eol(end_of_support)
