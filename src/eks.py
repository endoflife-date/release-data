import datetime
import json
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
                version = "%s-%s" % (k8s_version, eks_version)
                all_versions[version] = d
                print("%s: %s" % (version, d))
    print("::endgroup::")
    return all_versions


if __name__ == "__main__":
    versions = parse_platforms_page()
    with open("releases/eks.json", "w") as f:
        f.write(json.dumps(versions, indent=2))
