import datetime
from bs4 import BeautifulSoup
from common import endoflife
from datetime import datetime


URLS = [
    "https://docs.redis.com/latest/rs/installing-upgrading/product-lifecycle/"
]


def parse():
    all_versions = {}
    print("::group::redis")
    for url in URLS:
        response = endoflife.fetch_url(url)
        soup = BeautifulSoup(response, features="html5lib")
        for tr in soup.select("table")[0].findAll("tr")[1:]:
            td_list = tr.findAll("td")
            # split on En Dash unicode U+2013
            version = td_list[0].get_text().strip().split("–")[0].strip()
            date_text = td_list[1].get_text().strip()
            if len(date_text) > 1:
                d = datetime.strptime(date_text, "%B %d, %Y").strftime("%Y-%m-%d")
                all_versions[version] = d
                print(f"{version}: {d}")
    print("::endgroup::")
    return all_versions

versions = parse()
endoflife.write_releases('redis', versions)
