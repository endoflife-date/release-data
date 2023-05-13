import frontmatter

from glob import glob
from os import path


def list_products(method, products_filter=None, pathname = "website/products"):
    """Return a list of products that are using the same given update method.
    """
    products_with_method = {}

    for product_file in glob(f"{pathname}/*.md"):
        product_name = path.splitext(path.basename(product_file))[0]
        if products_filter and product_name != products_filter:
            continue

        with open(product_file, "r") as f:
            data = frontmatter.load(f)
            if "auto" in data:
                configs = list(filter(
                    lambda config: method in config.keys(),
                    data["auto"]
                ))
                if len(configs) > 0:
                    products_with_method[product_name] = configs

    return products_with_method
