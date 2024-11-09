import logging
import re
import sys

from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

"""Fetches EOL dates Atlassian EOL page.

The only needed argument is the last part of the product title identifier on the Atlassian EOL page,
such as `JiraSoftware` (from `AtlassianSupportEndofLifePolicy-JiraSoftware`).
"""

METHOD = "atlassian_eol"
REGEX = r"(?P<release>\d+(\.\d+)+) \(EOL date: (?P<date>.+)\).*$"
PATTERN = re.compile(REGEX, re.MULTILINE)

p_filter = sys.argv[1] if len(sys.argv) > 1 else None
m_filter = sys.argv[2] if len(sys.argv) > 2 else None
for config in endoflife.list_configs(p_filter, METHOD, m_filter):
    with releasedata.ProductData(config.product) as product_data:
        response = http.fetch_url('https://confluence.atlassian.com/support/atlassian-support-end-of-life-policy-201851003.html')
        soup = BeautifulSoup(response.text, features="html5lib")

        for li in soup.select(f"#AtlassianSupportEndofLifePolicy-{config.url}+ul li"):
            match = PATTERN.match(li.get_text(strip=True))
            if not match:
                logging.warning(f"Failed to parse EOL date from '{li.get_text(strip=True)}'")
                continue

            version = match.group("release")
            date = dates.parse_date(match.group("date"))
            releases = product_data.get_release(version)
            releases.set_eol(date)
