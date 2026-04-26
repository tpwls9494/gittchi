import os
from gittchi.llm.personas import get_system_prompt, FALLBACK_LINES

NEUTRAL_SYSTEM = "주어진 데이터를 바탕으로 한국어로 간결하고 객관적으로 답한다."


def _get_api_key(config_key: str) -> str:
    return os.environ.get("GITTCHI_API_KEY", config_key)


def call_llm(
    pet_type: str,
    pet_name: str,
    model: str,
    api_key: str,
    user_prompt: str = "",
    extra_messages: list[dict] | None = None,  # multi-turn
    system_extra: str = "",
    fallback_key: str = "commit",
    override_system: str | None = None,  # 분석용 — 펫 페르소나 대신 중립 시스템 사용
    empty_on_error: bool = False,         # True면 오류 시 "" 반환 (페르소나 fallback 저장 방지)
) -> str:
    import litellm  # lazy — top-level import 시 CLI 시작 0.5s+ 느려짐
    litellm.suppress_debug_info = True

    key = _get_api_key(api_key)
    system = override_system if override_system is not None else get_system_prompt(pet_type)
    if system_extra:
        system = f"{system}\n\n{system_extra}"

    messages = extra_messages if extra_messages is not None else [{"role": "user", "content": user_prompt}]

    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "system", "content": system}] + messages,
            api_key=key or None,
            timeout=15,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        if empty_on_error:
            return ""
        return FALLBACK_LINES.get(pet_type, FALLBACK_LINES["cat"]).get(fallback_key, "...")
