import re
from common import endoflife
from datetime import datetime

URL = "https://raw.githubusercontent.com/rocky-linux/wiki.rockylinux.org/development/docs/include/releng/version_table.md"
REGEX = r"^(\d+\.\d+)$"

def parse_date(date_str):
    date_str = date_str.replace(',', '').strip()
    date_obj = datetime.strptime(date_str, "%B %d %Y")
    return date_obj.strftime("%Y-%m-%d")

def parse_markdown_table(table_text):
    lines = table_text.strip().split('\n')
    versions = {}

    for line in lines:
        items = line.split('|')
        if len(items) >=5 and re.match(REGEX, items[1].strip()):
            version = items[1].strip()
            date = parse_date(items[3])
            print(f"{version}: {date}")
            versions[version] = date

    return versions

print("::group::rockylinux")
response = endoflife.fetch_url(URL)

versions = parse_markdown_table(response)
endoflife.write_releases('rockylinux', versions)

print("::endgroup::")
