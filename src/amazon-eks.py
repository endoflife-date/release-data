import logging

from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

"""Fetches EKS versions from AWS docs.
Now that AWS no longer publishes docs on GitHub, we use the Web Archive to get the older versions."""

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        response = http.fetch_url(config.url)
        html = BeautifulSoup(response.text, features="html5lib")
        for tr in html.select("#main-col-body")[0].findAll("tr"):
            cells = tr.findAll("td")
            if not cells:
                continue

            k8s_version_text = cells[0].text.strip()
            k8s_version_match = config.first_match(k8s_version_text)
            if not k8s_version_match:
                logging.warning(f"Skipping {k8s_version_text}: does not match version regex(es)")
                continue

            eks_version = cells[1].text.strip()
            # K8S patch version is not kept to match versions on https://github.com/aws/eks-distro/tags
            version = f"{k8s_version_match.group('major')}.{k8s_version_match.group('minor')}-{eks_version.replace('.', '-')}"

            date_str = cells[-1].text.strip()
            date_str = date_str.replace("April 18.2025", "April 18 2025") # temporary fix for a typo in the source
            date = dates.parse_date_or_month_year_date(date_str)

            product_data.declare_version(version, date)
