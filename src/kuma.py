import yaml
from common import dates, http, releasedata

"""Fetch version data for Kuma from https://raw.githubusercontent.com/kumahq/kuma/master/versions.yml
"""

with releasedata.ProductData("kuma") as product_data:
    yml_response = http.fetch_url("https://raw.githubusercontent.com/kumahq/kuma/master/versions.yml")
    versions_data = yaml.safe_load(yml_response.text)

    # Iterate through the versions and their associated dates
    for version_info in versions_data:
        if 'version' in version_info and 'releaseDate' in version_info:
            release_name = version_info['release'].replace('.x', '')
            release = product_data.get_release(release_name)

            release_date_str = version_info['releaseDate']
            release_date = dates.parse_date(release_date_str)
            release.set_field('releaseDate', release_date)

            eol_str = version_info['endOfLifeDate']
            eol = dates.parse_date(eol_str)
            release.set_field('eol', eol)
