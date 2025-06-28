import logging

from common import dates, http, releasedata

"""Fetches Satellite versions from access.redhat.com.

A few of the older versions, such as 'Satellite 6.1 GA Release (Build 6.1.1)', were ignored because too hard to parse."""

for config in releasedata.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        html = http.fetch_html(config.url)

        for table in html.findAll("tbody"):
            for tr in table.findAll("tr"):
                td_list = tr.findAll("td")

                version_str = td_list[0].get_text().replace(' GA', '.0').strip()  # x.y GA => x.y.0
                version_match = config.first_match(version_str)
                if not version_match:
                    logging.warning(f"Skipping version '{version_str}': does not match any version pattern.")
                    continue
                version = version_match["version"].replace('-', '.')  # a.b.c-d => a.b.c.d

                date_str = td_list[1].get_text().strip()
                date_str = '2024-12-04' if date_str == '2024-12-041' else date_str  # there is a typo for 6.15.5
                date = dates.parse_date(date_str)

                product_data.declare_version(version, date)
