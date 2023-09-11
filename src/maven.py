import datetime
import json
import re
import sys
from common import endoflife

METHOD = "maven"
VERSION_REGEX = r'^\d+\.\d+(\.\d+)?$'


# TODO: Add support for custom regexes
# Hasn't been needed yet, so only write if we need it
def valid_version(version):
    if re.match(VERSION_REGEX, version):
        return True
    return False


def fetch_json(group_id, artifact_id, start):
    url = f"https://search.maven.org/solrsearch/select?q=g:{group_id}+AND+a:{artifact_id}&core=gav&rows=100&wt=json&start={start}"
    response = endoflife.fetch_url(url)
    return json.loads(response)


def fetch_releases(package_identifier):
    releases = {}
    start = 0
    group_id, artifact_id = package_identifier.split("/")

    while True:
        data = fetch_json(group_id, artifact_id, start)

        for row in data["response"]["docs"]:
            version = row["v"]
            if valid_version(version):
                date = datetime.datetime.utcfromtimestamp(row["timestamp"] / 1000).strftime("%Y-%m-%d")
                releases[version] = date
                print(f"{version}: {date}")

        start += 100
        if data["response"]["numFound"] <= start:
            break

    return releases


def update_product(product_name, configs):
    releases = {}

    for config in configs:
        releases = releases | fetch_releases(config[METHOD])

    endoflife.write_releases(product_name, dict(
        # sort by date then version (desc)
        sorted(releases.items(), key=lambda x: (x[1], x[0]), reverse=True)
    ))


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product, configs in endoflife.list_products(METHOD, p_filter).items():
    print(f"::group::{product}")
    update_product(product, configs)
    print("::endgroup::")
