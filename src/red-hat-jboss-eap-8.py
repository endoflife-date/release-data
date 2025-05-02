import re
from xml.dom.minidom import parseString

from common import dates, http, releasedata

"""Fetches the latest RedHat JBoss EAP version data for JBoss 8.0"""

with releasedata.ProductData("red-hat-jboss-eap") as product_data:
    response = http.fetch_url("https://maven.repository.redhat.com/ga/org/jboss/eap/channels/eap-8.0/maven-metadata.xml")

    xml = parseString(response.text)
    versioning = xml.getElementsByTagName("metadata")[0].getElementsByTagName("versioning")[0]

    latest_str = versioning.getElementsByTagName("latest")[0].firstChild.nodeValue
    latest_name = "8.0." + re.match(r"^..(.*)\.GA", latest_str).group(1)

    latest_date_str = versioning.getElementsByTagName("lastUpdated")[0].firstChild.nodeValue
    latest_date = dates.parse_datetime(latest_date_str)

    product_data.declare_version(latest_name, latest_date)
