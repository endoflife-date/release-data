import yaml
from common import dates, http, releasedata
from common.git import Git

"""Fetch version data for Kuma from https://raw.githubusercontent.com/kumahq/kuma/master/versions.yml
"""

with releasedata.ProductData("kuma") as product_data:
    yml_response = http.fetch_url("https://raw.githubusercontent.com/kumahq/kuma/master/versions.yml")
    versions_data = yaml.safe_load(yml_response.text)
    
    # Iterate through the versions and their associated dates
    for version_info in versions_data:
        if 'version' in version_info and 'releaseDate' in version_info:
            version = version_info['version']

            date_str = version_info['releaseDate']
            date = dates.parse_date(date_str)
            
            product_data.declare_version(version, date)
