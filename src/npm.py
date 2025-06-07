from common import dates, endoflife, http, releasedata

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        data = http.fetch_url(f"https://registry.npmjs.org/{config.url}").json()
        for version_str in data["versions"]:
            version_match = config.first_match(version_str)
            if version_match:
                version = config.render(version_match)
                date = dates.parse_datetime(data["time"][version_str])
                product_data.declare_version(version, date)
