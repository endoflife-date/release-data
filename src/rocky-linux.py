from common import dates, endoflife, http, releasedata

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        response = http.fetch_url(config.url)
        for line in response.text.strip().split('\n'):
            items = line.split('|')
            if len(items) >= 5 and config.first_match(items[1].strip()):
                version = items[1].strip()
                date = dates.parse_date(items[3])
                product_data.declare_version(version, date)
