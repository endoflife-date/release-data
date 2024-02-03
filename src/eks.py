from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

"""Fetches EKS versions from AWS docs.
Now that AWS no longer publishes docs on GitHub, we use the Web Archive to still get the older versions."""

URLS = [
    # 1.19.eks.1
    "https://web.archive.org/web/20221007150452/https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html",
    # + 1.20
    "https://web.archive.org/web/20230521061347/https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html",
    # + latest
    "https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html",
]

with releasedata.ProductData("eks") as product_data:
    for version_list in http.fetch_urls(URLS):
        version_list_soup = BeautifulSoup(version_list.text, features="html5lib")
        for tr in version_list_soup.select("#main-col-body")[0].findAll("tr"):
            cells = tr.findAll("td")
            if not cells:
                continue

            k8s_version = cells[0].text.strip()
            eks_version = cells[1].text.strip()
            date_str = cells[-1].text.strip()

            k8s_version_match = endoflife.DEFAULT_VERSION_PATTERN.match(k8s_version)
            if k8s_version_match:
                date = dates.parse_date(date_str)
                # K8S patch version is not kept to match versions on https://github.com/aws/eks-distro/tags.
                version = f"{k8s_version_match.group('major')}.{k8s_version_match.group('minor')}-{eks_version.replace('.', '-')}"
                product_data.declare_version(version, date)
