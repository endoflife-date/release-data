import logging
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData, ProductVersion

"""Fetch TestRail Server versions and support dates.

TestRail publishes no version feed, so this script combines two sources.

Release notes live in a Zendesk help center. Its public API is readable even though
support.testrail.com answers 403 to non-browser clients on the HTML pages:

    https://support.testrail.com/api/v2/help_center/en-us/sections/<section>/articles.json

Article titles carry the version and the build number, either as "TestRail 10.7.1 Default (1003)"
or as "TestRail 10.7.1.1003 Server", both meaning 10.7.1.1003.

That alone would overstate what self-hosted users can install, because TestRail ships every version
to Cloud but only some of them as a Server package. The vendor's supported-versions table is no help
here, as it lists Cloud-only builds such as 9.7.2.1003 and 9.5.3.1058. A build is therefore taken as
a Server package when any of these holds:

1. the Server release notes section carries an article for it;
2. the product file already names it as a release cycle's latest;
3. the distribution archive still serves it, that is

       https://secure.testrail.com/downloads/testrail/testrail-<version>-<ioncube>.zip

   answers 200 to a HEAD request. The <ioncube> suffix names the ionCube loader the package is
   built against and changes every few releases, so candidates are tried newest-first.

The archive is the broadest of the three but it is not proof of absence, only of presence. TestRail
moved these downloads to object storage during 2025 and some packages stopped resolving even though
they had shipped and are still installed in the wild; 9.4.1.1001 and 9.5.1.1042 are two of them.
That is what the first two signals are for, and in particular why a version the product file already
documents is kept whatever the archive answers today: without that, delisting the newest package of
a cycle would silently walk its latest backwards.

Do not read release dates from that archive: its Last-Modified headers reflect a bulk migration to
object storage rather than the release, and most files report the same August 2025 timestamp.

Release dates are taken from the first source that knows the build, in this order:

1. the GA date column of the supported-versions table, which is the vendor's own statement;
2. a "Server release date:" line at the top of the article body;
3. a "Cloud release date:" line at the top of the article body;
4. the creation date of the article announcing the build on the Cloud release track;
5. the creation date of the article announcing the Server package.

The last one comes last because those articles are drafted well ahead of the release: the article
for 10.7.1.1003 was created on 2026-07-27, weeks before the build itself was produced. It is still
needed, because a few builds such as 9.5.1.1126 only ever got a Server article.

Only versions from 8.0 onwards are discovered. Release notes for older versions name no build number
in their titles, so no distribution archive can be addressed for them, and those cycles are left to
the product file.

Support windows follow https://support.testrail.com/hc/en-us/articles/14334287387796 : one year of
Active Support, then one year of Limited Support, counted from each build's general availability.
Because the window is per build, a cycle stays supported for two years after its last build, so eoas
and eol are derived from the newest build known for the cycle. Release dates are left alone, as the
cycles this script cannot see would otherwise be the only ones missing them.
"""

KB_API = "https://support.testrail.com/api/v2/help_center/en-us"

# Release notes for the current Cloud track, and everything archived from 1.0 up to 8.1. Creation
# dates in these two sections track the announcement closely.
CLOUD_SECTIONS = ("10423156702740", "18099145794196")
# Release notes for the Server and Docker packages, drafted ahead of the release.
SERVER_SECTION = "10423185248404"

# "TestRail Server supported versions", holding the vendor's GA dates.
SUPPORTED_VERSIONS_ARTICLE = "14334287387796"

# "TestRail 10.7.1.1003 Server", "TestRail 10.7.1.1003 Docker Image".
DOTTED_BUILD_PATTERN = re.compile(r"^TestRail (\d+\.\d+\.\d+\.\d+)(?:\s|$)")
# "TestRail 10.7.1 Default (1003)", "TestRail 8.1.0 Default (6185)".
PARENTHESIZED_BUILD_PATTERN = re.compile(r"^TestRail (\d+\.\d+\.\d+)\s+(?:\w+\s+)*\((\d+)\)")
# A full version, as used in the supported-versions table.
FULL_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+\.\d+$")

TAG_PATTERN = re.compile(r"<[^>]+>")
RELEASE_DATE_PATTERN = re.compile(
    r"(?P<track>Cloud|Server(?:\s*&(?:amp;)?\s*Docker)?)\s+release date\s*:\s*(?P<date>[^<\n]{4,40})",
    re.IGNORECASE)

# ionCube loader suffixes, newest first.
IONCUBE_SUFFIXES = ("ion81", "ion72", "ion71", "ion70", "ion53", "ion51")

