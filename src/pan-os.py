from common import dates, http, releasedata

"""Fetches pan-os versions from https://github.com/mrjcap/panos-versions/."""

with releasedata.ProductData("pan-os") as product_data:
    versions = http.fetch_url("https://raw.githubusercontent.com/mrjcap/panos-versions/master/PaloAltoVersions.json").json()

    for version in versions:
        name = version['version']
        date = dates.parse_datetime(version['released-on'])
        product_data.declare_version(name, date)
