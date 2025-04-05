import logging
import sys
import urllib.parse

from common import dates, endoflife, http, releasedata

"""Fetches EOL dates from the Red Hat Product Life Cycle Data API.

This script works based on a definition provided in the product's frontmatter to map Red Hat phases to endoflife.date fields.

More information on https://docs.redhat.com/documentation/red_hat_product_life_cycle_data_api/.
"""

METHOD = "redhat_lifecycles"


class Mapping:
    def __init__(self, phases_by_field: dict[str, str]) -> None:
        self.fields_by_phase = {v.lower(): k for k, v in phases_by_field.items()}

    def get_field_for(self, phase_name: str) -> str | None:
        return self.fields_by_phase.get(phase_name.lower(), None)

p_filter = sys.argv[1] if len(sys.argv) > 1 else None
m_filter = sys.argv[2] if len(sys.argv) > 2 else None
for config in endoflife.list_configs(p_filter, METHOD, m_filter):
    with releasedata.ProductData(config.product) as product_data:
        name = urllib.parse.quote(config.url)
        mapping = Mapping(config.data["fields"])

        data = http.fetch_url('https://access.redhat.com/product-life-cycles/api/v1/products?name=' + name).json()

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
