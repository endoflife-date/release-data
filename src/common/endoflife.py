import json
import frontmatter
from glob import glob
from os import path

# Handle versions having at least 2 digits (ex. 1.2) and at most 4 digits (ex. 1.2.3.4), with an optional leading "v".
# Major version must be >= 1.
DEFAULT_VERSION_REGEX = r"^v?(?P<major>[1-9]\d*)\.(?P<minor>\d+)(\.(?P<patch>\d+)(\.(?P<tiny>\d+))?)?$"
DEFAULT_TAG_TEMPLATE = "{{major}}.{{minor}}{% if patch %}.{{patch}}{% if tiny %}.{{tiny}}{%endif%}{%endif%}"


def load_product(product_name, pathname="website/products") -> frontmatter.Post:
    """Load the product's file frontmatter.
    """
    with open(f"{pathname}/{product_name}.md") as f:
        return frontmatter.load(f)


def list_products(method, products_filter=None, pathname="website/products") -> dict[str, list[dict]]:
    """Return a list of products that are using the same given update method.
    """
    products_with_method = {}

    for product_file in glob(f"{pathname}/*.md"):
        product_name = path.splitext(path.basename(product_file))[0]
        if products_filter and product_name != products_filter:
            continue

        with open(product_file) as f:
            data = frontmatter.load(f)
            if "auto" in data:
                configs = list(filter(
                    lambda config: method in config.keys(),
                    data["auto"]
                ))
                if len(configs) > 0:
                    products_with_method[product_name] = configs

    return products_with_method


# Keep the default timeout high enough to avoid errors with web.archive.org.


def write_releases(product, releases, pathname="releases") -> None:
    with open(f"{pathname}/{product}.json", "w") as f:
        f.write(json.dumps(dict(
            # sort by date then version (desc)
            sorted(releases.items(), key=lambda x: (x[1], x[0]), reverse=True)
        ), indent=2))
