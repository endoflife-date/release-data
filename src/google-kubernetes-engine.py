import re

from common import dates, endoflife, http, releasedata

# https://regex101.com/r/zPxBqT/1
VERSION_PATTERN = re.compile(r"\d.\d+\.\d+-gke\.\d+")
URL_BY_PRODUCT = {
    "google-kubernetes-engine": "https://cloud.google.com/kubernetes-engine/docs/release-notes-nochannel",
    "google-kubernetes-engine-stable": "https://cloud.google.com/kubernetes-engine/docs/release-notes-stable",
    "google-kubernetes-engine-regular": "https://cloud.google.com/kubernetes-engine/docs/release-notes-regular",
    "google-kubernetes-engine-rapid": "https://cloud.google.com/kubernetes-engine/docs/release-notes-rapid",
}

for config in endoflife.list_configs_from_argv(): # noqa: B007 multiple JSON produced for historical reasons
    for product_name, url in URL_BY_PRODUCT.items():
        with releasedata.ProductData(product_name) as product_data:
            html = http.fetch_html(url)

            for section in html.find_all('section', class_='releases'):
                for h2 in section.find_all('h2'):  # h2 contains the date
                    date = dates.parse_date(h2.get('data-text'))

                    next_div = h2.find_next('div')  # The div next to the h2 contains the notes about changes made on that date
                    for li in next_div.find_all('li'):
                        if "versions are now available" in li.text:
                            for version in VERSION_PATTERN.findall(li.find('ul').text):
                                product_data.declare_version(version, date)
