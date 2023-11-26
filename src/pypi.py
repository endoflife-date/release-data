import json
import re
import sys
from common import dates
from common import endoflife

METHOD = "pypi"
DEFAULT_TAG_TEMPLATE = (  # Same as used in Ruby (update.rb)
    "{{major}}{% if minor %}.{{minor}}{% if patch %}.{{patch}}{%endif%}{%endif%}"
)
REGEX = r"^(?:(\d+\.(?:\d+\.)*\d+))$"


def fetch_releases(pypi_id, regex):
    releases = {}

    if not isinstance(regex, list):
        regex = [regex]

    url = f"https://pypi.org/pypi/{pypi_id}/json"
    response = endoflife.fetch_url(url)
    data = json.loads(response)
    for version in data["releases"]:
        R = data["releases"][version]
        matches = False
        for r in regex:
            if re.match(r, version):
                matches = True
        if matches and R:
            d = dates.parse_datetime(R[0]["upload_time"], to_utc=False).strftime("%Y-%m-%d")
            releases[version] = d
            print(f"{version}: {d}")

    return releases


def update_product(product_name, configs):
    versions = {}

    for config in configs:
        config = {"regex": REGEX} | config
        versions = versions | fetch_releases(config[METHOD], config["regex"])

    endoflife.write_releases(product_name, versions)


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product, configs in endoflife.list_products(METHOD, p_filter).items():
    print(f"::group::{product}")
    update_product(product, configs)
    print("::endgroup::")
