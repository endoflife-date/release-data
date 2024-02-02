import logging
import os
import re
from datetime import datetime
from pathlib import Path

import frontmatter
from liquid import Template

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

        regexes_include = config.get("regex", DEFAULT_VERSION_REGEX)
        regexes_include = regexes_include if isinstance(regexes_include, list) else [regexes_include]
        self.include_version_patterns = [re.compile(r) for r in regexes_include]

        regexes_exclude = config.get("regex_exclude", [])
        regexes_exclude = regexes_exclude if isinstance(regexes_exclude, list) else [regexes_exclude]
        self.exclude_version_patterns = [re.compile(r) for r in regexes_exclude]

    def first_match(self, version: str) -> re.Match | None:
        for exclude_pattern in self.exclude_version_patterns:
            if exclude_pattern.match(version):
                return None

        for include_pattern in self.include_version_patterns:
            match = include_pattern.match(version)
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
            message = f"mixed auto-update methods declared for {self.name}, this is not yet supported"
            raise ValueError(message)

        return configs

    def get_release_date(self, release_cycle: str) -> datetime | None:
        for release in self.data["releases"]:
            if release["releaseCycle"] == release_cycle:
                return release["releaseDate"]
        return None


def list_products(method: str, products_filter: str = None) -> list[ProductFrontmatter]:
    """Return a list of products that are using the same given update method."""
    products = []

    for product_file in PRODUCTS_PATH.glob("*.md"):
        product_name = product_file.stem
        if products_filter and product_name != products_filter:
            continue

        product = ProductFrontmatter(product_name)
        configs = product.get_auto_configs(method)
        if len(configs) > 0:
            products.append(product)

    return products
