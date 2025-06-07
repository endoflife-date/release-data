import re
from xml.dom.minidom import parseString

from common import dates, endoflife, http, releasedata

"""Fetches the latest RedHat JBoss EAP version data for JBoss 8.0"""

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        response = http.fetch_url(config.url)

        xml = parseString(response.text)
        versioning = xml.getElementsByTagName("metadata")[0].getElementsByTagName("versioning")[0]

        latest_str = versioning.getElementsByTagName("latest")[0].firstChild.nodeValue
        latest_name = "8.0." + re.match(r"^..(.*)\.GA", latest_str).group(1)

        latest_date_str = versioning.getElementsByTagName("lastUpdated")[0].firstChild.nodeValue
        latest_date = dates.parse_datetime(latest_date_str)

        product_data.declare_version(latest_name, latest_date)
