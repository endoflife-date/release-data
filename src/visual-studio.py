from common import dates, endoflife, http, releasedata

for config in endoflife.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        html = http.fetch_html(config.url)

        for table in html.find_all("table"):
            headers = [th.get_text().strip().lower() for th in table.find_all("th")]
            if "version" not in headers or "release date" not in headers:
                continue

            version_index = headers.index("version")
            date_index = headers.index("release date")
            for row in table.findAll("tr"):
                cells = row.findAll("td")
                if len(cells) < (max(version_index, date_index) + 1):
                    continue

                version = cells[version_index].get_text().strip()
                date = cells[date_index].get_text().strip()
                date = dates.parse_date(date)

                if date and version and config.first_match(version):
                    product_data.declare_version(version, date)