# Lowest version each loader was used for, newest first.
IONCUBE_BY_VERSION = (
    ((8, 0), ("ion81",)),
    ((6, 5), ("ion72",)),
    ((5, 7), ("ion71",)),
    ((5, 4), ("ion70", "ion53", "ion51")),
    ((3, 1), ("ion53", "ion51")),
)

# Date sources, most trustworthy first. See the module docstring.
FROM_SUPPORTED_VERSIONS_TABLE = 0
FROM_SERVER_DATE_LINE = 1
FROM_CLOUD_DATE_LINE = 2
FROM_CLOUD_ARTICLE = 3
FROM_SERVER_ARTICLE = 4

ACTIVE_SUPPORT_YEARS = 1
LIMITED_SUPPORT_YEARS = 2

MAX_WORKERS = 8
TIMEOUT = 30


def _version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def _cycle_of(version: str) -> str:
    major, minor = version.split(".")[:2]
    return f"{major}.{minor}"


def _plus_years(moment: datetime, years: int) -> datetime:
    try:
        return moment.replace(year=moment.year + years)
    except ValueError:  # 29 February on a non-leap year.
        return moment.replace(year=moment.year + years, day=28)


def _ioncube_candidates(version: str) -> tuple[str, ...]:
    key = _version_key(version)[:2]
    for lowest, suffixes in IONCUBE_BY_VERSION:
        if key >= lowest:
            return suffixes + tuple(s for s in IONCUBE_SUFFIXES if s not in suffixes)
    return ("ion51", *(s for s in IONCUBE_SUFFIXES if s != "ion51"))


def _parse_version(title: str) -> str | None:
    """Return the four-part version a release notes article is about, if it names a build."""
    dotted = DOTTED_BUILD_PATTERN.match(title)
    if dotted:
        return dotted.group(1)

    parenthesized = PARENTHESIZED_BUILD_PATTERN.match(title)
    if parenthesized:
        return f"{parenthesized.group(1)}.{parenthesized.group(2)}"

    # Titles such as "TestRail 7.5 Default" and "TestRail Beta 1.0.4" name no build, so no
    # distribution archive can be addressed for them.
    return None


def _parse_date_lines(body: str) -> dict[int, str]:
    """Return the release date lines at the top of an article body, keyed by their source."""
    found = {}
    for match in RELEASE_DATE_PATTERN.finditer(TAG_PATTERN.sub("\n", body or "")):
        is_server = match.group("track").lower().startswith("server")
        source = FROM_SERVER_DATE_LINE if is_server else FROM_CLOUD_DATE_LINE
        found.setdefault(source, match.group("date").strip())
    return found


class _Candidate:
    """A build seen in the release notes, with the best release date found for it so far."""

    def __init__(self) -> None:
        self.source = None
        self.date = None

    def offer(self, source: int, date: datetime) -> None:
        if self.source is None or source < self.source:
            self.source, self.date = source, date


def _fetch_supported_versions() -> dict[str, datetime]:
    """Read the GA date of every build listed in the supported-versions table."""
    article = http.fetch_json(f"{KB_API}/articles/{SUPPORTED_VERSIONS_ARTICLE}.json")["article"]
    soup = BeautifulSoup(article["body"], features="html5lib")

    ga_dates = {}
    for row in soup.find_all("tr"):
        cells = [cell.get_text(strip=True) for cell in row.find_all("td")]
        if len(cells) < 2 or not FULL_VERSION_PATTERN.match(cells[0]):
            continue

        try:
            ga_dates[cells[0]] = dates.parse_date(cells[1])
        except ValueError:
            logging.warning(f"ignoring unparseable GA date '{cells[1]}' for {cells[0]}")

    logging.info(f"found {len(ga_dates)} builds in the supported-versions table")
    return ga_dates


def _fetch_announced_builds() -> tuple[dict[str, datetime], set[str]]:
    """Return the release date of every announced build, and which of them shipped for Server.

    A build is known to have shipped for Server when the Server release notes section carries an
    article for it. That is a positive signal only: most Server packages never got one.
    """
    candidates: dict[str, _Candidate] = {}
    documented_for_server: set[str] = set()

    for version, ga_date in _fetch_supported_versions().items():
        candidates.setdefault(version, _Candidate()).offer(FROM_SUPPORTED_VERSIONS_TABLE, ga_date)

    for section in (*CLOUD_SECTIONS, SERVER_SECTION):
        article_source = FROM_SERVER_ARTICLE if section == SERVER_SECTION else FROM_CLOUD_ARTICLE
        url = f"{KB_API}/sections/{section}/articles.json?per_page=100"

        while url:
            page = http.fetch_json(url)

            for article in page.get("articles", []):
                version = _parse_version(article["title"])
                if not version:
                    continue

                if section == SERVER_SECTION:
                    documented_for_server.add(version)

                candidate = candidates.setdefault(version, _Candidate())
                for source, text in _parse_date_lines(article.get("body")).items():
                    try:
                        candidate.offer(source, dates.parse_date(text))
                    except ValueError:
                        logging.warning(f"ignoring unparseable date '{text}' in '{article['title']}'")

                if article.get("created_at"):
                    candidate.offer(article_source, dates.parse_datetime(article["created_at"]))

            url = page.get("next_page")

    announced = {version: c.date for version, c in candidates.items() if c.date}
    logging.info(f"found {len(announced)} announced builds, {len(documented_for_server)} of them "
                 f"documented as Server packages")
    return announced, documented_for_server


