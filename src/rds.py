import re
from bs4 import BeautifulSoup
from common import http
from common import dates
from common import endoflife

VERSION_REGEX = r"(?P<v>\d+(?:\.\d+)*)"  # https://regex101.com/r/BY1vwV/1
DBS = {
    "mysql": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/MySQL.Concepts.VersionMgmt.html",
    "postgresql": "https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-release-calendar.html",
}

for db, url in DBS.items():
    print(f"::group::{db}")
    versions = {}

    response = http.fetch_url(url)
    soup = BeautifulSoup(response.text, features="html5lib")

    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            columns = row.find_all("td")

            # Must match both the 'Supported XXX minor versions' and
            # 'Supported XXX major versions' to have correct release dates
            if len(columns) > 3:
                m = re.search(VERSION_REGEX, columns[0].text.strip(), flags=re.IGNORECASE)
                if m:
                    date = dates.parse_date(columns[2].text).strftime("%Y-%m-%d")
                    if date:
                        version = m.group("v")
                        print(f"{version} : {date}")
                        versions[version] = date

    endoflife.write_releases(f"amazon-rds-{db.lower()}", versions)
    print("::endgroup::")
