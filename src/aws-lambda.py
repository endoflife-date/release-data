from bs4 import BeautifulSoup
from common import http
from common import endoflife
from datetime import datetime

"""Fetches AWS lambda runtimes from https://docs.aws.amazon.com.

This script does not retrieve release dates, as they are only available in release announcements.
Instead, it uses the release dates from the endoflife.date product file. This has the advantage of
being warned about new releases, without having releaseDate information (wrongly) updated.

If one day release dates are available in the AWS documentation, it would be better to make use
them though. Note that this would also be unnecessary if it was possible to disable release/latest
release dates updates in the latest.py script."""


def get_release_data(product):
    try:
        return endoflife.load_product(product.name)
    except FileNotFoundError:
        print(f"{product.name} file not found, real release dates will not be used.")
        return {}


def release_date(releaseCycle, releases_data):
    if 'releases' in releases_data.keys():
        for release in releases_data['releases']:
            if releaseCycle == release['releaseCycle']:
                return release['releaseDate']

    return datetime.now()


product = endoflife.Product("aws-lambda")
print(f"::group::{product.name}")
releases_data = get_release_data(product)
response = http.fetch_url("https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html")
soup = BeautifulSoup(response.text, features="html5lib")

for row in soup.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) != 6 and len(cells) != 5: # 6 = Supported Runtimes, 5 = Unsupported Runtimes
        continue

    identifier = cells[1].get_text().strip()
    date = release_date(identifier, releases_data)
    product.declare_version(identifier, date)

product.write()
print("::endgroup::")
