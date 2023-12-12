from common import dates
from common import endoflife
from common import http

product = endoflife.Product("typo3")
print(f"::group::{product.name}")
data = http.fetch_url("https://get.typo3.org/api/v1/release/").json()
for v in data:
    if v['type'] == 'development':
        continue

    version = v["version"]
    date = dates.parse_datetime(v["date"], to_utc=False) # utc kept for now for backwards compatibility
    product.declare_version(version, date)

product.write()
print("::endgroup::")
