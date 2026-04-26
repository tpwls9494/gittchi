from datetime import datetime, timezone
from rich.console import Console
from rich.panel import Panel
from gittchi.config import load_config
from gittchi.state.pet import load_pet
from gittchi.state.memory import load_memory
from gittchi.state.store import TamperedError
from gittchi.ui.ascii_pets import get as get_kaomoji
from gittchi.rules.status import compute_status
from gittchi.ui.render import xp_bar

console = Console()

PET_EMOJI = {"dog": "🐶", "cat": "🐱", "rabbit": "🐰", "bear": "🐻"}


def run() -> None:
    config = load_config()
    if not config.pet_name:
        console.print("[yellow]아직 초기화 안 됨. gittchi init 실행[/yellow]")
        return

    try:
        pet = load_pet()
        memory = load_memory()
    except TamperedError:
        console.print("[bold red]⚠️  변조 감지[/bold red] — gittchi init으로 재시작하세요.")
        return

    if pet is None:
        console.print("[yellow]펫 데이터 없음. gittchi init 실행[/yellow]")
        return

    lt = memory.long_term
    status_name, status_emoji = compute_status(pet.last_commit_at, pet.streak_days)
    kaomoji = get_kaomoji(config.pet_type, status_name)
    pet_icon = PET_EMOJI.get(config.pet_type, "🐾")

    # 함께한 날 계산 — created_at 기준 (last_commit_at은 커밋마다 갱신되어 사용 불가)
    now_ts = datetime.now(timezone.utc).timestamp()
    anchor = pet.created_at if pet.created_at > 0 else pet.last_commit_at
    days_together = max(1, int((now_ts - anchor) / 86400)) if anchor > 0 else 1

    # 헤더
    owner = lt.github_username or config.github_username or "unknown"
    console.print()
    console.print(Panel(
        f"[bold]{pet_icon} {config.pet_name}[/bold]  Lv.{pet.level}  {kaomoji}\n"
        f"주인: [cyan]{owner}[/cyan]   "
        f"함께한 날: [green]{days_together}일[/green]   "
        f"총 커밋: [yellow]{pet.total_commits}개[/yellow]",
        border_style="yellow",
        padding=(0, 1),
    ))

    # Developer DNA
    if lt.ai_summary:
        console.print(Panel(
            f"[dim italic]\"{lt.ai_summary}\"[/dim italic]",
            title="🧠 Developer DNA",
            border_style="blue",
            padding=(0, 1),
        ))

    # Tech Stack
    if lt.language_pct:
        stack_lines = []
        for lang, pct in list(lt.language_pct.items())[:6]:
            bar = "█" * round(pct / 10) + "░" * (10 - round(pct / 10))
            stack_lines.append(f"  {lang:<12} {bar}  {pct:.0f}%")
        console.print(Panel(
            "\n".join(stack_lines),
            title="🛠  Tech Stack",
            border_style="green",
            padding=(0, 1),
        ))

    # 활동 패턴
    from gittchi.portfolio.generator import count_commit_types
    counts = count_commit_types(memory)
    total = sum(counts.values()) or 1
    type_str = "  ".join(
        f"{k} {round(v/total*100)}%"
        for k, v in sorted(counts.items(), key=lambda x: -x[1])[:4]
    ) if counts else "커밋 없음"

    console.print(Panel(
        f"  연속 커밋: [green]{pet.streak_days}일[/green]   "
        f"XP {xp_bar(pet.xp)} {pet.xp}/100\n"
        f"  커밋 타입:  {type_str}",
        title="📅 활동 패턴",
        border_style="magenta",
        padding=(0, 1),
    ))

    # AI 포트폴리오 생성
    with console.status("[dim]포트폴리오 생성 중...[/dim]"):
        from gittchi.portfolio.generator import generate
        analysis = generate(
            pet_type=config.pet_type,
            pet_name=config.pet_name,
            model=config.model,
            api_key=config.api_key,
            pet=pet,
            memory=memory,
            github_username=owner,
            days_together=days_together,
        )

    if not analysis:
        analysis = "[dim]API 키가 없거나 호출에 실패했습니다. gittchi init에서 API 키를 확인하세요.[/dim]"

    console.print(Panel(
        analysis,
        title="✨ AI 분석",
        border_style="cyan",
        padding=(0, 1),
    ))

    # 업적
    from gittchi.rules.achievements import ACHIEVEMENTS
    unlocked = set(memory.unlocked_achievements)
    unlocked_list = [a for a in ACHIEVEMENTS if a.id in unlocked]
    if unlocked_list:
        line = "  ".join(f"{a.emoji} {a.name}" for a in unlocked_list)
        console.print(Panel(
            line,
            title=f"🎖️  업적 ({len(unlocked_list)}/{len(ACHIEVEMENTS)})",
            border_style="yellow",
            padding=(0, 1),
        ))

    console.print()
