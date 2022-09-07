from glob import glob
import os
import sys
import json
import frontmatter
import urllib.request
import datetime

def fetch_releases(package_identifier):
    groupId, artifactId = package_identifier.split("/")
    releases = {}
    start = 0
    while True:
      url = "https://search.maven.org/solrsearch/select?q=g:%s+AND+a:%s&core=gav&rows=100&wt=json&start=%s" % (groupId, artifactId, start)
      with urllib.request.urlopen(url, data=None, timeout=5) as response:
          data = json.load(response)
          for row in data['response']['docs']:
              date = datetime.datetime.utcfromtimestamp(row['timestamp'] / 1000)
              version = row['v']
              if not any(exception in version for exception in ['alpha', 'beta', 'nightly', 'rc']):
                abs_date = date.strftime("%Y-%m-%d")
                releases[version] = abs_date
                print("%s: %s" % (version, abs_date))
          start+=100
          if data['response']['numFound'] <= start:
            break
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
                  for key, _ in config.items():
                      if key == "maven":
                          update_product(product_name, config)

def update_product(product_name, config):
    print("::group::%s" % product_name)
    r = fetch_releases(config['maven'])
    with open("releases/%s.json" % product_name, "w") as f:
        f.write(json.dumps(r, indent=2))
    print("::endgroup::")

if __name__ == "__main__":
  if len(sys.argv) > 1:
    update_releases(sys.argv[1])
  else:
    update_releases()
