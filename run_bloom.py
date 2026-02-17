import os
from pathlib import Path

os.environ["OPENAI_API_KEY"] = "not-needed"
os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1"

from bloom import utils
from bloom.stages.step1_understanding import run_understanding
from bloom.stages.step2_ideation import run_ideation

config_dir = Path("bloom-data")
config = utils.load_config(str(config_dir / "seed.yaml"), config_dir=config_dir)

print("=== Running Understanding Stage ===")
run_understanding(config=config, config_dir=config_dir)

print("\n=== Running Ideation Stage ===")
run_ideation(config=config, config_dir=config_dir)

print("\n=== Done ===")
results_dir = Path("bloom-results/merit-based-triage")
for f in sorted(results_dir.glob("*.json")):
    print(f"Output: {f}")
