from rich.console import Console
from rich.prompt import Prompt
from gittchi.config import Config, save_config
from gittchi.git_io.hook_installer import get_current_hooks_path, install
from gittchi.paths import home

console = Console()

PET_TYPES = {
    "1": ("dog",    "🐶 강아지 (열정형)"),
    "2": ("cat",    "🐱 고양이 (츤데레)"),
    "3": ("rabbit", "🐰 토끼 (감성형)"),
    "4": ("bear",   "🐻 곰 (듬직형)"),
}


def run() -> None:
    from gittchi.config import load_config
    from rich.prompt import Confirm

    existing = load_config()
    if existing.pet_name:
        console.print(
            f"\n[yellow]⚠️  이미 [bold]{existing.pet_name}[/bold]이(가) 있어요.[/yellow]\n"
            "재설정하면 현재 펫의 XP·레벨·기억이 모두 초기화됩니다."
        )
        if not Confirm.ask("계속하시겠어요?", default=False):
            console.print("[dim]취소됐습니다.[/dim]\n")
            return

    console.print("\n[bold yellow]🥚 Gittchi에 오신 걸 환영합니다![/bold yellow]\n")

    name = Prompt.ask("펫의 이름을 지어주세요")

    console.print("\n어떤 펫으로 키울까요?")
    for key, (_, label) in PET_TYPES.items():
        console.print(f"  [{key}] {label}")
    pet_choice = Prompt.ask("선택", choices=list(PET_TYPES.keys()), default="2")
    pet_type, pet_label = PET_TYPES[pet_choice]

    github_username = Prompt.ask(
        "\nGitHub username [dim](선택, 엔터로 건너뜀)[/dim]", default=""
    )

    console.print("\nAI API 키를 입력해주세요 [dim](Gemini / Claude / GPT)[/dim]")
    console.print("[dim]GITTCHI_API_KEY 환경변수로 대신 설정 가능[/dim]")
    api_key = Prompt.ask("API 키", password=True, default="")

    model = Prompt.ask("\n모델", default="gemini/gemini-2.5-flash")

    prev = get_current_hooks_path()

    config = Config(
        pet_name=name,
        pet_type=pet_type,
        github_username=github_username,
        api_key=api_key,
        model=model,
        prev_hooks_path=prev or None,
    )

    home().mkdir(parents=True, exist_ok=True)
    save_config(config)
    install(prev_hooks_path=prev)

    # HMAC 키 생성 + 초기 펫 상태 저장
    from gittchi.state.hmac_key import load_or_create
    from gittchi.state.pet import new_pet, save_pet
    from gittchi.state.memory import Memory, LongTermProfile, save_memory
    from gittchi.llm.client import call_llm
    from gittchi.llm.prompts import (
        first_impression_prompt,
        first_impression_with_profile_prompt,
        profile_generation_prompt,
    )

    load_or_create()
    save_pet(new_pet())

    console.print(f"\n[bold green]✓[/bold green] {pet_label} [bold]{name}[/bold] 탄생!")
    console.print("[dim]이제 모든 레포에서 커밋하면 자동으로 반응합니다.[/dim]")

    # GitHub 분석 (username 있을 때만)
    memory = Memory()
    greeting_prompt = first_impression_prompt(name, github_username)

    if github_username:
        with console.status(f"[dim]{github_username} GitHub 분석 중...[/dim]"):
            from gittchi.git_io.github_api import fetch, language_percentages
            profile = fetch(github_username)

        if profile:
            lang_pct = language_percentages(profile)  # 언어 없으면 빈 dict (정상)
            top_langs = list(lang_pct.keys())[:5]

            with console.status(f"[dim]{name} 분석 중...[/dim]"):
                from gittchi.llm.client import NEUTRAL_SYSTEM
                ai_summary = call_llm(
                    pet_type=pet_type,
                    pet_name=name,
                    model=model,
                    api_key=api_key,
                    user_prompt=profile_generation_prompt(github_username, lang_pct, profile.notable_repos),
                    override_system=NEUTRAL_SYSTEM,
                    empty_on_error=True,  # 실패 시 페르소나 fallback 저장 방지
                )

            memory.long_term = LongTermProfile(
                github_username=github_username,
                top_languages=top_langs,
                language_pct=lang_pct,
                notable_repos=profile.notable_repos,
                ai_summary=ai_summary,  # 실패 시 "" — petinfo에서 graceful 처리
            )
            if ai_summary:
                greeting_prompt = first_impression_with_profile_prompt(name, ai_summary)
        else:
            # fetch 실패(네트워크/rate limit)해도 username은 저장
            memory.long_term = LongTermProfile(github_username=github_username)
            console.print("[dim]GitHub 분석 실패. username만 저장됩니다.[/dim]")

    save_memory(memory)

    # 첫 인사
    with console.status(f"[dim]{name} 등장 중...[/dim]"):
        greeting = call_llm(
            pet_type=pet_type,
            pet_name=name,
            model=model,
            api_key=api_key,
            user_prompt=greeting_prompt,
            fallback_key="commit",
        )

    console.print(f"\n[bold]{name}[/bold]: \"{greeting}\"\n")
