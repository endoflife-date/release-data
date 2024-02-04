from common import dates, http, releasedata

with releasedata.ProductData("typo3") as product_data:
    data = http.fetch_url("https://get.typo3.org/api/v1/release/").json()
    for v in data:
        if v['type'] == 'development':
            continue

        version = v["version"]
        date = dates.parse_datetime(v["date"], to_utc=False)  # utc kept for now for backwards compatibility
        product_data.declare_version(version, date)
