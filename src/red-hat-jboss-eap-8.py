import re

from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches the latest RedHat JBoss EAP version data for JBoss 8.0"""

config = config_from_argv()
with ProductData(config.product) as product_data:
    xml = http.fetch_xml(config.url)

    versioning = xml.getElementsByTagName("metadata")[0].getElementsByTagName("versioning")[0]

    latest_str = versioning.getElementsByTagName("latest")[0].firstChild.nodeValue
    latest_name = "8.0." + re.match(r"^..(.*)\.GA", latest_str).group(1)

    latest_date_str = versioning.getElementsByTagName("lastUpdated")[0].firstChild.nodeValue
    latest_date = dates.parse_datetime(latest_date_str)

    product_data.declare_version(latest_name, latest_date)
