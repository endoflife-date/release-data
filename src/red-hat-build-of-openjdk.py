import logging
import re

from src.common import dates, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Fetches Red Hat build of OpenJDK versions from the Red Hat Security Data API.

Each errata (RHSA) lists the RPMs it ships. Only the source RPMs of the configured packages are
considered, which excludes the other builds shipped by Red Hat (portable, crypto-adapter, hum1...).
The release date of a version is the date of the earliest errata shipping it.

The mapping between release cycles and RPM package names is given by the `packages` configuration.
"""

PAGE_SIZE = 100  # maximum number of errata fetched for each package, assumes newest-first odering


def _version_pattern(package: str) -> re.Pattern:
    # Example: java-21-openjdk-1:21.0.13.0.9-1.1.el9.src => 21.0.13.0.9-1.1
    return re.compile(rf"^{re.escape(package)}-\d+:(?P<version>.+?)\.el\d+[^.]*\.src$")


def _fetch_versions(base_url: str, package: str) -> dict[str, dict]:
    pattern = _version_pattern(package)
    errata = http.fetch_json(f"{base_url}?package={package}&per_page={PAGE_SIZE}")

    versions = {}
    for entry in errata:
        date = dates.parse_datetime(entry["released_on"])
        for released_package in entry["released_packages"]:
            match = pattern.match(released_package)
            if not match:
                continue

            version = match["version"]
            if version not in versions or date < versions[version]:
                versions[version] = date

    return versions


def _sort_key(version_and_date: tuple[str, object]) -> tuple:
    version, date = version_and_date
    return date, [int(number) for number in re.findall(r"\d+", version)]


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        for release_cycle, package in config.data["packages"].items():
            versions = _fetch_versions(config.url, package)
            if not versions:
                message = f"no version found for {package}"
                raise ValueError(message)

            release = product_data.get_release(str(release_cycle))
            for version, date in versions.items():
                logging.debug("Processing version: %s with date %s", version, date)
                product_data.declare_version(version, date)

            # Versions of cycle 8 start with "1.8" (legacy Java naming), so they are not matched to
            # their release cycle by update-product-data.py, which matches on the cycle name prefix.
            # This only raises "not declared" alerts for 30 days after each release. Setting latest
            # explicitly here ensures it is still correct.
            latest_version, latest_date = max(versions.items(), key=_sort_key)
            release.set_field("latest", latest_version)
            release.set_field("latestReleaseDate", latest_date)
