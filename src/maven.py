from glob import glob
import os
import sys
import json
import frontmatter
import urllib.request
import datetime
import re

# Major.Minor + Optional Patch, no RC, nightly releases.
VERSION_REGEX = r'^\d+\.\d+(\.\d+)?$'


# TODO: Add support for custom regexes
# Hasn't been needed yet, so only write if we need it
def valid_version(version):
    if re.match(VERSION_REGEX, version):
        return True
    return False


def fetch_json(group_id, artifact_id, start):
    url = f"https://search.maven.org/solrsearch/select?q=g:{group_id}+AND+a:{artifact_id}&core=gav&rows=100&wt=json&start={start}"
    last_exception = None

    # search.maven.org often time out lately, retry the request in case of failures.
    for i in range(0, 5):
        try:
            with urllib.request.urlopen(url, data=None, timeout=5) as response:
                return json.load(response)
        except Exception as e:
            last_exception = e
            message = getattr(e, 'message', repr(e)) # https://stackoverflow.com/a/45532289/374236
            print(f"Error while requesting {url} ({message}), retrying ({i})...")
            continue

    raise last_exception


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
                print("%s: %s" % (version, date))

        start += 100
        if data["response"]["numFound"] <= start:
            break

    return releases


def update_releases(product_filter=None):
    for product_file in glob("website/products/*.md"):
        product_name = os.path.splitext(os.path.basename(product_file))[0]
        if product_filter and product_name != product_filter:
            continue
        with open(product_file, "r") as f:
            releases = {}
            found_maven = False
            print("::group::%s" % product_name)
            data = frontmatter.load(f)
            if "auto" in data:
                for config in data["auto"]:
                    for key, _ in config.items():
                        if key == "maven":
                            found_maven = True
                            releases = releases | fetch_releases(config["maven"])
            if found_maven:
                write_file(product_name, releases)
            print("::endgroup::")


def write_file(product_name, releases):
    with open("releases/%s.json" % product_name, "w") as f:
        f.write(json.dumps(dict(
            # sort by date then version (desc)
            sorted(releases.items(), key=lambda x: (x[1], x[0]), reverse=True)
        ), indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_releases(sys.argv[1])
    else:
        update_releases()
