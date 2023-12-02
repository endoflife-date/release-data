import re
from bs4 import BeautifulSoup
from common import http
from common import dates
from common import endoflife

# Now that AWS no longer publishes docs on GitHub,
# we use the Web Archive to still get the older versions
# Keep older pages at top of the list
URLS = [
    # 1.19.eks.1
    # Disabled, too much timed out.
    # "https://web.archive.org/web/20221007150452/https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html",
    # + 1.20
    # Disabled, too much timed out.
    # "https://web.archive.org/web/20230521061347/https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html",
    # + latest
    "https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html",
]


def parse_platforms_pages():
    all_versions = {}
    print("::group::eks")
    for url in URLS:
        response = http.fetch_url(url)
        soup = BeautifulSoup(response.text, features="html5lib")
        for tr in soup.select("#main-col-body")[0].findAll("tr"):
            td = tr.find("td")
            if td and re.match(endoflife.DEFAULT_VERSION_REGEX, td.text.strip()):
                data = tr.findAll("td")
                date = data[-1].text.strip()
                if len(date) > 0:
                    d = dates.parse_date(date).strftime("%Y-%m-%d")
                    k8s_version = ".".join(data[0].text.strip().split(".")[:-1])
                    eks_version = data[1].text.strip().replace(".", "-")
                    version = f"{k8s_version}-{eks_version}"
                    all_versions[version] = d
                    print(f"{version}: {d}")
    print("::endgroup::")
    return all_versions


versions = parse_platforms_pages()
endoflife.write_releases('eks', versions)
