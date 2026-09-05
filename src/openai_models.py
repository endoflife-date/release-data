import logging
import re

from src.common import http
from src.common.endoflife import AutoConfig, ProductFrontmatter
from src.common.releasedata import ProductData

"""Synchronize OpenAI model metadata from https://developers.openai.com/api/docs/models.
The updater discovers documented models, records their labels and links, and extracts snapshot aliases for matching releases.
Preview models and the gpt-daybreak family are excluded from the catalog.
"""

MODEL_LINK_PATTERN = re.compile(
    r"^- \[(?P<label>[^]]+)\]\((?P<link>[^)]+)\.md\): .+$",
    re.MULTILINE,
)
SNAPSHOTS_PATTERN = re.compile(r"^## Snapshots\s*$([\s\S]*?)(?=^## |\Z)", re.MULTILINE)
ALIAS_PATTERN = re.compile(r"`([a-zA-Z0-9][a-zA-Z0-9._+-]*)`")


def update(_product: ProductFrontmatter, config: AutoConfig) -> None:
    with ProductData(config.product) as product_data:
        catalog = http.fetch_url(f"{config.url}.md").text
        models = []

        for match in MODEL_LINK_PATTERN.finditer(catalog):
            label = match.group("label")
            model_link = f"https://developers.openai.com{match.group('link')}"
            model_id = model_link.rstrip("/").split("/")[-1]

            if "preview" in model_id.lower() or model_id.startswith("gpt-daybreak"):
                logging.debug("Skipping excluded model %s (%s)", model_id, label)
                continue

            models.append((label, model_link, model_id))

        model_pages = {
            response.url: response.text
            for response in http.fetch_urls([f"{model_link}.md" for _, model_link, _ in models])
        }

        for label, model_link, model_id in models:
            release = product_data.get_release(model_id)
            release.set_label(label)
            release.set_field("link", model_link)

            model_page = model_pages[f"{model_link}.md"]
            snapshots = SNAPSHOTS_PATTERN.search(model_page)
            aliases = ALIAS_PATTERN.findall(snapshots.group(1)) if snapshots else []
            release.set_field("aliases", aliases)
