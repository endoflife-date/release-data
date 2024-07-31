import re

from bs4 import BeautifulSoup
from common import dates, http, releasedata

# https://regex101.com/r/CwvyT3/2 only non beta versions
VERSION_PATTERN = re.compile(r"^(?:Subversion\s)(\d.\d+\.\d+$)")
# https://regex101.com/r/GsimYd/1
DATE_PATTERN = re.compile(r"^(?:\s\()(\w+,\s\d{1,2}\s\w+\s\d{4})")
URL = "https://subversion.apache.org/docs/release-notes/release-history.html"

with releasedata.ProductData("svn") as product_data:
    relnotes = http.fetch_url(URL)
    relnotes_soup = BeautifulSoup(relnotes.text, features="html5lib")

    ul = relnotes_soup.find("h2").find_next("ul")
    for li in ul.find_all("li"):
        b = li.find_next("b") # b contains the version
        if (version := VERSION_PATTERN.match(b.text)) is not None:
            # version found
            version = version.group(1)
            if (remaining_part := b.next_sibling) is not None:
                if (date := DATE_PATTERN.match(remaining_part)) is not None:
                    # date found
                    date = dates.parse_date(date.group(1))  
                    product_data.declare_version(version, date)
