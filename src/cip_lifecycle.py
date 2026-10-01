"""Fetches CIP SLTS lifecycle dates from gitlab.com/cip-project/cip-lifecycle.

The ``cip-kernel.yml`` file references YAML anchors defined in ``kernel.yml``
from the same repository, so both files are concatenated before parsing so
that aliases resolve in a single pass.

Each version's ``schedule`` is a list of phases. The product declares a
``fields`` mapping from an endoflife.date field name to a ``<phase>.<key>``
reference, for example ``eoes: phase2.end`` to map the end of CIP phase 2 to
the ``eoes`` field.

Version entries of the form ``4.19(-rt)`` cover both the standard and ``-rt``
variants; the parenthesised suffix is stripped before applying the version
regex. Pure ``-rt`` entries (for example ``4.4-rt``) are filtered out by the
regex.

If no field is applied at the end of the run, the script raises an error so
that upstream format drift is surfaced loudly instead of silently producing a
release with no extended-support data.
"""

import logging
import re

import yaml
from common import http
from common.releasedata import ProductData, config_from_argv

CIP_REPO_RAW = "https://gitlab.com/cip-project/cip-lifecycle/-/raw/master"
LIFECYCLE_FILES = ("kernel.yml", "cip-kernel.yml")
RT_SUFFIX = re.compile(r"\(-rt\)$")

config = config_from_argv()

field_mapping: dict[str, str] = config.data.get("fields", {})
if not field_mapping:
    message = f"no 'fields' mapping in auto config for {config}"
    raise ValueError(message)

responses = [http.fetch_url(f"{CIP_REPO_RAW}/{name}") for name in LIFECYCLE_FILES]
for response in responses:
    response.raise_for_status()

combined_text = "\n".join(response.text for response in responses)
projects = yaml.safe_load(combined_text)

project = next((p for p in projects if p.get("name") == config.url), None)
if project is None:
    message = f"project '{config.url}' not found in CIP lifecycle YAML"
    raise ValueError(message)

applied_field_count = 0
with ProductData(config.product) as product_data:
    for entry in project.get("versions", []):
        raw_version = entry.get("version", "")
        normalized = RT_SUFFIX.sub("", raw_version)
        match = config.first_match(normalized)
        if not match:
            logging.debug(f"skipping CIP version '{raw_version}' (no regex match)")
            continue

        release_name = config.render(match)
        phases_by_name = {p.get("phase"): p for p in entry.get("schedule", [])}

        # Resolve all field values first so we only touch the release when there is
        # at least one value to set; this avoids creating empty release entries
        # when the source format drifts.
        field_values: dict[str, object] = {}
        for field_name, phase_ref in field_mapping.items():
            phase_name, _, key = phase_ref.partition(".")
            if not key:
                logging.warning(
                    f"invalid mapping '{field_name}: {phase_ref}', expected '<phase>.<key>'",
                )
                continue
            phase = phases_by_name.get(phase_name)
            if phase is None or phase.get(key) is None:
                logging.warning(f"{release_name}: '{phase_ref}' not present in CIP schedule")
                continue
            field_values[field_name] = phase[key]

        if not field_values:
            continue

        release = product_data.get_release(release_name)
        for field_name, value in field_values.items():
            release.set_field(field_name, value)
            applied_field_count += 1

if applied_field_count == 0:
    message = (
        f"no CIP lifecycle fields were applied for {config}; "
        "upstream YAML structure may have changed"
    )
    raise ValueError(message)
