import datetime
import re
from bs4 import BeautifulSoup
from common import http
from common import endoflife

URL = "https://www.paloaltonetworks.com/services/support/end-of-life-announcements/end-of-life-summary"
ID_MAPPING = {
    "pan-os-panorama": "pan-os",
    "globalprotect": "pan-gp",
    "traps-esm-and-cortex": "pan-cortex-xdr",
}


def update_releases(html_identifier, file):
    versions = {}

    print(f"::group::{html_identifier}")
    response = http.fetch_url(URL)
    soup = BeautifulSoup(response.text, features="html5lib")

    table = soup.find(id=html_identifier)
    for tr in table.findAll("tr")[3:]:
        td_list = tr.findAll("td")
        version = (
            td_list[0].get_text().strip().lower().replace(" ", "-").replace("*", "")
        )
        if file == "pan-xdr":
            if "xdr" not in version:
                continue
        version = version.removesuffix("-(cortex-xdr-agent)")
        version = version.removesuffix("-(vm-series-only)")
        version = version.removesuffix("-(panorama-only)")
        if len(td_list) > 1 and version != "":
            # Date formats differ between different products
            try:
                month, date, year = td_list[1].get_text().split("/")
                abs_date = f"{year}-{month:0>2}-{date:0>2}"
            except ValueError:
                # A few dates have 1st, 2nd, 4th etc. Fix that:
                d = td_list[1].get_text()
                d = re.sub(r'(\w+) (\d{1,2})(?:\w{2}), (\d{4})', r'\1 \2, \3', d)
                date = datetime.datetime.strptime(d, "%B %d, %Y")
                abs_date = date.strftime("%Y-%m-%d")

            versions[version] = abs_date
            print(f"{version}: {abs_date}")

    endoflife.write_releases(file, versions)
    print("::endgroup::")


for html_id in ID_MAPPING:
    update_releases(html_id, ID_MAPPING[html_id])
