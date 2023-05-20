import json
import re
import sys
from common import endoflife
from datetime import datetime

METHOD = "pypi"
DEFAULT_TAG_TEMPLATE = (  # Same as used in Ruby (update.rb)
    "{{major}}{% if minor %}.{{minor}}{% if patch %}.{{patch}}{%endif%}{%endif%}"
)
REGEX = r"^(?:(\d+\.(?:\d+\.)*\d+))$"


def fetch_releases(pypi_id, regex):
    releases = {}

    if not isinstance(regex, list):
        regex = [regex]

    url = "https://pypi.org/pypi/%s/json" % pypi_id
    response = endoflife.fetch_url(url)
    data = json.loads(response)
    for version in data["releases"]:
        R = data["releases"][version]
        matches = False
        for r in regex:
            if re.match(r, version):
                matches = True
        if matches and R:
            d = datetime.fromisoformat(R[0]["upload_time"]).strftime("%Y-%m-%d")
            releases[version] = d
            print("%s: %s" % (version, d))

    return releases


def update_product(product_name, configs):
    releases = {}

    for config in configs:
        config = {"regex": REGEX} | config
        releases = releases | fetch_releases(config[METHOD], config["regex"])

    endoflife.write_releases(product_name, releases)


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product, configs in endoflife.list_products(METHOD, p_filter).items():
    print("::group::%s" % product)
    update_product(product, configs)
    print("::endgroup::")
