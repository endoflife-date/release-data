from bs4 import BeautifulSoup
from common import dates, http, releasedata

with releasedata.ProductData("graalvm") as product_data:
    release_calendar = http.fetch_url("https://www.graalvm.org/release-calendar/")
    release_calendar_soup = BeautifulSoup(release_calendar.text, features="html5lib")

    for tr in release_calendar_soup.find("h2", id="previous-releases").find_next("table").find("tbody").findAll("tr"):
        cells = tr.findAll("td")
        date = dates.parse_date(cells[0].get_text())

        # 'GraalVM for JDK' versions has to be prefixed as their release cycle collide with older
        # GraalVM release cycles. Example: GraalVM for JDK 20 and 20.0.
        versions_str = cells[2].get_text().replace("GraalVM for JDK ", "jdk-")
        for version in versions_str.split(", "):
            product_data.declare_version(version, date)
