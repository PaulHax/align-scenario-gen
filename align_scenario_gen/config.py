from pathlib import Path

import yaml

DEFAULTS = {
    "model": "claude-sonnet-4",
    "num_scenarios": 10,
    "num_choices": 2,
    "kdma_theme": "merit",
    "scenario_id": "generated-merit",
    "temperature": 1.0,
    "max_tokens": 4000,
    "output": "output/scenarios.json",
}


def load_config(path: str | Path) -> dict:
    with open(path) as f:
        user = yaml.safe_load(f) or {}
    return {**DEFAULTS, **user}
