import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from types import TracebackType
from typing import Optional, Type

# Do not update the format: it's also used to declare groups in the GitHub Actions logs.
logging.basicConfig(format="%(message)s", level=logging.INFO)

VERSIONS_PATH = Path(os.environ.get("VERSIONS_PATH", "releases"))


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

    def set_release_date(self, new_value: datetime) -> None:
        self.set_field("releaseDate", new_value)

    def set_support(self, new_value: datetime | bool) -> None:
        self.set_field("support", new_value)

    def set_eol(self, new_value: datetime | bool) -> None:
        self.set_field("eol", new_value)

    def set_extended_support(self, new_value: datetime | bool) -> None:
        self.set_field("extendedSupport", new_value)

    def set_field(self, field: str, new_value: any) -> None:
        new_value = new_value.strftime("%Y-%m-%d") if isinstance(new_value, datetime) else new_value
        old_value = self.data.get(field, None)
        if old_value != new_value:
            self.data[field] = new_value
            if old_value:
                logging.info(f"updated '{field}' in {self} from {old_value} to {new_value}")
            else:
                logging.info(f"set '{field}' in {self} to {new_value}")

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
        self.versions_path: Path = VERSIONS_PATH / f"{name}.json"
        self.releases = {}
        self.versions: dict[str, ProductVersion] = {}

    def __enter__(self) -> "ProductData":
        if self.versions_path.is_file():
            with self.versions_path.open() as f:
                for json_version in json.load(f)["versions"].values():
                    version = ProductVersion(self.name, json_version)
                    self.versions[version.name()] = version
            logging.info(f"loaded versions data for {self} from {self.versions_path}")
        else:
            logging.info(f"no versions data found for {self} at {self.versions_path}")

        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException],
                 exc_traceback: Optional[TracebackType]) -> None:
        if exc_value:
            message = f"an unexpected error occurred while updating {self} data"
            logging.error(message, exc_info=exc_value)
            raise ProductUpdateError(message) from exc_value

        logging.info("updating %s data",self.versions_path)
        ordered_releases = sorted(self.releases.values(), key=lambda v: v.name(), reverse=True)
        ordered_versions = sorted(self.versions.values(), key=lambda v: (v.date(), v.name()), reverse=True)
        with self.versions_path.open("w") as f:
            f.write(json.dumps({
                "releases": {release.name(): release.data for release in ordered_releases},
                "versions": {version.name(): version.data for version in ordered_versions},
            }, indent=2))

    def get_release(self, release: str) -> ProductRelease:
        if release not in self.releases:
            logging.info(f"adding release {release} to {self}")
            self.releases[release] = ProductRelease.of(self.name, release)

        return self.releases[release]

    def get_version(self, version: str) -> ProductVersion:
        return self.versions[version] if version in self.versions else None

    def declare_version(self, version: str, date: datetime) -> None:
        if version in self.versions and self.versions[version].date() != date:
            logging.info(f"overwriting {version} ({self.get_version(version).date()} -> {date}) for {self}")
            self.versions[version].replace_date(date)
        else:
            logging.info(f"adding version {version} ({date}) to {self}")
            self.versions[version] = ProductVersion.of(self.name, version, date)

    def declare_versions(self, dates_by_version: dict[str, datetime]) -> None:
        for (version, date) in dates_by_version.items():
            self.declare_version(version, date)

    def remove_version(self, version: str) -> None:
        if not self.get_version(version):
            logging.warning(f"version {version} cannot be removed as it does not exist for {self}")
            return

        logging.info(f"removing version {version} ({self.versions.pop(version)}) from {self}")

    def __repr__(self) -> str:
        return self.name
