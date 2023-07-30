import re
from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime
from typing import List, Dict

PRODUCT = "splunk"
URL = "https://docs.splunk.com/Documentation/Splunk"
RELEASE_NOTES_URL = "https://docs.splunk.com/Documentation/Splunk/{version}/ReleaseNotes/MeetSplunk"
DATE_FORMAT = "%B %d, %Y"


def convert_date(date: str) -> str:
    return datetime.strptime(date, DATE_FORMAT).strftime("%Y-%m-%d")

def fetch_versions(url: str, min: str = '0') -> List[str]:
    """
    Get all the versions and return a list.
    """
    resp = endoflife.fetch_url(url)
    soup = BeautifulSoup(resp, features="html5lib")
    options = soup.select("select#version-select > option")

    return sorted([
        x.attrs['value']
        for x in options
        if 'value' in x.attrs and x.attrs['value'].split('.') >= min.split('.')
    ], reverse=True, key=lambda x: x.split())

def fetch_version_dates(version: str, release_url: str = RELEASE_NOTES_URL) -> Dict[str, str]:
    """
    Check the versions docs and extract all possible dates.
    There may be dates for other versions too.
    """
    url = release_url.format(version=version)
    resp = endoflife.fetch_url(url)

    return {
        version: convert_date(date)
        for (version, date) in re.findall(
            r"Splunk Enterprise (?P<version>\d+\.\d+\.\d+(?:\.\d+)?) was released on (?P<date>\w+\s\d\d?,\s\d{4})\.",
            resp,
            re.MULTILINE,
        )
    }

releases = dict()
# release data is only available for 7.2+
for version in fetch_versions(URL, min='7.2'):
    if version in releases:
        continue
    releases = {**releases, **fetch_version_dates(version)}

print(f"::group::{PRODUCT}")
for version, date in releases.items():
    print(f"{version}: {date}")

endoflife.write_releases(PRODUCT, dict(
    # sort by version then date (asc)
    sorted(releases.items(), key=lambda x: (x[0], x[1]))
))
print("::endgroup::")
