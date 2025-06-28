import logging

from common import dates, http, releasedata

"""Fetch version data for Kuma from https://raw.githubusercontent.com/kumahq/kuma/master/versions.yml.
"""

RELEASE_FIELD = 'release'
RELEASE_DATE_FIELD = 'releaseDate'
EOL_FIELD = 'endOfLifeDate'

for config in releasedata.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        versions_data = http.fetch_yaml(config.url)

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
