import logging
import re
import xml.dom.minidom

from bs4 import BeautifulSoup
from common import dates, http, releasedata

"""Fetches RedHat JBoss EAP version data for JBoss 7.4 and 8.0"""

JBOSS_7_VERSIONS_URL = "https://access.redhat.com/articles/2332721"
JBOSS_8_METADATA_URL = "https://maven.repository.redhat.com/ga/org/jboss/eap/channels/eap-8.0/maven-metadata.xml"

# Given a dict, find inside the list of phases the one that matches the phase_name, extract and parse it's associated date
def find_date_field(elem, phase_name):
    entry = list(filter(lambda it: it.get("name") == phase_name, elem["phases"]))[0]
    return dates.parse_datetime(entry["date"])

with releasedata.ProductData("redhat-jboss-eap") as product_data:

    # JBoss 7.4 versions
    response = http.fetch_url(JBOSS_7_VERSIONS_URL)
    soup = BeautifulSoup(response.text, features="html5lib")
    table = soup.find("table")
    for (i, row) in enumerate(table.find_all("tr")):
        if i == 0: # Skip the first row (header)
            continue

        columns = row.find_all("td")
        # Get the version name and release date
        name = columns[0].getText().strip()
        if name == "GA":
            name = "7.4.0"
        name = name.replace("Update ", "7.4.")
        release_date_str = columns[1].getText().strip()
        if release_date_str == "TBD": # Placeholder for a future release
            continue
        release_date = dates.parse_date(release_date_str)

        # Declare the version
        product_data.declare_version(name, release_date)

    # JBoss 8 versions
    response = http.fetch_url(JBOSS_8_METADATA_URL)
    xml_response = xml.dom.minidom.parseString(response.text)
    metadata = xml_response.getElementsByTagName("metadata")[0]
    versioning = metadata.getElementsByTagName("versioning")[0]
    latest = versioning.getElementsByTagName("latest")[0].firstChild.nodeValue
    latest_version = "8.0." + re.match(r"^..(.*)\.GA", latest).group(1)

    last_updated_str = versioning.getElementsByTagName("lastUpdated")[0].firstChild.nodeValue
    # Split the field into 4 digits for year, 2 for month, 2 for day, 2 for hour, 2 for minute, and 2 for second
    lu = re.match(r"^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})", last_updated_str)
    # Format the date as %Y-%m-%d %H:%M:%S
    last_updated_formatted = f"{lu.group(1)}-{lu.group(2)}-{lu.group(3)} {lu.group(4)}:{lu.group(5)}:{lu.group(6)}"
    product_data.declare_version(latest_version, dates.parse_datetime(last_updated_formatted))
