from glob import glob
import os
import re
import json
import frontmatter
import urllib.request
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from liquid import Template

# Same as used in Ruby (update.rb)
DEFAULT_TAG_TEMPLATE = "{{major}}{% if minor %}.{{minor}}{% if patch %}.{{patch}}{%endif%}{%endif%}"

def get_versions_from_headline(regex, headline, template):
  if not isinstance(regex, list):
    regex = [regex]
  for r in regex:
    matches = re.match(r.strip(), headline)
    if matches:
        match_data = matches.groupdict()
        version_string = template.render(**match_data)
        return version_string.split("\n")

  return {}

def fetch_releases(distrowatch_id, regex, template):
    releases = {}
    l_template = Template(template)
    url = "https://distrowatch.com/index.php?distribution=%s" % distrowatch_id
    with urllib.request.urlopen(url, data=None, timeout=5) as response:
        soup = BeautifulSoup(response, features="html5lib")
        for table in soup.select("td.News1>table.News"):
            headline = table.select_one("td.NewsHeadline a[href]").get_text().strip()
            date = table.select_one("td.NewsDate").get_text()
            for v in get_versions_from_headline(regex, headline, l_template):
              print("%s: %s" % (v, date))
              releases[v] = date
    return releases

def update_releases():
  for product_file in glob("website/products/*.md"):
      product_name = os.path.splitext(os.path.basename(product_file))[0]
      with open(product_file, "r") as f:
          data = frontmatter.load(f)
          if "auto" in data:
              for config in data["auto"]:
                  for key, d_id in config.items():
                      if key == "distrowatch":
                          update_product(product_name, config)

def update_product(product_name, config):
  t = config.get("template", DEFAULT_TAG_TEMPLATE)
  if "regex" in config:
      print("::group::%s" % product_name)
      r = fetch_releases(config['distrowatch'], config["regex"], t)
      with open("releases/%s.json" % product_name, "w") as f:
          f.write(json.dumps(r, indent=2))
      print("::endgroup::")

if __name__ == "__main__":
  update_releases()
