import logging
import os
import re
from datetime import datetime
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
