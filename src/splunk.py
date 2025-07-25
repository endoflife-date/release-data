import re

from common import dates, http
from common.releasedata import ProductData, config_from_argv

VERSION_DATE_PATTERN = re.compile(r"Splunk Enterprise (?P<version>\d+\.\d+(?:\.\d+)*) was (?:first )?released on (?P<date>\w+\s\d\d?,\s\d{4})\.", re.MULTILINE)


def get_latest_minor_versions(versions: list[str]) -> list[str]:
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
    for version_group in version_groups.values():
        latest_patch = max(version_group, key=lambda v: int(v[2]))
        latest_versions.append('.'.join(latest_patch))

    return latest_versions


config = config_from_argv()
with ProductData(config.product) as product_data:
    html = http.fetch_html(config.url)

    all_versions = [option.attrs['value'] for option in html.select("select#version-select > option")]
    all_versions = [v for v in all_versions if v != "DataMonitoringAppPreview"]

    # Latest minor release notes contains release notes for all previous minor versions.
    # For example, 9.0.5 release notes also contains release notes for 9.0.0 to 9.0.4.
    latest_minor_versions = get_latest_minor_versions(all_versions)
    latest_minor_versions_urls = [f"{config.url}/{v}/ReleaseNotes/MeetSplunk" for v in latest_minor_versions]
    # Oddly using the endoflife.date user agent does not work for 9.0, 9.2 and 9.3.
    for response in http.fetch_urls(latest_minor_versions_urls, headers={'User-Agent': http.FIREFOX_USER_AGENT}):
        for (version_str, date_str) in VERSION_DATE_PATTERN.findall(response.text):
            version_str = f"{version_str}.0" if len(version_str.split(".")) == 2 else version_str  # convert x.y to x.y.0
            date = dates.parse_date(date_str)
            product_data.declare_version(version_str, date)
