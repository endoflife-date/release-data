import argparse
import datetime
import json
import logging
import re
from pathlib import Path

import frontmatter
from packaging.version import InvalidVersion, Version
from ruamel.yaml import YAML
from ruamel.yaml.representer import RoundTripRepresenter
from ruamel.yaml.resolver import Resolver

from src.common.endoflife import list_products
from src.common.gha import GitHubOutput
from src.common.releasedata import DATA_DIR

"""
Updates the `release`, `latest` and `latestReleaseDate` property in automatically updated pages
As per data from _data/release-data. This script runs on dependabot upgrade PRs via GitHub Actions for
_data/release-data and commits back the updated data.
This is written in Python because the only package that supports writing back YAML with comments is ruamel
"""


class ReleaseCycle:
    def __init__(self, product: "Product", data: dict) -> None:
        self.product = product.name
        self.data = data
        self.name = data["releaseCycle"]
        self.matched = False
        self.updated = False

    def update_with(self, release: dict) -> None:
        for key, value in release.items():
            if isinstance(value, str) and re.fullmatch(r'^\d{4}-\d{2}-\d{2}$', value):
                value = datetime.date.fromisoformat(value)

            old_value = self.data.get(key, None)
            if old_value != value:
                logging.info(f"{self} {key} updated from {old_value} to {value} using release data")
                self.data[key] = value
                self.updated = True

    def update_with_version(self, version: str, date: datetime.date) -> None:
        logging.debug(f"will try to update {self} with {version} ({date})")
        self.matched = True
        self.__update_release_date(date)
        self.__update_latest(version, date)

    def latest(self) -> str | None:
        return self.data.get("latest", None)

    def includes(self, version: str) -> bool:
        """matches releases that are exact (such as 4.1 being the first release for the 4.1 release cycle)
        or releases that include a dot just after the release cycle (4.1.*)
        This is important to avoid edge cases like a 4.10.x release being marked under the 4.1 release cycle."""
        if not version.startswith(self.name):
            return False

        if len(version) == len(self.name):  # exact match
            return True

        char_after_prefix = version[len(self.name)]
        return not char_after_prefix.isdigit()

    def __update_release_date(self, date: datetime.date) -> None:
        release_date = self.data.get("releaseDate", None)
        if release_date and release_date > date:
            logging.info(f"{self} releaseDate updated from {release_date} to {date} using version data")
            self.data["releaseDate"] = date
            self.updated = True

    def __update_latest(self, version: str, date: datetime.date) -> None:
        old_latest = self.data.get("latest", None)
        old_latest_date = self.data.get("latestReleaseDate", None)

        update_detected = False
        if not old_latest:
            logging.info(f"{self} latest set to {version} ({date}) using version data")
            update_detected = True

        elif old_latest == version and old_latest_date != date:
            logging.info(f"{self} latestReleaseDate updated from {old_latest_date} to {date} using version data")
            update_detected = True

        else:
            try:  # Do our best attempt at comparing the version numbers
                if Version(old_latest) < Version(version):
                    logging.info(f"{self} latest updated from {old_latest} ({old_latest_date}) to {version} ({date}) using version data")
                    update_detected = True
            except InvalidVersion: # If we can't compare the version numbers, compare the dates
                logging.debug(f"could not compare {old_latest} with {version} for {self}, comparing dates instead")
                if old_latest_date < date:
                    logging.info(f"{self} latest updated from {old_latest} ({old_latest_date}) to {version} ({date}) using version data")
                    update_detected = True

        if update_detected:
            self.data["latest"] = version
            self.data["latestReleaseDate"] = date
            self.updated = True

    def __str__(self) -> str:
        return self.product + '#' + self.name


