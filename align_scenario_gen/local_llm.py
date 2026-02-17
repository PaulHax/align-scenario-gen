from llama_cpp import Llama

_model_cache: dict[str, Llama] = {}

DEFAULT_LOCAL_MODEL = {
    "repo_id": "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF",
    "filename": "*Q4_K_M.gguf",
    "n_ctx": 4096,
    "n_gpu_layers": -1,
    "main_gpu": 0,
}


def get_model(
    repo_id: str,
    filename: str,
    n_ctx: int = 4096,
    n_gpu_layers: int = -1,
    main_gpu: int = 0,
) -> Llama:
    key = f"{repo_id}:{filename}"
    if key not in _model_cache:
        print(f"Loading model {repo_id} ({filename}) on GPU {main_gpu}...")
        _model_cache[key] = Llama.from_pretrained(
            repo_id=repo_id,
            filename=filename,
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            main_gpu=main_gpu,
            verbose=False,
        )
    return _model_cache[key]


def local_chat(
    config: dict,
    messages: list[dict],
    system_prompt: str | None = None,
    max_tokens: int = 4000,
    temperature: float = 1.0,
) -> str:
    local_cfg = {**DEFAULT_LOCAL_MODEL, **config.get("local_model", {})}
    model = get_model(
        local_cfg["repo_id"],
        local_cfg["filename"],
        local_cfg["n_ctx"],
        local_cfg["n_gpu_layers"],
        local_cfg["main_gpu"],
    )

    all_messages = []
    if system_prompt:
        all_messages.append({"role": "system", "content": system_prompt})
    all_messages.extend(messages)

    response = model.create_chat_completion(
        messages=all_messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response["choices"][0]["message"]["content"]
