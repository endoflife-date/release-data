import sys

from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

METHOD = 'distrowatch'

p_filter = sys.argv[1] if len(sys.argv) > 1 else None
m_filter = sys.argv[2] if len(sys.argv) > 2 else None
for config in endoflife.list_configs(p_filter, METHOD, m_filter):
    with releasedata.ProductData(config.product) as product_data:
        response = http.fetch_url(f"https://distrowatch.com/index.php?distribution={config.url}")
        soup = BeautifulSoup(response.text, features="html5lib")

        for table in soup.select("td.News1>table.News"):
            headline = table.select_one("td.NewsHeadline a[href]").get_text().strip()
            versions_match = config.first_match(headline)
            if not versions_match:
                continue

            # multiple versions may be released at once (e.g. Ubuntu 16.04.7 and 18.04.5)
            versions = config.render(versions_match).split("\n")
            date = dates.parse_date(table.select_one("td.NewsDate").get_text())

            for version in versions:
                product_data.declare_version(version, date)
