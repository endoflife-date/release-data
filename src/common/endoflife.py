import json
import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import frontmatter
from liquid import Template

# Do not update the format: it's also used to declare groups in the GitHub Actions logs.
logging.basicConfig(format="%(message)s", level=logging.INFO)

# Handle versions having at least 2 digits (ex. 1.2) and at most 4 digits (ex. 1.2.3.4), with an optional leading "v".
# Major version must be >= 1.
DEFAULT_VERSION_REGEX = r"^v?(?P<major>[1-9]\d*)\.(?P<minor>\d+)(\.(?P<patch>\d+)(\.(?P<tiny>\d+))?)?$"
DEFAULT_VERSION_PATTERN = re.compile(DEFAULT_VERSION_REGEX)
DEFAULT_VERSION_TEMPLATE = "{{major}}{% if minor %}.{{minor}}{% if patch %}.{{patch}}{% if tiny %}.{{tiny}}{% endif %}{% endif %}{% endif %}"

PRODUCTS_PATH = Path(os.environ.get("PRODUCTS_PATH", "website/products"))
VERSIONS_PATH = Path(os.environ.get("VERSIONS_PATH", "releases"))


class AutoConfig:
    def __init__(self, method: str, config: dict) -> None:
        self.method = method
        self.url = config[method]
        self.version_template = Template(config.get("template", DEFAULT_VERSION_TEMPLATE))

        regexes = config.get("regex", DEFAULT_VERSION_REGEX)
        regexes = regexes if isinstance(regexes, list) else [regexes]
        self.version_patterns = [re.compile(regex) for regex in regexes]

    def first_match(self, version: str) -> re.Match | None:
        for pattern in self.version_patterns:
            match = pattern.match(version)
            if match:
                return match
        return None

    def render(self, match: re.Match) -> str:
        return self.version_template.render(**match.groupdict())


class ProductFrontmatter:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.path: Path = PRODUCTS_PATH / f"{name}.md"

        self.data = None
        if self.path.is_file():
            with self.path.open() as f:
                self.data = frontmatter.load(f)
                logging.info(f"loaded product data for {self.name} from {self.path}")
        else:
            logging.warning(f"no product data found for {self.name} at {self.path}")

    def get_auto_configs(self, method: str) -> list[AutoConfig]:
        configs = []

        if "auto" in self.data:
            for config in self.data["auto"]:
                if method in config:
                    configs.append(AutoConfig(method, config))

        if len(configs) > 0 and len(configs) != len(self.data["auto"]):
            logging.error(f"mixed auto-update methods declared for {self.name}, this is not yet supported")

        return configs

    def get_release_date(self, release_cycle: str) -> datetime | None:
        for release in self.data["releases"]:
            if release["releaseCycle"] == release_cycle:
                return release["releaseDate"]
        return None


class ProductVersion:
    def __init__(self, product: "Product", name: str, date: datetime) -> None:
        self.product = str(product)
        self.name = name
        self.date = date

    @staticmethod
    def from_json(product: "Product", data: dict) -> "ProductVersion":
        name = data["name"]
        date = datetime.strptime(data["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return ProductVersion(product, name, date)

    def __dict__(self) -> dict:
        return {
            "name": self.name,
            "date": self.date.strftime("%Y-%m-%d"),
        }

    def __repr__(self) -> str:
        return f"{self.product}#{self.name} ({self.date})"


class Product:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.versions_path: Path = VERSIONS_PATH / f"{name}.json"
        self.versions: dict[str, ProductVersion] = {}
        logging.info(f"::group::{self}")

    @staticmethod
    def from_file(name: str) -> "Product":
        product = Product(name)

        if product.versions_path.is_file():
            with product.versions_path.open() as f:
                for json_version in json.load(f)["versions"].values():
                    version = ProductVersion.from_json(product, json_version)
                    product.versions[version.name] = version
            logging.info(f"loaded versions data for {product} from {product.versions_path}")
        else:
            logging.warning(f"no versions data found for {product} at {product.versions_path}")

        return product

    def has_version(self, version: str) -> bool:
        return version in self.versions

    def get_version_date(self, version: str) -> datetime:
        return self.versions[version].date if version in self.versions else None

    def declare_version(self, version: str, date: datetime) -> None:
        if version in self.versions:
            if self.versions[version].date != date:
                logging.warning(f"overwriting {version} ({self.get_version_date(version)} -> {date}) for {self}")
            else:
                return  # already declared

        logging.info(f"adding version {version} ({date}) to {self}")
        self.versions[version] = ProductVersion(self, version, date)

    def declare_versions(self, dates_by_version: dict[str, datetime]) -> None:
        for (version, date) in dates_by_version.items():
            self.declare_version(version, date)

    def replace_version(self, version: str, date: datetime) -> None:
        if version not in self.versions:
            msg = f"version {version} cannot be replaced as it does not exist for {self}"
            raise ValueError(msg)

        logging.info(f"replacing version {version} ({self.get_version_date(version)} -> {date}) in {self}")
        self.versions[version].date = date

    def remove_version(self, version: str) -> None:
        if not self.has_version(version):
            logging.warning(f"version {version} cannot be removed as it does not exist for {self}")
            return

        logging.info(f"removing version {version} ({self.versions.pop(version)}) from {self}")

    def write(self) -> None:
        # sort by date then version (desc)
        ordered_versions = sorted(self.versions.values(), key=lambda v: (v.date, v.name), reverse=True)
        with self.versions_path.open("w") as f:
            f.write(json.dumps({
                "versions": {version.name: version.__dict__() for version in ordered_versions},
            }, indent=2))
        logging.info("::endgroup::")

    def __repr__(self) -> str:
        return self.name


def list_products(method: str, products_filter: str = None) -> list[str]:
    """Return a list of products that are using the same given update method."""
    products = []

    for product_file in PRODUCTS_PATH.glob("*.md"):
        product_name = product_file.stem
        if products_filter and product_name != products_filter:
            continue

        product = ProductFrontmatter(product_name)
        if len(product.get_auto_configs(method)) > 0:
            products.append(product_name)

    return products
