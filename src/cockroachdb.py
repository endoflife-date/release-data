import re

from bs4 import BeautifulSoup
from common import dates, http, releasedata

VERSION_REGEX = re.compile(r"(?P<version>\d+(?:\.\d+)*)", flags=re.IGNORECASE) # https://regex101.com/r/ifoWfx/1

with releasedata.ProductData("cockroachdb") as product_data:
    releases_response = http.fetch_url('https://www.cockroachlabs.com/docs/releases/release-support-policy')
    releases_soup = BeautifulSoup(releases_response.text, features="html5lib")

    for table in releases_soup.find_all("table"):
        for row in table.find_all("tr"):
            columns = row.find_all("td")
            if len(columns) <= 3:
                continue

            version_match = VERSION_REGEX.search(columns[0].text.strip())
            if not version_match:
                continue

            release_version = version_match.group("version")
            release = product_data.get_release(release_version)
            release.set_release_date(dates.parse_date(columns[1].text))
            release.set_support(dates.parse_date(columns[2].text))
            release.set_eol(dates.parse_date(columns[3].text))

            # versions
            release_response = http.fetch_url('https://www.cockroachlabs.com/docs/releases/v'+release_version)
            release_soup = BeautifulSoup(release_response.text, features="html5lib")

            content = release_soup.find(class_="post-content")
            for version in content.find_all("h2"):
                if not version.find_next("p").text.startswith("Release Date"):
                    continue

                version_release_date = version.find_next("p").text.removeprefix("Release Date:").strip()
                if len(version_release_date) == 0:
                    continue

                product_data.declare_version(version.text, dates.parse_date(version_release_date))
