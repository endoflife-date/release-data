from glob import glob
import os
import re
import sys
import json
import frontmatter
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
from html.parser import HTMLParser
from liquid import Template

# Same as used in Ruby (update.rb)
DEFAULT_TAG_TEMPLATE = "{{major}}{% if minor %}.{{minor}}{% if patch %}.{{patch}}{%endif%}{%endif%}"
REGEX = r'^(?:(\d+\.(?:\d+\.)*\d+))$'

def fetch_releases(pypi_id, regex):
    releases = {}

    if not isinstance(regex, list):
      regex = [regex]

    url = "https://pypi.org/pypi/%s/json" % pypi_id
    with urllib.request.urlopen(url, data=None, timeout=5) as response:
      data = json.loads(response.read().decode("utf-8"))
      for version in data['releases']:
        R = data['releases'][version]
        matches = False
        for r in regex:
          if re.match(r, version):
            matches = True
        if matches:
          d = datetime.fromisoformat(R[0]['upload_time']).strftime("%Y-%m-%d")
          releases[version] = d
          print("%s: %s" % (version, d))

    return releases

def update_releases(product_filter=None):
  for product_file in glob("website/products/*.md"):
      product_name = os.path.splitext(os.path.basename(product_file))[0]
      if product_filter and product_name != product_filter:
        continue
      with open(product_file, "r") as f:
          data = frontmatter.load(f)
          if "auto" in data:
              for config in data["auto"]:
                  for key, d_id in config.items():
                      if key == "pypi":
                          update_product(product_name, config)

def update_product(product_name, config):
  if "pypi" in config:
      print("::group::%s" % product_name)
      config = config | {"regex": REGEX}
      r = fetch_releases(config['pypi'], config["regex"])
      with open("releases/%s.json" % product_name, "w") as f:
          f.write(json.dumps(r, indent=2))
      print("::endgroup::")

if __name__ == "__main__":
  if len(sys.argv) > 1:
    update_releases(sys.argv[1])
  else:
    update_releases()
