from common import http
from common import dates
from common import endoflife

product = endoflife.Product("rockylinux")
print(f"::group::{product.name}")
response = http.fetch_url("https://raw.githubusercontent.com/rocky-linux/wiki.rockylinux.org/development/docs/include/releng/version_table.md")

for line in response.text.strip().split('\n'):
    items = line.split('|')
    if len(items) >= 5 and endoflife.DEFAULT_VERSION_PATTERN.match(items[1].strip()):
        version = items[1].strip()
        date = dates.parse_date(items[3])
        product.declare_version(version, date)

product.write()
print("::endgroup::")
