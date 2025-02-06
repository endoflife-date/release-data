import re

from bs4 import BeautifulSoup
from common import dates, http, releasedata

"""Fetches Amazon Aurora versions from the version management pages on AWS docs."""

PRODUCTS = {
    "aws-aurora-mysql": ["https://docs.aws.amazon.com/AmazonRDS/latest/AuroraMySQLReleaseNotes/AuroraMySQL.release-calendars.html"],
    "aws-aurora-postgresql": ["https://docs.aws.amazon.com/AmazonRDS/latest/AuroraPostgreSQLReleaseNotes/aurorapostgresql-release-calendar.html"],
}

VERSION_REGEX = re.compile(r"(?P<version>\d+(?:\.\d+)*)", flags=re.IGNORECASE)
FULL_DATE_REGEX = re.compile(
    r"(?P<version>\d+(?:\.\d+)*)", flags=re.IGNORECASE)


def convertDate(date_text: str, default_day=1) -> dates.date:
    try:
        date = dates.parse_date(date_text)
    except ValueError:
        date = dates.parse_month_year_date(
            date_text)
        date = date.replace(day=default_day)
    return date

def containsOneOf(text: str, substrings: list[str]) -> bool:
    for substring in substrings:
        if substring in text:
            return True
    return False

for product_name, urls in PRODUCTS.items():
    with releasedata.ProductData(product_name) as product_data:
        for url in urls:
            response = http.fetch_url(url)
            soup = BeautifulSoup(response.text, features="html5lib")

            for table in soup.find_all("table"):
                index = 0
                version_column = None
                release_date_column = None
                eoas_date_column = None
                eoes_date_column = None

                for row in table.find_all("th"):
                    if containsOneOf(row.text, ["Aurora major version","Aurora MySQL version","PostgreSQL major version","PostgreSQL minor engine version"]):
                        version_column = index
                    if containsOneOf(row.text, ["Aurora release date", "Aurora MySQL release date"]):
                        release_date_column = index
                    if containsOneOf(row.text, ["Aurora end of standard support date", "Aurora MySQL end of standard support date"]):
                        eoas_date_column = index
                    if containsOneOf(row.text, ["End of RDS Extended Support date", "RDS end of Extended Support date"]):
                        eoes_date_column = index
                    index += 1

                for row in table.find_all("tr"):
                    columns = row.find_all("td")
                    if len(columns) < 3:
                        continue

                    release_added = False
                    version_match = VERSION_REGEX.search(
                        columns[version_column].text.strip())
                    if version_match:
                        version = version_match.group("version")
                        releases = product_data.get_release(version)

                        if release_date_column is not None:
                            release_text = columns[release_date_column].text
                            try:
                                release_date = convertDate(release_text, 31)
                                product_data.declare_version(
                                    version, release_date)
                            except ValueError:
                                print(
                                    f"Failed to parse release date \"{release_text}\" for {product_name} {version}")

                        if eoas_date_column is not None:
                            eoas_text = columns[eoas_date_column].text
                            try:
                                eoas_date = convertDate(eoas_text)
                                releases.set_eoas(eoas_date)
                                release_added = True
                            except ValueError:
                                print(
                                    f"Failed to parse eoas date \"{eoas_text}\" for {product_name} {version}")

                        if eoes_date_column is not None:
                            eoes_text = columns[eoes_date_column].text
                            try:
                                eoes_date = convertDate(eoes_text)
                                releases.set_eoes(eoes_date)
                                release_added = True
                            except ValueError:
                                print(
                                    f"Failed to parse eoes date \"{eoes_text}\" for {product_name} {version}")

                        if not release_added:
                            product_data.remove_release(version)
