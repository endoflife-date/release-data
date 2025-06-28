import logging
import re

from common import dates, endoflife, http, releasedata

"""Fetches releases from VirtualBox download page."""

EOL_REGEX = re.compile(r"^\(no longer supported, support ended (?P<value>\d{4}/\d{2})\)$")

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        html = http.fetch_html(config.url)


        for li in html.select_one("#DownloadVirtualBoxOldBuilds + ul").find_all("li"):
            li_text = li.find("a").text.strip()

            release_match = config.first_match(li_text)
            if not release_match:
                logging.info(f"Skipping '{li_text}': does not match expected pattern")
                continue

            release_name = release_match.group("value")
            release = product_data.get_release(release_name)

            eol_text = li.find("em").text.lower().strip()
            eol_match = EOL_REGEX.match(eol_text)
            if not eol_match:
                logging.info(f"Ignoring '{eol_text}': does not match {EOL_REGEX}")
                continue

            eol_date_str = eol_match.group("value")
            eol_date = dates.parse_month_year_date(eol_date_str)
            release.set_eol(eol_date)
