import re
import xml.dom.minidom
from common import http
from common import dates
from common import endoflife

"""Fetches Amazon Neptune versions from its RSS feed on docs.aws.amazon.com."""

RSS_URL = "https://docs.aws.amazon.com/neptune/latest/userguide/rssupdates.rss"
VERSION_PATTERN = re.compile(r"^Engine version (?P<version>[0-9R.]+)$")

product = endoflife.Product("amazon-neptune")
print(f"::group::{product.name}")
rss_response = http.fetch_url(RSS_URL)
rss = xml.dom.minidom.parseString(rss_response.text)

for entry in rss.getElementsByTagName("item"):
    version_str = entry.getElementsByTagName("title")[0].firstChild.nodeValue
    date_str = entry.getElementsByTagName("pubDate")[0].firstChild.nodeValue

    version_match = VERSION_PATTERN.match(version_str)
    if version_match:
        product.declare_version(version_match['version'], dates.parse_datetime(date_str))

product.write()
print("::endgroup::")
