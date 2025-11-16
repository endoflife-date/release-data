from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches Silverstripe releases from https://www.silverstripe.org/software/roadmap/ JSON data."""

config = config_from_argv()
with ProductData(config.product) as product_data:
    json = http.fetch_json(config.url)
    for release_data in json["data"]:
        release_name = release_data["version"]
        release = product_data.get_release(release_name)

        release_date_str = release_data.get("releaseDate")
        release.set_release_date(dates.parse_date_or_month_year_date(release_date_str))

        eoas_date_str = release_data.get("partialSupport")
        release.set_eoas(dates.parse_date_or_month_year_date(eoas_date_str))

        eol_date_str = release_data.get("supportEnds")
        release.set_eol(dates.parse_date_or_month_year_date(eol_date_str))
