import json
from common import endoflife
from datetime import datetime

PHP_MAJOR_VERSIONS = [4, 5, 7, 8]


# Date format is 03 Nov 2022
# With some versions using 03 November 2022 instead
# we return it as YYYY-MM-DD
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y").strftime("%Y-%m-%d")
    except ValueError:
        return datetime.strptime(date_str, "%d %B %Y").strftime("%Y-%m-%d")


def fetch_versions(major_version):
    url = f"https://www.php.net/releases/index.php?json&max=-1&version={major_version}"
    response = endoflife.fetch_url(url)
    data = json.loads(response)
    for v in data:
        data[v] = parse_date(data[v]["date"])
        print(f"{v}: {data[v]}")

    return data


print("::group::php")
releases = {}

for major_version in PHP_MAJOR_VERSIONS:
    releases |= fetch_versions(major_version)

endoflife.write_releases('php', dict(sorted(
    releases.items(), key=lambda x: list(map(int, x[0].split(".")))
)))
print("::endgroup::")
