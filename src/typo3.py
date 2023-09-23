import json
from common import endoflife

PRODUCT = "typo3"
URL = "https://get.typo3.org/api/v1/release/"

print(f"::group::{PRODUCT}")
releases = {}

response = endoflife.fetch_url(URL)
data = json.loads(response)
for v in data:
    if v['type'] != 'development':
        date = v["date"][0:10]
        releases[v["version"]] = date
        print(f"{v['version']}: {date}")

endoflife.write_releases(PRODUCT, dict(sorted(
    releases.items(), key=lambda x: list(map(int, x[0].split(".")))
)))
print("::endgroup::")
