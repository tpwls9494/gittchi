from rich.console import Console
from rich.prompt import Prompt
from gittchi.config import load_config
from gittchi.state.pet import load_pet, new_pet
from gittchi.state.memory import load_memory, recent_messages, Memory
from gittchi.state.store import TamperedError
from gittchi.rules.status import compute_status
from gittchi.llm.client import call_llm
from gittchi.llm.prompts import hello_system_context

console = Console()
MAX_TURNS = 10


def run(message: str | None = None) -> None:
    config = load_config()
    if not config.pet_name:
        console.print("[yellow]아직 초기화 안 됨. gittchi init 실행[/yellow]")
        return

    try:
        pet = load_pet()
    except TamperedError:
        pet = None
    pet = pet or new_pet()

    try:
        memory = load_memory()
    except TamperedError:
        memory = Memory()

    status_name, status_emoji = compute_status(pet.last_commit_at, pet.streak_days)
    if pet.is_angry:
        status_name, status_emoji = "화남", "😤"

    # pet_type이 바뀌면 채팅 기록 초기화 (이전 페르소나 톤 오염 방지)
    if memory.chat_pet_type != config.pet_type:
        memory.chat_history = []
        memory.chat_pet_type = config.pet_type

    recent = recent_messages(memory, n=5)  # 10→5 컨텍스트 줄여 응답 속도 개선
    profile_summary = memory.long_term.ai_summary
    system_ctx = hello_system_context(recent, profile_summary, status_name)

    fallback_key = "neglect" if (pet.total_commits > 0 and pet.streak_days == 0) else "commit"

    # ── 단발 모드: 메시지를 인수로 받은 경우 ────────────────────────────────
    if message:
        # 이전 대화 이어받기
        chat_history = list(memory.chat_history)
        chat_history.append({"role": "user", "content": message})

        response = call_llm(
            pet_type=config.pet_type,
            pet_name=config.pet_name,
            model=config.model,
            api_key=config.api_key,
            extra_messages=chat_history,
            system_extra=system_ctx,
            fallback_key=fallback_key,
        )
        console.print(f"\n[bold]{config.pet_name}[/bold]: \"{response}\"")
        console.print(f"[dim]{status_emoji} {status_name}  |  Lv.{pet.level}[/dim]\n")

        # 대화 저장
        chat_history.append({"role": "assistant", "content": response})
        memory.chat_history = chat_history[-(MAX_TURNS * 2):]
        memory.chat_pet_type = config.pet_type
        from gittchi.state.memory import save_memory
        save_memory(memory)
        return

    # ── 대화 모드: 인수 없이 실행한 경우 (터미널 REPL) ──────────────────────
    opening = call_llm(
        pet_type=config.pet_type,
        pet_name=config.pet_name,
        model=config.model,
        api_key=config.api_key,
        user_prompt="주인이 말을 걸었어. 짧게 반응해줘.",
        system_extra=system_ctx,
        fallback_key=fallback_key,
    )
    console.print(f"\n[bold]{config.pet_name}[/bold]: \"{opening}\"")
    console.print(f"[dim]{status_emoji} {status_name}  |  Lv.{pet.level}  |  빈 입력으로 종료[/dim]\n")

    # 이전 대화 이어받기
    chat_history = list(memory.chat_history) or [
        {"role": "user", "content": "주인이 말을 걸었어."},
        {"role": "assistant", "content": opening},
    ]

    while True:
        try:
            user_input = Prompt.ask("[dim]>[/dim]")
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input.strip():
            break

        chat_history.append({"role": "user", "content": user_input})

        response = call_llm(
            pet_type=config.pet_type,
            pet_name=config.pet_name,
            model=config.model,
            api_key=config.api_key,
            extra_messages=chat_history,
            system_extra=system_ctx,
            fallback_key="commit",
        )

        console.print(f"[bold]{config.pet_name}[/bold]: \"{response}\"")
        chat_history.append({"role": "assistant", "content": response})

        if len(chat_history) > MAX_TURNS * 2:
            chat_history = chat_history[-(MAX_TURNS * 2):]

    # 종료 시 대화 저장
    memory.chat_history = chat_history
    memory.chat_pet_type = config.pet_type
    from gittchi.state.memory import save_memory
    save_memory(memory)
    console.print()
