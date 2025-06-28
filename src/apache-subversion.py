import logging

from common import dates, http, releasedata

for config in releasedata.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        html = http.fetch_html(config.url)

        ul = html.find("h2").find_next("ul")
        for li in ul.find_all("li"):
            text = li.get_text(strip=True)
            match = config.first_match(text)
            if not match:
                logging.info(f"Skipping {text}, does not match any regex")
                continue

            version = match.group("version")
            date = dates.parse_date(match.group("date"))
            product_data.declare_version(version, date)
