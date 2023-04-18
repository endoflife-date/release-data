import urllib.request
import datetime
import json

PHP_MAJOR_VERSIONS = [4, 5, 7, 8]


# Date format is 03 Nov 2022
# With some versions using 03 November 2022 instead
# we return it as YYYY-MM-DD
def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%d %b %Y").strftime("%Y-%m-%d")
    except ValueError:
        return datetime.datetime.strptime(date_str, "%d %B %Y").strftime("%Y-%m-%d")


def fetch_versions(major_version):
    url = f"https://www.php.net/releases/index.php?json&max=-1&version={major_version}"
    with urllib.request.urlopen(url, data=None, timeout=5) as response:
        data = json.loads(response.read())
        for v in data:
            data[v] = parse_date(data[v]["date"])
            print(f"{v}: {data[v]}")

        return data


with open("releases/php.json", "w") as f:
    print("::group::php")
    releases = {}

    for major_version in PHP_MAJOR_VERSIONS:
        releases |= fetch_versions(major_version)

    f.write(
        json.dumps(
            dict(sorted(
                releases.items(),
                key=lambda x: list(map(str, x[0].split(".")))
            )),
            indent=2,
        )
    )

    print("::endgroup::")
