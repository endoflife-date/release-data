import sys
from datetime import datetime, timezone

from common import endoflife, http, releasedata

METHOD = "maven"

p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product_name in endoflife.list_products(METHOD, p_filter):
    product = releasedata.Product(product_name)
    product_frontmatter = endoflife.ProductFrontmatter(product.name)
    for config in product_frontmatter.get_auto_configs(METHOD):
        start = 0
        group_id, artifact_id = config.url.split("/")

        while True:
            url = f"https://search.maven.org/solrsearch/select?q=g:{group_id}+AND+a:{artifact_id}&core=gav&wt=json&start={start}&rows=100"
            data = http.fetch_url(url).json()

            for row in data["response"]["docs"]:
                version_match = config.first_match(row["v"])
                if version_match:
                    version = config.render(version_match)
                    date = datetime.fromtimestamp(row["timestamp"] / 1000, tz=timezone.utc)
                    product.declare_version(version, date)

            start += 100
            if data["response"]["numFound"] <= start:
                break

    product.write()
