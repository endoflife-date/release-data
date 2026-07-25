from src.common import releasedata
from src.common.endoflife import AutoConfig, ProductFrontmatter

"""Copy releases, without their properties, from product data (frontmatter) to release data.

This script is not intended to be declared in the frontmatter: it is for internal use only.
It executes before all other scripts, and helps the following scripts to work with releases.
"""

def update(product: ProductFrontmatter, _config: AutoConfig) -> None:
    with releasedata.ProductData(product.name) as product_data:
        for frontmatter_release in product.get_releases():
            product_data.get_release(frontmatter_release.get("releaseCycle"))
