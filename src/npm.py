import sys
from common import dates
from common import http
from common import endoflife

METHOD = "npm"

p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product_name, configs in endoflife.list_products(METHOD, p_filter).items():
    product = endoflife.Product(product_name)
    print(f"::group::{product.name}")

    product_frontmatter = endoflife.ProductFrontmatter(product.name)
    for config in product_frontmatter.get_auto_configs(METHOD):
        data = http.fetch_url(f"https://registry.npmjs.org/{config.url}").json()
        for version_str in data["versions"]:
            version_match = config.first_match(version_str)
            if version_match:
                version = config.render(version_match)
                date = dates.parse_datetime(data["time"][version_str])
                product.declare_version(version, date)

    product.write()
    print("::endgroup::")
