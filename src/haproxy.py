import json
import re
import urllib.request

from bs4 import BeautifulSoup

"""Fetch HAProxy versions with their dates from https://www.haproxy.org/download/.
"""

PRODUCT = "haproxy"
CYCLE_REGEX = r"^(\d+\.\d+)/$"
# https://regex101.com/r/1JCnFC/1
VERSION_REGEX = r"^(\d{4})\/(\d{2})\/(\d{2})\s+:\s+(\d+\.\d+\.\d.?)$"


def fetch_cycles():
    cycles = []

    print("Fetching cycles")
    with urllib.request.urlopen(
        "https://www.haproxy.org/download/") as response:
        soup = BeautifulSoup(response, features="html5lib")
        for link in soup.select("a"):
            m = re.match(CYCLE_REGEX, link.attrs["href"])
            if m:
                cycle = m.groups()[0]
                cycles.append(cycle)
                print(f"Found {cycle}")

    # No changelog in https://www.haproxy.org/download/1.0/src
    cycles.remove("1.0")

    return cycles


def fetch_releases(cycles):
    releases = {}

    for cycle in cycles:
        url = f"https://www.haproxy.org/download/{cycle}/src/CHANGELOG"
        print(f"Fetching version from {url}")
        with urllib.request.urlopen(url) as response:
            for line in response:
                m = re.match(VERSION_REGEX, line.decode("utf-8"))
                if m:
                    year, month, day, version = m.groups()
                    date = f"{year}-{month}-{day}"
                    releases[version] = date

    return releases


def print_releases(releases):
    # Do not print versions in fetch_releases because it contains duplicates
    for version, date in releases.items():
        print(f"{version} : {date}")


def main():
    print(f"::group::{PRODUCT}")
    cycles = fetch_cycles()
    releases = fetch_releases(cycles)
    print_releases(releases)
    print("::endgroup::")

    with open(f"releases/{PRODUCT}.json", "w") as f:
        f.write(json.dumps(dict(
            # sort by date then version (desc)
            sorted(releases.items(), key=lambda x: (x[1], x[0]), reverse=True)
        ), indent=2))


if __name__ == '__main__':
    main()
