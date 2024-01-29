import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

# Do not update the format: it's also used to declare groups in the GitHub Actions logs.
logging.basicConfig(format="%(message)s", level=logging.INFO)

VERSIONS_PATH = Path(os.environ.get("VERSIONS_PATH", "releases"))


class ProductVersion:
    def __init__(self, product: "Product", data: dict) -> None:
        self.product = str(product)
        self.data = data

    @staticmethod
    def of(product: "Product", name: str, date: datetime) -> "ProductVersion":
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
                    version = ProductVersion(product, json_version)
                    product.versions[version.name()] = version
            logging.info(f"loaded versions data for {product} from {product.versions_path}")
        else:
            logging.warning(f"no versions data found for {product} at {product.versions_path}")

        return product

    def get_version(self, version: str) -> ProductVersion:
        return self.versions[version] if version in self.versions else None

    def declare_version(self, version: str, date: datetime) -> None:
        if version in self.versions and self.versions[version].date() != date:
            logging.info(f"overwriting {version} ({self.get_version(version).date()} -> {date}) for {self}")
            self.versions[version].replace_date(date)
        else:
            logging.info(f"adding version {version} ({date}) to {self}")
            self.versions[version] = ProductVersion.of(self, version, date)

    def declare_versions(self, dates_by_version: dict[str, datetime]) -> None:
        for (version, date) in dates_by_version.items():
            self.declare_version(version, date)

    def remove_version(self, version: str) -> None:
        if not self.get_version(version):
            logging.warning(f"version {version} cannot be removed as it does not exist for {self}")
            return

        logging.info(f"removing version {version} ({self.versions.pop(version)}) from {self}")

    def write(self) -> None:
        # sort by date then version (desc)
        ordered_versions = sorted(self.versions.values(), key=lambda v: (v.date(), v.name()), reverse=True)
        with self.versions_path.open("w") as f:
            f.write(json.dumps({
                "versions": {version.name(): version.data for version in ordered_versions},
            }, indent=2))
        logging.info("::endgroup::")

    def __repr__(self) -> str:
        return self.name
