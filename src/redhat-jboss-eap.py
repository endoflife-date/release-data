import logging

from bs4 import BeautifulSoup
from common import dates, http, releasedata

"""Fetches RedHat JBoss EAP releases and versions"""

VERSION_URLS = [
    "https://docs.redhat.com/en/documentation/red_hat_jboss_enterprise_application_platform/7.4/",
    "https://docs.redhat.com/en/documentation/red_hat_jboss_enterprise_application_platform/8.0/"
]

RELEASES_INFO = "https://access.redhat.com/product-life-cycles/api/v1/products?name=Red%20Hat%20JBoss%20Enterprise%20Application%20Platform"

# Given a dict, find inside the list of phases the one that matches the phase_name, extract and parse it's associated date
def find_date_field(elem, phase_name):
    entry = list(filter(lambda it: it.get("name") == phase_name, elem["phases"]))[0]
    return dates.parse_datetime(entry["date"])

with releasedata.ProductData("redhat-jboss-eap") as product_data:
    # Versions
    for response in http.fetch_urls(VERSION_URLS):
        soup = BeautifulSoup(response.text, features="html5lib")
        # Find all links inside a H3 heading
        links = [heading.find("a") for (i, heading) in enumerate(soup.find_all("h3")) if heading.find("a")]
        # From those links, keep the ones pointing to access.redhat.com containing the text " Update "
        links = [link for link in links if link.get("href").startswith("https://access.redhat.com/articles") and link.getText().find(" Update ") > 0]

        # For every link, get the last modified date of the associated knowledge base article and create a version entry
        for link in links:
            name = link.getText().strip()
            # Clean up the name to obtain an identifier in the form X.Y.Z[.W]
            identifier = name.replace(" Update", "").replace(" 0", ".").replace(" ", ".")
            article_url = link.get("href")
            article_response = http.fetch_url(article_url)
            article_soup = BeautifulSoup(article_response.text, features="html5lib")
            date_header = article_soup.find(class_="header")
            date_str = date_header.find("time").getText().strip()
            date = dates.parse_datetime(date_str)
            product_data.declare_version(identifier, date)

    # Releases
    response_json = http.fetch_url(RELEASES_INFO).json()
    for release_info in response_json["data"][0]["versions"]:
        release_name = release_info["name"].replace(".x", "")
        release = product_data.get_release(release_name)
        release.set_release_date(find_date_field(release_info, "General availability"))
        release.set_eoas(find_date_field(release_info, "Full support"))        
        release.set_eol(find_date_field(release_info, "Maintenance support"))
        release.set_eoes(find_date_field(release_info, "Extended life cycle support (ELS) 1"))
