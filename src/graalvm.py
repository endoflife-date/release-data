from bs4 import BeautifulSoup
from common import dates
from common import endoflife

URL = "https://www.graalvm.org/release-calendar/"
# https://regex101.com/r/877ibq/1
regex = r"RHEL (?P<major>\d)(\. ?(?P<minor>\d+))?(( Update (?P<minor2>\d))| GA)?"

def split_versions(text):
    # GraalVM for JDK versions has to be prefixed as their release cycle collide
    # with older GraalVM release cycles. Example: GraalVM for JDK 20 and 20.0.
    return text.replace("GraalVM for JDK ", "jdk-").split(", ")

print("::group::graalvm")
response = endoflife.fetch_url(URL)
soup = BeautifulSoup(response, features="html5lib")

versions = {}
for tr in soup.findAll("table")[1].find("tbody").findAll("tr"):
    td_list = tr.findAll("td")
    date = dates.parse_date(td_list[0].get_text()).strftime("%Y-%m-%d")

    for version in split_versions(td_list[2].get_text()):
        versions[version] = date
        print(f"{version}: {date}")

endoflife.write_releases('graalvm', versions)
print("::endgroup::")