def _is_published_for_server(base_url: str, version: str) -> bool:
    """Tell whether a build was distributed as a Server package."""
    for suffix in _ioncube_candidates(version):
        url = f"{base_url}/testrail-{version}-{suffix}.zip"
        try:
            response = requests.head(url, allow_redirects=True, timeout=TIMEOUT,
                                     headers={"User-Agent": http.ENDOFLIFE_BOT_USER_AGENT})
        except requests.RequestException as error:
            logging.warning(f"could not check {url}: {error}")
            continue

        if response.status_code == requests.codes.ok:
            logging.debug(f"{version} shipped for Server as {url}")
            return True

    logging.debug(f"{version} never shipped for Server")
    return False


def _documented_latest_versions(product: ProductFrontmatter) -> set[str]:
    """Return the versions the product file already names as a cycle's latest."""
    return {str(release["latest"]) for release in product.get_releases() or [] if release.get("latest")}


def _documented_latest_dates(product: ProductFrontmatter) -> dict[str, datetime]:
    """Return the latest release date the product file documents for each cycle."""
    documented = {}
    for release in product.get_releases() or []:
        latest_release_date = release.get("latestReleaseDate")
        if latest_release_date:
            documented[str(release.get("releaseCycle"))] = dates.to_datetime(latest_release_date)
    return documented


def _update_support_dates(product_data: ProductData, documented: dict[str, datetime]) -> None:
    """Derive each cycle's support dates from the newest build known for it."""
    versions_by_cycle: dict[str, list[ProductVersion]] = {}
    for version in product_data.versions.values():
        versions_by_cycle.setdefault(_cycle_of(version.name()), []).append(version)

    for cycle, versions in versions_by_cycle.items():
        # A Cloud-only last build of the cycle is deliberately ignored, as it extends support for
        # nobody running the self-hosted edition.
        last = max(versions, key=lambda v: (v.date(), _version_key(v.name())))

        # Builds are only discovered through the release notes, which name no build number for some
        # of the packages that were actually distributed, such as 5.6.0.3865 and 6.7.2.1043. Where
        # the product file documents a later build than the release notes know about, its dates are
        # the better ones and shortening the window from here would lose them.
        if cycle in documented and documented[cycle] > last.date():
            logging.info(f"leaving {cycle} alone: the product file documents a build released on "
                         f"{documented[cycle]:%Y-%m-%d}, later than {last.name()} ({last.date():%Y-%m-%d})")
            continue

        logging.debug(f"cycle {cycle} support runs from its last Server build {last.name()}")
        release = product_data.get_release(cycle)
        release.set_eoas(_plus_years(last.date(), ACTIVE_SUPPORT_YEARS))
        release.set_eol(_plus_years(last.date(), LIMITED_SUPPORT_YEARS))


def update(product: ProductFrontmatter, config: AutoConfig) -> None:
    base_url = config.url.rstrip("/")
    announced, documented_for_server = _fetch_announced_builds()
    documented = _documented_latest_dates(product)

    # A build the product file already names as a cycle's latest shipped for Server, whatever the
    # archive says today, so it is never dropped. Otherwise delisting the newest package of a cycle
    # would silently walk its latest backwards.
    known_for_server = documented_for_server | _documented_latest_versions(product)

    with ProductData(config.product) as product_data:
        for version in sorted(known_for_server & set(announced), key=_version_key):
            product_data.declare_version(version, announced[version])

        # Release data is rebuilt from scratch on every run, so everything else is checked against
        # the archive. One HEAD request is enough for all but the handful of versions published
        # against more than one ionCube loader.
        builds = sorted(set(announced) - known_for_server, key=_version_key)
        logging.info(f"checking {len(builds)} builds against the distribution archive")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            published = executor.map(lambda v: _is_published_for_server(base_url, v), builds)
            for version, is_published in zip(builds, published, strict=True):
                if is_published:
                    product_data.declare_version(version, announced[version])

        _update_support_dates(product_data, documented)
