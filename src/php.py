from common import dates, endoflife, http

MAIN_URL = "https://www.php.net/releases/index.php?json&max=-1"

product = endoflife.Product("php")
print(f"::group::{product.name}")

# Fetch major versions
latest_by_major = http.fetch_url(MAIN_URL).json()
major_version_urls = [f"{MAIN_URL}&version={major_version}" for major_version in latest_by_major]

# Fetch all versions for major versions
for major_versions_response in http.fetch_urls(major_version_urls):
    major_versions_data = major_versions_response.json()
    for version in major_versions_data:
        if endoflife.DEFAULT_VERSION_PATTERN.match(version):  # exclude versions such as "3.0.x (latest)"
            date = dates.parse_date(major_versions_data[version]["date"])
            product.declare_version(version, date)

product.write()
print("::endgroup::")
