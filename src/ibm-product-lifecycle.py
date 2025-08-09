import logging

from common import dates, http
from common.releasedata import ProductData, config_from_argv

"""Get release information from IBM's product lifecycle CSV file available.
See https://www.ibm.com/support/pages/product-lifecycle-list.
"""

def unquote(s: str) -> str:
    return s[1:-1] if s.startswith('"') and s.endswith('"') else s

config = config_from_argv()
with ProductData(config.product) as product_data:
    product_selector = config.data["product_selector"]
    response = http.fetch_url(config.url)

    records = response.text.splitlines()
    for record in records[1:]:  # Skip the header line
        fields = record.split(',')
        if len(fields) < 13:
            logging.warning("Skipping record with insufficient fields: %s", record)
            continue

        product_name = unquote(fields[1].strip())
        if product_selector != product_name:
            continue

        product_version = unquote(fields[2].strip())
        match = config.first_match(product_version)
        if not match:
            logging.warning("Skipping '%s' version %s, no match found", product_name, product_version)
            continue

        release_name = config.render(match)
        release = product_data.get_release(release_name)

        release_date_str = fields[6].strip()
        if release_date_str:
            logging.debug("Release announce for %s %s: %s", product_name, product_version, fields[7].strip())
            release_date = dates.parse_date(release_date_str)
            release.set_release_date(release_date)

        eol_date_str = fields[12].strip()
        if eol_date_str:
            logging.debug("EOL announce for %s %s: %s", product_name, product_version, fields[13].strip())
            eol_date = dates.parse_date(eol_date_str)
            release.set_eol(eol_date)

        eoes_date_str = fields[14].strip()
        if eoes_date_str:
            eoes_date = dates.parse_date(eoes_date_str)
            release.set_eoes(eoes_date)
