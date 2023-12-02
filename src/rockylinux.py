import re
from common import http
from common import dates
from common import endoflife

URL = "https://raw.githubusercontent.com/rocky-linux/wiki.rockylinux.org/development/docs/include/releng/version_table.md"


def parse_date(date_str):
    date_str = date_str.replace(',', '').strip()
    return dates.parse_date(date_str).strftime("%Y-%m-%d")


def parse_markdown_table(table_text):
    lines = table_text.strip().split('\n')
    versions = {}

    for line in lines:
        items = line.split('|')
        if len(items) >=5 and re.match(endoflife.DEFAULT_VERSION_REGEX, items[1].strip()):
            version = items[1].strip()
            date = parse_date(items[3])
            print(f"{version}: {date}")
            versions[version] = date

    return versions


print("::group::rockylinux")
response = http.fetch_url(URL)
versions = parse_markdown_table(response.text)
endoflife.write_releases('rockylinux', versions)
print("::endgroup::")
