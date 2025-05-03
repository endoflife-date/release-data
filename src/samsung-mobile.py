import logging
import re
from datetime import date, datetime, time, timezone

from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

"""Detect new models and aggregate EOL data for Samsung Mobile devices.

This script works cumulatively: when a model is not listed anymore on https://security.samsungmobile.com/workScope.smsb
it retains the date and use it as the model's EOL date.
"""

TITLES_BY_UPDATE_CADENCE = {
    "monthly": "Current Models for Monthly Security Updates",
    "quarterly": "Current Models for Quarterly Security Updates",
    "biannual": "Current Models for Biannual Security Updates",
}

EXCLUDED_MODELS = {
    "galaxy-tab-a7-10.4-2022": "still available according to https://www.gsmarena.com/samsung_galaxy_tab_a7_10_4_(2022)-11988.php",
    "galaxy-watch5-pro": "will be tracked in a dedicated product",
    "galaxy-watch5": "will be tracked in a dedicated product",
    "galaxy-watch4-classic": "will be tracked in a dedicated product",
    "galaxy-watch4": "will be tracked in a dedicated product",
    "galaxy-m13-india": "still available according to https://www.gsmarena.com/samsung_galaxy_m13_(india)-11654.php",
    "galaxy-a13-sm-a137": "still available according to https://www.gsmarena.com/samsung_galaxy_a13_(sm_a137)-11665.php",
    "galaxy-a-quantum2": "still available according to https://www.gsmarena.com/samsung_galaxy_quantum_2-10850.php",
}

with releasedata.ProductData("samsung-mobile") as product_data:
    today = dates.today()

    frontmatter = endoflife.ProductFrontmatter(product_data.name)
    frontmatter_release_names = frontmatter.get_release_names()

    # Copy EOL dates from frontmatter to product data
    for frontmatter_release in frontmatter.get_releases():
        eol = frontmatter_release.get("eol")
        eol = datetime.combine(eol, time.min, tzinfo=timezone.utc) if isinstance(eol, date) else eol

        release = product_data.get_release(frontmatter_release.get("releaseCycle"))
        release.set_eol(eol)

    response = http.fetch_url("https://security.samsungmobile.com/workScope.smsb")
    soup = BeautifulSoup(response.text, features="html5lib")
    for update_cadence, title in TITLES_BY_UPDATE_CADENCE.items():
        models_list = soup.find(string=lambda text, search=title: search in text if text else False).find_next("ul")

        for item in models_list.find_all("li"):
            models = item.text.replace("Enterprise Models:", "")
            logging.info(f"Found {models} for {update_cadence} security updates")

            for model in re.split(r',\s*', models):
                name = endoflife.to_identifier(model)

                release = product_data.get_release(name)
                release.set_label(model.strip())

                if name in frontmatter_release_names:
                    frontmatter_release_names.remove(name)
                    current_eol = release.get_eol()
                    if current_eol is True or (isinstance(current_eol, datetime) and current_eol <= today):
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
        if eol_model_name in EXCLUDED_MODELS:
            logging.debug(f"Skipping model {eol_model_name}: {EXCLUDED_MODELS[eol_model_name]}")
        elif current_eol is False:
            logging.info(f"Model {eol_model_name} is not EOL, setting eol")
            release.set_eol(today)
        elif isinstance(current_eol, datetime):
            if current_eol > today:
                logging.info(f"Model {eol_model_name} is not marked as EOL, setting eol as {today}")
                release.set_eol(today)
            else:
                logging.debug(f"Model {eol_model_name} is already EOL, keeping eol as {current_eol}")
