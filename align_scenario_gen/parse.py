import json
import re


def parse_scenario_json(raw_text: str) -> dict:
    cleaned = re.sub(r"```(?:json)?\s*", "", raw_text).strip().rstrip("`")
    # Replace control characters that local models sometimes emit
    cleaned = re.sub(r"[\x00-\x09\x0b\x0c\x0e-\x1f]", " ", cleaned)
    return json.loads(cleaned)
