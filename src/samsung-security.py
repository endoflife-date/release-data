import logging
import re
import sys
from datetime import date, datetime, time, timezone

from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

"""Detect new models and aggregate EOL data for Samsung Mobile devices.

This script works cumulatively: when a model is not listed anymore on https://security.samsungmobile.com/workScope.smsb
it retains the date and use it as the model's EOL date.
"""

TODAY = dates.today()

p_filter = sys.argv[1] if len(sys.argv) > 1 else None
m_filter = sys.argv[2] if len(sys.argv) > 2 else None
for config in endoflife.list_configs(p_filter, 'samsung-security', m_filter):
    with releasedata.ProductData(config.product) as product_data:
        frontmatter = endoflife.ProductFrontmatter(product_data.name)
        frontmatter_release_names = frontmatter.get_release_names()

        # Copy EOL dates from frontmatter to product data
        for frontmatter_release in frontmatter.get_releases():
            eol = frontmatter_release.get("eol")
            eol = datetime.combine(eol, time.min, tzinfo=timezone.utc) if isinstance(eol, date) else eol

            release = product_data.get_release(frontmatter_release.get("releaseCycle"))
            release.set_eol(eol)


        response = http.fetch_url(config.url)
        soup = BeautifulSoup(response.text, features="html5lib")

        sections = config.data.get("sections", {})
        for update_cadence, title in sections.items():
            models_list = soup.find(string=lambda text, search=title: search in text if text else False).find_next("ul")

            for item in models_list.find_all("li"):
                models = item.text.replace("Enterprise Models:", "")
                logging.info(f"Found {models} for {update_cadence} security updates")

                for model in re.split(r',\s*', models):
                    name = endoflife.to_identifier(model)
                    if config.is_excluded(name):
                        logging.debug(f"Ignoring model '{name}', excluded by configuration")
                        continue

                    release = product_data.get_release(name)
                    release.set_label(model.strip())

                    if name in frontmatter_release_names:
                        frontmatter_release_names.remove(name)
                        current_eol = release.get_eol()
                        if current_eol is True or (isinstance(current_eol, datetime) and current_eol <= TODAY):
                            logging.info(f"Known model {name} is incorrectly marked as EOL, updating eol")
                            release.set_eol(False)
                        else:
                            logging.debug(f"Known model {name} is not EOL, keeping eol as {current_eol}")

                    else:
                        logging.debug(f"Found new model {name}")
                        release.set_eol(False)

        # the remaining models in frontmatter_release_names are not listed anymore on the Samsung page => they are EOL
        for eol_model_name in frontmatter_release_names:
            release = product_data.get_release(eol_model_name)
            current_eol = release.get_eol()
            if config.is_excluded(eol_model_name):
                logging.debug(f"Skipping model {eol_model_name}, excluded by configuration")
            elif current_eol is False:
                logging.info(f"Model {eol_model_name} is not EOL, setting eol")
                release.set_eol(TODAY)
            elif isinstance(current_eol, datetime):
                if current_eol > TODAY:
                    logging.info(f"Model {eol_model_name} is not marked as EOL, setting eol as {TODAY}")
                    release.set_eol(TODAY)
                else:
                    logging.debug(f"Model {eol_model_name} is already EOL, keeping eol as {current_eol}")
