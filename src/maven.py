from datetime import datetime, timezone

from common import http, releasedata

for config in releasedata.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        start = 0
        group_id, artifact_id = config.url.split("/")

        while True:
            url = f"https://search.maven.org/solrsearch/select?q=g:{group_id}+AND+a:{artifact_id}&core=gav&wt=json&start={start}&rows=100"
            data = http.fetch_json(url)

            for row in data["response"]["docs"]:
                version_match = config.first_match(row["v"])
                if version_match:
                    version = config.render(version_match)
                    date = datetime.fromtimestamp(row["timestamp"] / 1000, tz=timezone.utc)
                    product_data.declare_version(version, date)

            start += 100
            if data["response"]["numFound"] <= start:
                break
