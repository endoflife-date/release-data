import json
from common import dates
from common import endoflife

PHP_MAJOR_VERSIONS = [4, 5, 7, 8]


def fetch_versions(major_version):
    url = f"https://www.php.net/releases/index.php?json&max=-1&version={major_version}"
    response = endoflife.fetch_url(url)
    data = json.loads(response)
    for v in data:
        data[v] = dates.parse_date(data[v]["date"]).strftime("%Y-%m-%d")
        print(f"{v}: {data[v]}")

    return data


print("::group::php")
versions = {}
for major_version in PHP_MAJOR_VERSIONS:
    versions |= fetch_versions(major_version)

endoflife.write_releases('php', versions)
print("::endgroup::")
