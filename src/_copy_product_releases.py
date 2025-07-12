from common import releasedata

"""Copy releases, without their properties, from product data (frontmatter) to release data.

This script is not intended to be declared in the frontmatter: it is for internal use only.
It executes before all other scripts, and helps the following scripts to work with releases.
"""

frontmatter, _ = releasedata.parse_argv(ignore_auto_config=True)
with releasedata.ProductData(frontmatter.name) as product_data:
    for frontmatter_release in frontmatter.get_releases():
        product_data.get_release(frontmatter_release.get("releaseCycle"))
