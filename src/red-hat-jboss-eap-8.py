import re

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetches the latest RedHat JBoss EAP version data for JBoss 8.0"""

def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        xml = http.fetch_xml(config.url)

        metadata = xml.getElementsByTagName("metadata")[0]
        versioning = metadata.getElementsByTagName("versioning")[0]

        artifact_id = metadata.getElementsByTagName("artifactId")[0].firstChild.nodeValue
        latest_str = versioning.getElementsByTagName("latest")[0].firstChild.nodeValue

        version_prefix = artifact_id.removeprefix("eap-")
        latest_name = version_prefix + "." + re.match(r"^1\.(.*)\.GA", latest_str).group(1)

        latest_date_str = versioning.getElementsByTagName("lastUpdated")[0].firstChild.nodeValue
        latest_date = dates.parse_datetime(latest_date_str)

        product_data.declare_version(latest_name, latest_date)
