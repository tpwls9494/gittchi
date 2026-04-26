import os
from gittchi.llm.personas import get_system_prompt, FALLBACK_LINES


def _get_api_key(config_key: str) -> str:
    return os.environ.get("GITTCHI_API_KEY", config_key)


def call_llm(
    pet_type: str,
    pet_name: str,
    model: str,
    api_key: str,
    user_prompt: str = "",
    extra_messages: list[dict] | None = None,  # multi-turn: [{"role": "user/assistant", "content": "..."}]
    system_extra: str = "",                     # 시스템 프롬프트에 append할 컨텍스트
    fallback_key: str = "commit",
) -> str:
    import litellm  # lazy — top-level import 시 CLI 시작 0.5s+ 느려짐

    key = _get_api_key(api_key)
    system = get_system_prompt(pet_type)
    if system_extra:
        system = f"{system}\n\n{system_extra}"

    messages = extra_messages if extra_messages is not None else [{"role": "user", "content": user_prompt}]

    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "system", "content": system}] + messages,
            api_key=key or None,
            timeout=6,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return FALLBACK_LINES.get(pet_type, FALLBACK_LINES["cat"]).get(fallback_key, "...")