class Product:
    def __init__(self, name: str, product_dir: Path, versions_dir: Path) -> None:
        self.name = name
        self.product_path = product_dir / f"{name}.md"
        self.release_data_path = versions_dir / f"{name}.json"

        with self.product_path.open() as product_file:
            # First read the frontmatter of the product file.
            yaml = YAML()
            yaml.preserve_quotes = True
            self.data = next(yaml.load_all(product_file))

            # Now read the content of the product file
            product_file.seek(0)
            _, self.content = frontmatter.parse(product_file.read())

        if self.release_data_path.exists():
            with self.release_data_path.open() as release_data_file:
                self.release_data = json.loads(release_data_file.read())
        else:
            self.release_data = None

        self.releases = [ReleaseCycle(self, release) for release in self.data["releases"]]
        self.updated = False
        self.unmatched_releases = {}
        self.unmatched_versions = {}

    # Placeholder function for mass-upgrading the structure of the product files.
    def upgrade_structure(self) -> None:
        logging.debug(f"upgrading {self.name} structure")
        # Do not forget to set self.updated to True

    def check_latest(self) -> None:
        for release in self.releases:
            latest = release.latest()
            if release.matched and latest not in self.release_data["versions"]:
                logging.warning(f"latest version {latest} for {release} not found in {self.release_data_path}")

    def process_release(self, release_data: dict) -> None:
        name = release_data.pop("name")  # name must not appear in updates

        release_matched = False
        for release in self.releases:
            if release.name == name:
                release_matched = True
                release.update_with(release_data)
                self.updated = self.updated or release.updated

        if not release_matched:
            # get the first available date in the release data
            date_str = (release_data.get("extendedSupport", None)
                        or release_data.get("eol", None)
                        or release_data.get("support", None)
                        or release_data.get("releaseDate", None))

            self.unmatched_releases[name] = datetime.date.fromisoformat(str(date_str)) if isinstance(date_str, str) else None

    def process_version(self, version_data: dict) -> None:
        name = version_data["name"]
        date = datetime.date.fromisoformat(version_data["date"])

        version_matched = False
        for release in self.releases:
            if release.includes(name):
                version_matched = True
                release.update_with_version(name, date)
                self.updated = self.updated or release.updated

        if not version_matched:
            self.unmatched_versions[name] = date

    def write(self) -> None:
        with self.product_path.open("w") as product_file:
            product_file.truncate()
            product_file.write("---\n")

            yaml_frontmatter = YAML()
            yaml_frontmatter.width = 4096  # prevent line-wrap
            yaml_frontmatter.indent(sequence=4)
            yaml_frontmatter.dump(self.data, product_file)

            product_file.write("\n---\n\n")
            product_file.write(self.content)
            product_file.write("\n")


def update_product(name: str, product_dir: Path, releases_dir: Path, output: GitHubOutput) -> None:
    product = Product(name, product_dir, releases_dir)
    product.upgrade_structure()

    if product.release_data:
        for version_data in product.release_data.get("versions", {}).values():
            product.process_version(version_data)

        # Do not move: release data has priority over version data.
        for release_data in product.release_data.get("releases", {}).values():
            product.process_release(release_data)

        product.check_latest()

    if product.updated:
        logging.info(f"Updating {product.product_path}")
        product.write()

    # List all unmatched versions released in the last 30 days
    today = datetime.datetime.now(tz=datetime.timezone.utc).date()
    __raise_alert_for_unmatched_versions(name, output, product, today, 30)
    __raise_alert_for_unmatched_releases(name, output, product, today, 30)


def __raise_alert_for_unmatched_versions(name: str, output: GitHubOutput, product: Product, today: datetime.date,
                                         suppress_alert_threshold_days: int) -> None:
    if len(product.unmatched_versions) == 0:
        return

    for version, date in product.unmatched_versions.items():
        if (today - date).days < suppress_alert_threshold_days:
            logging.warning(f"{name}:{version} ({date}) not included")
            output.println(f"{name}:{version} ({date})")


def __raise_alert_for_unmatched_releases(name: str, output: GitHubOutput, product: Product, today: datetime.date,
                                         suppress_alert_threshold_days: int) -> None:
    if len(product.unmatched_releases) == 0:
        return

    for release, date in product.unmatched_releases.items():
        if (not date) or ((today - date).days < suppress_alert_threshold_days):
            logging.warning(f"{name}:{release} not included")
            output.println(f"{name}:{release}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update product releases.')
    parser.add_argument('product', nargs='?', help='restrict update to the given product')
    parser.add_argument('-p', '--product-dir', required=True, help='path to the product directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose logging')
    args = parser.parse_args()

    logging.basicConfig(format=logging.BASIC_FORMAT, level=(logging.DEBUG if args.verbose else logging.INFO))

    # Force YAML to format version numbers as strings, see https://stackoverflow.com/a/71329221/368328.
    Resolver.add_implicit_resolver("tag:yaml.org,2002:string", re.compile(r"\d+(\.\d+){0,3}", re.X), list(".0123456789"))

    # Force ruamel to never use aliases when dumping, see https://stackoverflow.com/a/64717341/374236.
    # Example of dumping with aliases: https://github.com/endoflife-date/endoflife.date/pull/4368.
    RoundTripRepresenter.ignore_aliases = lambda x, y: True # NOQA: ARG005

    products_dir = Path(args.product_dir)
    data_dir = Path(__file__).resolve().parent / DATA_DIR
    products = list_products(products_dir, args.product)

    github_output = GitHubOutput("warning")
    with github_output:
        for product in products:
            logging.debug(f"Processing {product.name}")
            update_product(product.name, products_dir, data_dir, github_output)
