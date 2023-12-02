import json
from common import http
from common import endoflife

PRODUCT = "typo3"
URL = "https://get.typo3.org/api/v1/release/"

print(f"::group::{PRODUCT}")
versions = {}

response = http.fetch_url(URL)
data = json.loads(response.text)
for v in data:
    if v['type'] != 'development':
        date = v["date"][0:10]
        versions[v["version"]] = date
        print(f"{v['version']}: {date}")

endoflife.write_releases(PRODUCT, versions)
print("::endgroup::")
