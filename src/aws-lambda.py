
from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

"""Fetches AWS lambda runtimes from https://docs.aws.amazon.com.

This script does not retrieve release dates, as they are only available in release announcements.
Instead, it uses the release dates from the endoflife.date product file, or alternatively the
date the release was first detected (or the current date if none is found).

If one day release dates are available in the AWS documentation, it would be better to make use
them though. Note that this would also be unnecessary if it was possible to disable release/latest
release dates updates in the latest.py script."""

with releasedata.ProductData("aws-lambda") as product_data:
    product_frontmatter = endoflife.ProductFrontmatter(product_data.name)
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

            date = product_frontmatter.get_release_date(identifier)  # use the product releaseDate if available
            if date is None:
                date = dates.today()  # else use today's date

            product_data.declare_version(identifier, date)
