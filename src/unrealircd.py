import re

import mwparserfromhell
from common import dates, endoflife, http, releasedata

DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")

product = releasedata.Product("unrealircd")
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
