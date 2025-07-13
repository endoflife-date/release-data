import logging

from common import dates, releasedata

"""Remove empty releases or releases which are released in the future."""

TODAY = dates.today()

frontmatter, _ = releasedata.parse_argv(ignore_auto_config=True)
with releasedata.ProductData(frontmatter.name) as product_data:
    releases = list(product_data.releases.values()) # a copy is needed to avoid modifying the dict while iterating
    product_data.updated = True # mark the product data as updated even when there are no changes

    for release in releases:
        if release.is_empty():
            product_data.remove_release(release.name())
            logging.info(f"Removed empty release {release} from {product_data.name}")
            continue

        if release.was_released_after(TODAY):
            product_data.remove_release(release.name())
            logging.info(f"Removed future release {release} from {product_data.name}")
            continue

        logging.debug(f"Keeping release {release} in {product_data.name}")
