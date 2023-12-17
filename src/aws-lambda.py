import datetime
from bs4 import BeautifulSoup
from common import http
from common import endoflife

"""Fetches AWS lambda runtimes from https://docs.aws.amazon.com.

This script does not retrieve release dates, as they are only available in release announcements.
Instead, it uses the release dates from the endoflife.date product file, or alternatively the
date the release was first detected (or the current date if none is found).

If one day release dates are available in the AWS documentation, it would be better to make use
them though. Note that this would also be unnecessary if it was possible to disable release/latest
release dates updates in the latest.py script."""

print("::group::aws-lambda")
product = endoflife.Product("aws-lambda", load_product_data=True, load_versions_data=True)
response = http.fetch_url("https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html")
soup = BeautifulSoup(response.text, features="html5lib")

for table in soup.find_all("table"):
    headers = [th.get_text().strip().lower() for th in table.find("thead").find_all("tr")[1].find_all("th")]
    if "identifier" not in headers:
        continue

    identifier_index = headers.index("identifier")
    for row in table.find("tbody").find_all("tr"):
        cells = row.find_all("td")
        identifier = cells[identifier_index].get_text().strip()

        date = product.get_release_date(identifier)  # use the product releaseDate if available
        if date is None:
            date = product.get_old_version_date(identifier)  # else use the previously found date
        if date is None:
            date = datetime.date.today()  # else use today's date

        product.declare_version(identifier, date)

product.write()
print("::endgroup::")
