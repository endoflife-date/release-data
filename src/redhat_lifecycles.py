import logging
import urllib.parse

from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Fetches EOL dates from the Red Hat Product Life Cycle Data API.

This script works based on a definition provided in the product's frontmatter to map Red Hat phases to endoflife.date fields.

More information on https://docs.redhat.com/documentation/red_hat_product_life_cycle_data_api/.
"""

class Mapping:
    def __init__(self, phases_by_field: dict[str, str]) -> None:
        self.fields_by_phase = {v.lower(): k for k, v in phases_by_field.items()}

    def get_field_for(self, phase_name: str) -> str | None:
        return self.fields_by_phase.get(phase_name.lower(), None)

config = config_from_argv()
with ProductData(config.product) as product_data:
    name = urllib.parse.quote(config.url)
    mapping = Mapping(config.data["fields"])

    data = http.fetch_json('https://access.redhat.com/product-life-cycles/api/v1/products?name=' + name)

    for version in data["data"][0]["versions"]:
        version_name = version["name"]
        version_match = config.first_match(version_name)
        if not version_match:
            logging.warning(f"Ignoring version '{version_name}', config is {config}")
            continue

        release = product_data.get_release(config.render(version_match))
        for phase in version["phases"]:
            field = mapping.get_field_for(phase["name"])
            if not field:
                logging.debug(f"Ignoring phase '{phase['name']}': not mapped")
                continue

            date = dates.parse_datetime(phase["date"])
            release.set_field(field, date)
