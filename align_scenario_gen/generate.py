import json
from pathlib import Path

from .convert import scenario_to_record
from .parse import parse_scenario_json
from .prompt import SYSTEM_PROMPT, build_user_prompt


def _call_llm(config: dict, messages: list[dict]) -> str:
    if config["model"] == "local":
        from .local_llm import local_chat

        return local_chat(
            config,
            messages,
            system_prompt=SYSTEM_PROMPT,
            max_tokens=config["max_tokens"],
            temperature=config["temperature"],
        )

    from bloom.utils import get_model_id, litellm_chat, parse_message

    model_id = get_model_id(config["model"])
    response = litellm_chat(
        model_id=model_id,
        messages=messages,
        system_prompt=SYSTEM_PROMPT,
        max_tokens=config["max_tokens"],
        temperature=config["temperature"],
    )
    return parse_message(response)["content"]


def run(config: dict) -> list[dict]:
    user_prompt = build_user_prompt(config["kdma_theme"], config["num_choices"])
    messages = [{"role": "user", "content": user_prompt}]

    max_retries = 3
    records = []
    for i in range(config["num_scenarios"]):
        print(f"Generating scenario {i + 1}/{config['num_scenarios']}...")
        for attempt in range(max_retries):
            content = _call_llm(config, messages)
            try:
                scenario = parse_scenario_json(content)
                break
            except (json.JSONDecodeError, KeyError) as e:
                if attempt < max_retries - 1:
                    print(f"  Parse failed ({e}), retrying...")
                else:
                    raise
        record = scenario_to_record(scenario, config["scenario_id"], i)
        records.append(record)

    output_path = Path(config["output"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(records, indent=2))
    print(f"Wrote {len(records)} scenarios to {output_path}")
    return records
