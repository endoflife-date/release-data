from common import dates, http
from common.releasedata import ProductData, config_from_argv

config = config_from_argv()
with ProductData(config.product) as product_data:
    response = http.fetch_url(config.url)
    for line in response.text.strip().split('\n'):
        items = line.split('|')
        if len(items) >= 5 and config.first_match(items[1].strip()):
            version = items[1].strip()
            date = dates.parse_date(items[3])
            product_data.declare_version(version, date)
