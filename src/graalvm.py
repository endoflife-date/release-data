from bs4 import BeautifulSoup
from common import http
from common import dates
from common import endoflife

product = endoflife.Product("graalvm")
print(f"::group::{product.name}")
release_calendar = http.fetch_url("https://www.graalvm.org/release-calendar/")
release_calendar_soup = BeautifulSoup(release_calendar.text, features="html5lib")

for tr in release_calendar_soup.findAll("table")[1].find("tbody").findAll("tr"):
    cells = tr.findAll("td")
    date = dates.parse_date(cells[0].get_text())

    # 'GraalVM for JDK' versions has to be prefixed as their release cycle collide with older
    # GraalVM release cycles. Example: GraalVM for JDK 20 and 20.0.
    versions_str = cells[2].get_text().replace("GraalVM for JDK ", "jdk-")
    for version in versions_str.split(", "):
        product.declare_version(version, date)

product.write()
print("::endgroup::")
