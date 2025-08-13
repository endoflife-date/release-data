from common import dates, http
from common.releasedata import ProductData, config_from_argv

config = config_from_argv()
with ProductData(config.product) as product_data:
    data = http.fetch_json(config.url)
    for release_record in data:
        release_match = config.first_match(release_record.get("id", ""))
        if release_match:
            release_name = config.render(release_match)
            release = product_data.get_release(release_name)
            release.set_release_date(dates.parse_date(release_record.get("start")))
            release.set_eol(dates.parse_date(release_record.get("end")))
