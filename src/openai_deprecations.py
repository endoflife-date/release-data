import logging
import re
from datetime import datetime

from bs4.element import Tag

from src.common import dates, endoflife, http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData, ProductRelease

"""Parse deprecation tables from https://platform.openai.com/docs/deprecations and populate end-of-availability dates, shutdown dates, and recommended replacements.

This updater only enriches existing releases; it never discovers or creates new model releases.
Support model cells containing code elements or pipe-separated identifiers, resolve models through canonical names and aliases, and skip API endpoints and preview models.
"""


def parse_models(cell: Tag) -> list[str]:
    models = [code.get_text(strip=True) for code in cell.select("code")]
    if models:
        return models

    models = [model.strip() for model in cell.get_text(" ", strip=True).split("|")]
    return [model for model in models if model and not re.search(r"[\s:]", model)]


def parse_deprecation_date(table: Tag) -> datetime:
    title = table.find_previous(["h1", "h2", "h3", "h4", "h5", "h6"])
    if title is None:
        message = "deprecation table has no title"
        raise ValueError(message)

    match = re.match(r"\d{4}-\d{2}-\d{2}", title.get_text(" ", strip=True))
    if match is None:
        message = f"deprecation title has no leading date: {title.get_text(' ', strip=True)}"
        raise ValueError(message)

    return dates.parse_date(match.group())


def get_release(product_data: ProductData, model: str) -> ProductRelease | None:
    model_identifier = endoflife.to_identifier(model)
    release = product_data.releases.get(model_identifier)
    if release is not None:
        return product_data.get_release(release.name())

    for release in product_data.releases.values():
        aliases = release.get_field("aliases") or []
        if any(endoflife.to_identifier(alias) == model_identifier for alias in aliases):
            return product_data.get_release(release.name())

    return None


def set_deprecation(product_data: ProductData, model: str, eoas: datetime, eol: datetime, replacement: str) -> None:
    release = get_release(product_data, model)
    if release is None:
        logging.warning("Skipping deprecation for %s, corresponding release was not found", model)
        return

    existing_eol = release.get_eol()
    existing_eoas = release.get_field("eoas")
    existing_replacement = release.get_field("recommendedReplacement")

    if (
        (existing_eol is not None and existing_eol != eol)
        or (existing_eoas is not None and existing_eoas != eoas.strftime("%Y-%m-%d"))
        or (existing_replacement is not None and existing_replacement != replacement)
    ):
        logging.warning(
            "Conflicting deprecation data for %s: existing eoas=%s, shutdown=%s, replacement=%s; "
            "new eoas=%s, shutdown=%s, replacement=%s; keeping first result",
            model,
            existing_eoas,
            existing_eol,
            existing_replacement,
            eoas,
            eol,
            replacement,
        )

    if existing_eoas is None:
        release.set_eoas(eoas)
    if existing_eol is None:
        release.set_eol(eol)
    if existing_replacement is None and replacement != "---":
        release.set_field("recommendedReplacement", replacement)


def get_column_indices(table: Tag) -> tuple[int, int, int] | None:
    headers = [header.get_text(" ", strip=True).lower() for header in table.select("thead th")]
    if not headers:
        logging.debug("Skipping deprecation table without headers")
        return None

    try:
        date_index = headers.index("shutdown date")
        model_index = next(i for i, header in enumerate(headers) if "model" in header or "system" in header)
        replacement_index = next(
            i for i, header in enumerate(headers) if "replacement" in header or "substitute" in header
        )
    except (StopIteration, ValueError):
        logging.debug("Skipping deprecation table with unsupported headers: %s", headers)
        return None

    return date_index, model_index, replacement_index


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        soup = http.fetch_html(config.url)

        for table in soup.select("table"):
            try:
                eoas = parse_deprecation_date(table)
            except ValueError as error:
                logging.debug("Skipping deprecation table without a valid title date: %s", error)
                continue

            indices = get_column_indices(table)
            if indices is None:
                continue
            date_index, model_index, replacement_index = indices

            for row in table.select("tbody tr"):
                cells = row.select("td, th")
                if max(date_index, model_index, replacement_index) >= len(cells):
                    logging.warning("Skipping deprecation row with insufficient cells: %s", row.get_text(" ", strip=True))
                    continue

                try:
                    eol = dates.parse_date(cells[date_index].get_text(" ", strip=True).replace("‑", "-"))
                except ValueError:
                    logging.warning("Skipping deprecation row with invalid EOL date: %s", row.get_text(" ", strip=True))
                    continue

                models = parse_models(cells[model_index])
                replacement = cells[replacement_index].get_text(" ", strip=True).removesuffix("*")
                for model in models:
                    if model.startswith("/") or "preview" in model.lower():
                        model_type = "API endpoint" if model.startswith("/") else "preview model"
                        logging.debug("Skipping %s %s", model_type, model)
                        continue
                    set_deprecation(product_data, model, eoas, eol, replacement)
