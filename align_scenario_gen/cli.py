import argparse

from .config import load_config
from .generate import run


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic moral dilemma scenarios for ADM evaluation"
    )
    parser.add_argument("config", help="Path to YAML config file")
    parser.add_argument("--num-scenarios", type=int)
    parser.add_argument("--model", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()

    config = load_config(args.config)
    for key in ("num_scenarios", "model", "output"):
        val = getattr(args, key)
        if val is not None:
            config[key] = val

    run(config)
