import logging
import re

from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches releases from https://www.freebsd.org."""

VERSION_AND_DATE_PATTERN = re.compile(r"^(Release )?(?P<release>\d+\.\d+)\s*\((?P<date>\w+( \d+)?, \d+)\)")

config = config_from_argv()
with ProductData(config.product) as product_data:
    html = http.fetch_html(config.url)

    for li in html.select("li"):
        text = li.get_text(strip=True)

        match = VERSION_AND_DATE_PATTERN.search(text)
        if not match:
            logging.debug(f"Skipping {text}, does not match pattern")
            continue

        logging.debug(f"Processing {text}")
        release_name = match.group("release")
        release = product_data.get_release(release_name)
        release.set_field('releaseLabel', f"releng/{release_name}")

        release_date = dates.parse_date_or_month_year_date(match.group("date"))
        release.set_release_date(release_date)
