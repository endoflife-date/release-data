import json
import urllib.request
import datetime
from bs4 import BeautifulSoup

URL = "https://www.paloaltonetworks.com/services/support/end-of-life-announcements/end-of-life-summary"

ID_MAPPING = {
    "pan-os-panorama": "pan-os",
    "globalprotect": "pan-gp",
    "traps-esm-and-cortex": "pan-xdr",
}


def update_releases(html_identifier, file):
    versions = {}
    with urllib.request.urlopen(URL, data=None, timeout=5) as response:
        soup = BeautifulSoup(response, features="html5lib")
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
            try:
                month, date, year = td_list[1].get_text().split("/")
                abs_date = f"{year}-{month:0>2}-{date:0>2}"
            except Exception:
                date = datetime.datetime.strptime(td_list[1].get_text(), "%B %d, %Y")
                abs_date = date.strftime("%Y-%m-%d")

            versions[version] = abs_date

    with open("releases/%s.json" % file, "w") as f:
        f.write(json.dumps(versions, indent=2))


for html_id in ID_MAPPING:
    update_releases(html_id, ID_MAPPING[html_id])
