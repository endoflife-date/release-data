from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches versions from repositories managed with cgit, such as the Linux kernel repository.
Ideally we would want to use the git repository directly, but cgit-managed repositories don't support partial clone."""

config = config_from_argv()
with ProductData(config.product) as product_data:
    html = http.fetch_html(config.url + '/refs/tags')

    for table in html.find_all("table", class_="list"):
        for row in table.find_all("tr"):
            columns = row.find_all("td")
            if len(columns) != 4:
                continue

            version_str = columns[0].text.strip()
            version_match = config.first_match(version_str)
            if not version_match:
                continue

            datetime_td = columns[3].find_next("span")
            datetime_str = datetime_td.attrs["title"] if datetime_td else None
            if not datetime_str:
                continue

            version = config.render(version_match)
            date = dates.parse_datetime(datetime_str)
            product_data.declare_version(version, date)
