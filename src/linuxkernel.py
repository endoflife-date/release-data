import json
import re
from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime, timezone

"""Fetch Linux Kernel versions with their dates from
https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/refs/tags.

Ideally we would want to use the kernel.org git repository directly
(https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/), but it does
not support partial clone so we cannot.
"""

PRODUCT = "linuxkernel"
URL = "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/refs/tags"


# Parse date with format 2023-05-01 08:32:34 +0900 and convert to UTC
def parse_date(d):
    return datetime.strptime(d, "%Y-%m-%d %H:%M:%S %z")\
        .astimezone(timezone.utc)\
        .strftime("%Y-%m-%d")


def make_bs_request(url):
    response = endoflife.fetch_url(url)
    return BeautifulSoup(response, features="html5lib")


def fetch_releases():
    releases = {}

    soup = make_bs_request(URL)
    for table in soup.find_all("table", class_='list'):
        for row in table.find_all("tr"):
            columns = row.find_all("td")
            if len(columns) == 4:
                version_text = columns[0].text.strip()
                datetime_td = columns[3].find_next('span')
                datetime_text = datetime_td.attrs['title'] if datetime_td else None
                if version_text.startswith('v') and datetime_text:
                    r = r"v(?P<v>\d+(?:\.\d+)*)$"
                    m = re.search(r, version_text, flags=re.IGNORECASE)
                    if m:
                        version = m.group("v")
                        date = parse_date(datetime_text)
                        print(f"{version} : {date}")
                        releases[version] = date

    return releases


def main():
    print(f"::group::{PRODUCT}")
    releases = fetch_releases()
    print("::endgroup::")

    with open(f"releases/{PRODUCT}.json", "w") as f:
        f.write(json.dumps(dict(
            # sort by version then date (asc)
            sorted(releases.items(), key=lambda x: (x[0], x[1]))
        ), indent=2))


if __name__ == '__main__':
    main()
