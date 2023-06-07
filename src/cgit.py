import json
import os
import re
import sys
import urllib.request

from datetime import datetime, timezone
from glob import glob

import frontmatter
from bs4 import BeautifulSoup
from liquid import Template

# Same as used in Ruby (update.rb)
DEFAULT_TAG_TEMPLATE = (
    "{{major}}{% if minor %}.{{minor}}{% if patch %}.{{patch}}{%endif%}{%endif%}"
)
DEFAULT_VERSION_REGEX = (
    r"^v?(?P<major>[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.?(?P<patch>0|[1-9]\d*)?$"
)


# Parse date with format 2023-05-01 08:32:34 +0900 and convert to UTC
def parse_date(d):
    return (
        datetime.strptime(d, "%Y-%m-%d %H:%M:%S %z")
        .astimezone(timezone.utc)
        .strftime("%Y-%m-%d")
    )


def make_bs_request(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=5) as response:
        return BeautifulSoup(response.read(), features="html5lib")


def fetch_releases(url, regex, template):
    releases = {}

    soup = make_bs_request(url)
    for table in soup.find_all("table", class_="list"):
        for row in table.find_all("tr"):
            columns = row.find_all("td")
            if len(columns) == 4:
                version_text = columns[0].text.strip()
                datetime_td = columns[3].find_next("span")
                datetime_text = datetime_td.attrs["title"] if datetime_td else None
                if datetime_text:
                    matches = re.match(regex.strip(), version_text)
                    if matches:
                        match_data = matches.groupdict()
                        version_string = template.render(**match_data)
                        date = parse_date(datetime_text)
                        print(f"{version_string} : {date}")
                        releases[version_string] = date

    return releases


def update_product(product_name, config):
    template = l_template = Template(config.get("template", DEFAULT_TAG_TEMPLATE))
    regex = config.get("regex", DEFAULT_VERSION_REGEX)

    print(f"::group::{product_name}")
    releases = fetch_releases(config["cgit"], regex, template)
    print("::endgroup::")

    with open(f"releases/{product_name}.json", "w") as f:
        f.write(
            json.dumps(
                dict(
                    # sort by version then date (asc)
                    sorted(releases.items(), key=lambda x: (x[0], x[1]))
                ),
                indent=2,
            )
        )


def update_releases(product_filter=None):
    for product_file in glob("website/products/*.md"):
        product_name = os.path.splitext(os.path.basename(product_file))[0]
        if product_filter and product_name != product_filter:
            continue
        with open(product_file, "r") as f:
            data = frontmatter.load(f)
            if "auto" in data:
                for config in data["auto"]:
                    for key, d_id in config.items():
                        if key == "cgit":
                            update_product(product_name, config)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_releases(sys.argv[1])
    else:
        update_releases()
