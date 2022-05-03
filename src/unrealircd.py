import mwparserfromhell
import json
import re
import urllib.request

URL = "https://www.unrealircd.org/docwiki/index.php?title=History_of_UnrealIRCd_releases&action=raw"
REGEX = r'^(?:(\d+\.(?:\d+\.)*\d+))$'

list = {}
with urllib.request.urlopen(URL) as response:
  text = response.read()
  wikicode = mwparserfromhell.parse(text)
  for tr in wikicode.ifilter_tags(matches=lambda node: node.tag == "tr"):
    items = tr.contents.filter_tags(matches=lambda node: node.tag == "td")
    if len(items) >=2:
      maybe_version = items[0].__strip__()
      if re.match(REGEX, maybe_version):
        maybe_date = items[1].__strip__()
        if re.match(r'\d{4}-\d{2}-\d{2}', maybe_date):
          list[maybe_version] = maybe_date


with open('releases/custom/unrealircd.json', 'w') as f:
  f.write(json.dumps(list, indent=2))
