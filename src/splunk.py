import re
from bs4 import BeautifulSoup
from common import http
from common import dates
from common import endoflife

VERSION_DATE_PATTERN = re.compile(r"Splunk Enterprise (?P<version>\d+\.\d+(?:\.\d+)*) was (?:first )?released on (?P<date>\w+\s\d\d?,\s\d{4})\.", re.MULTILINE)


def get_latest_minor_versions(versions):
    versions_split = [v.split('.') for v in versions]

    # Group versions by major and minor version
    version_groups = {}
    for version in versions_split:
        major, minor = map(int, version[:2])
        # Release notes for versions before 7.2 don't contain release information
        if major < 7 or (major == 7 and minor < 2):
            continue
        major_minor = '.'.join(version[:2])
        if major_minor not in version_groups:
            version_groups[major_minor] = []
        version_groups[major_minor].append(version)

    # For each group, find the version with the highest patch version
    latest_versions = []
    for major_minor, group in version_groups.items():
        latest_patch = max(group, key=lambda version: int(version[2]))
        latest_versions.append('.'.join(latest_patch))

    return latest_versions


product = endoflife.Product("splunk")
print(f"::group::{product.name}")
main = http.fetch_url("https://docs.splunk.com/Documentation/Splunk")
soup = BeautifulSoup(main.text, features="html5lib")

all_versions = list(map(lambda option: option.attrs['value'], soup.select("select#version-select > option")))

# Latest minor release notes contains release notes for all previous minor versions.
# For example, 9.0.5 release notes also contains release notes for 9.0.0 to 9.0.4.
latest_minor_versions = get_latest_minor_versions(all_versions)
latest_minor_versions_urls = [f"https://docs.splunk.com/Documentation/Splunk/{v}/ReleaseNotes/MeetSplunk" for v in latest_minor_versions]
for response in http.fetch_urls(latest_minor_versions_urls):
    for (version, date_str) in VERSION_DATE_PATTERN.findall(response.text):
        version = f"{version}.0" if len(version.split(".")) == 2 else version  # convert x.y to x.y.0
        date = dates.parse_date(date_str)
        product.declare_version(version, date)

product.write()
print("::endgroup::")
