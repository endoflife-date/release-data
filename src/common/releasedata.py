import argparse
import json
import logging
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from types import TracebackType
from typing import Optional, Type

from . import endoflife

SRC_DIR = Path('src')
DATA_DIR = Path('releases')


class ProductUpdateError(Exception):
    """Custom exceptions raised when unexpected errors occur during product updates."""


class ProductRelease:
    def __init__(self, product: str, data: dict = None) -> None:
        self.product = product
        self.data = data if data else {}

    @staticmethod
    def of(product: str, name: str) -> "ProductRelease":
        return ProductRelease(product, { "name": name })

    def name(self) -> str:
        return self.data["name"]

    def set_label(self, new_value: str) -> None:
        self.set_field("releaseLabel", new_value)

    def set_release_date(self, new_value: datetime) -> None:
        self.set_field("releaseDate", new_value)

    def get_release_date(self) -> datetime | None:
        if "releaseDate" not in self.data:
            return None

        return datetime.strptime(self.data["releaseDate"], "%Y-%m-%d").replace(tzinfo=timezone.utc)

    def set_eoas(self, new_value: datetime | bool) -> None:
        self.set_field("eoas", new_value)

    def set_eol(self, new_value: datetime | bool) -> None:
        self.set_field("eol", new_value)

    def get_eol(self) -> datetime | bool | None:
        if "eol" not in self.data:
            return None

        eol = self.data["eol"]
        if isinstance(eol, bool):
            return eol

        return datetime.strptime(self.data["eol"], "%Y-%m-%d").replace(tzinfo=timezone.utc)

    def set_eoes(self, new_value: datetime | bool) -> None:
        self.set_field("eoes", new_value)

    def set_field(self, field: str, new_value: any) -> None:
        new_value = new_value.strftime("%Y-%m-%d") if isinstance(new_value, datetime) else new_value
        new_value = new_value.strftime("%Y-%m-%d") if isinstance(new_value, date) else new_value
        old_value = self.data.get(field, None)
        if old_value != new_value:
            self.data[field] = new_value
            if old_value:
                logging.info(f"updated '{field}' in {self} from {old_value} to {new_value}")
            else:
                logging.info(f"set '{field}' in {self} to {new_value}")

    def is_empty(self) -> bool:
        return len(self.data) == 1  # only the name is set

    def was_released_after(self, date: datetime) -> bool:
        release_date = self.get_release_date()
        return release_date and release_date > date

    def __repr__(self) -> str:
        return f"{self.product}#{self.name()}"


class ProductVersion:
    def __init__(self, product: str, data: dict) -> None:
        self.product = product
        self.data = data

    @staticmethod
    def of(product: str, name: str, date: datetime) -> "ProductVersion":
        return ProductVersion(product, {
            "name": name,
            "date": date.strftime("%Y-%m-%d"),
        })

    def name(self) -> str:
        return self.data["name"]

    def date(self) -> datetime:
        return datetime.strptime(self.data["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)

    def replace_date(self, date: datetime) -> None:
        self.data["date"] = date.strftime("%Y-%m-%d")

    def __repr__(self) -> str:
        return f"{self.product}#{self.name()} ({self.date()})"


class ProductData:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.path: Path = DATA_DIR / f"{name}.json"
        self.releases: dict[str, ProductRelease] = {}
        self.versions: dict[str, ProductVersion] = {}
        self.updated: bool = False

    def __enter__(self) -> "ProductData":
        if self.path.is_file():
            with self.path.open() as f:
                json_data = json.load(f)
                for json_version in json_data.get("versions", {}).values():
                    version = ProductVersion(self.name, json_version)
                    self.versions[version.name()] = version
                for json_release in json_data.get("releases", {}).values():
                    release = ProductRelease(self.name, json_release)
                    self.releases[release.name()] = release
            logging.info(f"loaded data for {self} from {self.path}")
        else:
            logging.info(f"no data found for {self} at {self.path}")

        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException],
                 exc_traceback: Optional[TracebackType]) -> None:
        if exc_value:
            message = f"an unexpected error occurred while updating {self} data"
            logging.error(message, exc_info=exc_value)
            raise ProductUpdateError(message) from exc_value

        if not self.updated:
            message = f"no update detected for {self}"
            logging.error(message)
            raise ProductUpdateError(message)

        logging.info("updating %s data", self.path)
        ordered_releases = sorted(self.releases.values(), key=lambda v: v.name(), reverse=True)
        ordered_versions = sorted(self.versions.values(), key=lambda v: (v.date(), v.name()), reverse=True)
        with self.path.open("w") as f:
            f.write(json.dumps({
                "releases": {release.name(): release.data for release in ordered_releases},
                "versions": {version.name(): version.data for version in ordered_versions},
            }, indent=2))

    def get_release(self, release_name: str) -> ProductRelease:
        if release_name not in self.releases:
            logging.info(f"adding release {release_name} to {self}")
            self.releases[release_name] = ProductRelease.of(self.name, release_name)

        self.updated = True
        return self.releases[release_name]

    def get_latest_release(self) -> ProductRelease | None:
        return next(iter(self.releases.values()), None)  # assuming releases are sorted in descending order

    def remove_release(self, release_name: str) -> None:
        if release_name not in self.releases:
            logging.warning(f"release {release_name} cannot be removed as it does not exist for {self}")
            return

        logging.info(f"removing release {release_name} ({self.releases.pop(release_name)}) from {self}")
        self.updated = True

    def get_version(self, version_name: str) -> ProductVersion:
        return self.versions[version_name] if version_name in self.versions else None

    def declare_version(self, version_name: str, versions_date: datetime) -> None:
        self.updated = True
        if version_name in self.versions and self.versions[version_name].date() != versions_date:
            logging.info(f"overwriting {version_name} ({self.get_version(version_name).date()} -> {versions_date}) for {self}")
            self.versions[version_name].replace_date(versions_date)
        else:
            logging.info(f"adding version {version_name} ({versions_date}) to {self}")
            self.versions[version_name] = ProductVersion.of(self.name, version_name, versions_date)

    def remove_version(self, version_name: str) -> None:
        if version_name not in self.versions:
            logging.warning(f"version {version_name} cannot be removed as it does not exist for {self}")
            return

        logging.info(f"removing version {version_name} ({self.versions.pop(version_name)}) from {self}")

    def __repr__(self) -> str:
        return self.name


def config_from_argv() -> endoflife.AutoConfig:
    return parse_argv()[1]

def parse_argv(ignore_auto_config: bool = False) -> tuple[endoflife.ProductFrontmatter, endoflife.AutoConfig]:
    parser = argparse.ArgumentParser(description=sys.argv[0])
    parser.add_argument('-p', '--product', required=True, help='path to the product')
    parser.add_argument('-m', '--method', required=True, help='method to filter by')
    parser.add_argument('-u', '--url', required=True, help='url to filter by')
    parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose logging')
    args = parser.parse_args()

    # Do not update the format: it's also used to declare groups in the GitHub Actions logs.
    logging.basicConfig(format="%(message)s", level=(logging.DEBUG if args.verbose else logging.INFO))

    product = endoflife.ProductFrontmatter(Path(args.product))
    auto_config = None if ignore_auto_config else product.auto_config(args.method, args.url)
    return product, auto_config
