import re
import sys
from bs4 import BeautifulSoup
from common import http
from common import dates
from common import endoflife
from liquid import Template

"""Fetch versions with their dates from a cgit repository, such as
https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git.

Ideally we would want to use the git repository directly, but cgit repositories
do not support partial clone so we cannot.
"""

METHOD = 'cgit'


def fetch_releases(url, regex, template):
    releases = {}

    response = http.fetch_url(url + '/refs/tags')
    soup = BeautifulSoup(response.text, features="html5lib")
    l_template = Template(template)

    for table in soup.find_all("table", class_="list"):
        for row in table.find_all("tr"):
            columns = row.find_all("td")
            if len(columns) == 4:
                version_text = columns[0].text.strip()
                datetime_td = columns[3].find_next("span")
                datetime_text = datetime_td.attrs["title"] if datetime_td else None
                if datetime_text:
                    matches = re.match(regex.strip(), version_text)
                    if matches:
                        match_data = matches.groupdict()
                        version_string = l_template.render(**match_data)
                        date = dates.parse_datetime(datetime_text).strftime("%Y-%m-%d")
                        print(f"{version_string} : {date}")
                        releases[version_string] = date

    return releases


def update_product(product_name, configs):
    versions = {}

    for config in configs:
        t = config.get("template", endoflife.DEFAULT_TAG_TEMPLATE)
        regex = config.get("regex", endoflife.DEFAULT_VERSION_REGEX)
        versions = versions | fetch_releases(config[METHOD], regex, t)

    endoflife.write_releases(product_name, versions)


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product, configs in endoflife.list_products(METHOD, p_filter).items():
    print(f"::group::{product}")
    update_product(product, configs)
    print("::endgroup::")
