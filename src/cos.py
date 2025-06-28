import datetime
import re

from bs4 import BeautifulSoup
from common import dates, http, releasedata

MILESTONE_PATTERN = re.compile(r'COS \d+ LTS')
VERSION_PATTERN = re.compile(r"^(cos-\d+-\d+-\d+-\d+)")


def parse_date(date_text: str) -> datetime:
    date_text = date_text.strip().replace('Date: ', '')
    date_text = re.sub(r'Sep[a-zA-Z]+', 'Sep', date_text)
    return dates.parse_date(date_text)


for config in releasedata.list_configs_from_argv():
    with releasedata.ProductData(config.product) as product_data:
        main = http.fetch_url(config.url)
        main_soup = BeautifulSoup(main.text, features="html5lib")
        milestones = [cell.text.split(' ')[1] for cell in main_soup.find_all('td', string=MILESTONE_PATTERN)]

        milestones_urls = [f"{main.url}m{milestone}" for milestone in milestones]
        for milestone in http.fetch_urls(milestones_urls):
            milestone_soup = BeautifulSoup(milestone.text, features="html5lib")
            for article in milestone_soup.find_all('article', class_='devsite-article'):
                for heading in article.find_all(['h2', 'h3']):  # headings contains the date, which we parse
                    version_str = heading.get('data-text')
                    version_match = VERSION_PATTERN.match(version_str)
                    if not version_match:
                        continue

                    try:  # 1st row is the header, so pick the first td in the 2nd row
                        date_str = heading.find_next('tr').find_next('tr').find_next('td').text
                    except AttributeError:  # In some older releases, it is mentioned as Date: [Date]
                        date_str = heading.find_next('i').text

                    try:
                        date = parse_date(date_str)
                    except ValueError:  # for some h3, the date is in the previous h2
                        date_str = heading.find_previous('h2').get('data-text')
                        date = parse_date(date_str)

                    product_data.declare_version(version_match.group(1), date)
