import re
import xml.dom.minidom

from common import dates, http, releasedata

"""Fetches Amazon Neptune versions from its RSS feed on docs.aws.amazon.com."""

RSS_URL = "https://docs.aws.amazon.com/neptune/latest/userguide/rssupdates.rss"
VERSION_PATTERN = re.compile(r"^Engine version (?P<version>[0-9R.]+)$")

product = releasedata.Product("amazon-neptune")
rss_response = http.fetch_url(RSS_URL)
rss = xml.dom.minidom.parseString(rss_response.text)

for entry in rss.getElementsByTagName("item"):
    version_str = entry.getElementsByTagName("title")[0].firstChild.nodeValue
    date_str = entry.getElementsByTagName("pubDate")[0].firstChild.nodeValue

    version_match = VERSION_PATTERN.match(version_str)
    if version_match:
        product.declare_version(version_match['version'], dates.parse_datetime(date_str))

product.write()
