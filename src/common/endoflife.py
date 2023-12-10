import frontmatter
import json
import logging
import os
from datetime import datetime
from glob import glob
logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.INFO)

# Handle versions having at least 2 digits (ex. 1.2) and at most 4 digits (ex. 1.2.3.4), with an optional leading "v".
# Major version must be >= 1.
DEFAULT_VERSION_REGEX = r"^v?(?P<major>[1-9]\d*)\.(?P<minor>\d+)(\.(?P<patch>\d+)(\.(?P<tiny>\d+))?)?$"
DEFAULT_TAG_TEMPLATE = "{{major}}.{{minor}}{% if patch %}.{{patch}}{% if tiny %}.{{tiny}}{%endif%}{%endif%}"

VERSIONS_PATH = os.environ.get("VERSIONS_PATH", "releases")


class Product:
    """Model an endoflife.date product.
    """

    def __init__(self, name: str):
        self.name: str = name
        self.versions = {}
        self.versions_path: str = f"{VERSIONS_PATH}/{name}.json"

    def has_version(self, version: str) -> bool:
        return version in self.versions

    def get_version_date(self, version: str) -> datetime:
        return self.versions[version] if version in self.versions else None

    def declare_version(self, version: str, date: datetime) -> None:
        if version in self.versions:
            if self.versions[version] != date:
                logging.warning(f"overwriting version {version} ({self.versions[version]} -> {date}) for {self.name}")
            else:
                return # already declared

        logging.info(f"adding version {version} ({date}) to {self.name}")
        self.versions[version] = date

    def declare_versions(self, dates_by_version: dict[str, datetime]) -> None:
        for (version, date) in dates_by_version.items():
            self.declare_version(version, date)

    def replace_version(self, version: str, date: datetime) -> None:
        if version not in self.versions:
            raise ValueError(f"version {version} cannot be replaced as it does not exist for {self.name}")

        logging.info(f"replacing version {version} ({self.versions[version]} -> {date}) to {self.name}")
        self.versions[version] = date

    def remove_version(self, version: str) -> None:
        if not self.has_version(version):
            logging.warning(f"version {version} cannot be removed as it does not exist for {self.name}")
            return

        logging.info(f"removing version {version} ({self.versions.pop(version)}) from {self.name}")

    def write(self) -> None:
        versions = {version: date.strftime("%Y-%m-%d") for version, date in self.versions.items()}
        with open(self.versions_path, "w") as f:
            f.write(json.dumps(dict(
                # sort by date then version (desc)
                sorted(versions.items(), key=lambda x: (x[1], x[0]), reverse=True)
            ), indent=2))

    def __repr__(self) -> str:
        return f"<{self.name}>"


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
        product_name = os.path.splitext(os.path.basename(product_file))[0]
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


def write_releases(product, releases, pathname="releases") -> None:
    with open(f"{pathname}/{product}.json", "w") as f:
        f.write(json.dumps(dict(
            # sort by date then version (desc)
            sorted(releases.items(), key=lambda x: (x[1], x[0]), reverse=True)
        ), indent=2))
