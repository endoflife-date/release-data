from bs4 import BeautifulSoup
from common import endoflife

"""Fetch new AWS lambda runtimes from https://docs.aws.amazon.com.

This script does not retrieve release dates, as they are only available
in release announcements. Instead, it uses the release dates from the
endoflife.date product file. This has the advantage of being warned
about new releases, without having releaseDate information (wrongly)
updated.

If one day release dates are available in the AWS documentation, it would
be better to make use them though. Note that this would also be unnecessary
if it was possible to disable release / latest release dates updates in the
latest.py script.
"""

PRODUCT = 'aws-lambda'
URL = 'https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html'


def fetch_product_file_release_date(releaseCycle, product):
    if 'releases' in product.keys():
        for release in product['releases']:
            if releaseCycle == release['releaseCycle']:
                return release['releaseDate'].strftime("%Y-%m-%d")

    return '9999-12-31'


print(f"::group::{PRODUCT}")
releases_data = {}
try:
    releases_data = endoflife.load_product(PRODUCT)
except FileNotFoundError:
    releases_data = {}
    print(f"{PRODUCT} file not found, real release dates will not be used.")

response = endoflife.fetch_url(URL)
soup = BeautifulSoup(response, features="html5lib")

versions = {}
for row in soup.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) == 6:  # Supported Runtimes
        identifier = cells[1].get_text().strip()
    elif len(cells) == 5:  # Unsupported Runtimes
        identifier = cells[1].get_text().strip()
    else:  # Header rows
        continue

    date = fetch_product_file_release_date(identifier, releases_data)
    versions[identifier] = date
    print(f"{identifier}: {date}")

endoflife.write_releases(PRODUCT, versions)
print("::endgroup::")
