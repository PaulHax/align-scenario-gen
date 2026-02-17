import json
import re


def parse_scenario_json(raw_text: str) -> dict:
    cleaned = re.sub(r"```(?:json)?\s*", "", raw_text).strip().rstrip("`")
    # Replace control characters that local models sometimes emit
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", cleaned)
    # Fix raw newlines/tabs inside JSON string values
    cleaned = _escape_strings(cleaned)
    return json.loads(cleaned)


def _escape_strings(text: str) -> str:
    result = []
    in_string = False
    escape_next = False
    for ch in text:
        if escape_next:
            result.append(ch)
            escape_next = False
            continue
        if ch == "\\" and in_string:
            result.append(ch)
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            result.append(ch)
            continue
        if in_string and ch == "\n":
            result.append("\\n")
            continue
        if in_string and ch == "\t":
            result.append("\\t")
            continue
        result.append(ch)
    return "".join(result)
