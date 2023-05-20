import datetime
import markdown
import re
from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime

URL = "https://raw.githubusercontent.com/awsdocs/amazon-eks-user-guide/master/doc_source/platform-versions.md"
REGEX = r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$"


def parse_platforms_page():
    all_versions = {}
    print("::group::eks")
    response = endoflife.fetch_url(URL)
    html = markdown.markdown(response, extensions=["tables"])
    soup = BeautifulSoup(html, features="html5lib")
    for tr in soup.findAll("tr"):
        td = tr.find("td")
        if td and re.match(REGEX, td.text):
            data = tr.findAll("td")
            date = data[-1].text
            if len(date) > 0:
                d = datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d")
                k8s_version = ".".join(data[0].text.split(".")[:-1])
                eks_version = data[1].text.replace(".", "-")
                version = f"{k8s_version}-{eks_version}"
                all_versions[version] = d
                print(f"{version}: {d}")
    print("::endgroup::")
    return all_versions


versions = parse_platforms_page()
endoflife.write_releases('eks', versions)
