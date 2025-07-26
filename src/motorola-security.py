import json
import logging
import re

from common import dates, endoflife, http
from common.releasedata import ProductData, config_from_argv


def extract_data(url: str, key_to_search_for: str) -> dict | None:
    """Extract JSON data from Motorola Mobility security updates page."""
    html = http.fetch_html(url)

    # find all script tags with no src attribute and containing a CDATA section.
    all_scripts = [str(t.getText) for t in html.find_all("script", src=False)]
    candidate_scripts = [s for s in all_scripts if key_to_search_for in s]
    if len(candidate_scripts) != 1:
        msg = f"Expected exactly one script containing {key_to_search_for}, found {len(candidate_scripts)}"
        raise ValueError(msg)

    # Ideally, we would use an actual JavaScript parser to find our desired content.
    lines = candidate_scripts[0].split("\n")
    candidate_lines = [line for line in lines if key_to_search_for in line]
    if len(candidate_lines) != 1:
        msg = f"Expected exactly one containing {key_to_search_for} in JS, got {len(candidate_lines)}"
        raise ValueError(msg)

    candidate_line = candidate_lines[0]
    raw_json = re.search(r"\{.+}", candidate_line)
    if not raw_json:
        msg = f"Failed to find JSON in {candidate_line}"
        raise ValueError(msg)

    logging.debug(f"Found : {raw_json}")
    return json.loads(raw_json.group(0))

config = config_from_argv()
with ProductData(config.product) as product_data:
    json_data = extract_data(config.url, "guidedAssistant")

    for question in json_data["j"]["guidedAssistant"]["questions"]:
        if not question.get("responses") or question["responses"][0].get("text") != "Security patch details for all Motorola products":
            logging.debug(f"Skipping {question}")
            continue

        lines = question["taglessText"].replace("\xa0", " ").split("\n")
        logging.debug(lines)

        product_id = question["agentText"]
        label = lines[0].strip()
        name = endoflife.to_identifier(label)
        release = product_data.get_release(name)
        release.set_field("link", f"https://en-us.support.motorola.com/app/software-security-update/g_id/7112/productid/{product_id}")
        for line in lines:
            if (m := re.search(r"^Device launched on (.*)$", line)):
                date = dates.parse_date_or_month_year_date(m.group(1).strip()).replace(day=1)
                release.set_release_date(date)
            if (m := re.search(r"^Security updates will stop on (.*)$", line)):
                eol = dates.parse_date_or_month_year_date(m.group(1).strip())
                release.set_eol(eol)
