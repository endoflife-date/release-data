import re
from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime

PRODUCT = "splunk"
URL = "https://docs.splunk.com/Documentation/Splunk"
RELNOTES_URL_TEMPLATE = "https://docs.splunk.com/Documentation/Splunk/{version}/ReleaseNotes/MeetSplunk"
PATTERN = r"Splunk Enterprise (?P<version>\d+\.\d+(?:\.\d+)*) was released on (?P<date>\w+\s\d\d?,\s\d{4})\."


def convert_date(date: str) -> str:
    return datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d")


print(f"::group::{PRODUCT}")
releases = dict()
main = endoflife.fetch_url(URL)
soup = BeautifulSoup(main, features="html5lib")

all_versions = list(map(
    lambda option: option.attrs['value'],
    soup.select("select#version-select > option")
))

# Release notes for versions before 7.2 don't contain release information
eligible_versions = list(filter(
    lambda v: v.split('.') >= '7.2'.split('.'),
    all_versions
))

for v in eligible_versions:
    relnotes = endoflife.fetch_url(RELNOTES_URL_TEMPLATE.format(version=v))
    for (version, date_str) in re.findall(PATTERN, relnotes, re.MULTILINE):
        date = convert_date(date_str)
        releases[version] = date
        print(f"{version}: {date}")

endoflife.write_releases(PRODUCT, dict(
    # sort by version then date (asc)
    sorted(releases.items(), key=lambda x: (x[0], x[1]))
))
print("::endgroup::")
