import json
import re
from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime

dbs = {
    "mysql": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/MySQL.Concepts.VersionMgmt.html",
    "postgresql": "https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-release-calendar.html",
}


def parse_date(d):
    return datetime.strptime(d, "%d %B %Y").strftime("%Y-%m-%d")


for db, url in dbs.items():
    print(f"::group::{db}")
    releases = {}

    response = endoflife.fetch_url(url)
    soup = BeautifulSoup(response, features="html5lib")

    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            columns = row.find_all("td")

            # Must match both the 'Supported XXX minor versions' and
            # 'Supported XXX major versions' to have correct release dates
            if len(columns) > 3:
                r = r"(?P<v>\d+(?:\.\d+)*)" # https://regex101.com/r/BY1vwV/1
                m = re.search(r, columns[0].text.strip(), flags=re.IGNORECASE)
                if m:
                    version = m.group("v")
                    date = parse_date(columns[2].text.strip())
                    print(f"{version} : {date}")
                    releases[version] = date

    print("::endgroup::")
    with open(f"releases/amazon-rds-{db.lower()}.json", "w") as f:
        json.dump(dict(
            # sort by date then version (desc)
            sorted(releases.items(), key=lambda x: (x[1], x[0]), reverse=True)
        ), f, indent=2)
