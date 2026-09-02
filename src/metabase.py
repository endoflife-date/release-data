import logging

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetch Metabase release cycles from a version-info feed.

Metabase publishes the data behind https://www.metabase.com/version-support as JSON:

- https://static.metabase.com/version-info.json for the open source edition (versions v0.x),
- https://static.metabase.com/version-info-ee.json for the enterprise edition (versions v1.x).

Only the major_version_support array is read, which holds one entry per supported major version:

    {"major": 63, "released": "2026-07-07", "lts": false, "eol": "2026-11-01"}

Both editions share the major version and are released on the same day, so both feeds report the
same dates. The release cycle name is rendered from the major version using the config's template,
which defaults to the major version alone. Use `template: "0.{{major}}"` to prefix the cycle names
with the license digit that Metabase puts in front of every version.

The feeds also list individual versions, but with three components only (v0.63.16), while Metabase
itself and its container images report four (v0.63.16.1). Versions are therefore left to another
method, such as `git` on the tags of https://github.com/metabase/metabase.git.
"""

EOL_FIELD = "eol"
LTS_FIELD = "lts"
MAJOR_FIELD = "major"
MAJOR_VERSIONS_FIELD = "major_version_support"
RELEASE_DATE_FIELD = "released"


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        version_info = http.fetch_json(config.url)

        for major_version in version_info.get(MAJOR_VERSIONS_FIELD, []):
            major = major_version.get(MAJOR_FIELD)
            if not major:
                logging.info(f"skipping {major_version}: no {MAJOR_FIELD} field")
                continue

            release = product_data.get_release(config.version_template.render(major=major))

            if release_date := major_version.get(RELEASE_DATE_FIELD):
                release.set_release_date(dates.parse_date(release_date))

            if eol := major_version.get(EOL_FIELD):
                release.set_eol(dates.parse_date(eol))

            # Only a set flag is reported, as endoflife.date omits the field for non-LTS cycles.
            if major_version.get(LTS_FIELD):
                release.set_field(LTS_FIELD, True)
