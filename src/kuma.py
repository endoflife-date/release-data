import logging

import yaml
from common import dates, http, releasedata

"""Fetch version data for Kuma from https://raw.githubusercontent.com/kumahq/kuma/master/versions.yml.
"""

RELEASE_FIELD = 'release'
RELEASE_DATE_FIELD = 'releaseDate'
EOL_FIELD = 'endOfLifeDate'

with releasedata.ProductData("kuma") as product_data:
    yml_response = http.fetch_url("https://raw.githubusercontent.com/kumahq/kuma/master/versions.yml")
    versions_data = yaml.safe_load(yml_response.text)

    # Iterate through the versions and their associated dates
    for version_info in versions_data:
        release_name = version_info[RELEASE_FIELD]
        if not release_name.endswith('.x'):
            logging.info(f"skipping release with name {release_name}: does not end with '.x'")
            continue

        if RELEASE_DATE_FIELD not in version_info or EOL_FIELD not in version_info:
            logging.info(f"skipping release with name {release_name}: does not contain {RELEASE_DATE_FIELD} or {EOL_FIELD} fields")
            continue

        release = product_data.get_release(release_name.replace('.x', ''))

        release_date = dates.parse_date(version_info[RELEASE_DATE_FIELD])
        release.set_field('releaseDate', release_date)

        eol = dates.parse_date(version_info[EOL_FIELD])
        release.set_field('eol', eol)
