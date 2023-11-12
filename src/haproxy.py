import re
from bs4 import BeautifulSoup
from common import endoflife

"""Fetch HAProxy versions with their dates from https://www.haproxy.org/.
"""

PRODUCT = "haproxy"
CYCLE_REGEX = r"^(\d+\.\d+)/$"
# https://regex101.com/r/1JCnFC/1
VERSION_REGEX = r"^(\d{4})\/(\d{2})\/(\d{2})\s+:\s+(\d+\.\d+\.\d.?)$"


def fetch_cycles():
    cycles = []

    response = endoflife.fetch_url('https://www.haproxy.org/download/')
    soup = BeautifulSoup(response, features="html5lib")
    for link in soup.select("a"):
        m = re.match(CYCLE_REGEX, link.attrs["href"])
        if m:
            cycle = m.groups()[0]
            cycles.append(cycle)

    # No changelog in https://www.haproxy.org/download/1.0/src
    cycles.remove("1.0")

    return cycles


def fetch_releases(cycles):
    releases = {}

    for cycle in cycles:
        url = f"https://www.haproxy.org/download/{cycle}/src/CHANGELOG"
        response = endoflife.fetch_url(url)
        for line in response.split('\n'):
            m = re.match(VERSION_REGEX, line)
            if m:
                year, month, day, version = m.groups()
                date = f"{year}-{month}-{day}"
                releases[version] = date

    return releases


def print_releases(releases):
    # Do not print versions in fetch_releases because it contains duplicates
    for version, date in releases.items():
        print(f"{version} : {date}")


print(f"::group::{PRODUCT}")
all_cycles = fetch_cycles()
all_versions = fetch_releases(all_cycles)
print_releases(all_versions)
endoflife.write_releases(PRODUCT, all_versions)
print("::endgroup::")
