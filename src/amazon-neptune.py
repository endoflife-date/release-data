import re
from common import http
from common import dates
from common import endoflife
from xml.dom.minidom import parseString

"""Fetch versions with their dates from the RSS feed of
https://docs.aws.amazon.com/neptune/latest/userguide/engine-releases.html.
"""

PRODUCT = "amazon-neptune"
REGEX = r"^Engine version (?P<version>[0-9R.]+)$"
URL = "https://docs.aws.amazon.com/neptune/latest/userguide/rssupdates.rss"

print(f"::group::{PRODUCT}")
versions = {}

response = http.fetch_url(URL)
rss = parseString(response.text)
for item in rss.getElementsByTagName("item"):
    title = item.getElementsByTagName("title")[0].firstChild.nodeValue
    pubDate = item.getElementsByTagName("pubDate")[0].firstChild.nodeValue
    matches = re.match(REGEX, title)
    if matches:
        version = matches['version']
        date = dates.parse_datetime(pubDate).strftime("%Y-%m-%d")
        versions[version] = date
        print(f"{version}: {date}")

endoflife.write_releases(PRODUCT, versions)
print("::endgroup::")
