import re
from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime

PRODUCT = "splunk"
URL = "https://docs.splunk.com/Documentation/Splunk"
RELNOTES_URL_TEMPLATE = "https://docs.splunk.com/Documentation/Splunk/{version}/ReleaseNotes/MeetSplunk"
PATTERN = r"Splunk Enterprise (?P<version>\d+\.\d+(?:\.\d+)*) was (?:first )?released on (?P<date>\w+\s\d\d?,\s\d{4})\."


def convert_date(date: str) -> str:
    return datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d")


print(f"::group::{PRODUCT}")
versions = dict()
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

# Sort from highest to lowest version so that we can skip versions we already
# have (because, for example, 9.0.5 release notes also contains release notes
# for 9.0.0 to 9.0.4).
sorted_versions = sorted(
    eligible_versions,
    key=lambda x: list(map(int, x.split("."))), reverse=True
)

for v in sorted_versions:
    if v in versions:
        continue # if we already know the release date, skip it

    relnotes = endoflife.fetch_url(RELNOTES_URL_TEMPLATE.format(version=v))
    for (version, date_str) in re.findall(PATTERN, relnotes, re.MULTILINE):
        # convert x.y to x.y.0
        version = f"{version}.0" if len(version.split(".")) == 2 else version
        date = convert_date(date_str)
        versions[version] = date
        print(f"{version}: {date}")

endoflife.write_releases(PRODUCT, versions)
print("::endgroup::")
