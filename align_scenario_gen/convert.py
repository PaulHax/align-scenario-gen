def scenario_to_record(scenario: dict, scenario_id: str, scene_index: int) -> dict:
    sid = str(scene_index)
    choices = [
        {
            "action_id": f"{sid}.action_{i}",
            "action_type": "SITREP",
            "unstructured": choice["label"],
            "kdma_association": None,
        }
        for i, choice in enumerate(scenario["choices"])
    ]
    return {
        "input": {
            "scenario_id": scenario_id,
            "full_state": {
                "unstructured": scenario["unstructured"],
                "meta_info": {"scene_id": sid},
                "scenario_complete": False,
            },
            "choices": choices,
        }
    }
