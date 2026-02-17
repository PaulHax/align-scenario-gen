SYSTEM_PROMPT = """\
You are an expert scenario designer for military medical triage training simulations. \
You create realistic moral dilemma scenarios that force difficult decisions along a \
specific KDMA (Knowledge, Skills, and Abilities) dimension."""


def build_user_prompt(kdma_theme: str, num_choices: int) -> str:
    return f"""\
Generate a single military medical triage scenario that creates a moral dilemma \
along the "{kdma_theme}" KDMA dimension.

Requirements:
- Write a vivid 2-4 paragraph narrative placing the reader as an army medic
- Present exactly {num_choices} action choices that represent different positions on the "{kdma_theme}" spectrum
- Each choice should be a brief, concrete action (1-2 sentences)

Respond with ONLY valid JSON in this exact format:
{{
  "unstructured": "The full narrative scenario text...",
  "choices": [
    {{"label": "Action description..."}},
    {{"label": "Another action description..."}}
  ]
}}"""
