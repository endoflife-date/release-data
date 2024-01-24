import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

# Do not update the format: it's also used to declare groups in the GitHub Actions logs.
logging.basicConfig(format="%(message)s", level=logging.INFO)

VERSIONS_PATH = Path(os.environ.get("VERSIONS_PATH", "releases"))


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
