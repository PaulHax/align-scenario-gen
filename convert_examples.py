"""Convert align-system input_output.json records into bloom example transcripts."""

import json
from pathlib import Path

EXPERIMENTS_DIR = Path("/home/paulhax/src/itm/experiments")
OUTPUT_DIR = Path("bloom-data/behaviors/examples/merit-based-triage")

MERIT_DIRS = sorted(
    EXPERIMENTS_DIR.glob("phase2_feb2026_results_local/phase2_baseline/Feb2026-MF-*")
)


def record_to_transcript(record: dict) -> dict | None:
    inp = record.get("input", {})
    out = record.get("output")
    if not out or not inp.get("full_state", {}).get("unstructured"):
        return None

    narrative = inp["full_state"]["unstructured"]
    choices = inp.get("choices", [])
    choice_text = "\n".join(
        f"- {c['unstructured']}" for c in choices
    )

    user_content = f"{narrative}\n\nAvailable actions:\n{choice_text}"

    action = out.get("action", {})
    chosen = action.get("unstructured", "")
    justification = action.get("justification", "")
    kdma = action.get("kdma_association", {})
    merit_val = kdma.get("merit", "?")

    assistant_content = f"I choose: {chosen}\n\nReasoning: {justification}"
    if merit_val != "?":
        assistant_content += f"\n\n[Merit alignment: {merit_val}]"

    return {
        "conversation": [
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": assistant_content},
        ]
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    example_num = 0

    for exp_dir in MERIT_DIRS:
        io_file = exp_dir / "input_output.json"
        if not io_file.exists():
            continue

        records = json.loads(io_file.read_text())
        for record in records[:2]:
            transcript = record_to_transcript(record)
            if not transcript:
                continue

            example_num += 1
            out_path = OUTPUT_DIR / f"example{example_num}.json"
            out_path.write_text(json.dumps(transcript, indent=2))

        if example_num >= 6:
            break

    print(f"Wrote {example_num} examples to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
