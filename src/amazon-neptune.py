import re
from xml.dom.minidom import parseString
from common import endoflife
from datetime import datetime

"""Fetch versions with their dates from the RSS feed of
https://docs.aws.amazon.com/neptune/latest/userguide/engine-releases.html.
"""

PRODUCT = "amazon-neptune"
REGEX = r"^Engine version (?P<version>[0-9R.]+)$"
URL = "https://docs.aws.amazon.com/neptune/latest/userguide/rssupdates.rss"

print(f"::group::{PRODUCT}")
versions = {}

response = endoflife.fetch_url(URL)
rss = parseString(response)
for item in rss.getElementsByTagName("item"):
    title = item.getElementsByTagName("title")[0].firstChild.nodeValue
    pubDate = item.getElementsByTagName("pubDate")[0].firstChild.nodeValue
    matches = re.match(REGEX, title)
    if matches:
        version = matches['version']
        date = datetime.strptime(pubDate, "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d")
        versions[version] = date
        print(f"{version}: {date}")

endoflife.write_releases(PRODUCT, dict(
    # sort by date then version (desc)
    sorted(versions.items(), key=lambda x: (x[1], x[0]), reverse=True)
))
print("::endgroup::")
