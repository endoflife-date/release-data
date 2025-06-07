from common import dates, endoflife, http, releasedata

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        data = http.fetch_url(config.url).json()
        for v in data:
            if v['type'] == 'development':
                continue

            version = v["version"]
            date = dates.parse_datetime(v["date"], to_utc=False)  # utc kept for now for backwards compatibility
            product_data.declare_version(version, date)
