import re

from bs4 import BeautifulSoup
from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches versions from Adobe ColdFusion release notes on helpx.adobe.com."""

VERSION_AND_DATE_PATTERN = re.compile(r"Release Date[,|:]? (.*?)\).*?Build Number: (.*?)$",
                                      re.DOTALL | re.MULTILINE | re.IGNORECASE)

config = config_from_argv()
with ProductData(config.product) as product_data:
    html = BeautifulSoup(http.fetch_javascript_url(config.url), "html5lib")

    for p in html.findAll("div", class_="text"):
        version_and_date_str = p.get_text().strip().replace('\xa0', ' ')
        for (date_str, version_str) in VERSION_AND_DATE_PATTERN.findall(version_and_date_str):
            date = dates.parse_date(date_str)
            version = version_str.strip().replace(",", ".")  # 11,0,0,289974 -> 11.0.0.289974
            product_data.declare_version(version, date)
