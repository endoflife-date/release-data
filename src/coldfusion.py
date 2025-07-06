import re

from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches versions from Adobe ColdFusion release notes on helpx.adobe.com.

x.y.0 release dates are unfortunately not available in the release notes and have to updated them manually each time a
new minor version is released.
"""

VERSION_AND_DATE_PATTERN = re.compile(r"Release Date[,|:]? (.*?)\).*?Build Number: (.*?)$",
                                      re.DOTALL | re.MULTILINE | re.IGNORECASE)

# .0 release dates are not available in the release notes.
FIXED_VERSIONS = {
    "10.0.0": dates.date(2012, 5, 15),  # https://en.wikipedia.org/wiki/Adobe_ColdFusion#Adobe_ColdFusion_10
    "11.0.0": dates.date(2014, 4, 29),  # https://en.wikipedia.org/wiki/Adobe_ColdFusion#Adobe_ColdFusion_11
    "2016.0.0": dates.date(2016, 2, 16),  # https://en.wikipedia.org/wiki/Adobe_ColdFusion#Adobe_ColdFusion_(2016_Release)
    "2018.0.0": dates.date(2018, 7, 12),  # https://coldfusion.adobe.com/2018/07/new-coldfusion-release-adds-performance-monitoring-toolset-for-measuring-monitoring-and-managing-high-performing-web-apps/
    "2021.0.0": dates.date(2020, 11, 11),  # https://community.adobe.com/t5/coldfusion-discussions/introducing-adobe-coldfusion-2021-release/m-p/11585468
    "2023.0.0": dates.date(2022, 5, 16),  # https://coldfusion.adobe.com/2023/05/coldfusion2023-release/
}

config = config_from_argv()
with ProductData(config.product) as product_data:
    html = http.fetch_html(config.url)

    for p in html.findAll("div", class_="text"):
        version_and_date_str = p.get_text().strip().replace('\xa0', ' ')
        for (date_str, version_str) in VERSION_AND_DATE_PATTERN.findall(version_and_date_str):
            date = dates.parse_date(date_str)
            version = version_str.strip().replace(",", ".")  # 11,0,0,289974 -> 11.0.0.289974
            product_data.declare_version(version, date)

    product_data.declare_versions(FIXED_VERSIONS)
