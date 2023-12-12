import mwparserfromhell
import re
from common import dates
from common import endoflife
from common import http

DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")

product = endoflife.Product("unrealircd")
print(f"::group::{product.name}")
response = http.fetch_url("https://www.unrealircd.org/docwiki/index.php?title=History_of_UnrealIRCd_releases&action=raw")
wikicode = mwparserfromhell.parse(response.text)

for tr in wikicode.ifilter_tags(matches=lambda node: node.tag == "tr"):
    items = tr.contents.filter_tags(matches=lambda node: node.tag == "td")
    if len(items) < 2:
        continue

    version = items[0].__strip__()
    date_str = items[1].__strip__()
    if endoflife.DEFAULT_VERSION_PATTERN.match(version) and DATE_PATTERN.match(date_str):
        date = dates.parse_date(date_str)
        product.declare_version(version, date)

product.write()
print("::endgroup::")
