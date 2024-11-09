import itertools
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
    def __init__(self, product: str, data: dict) -> None:
        self.product = product
        self.data = data
        self.method = next(key for key in data if key not in ("template", "regex", "regex_exclude"))
        self.url = data[self.method]
        self.version_template = Template(data.get("template", DEFAULT_VERSION_TEMPLATE))

        self.script = f"{self.url}.py" if self.method == "custom" else f"{self.method}.py"

        regexes_include = data.get("regex", DEFAULT_VERSION_REGEX)
        regexes_include = regexes_include if isinstance(regexes_include, list) else [regexes_include]
        self.include_version_patterns = [re.compile(r, re.MULTILINE) for r in regexes_include]

        regexes_exclude = data.get("regex_exclude", [])
        regexes_exclude = regexes_exclude if isinstance(regexes_exclude, list) else [regexes_exclude]
        self.exclude_version_patterns = [re.compile(r, re.MULTILINE) for r in regexes_exclude]

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

    def __repr__(self) -> str:
        return f"{self.product}#{self.method}({self.url})"


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

    def has_auto_configs(self) -> bool:
        return self.data and "methods" in self.data.get("auto", {})

    def is_auto_update_cumulative(self) -> bool:
        return self.data.get("auto", {}).get("cumulative", False)

    def auto_configs(self, method_filter: str = None, url_filter: str = None) -> list[AutoConfig]:
        configs = []

        configs_data = self.data.get("auto", {}).get("methods", [])
        for config_data in configs_data:
            config = AutoConfig(self.name, config_data)
            if ((method_filter and config.method != method_filter)
                or (url_filter and config.url != url_filter)):
                continue

            configs.append(config)

        return configs

    def get_title(self) -> str:
        return self.data["title"]

    def get_permalink(self) -> str:
        return self.data["permalink"]

    def get_releases(self) -> list[dict]:
        return self.data.get("releases", [])

    def get_release_names(self) -> list[str]:
        return [release["releaseCycle"] for release in self.get_releases()]

    def get_release_date(self, release_cycle: str) -> datetime | None:
        for release in self.get_releases():
            if release["releaseCycle"] == release_cycle:
                return release["releaseDate"]
        return None


def list_products(products_filter: str = None) -> list[ProductFrontmatter]:
    """Return a list of products that are using the same given update method."""
    products = []

    for product_file in sorted(PRODUCTS_PATH.glob("*.md")):
        product_name = product_file.stem
        if products_filter and product_name != products_filter:
            continue

        try:
            products.append(ProductFrontmatter(product_name))
        except Exception as e:
            logging.exception(f"failed to load product data for {product_name}: {e}")

    return products


def list_configs(products_filter: str = None, methods_filter: str = None, urls_filter: str = None) -> list[AutoConfig]:
    products = list_products(products_filter)
    configs_by_product = [p.auto_configs(methods_filter, urls_filter) for p in products]
    return list(itertools.chain.from_iterable(configs_by_product))  # flatten the list of lists
