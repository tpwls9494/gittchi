from rich.console import Console
from rich.panel import Panel
from gittchi.config import load_config
from gittchi.state.pet import load_pet
from gittchi.state.store import TamperedError
from gittchi.rules.status import compute_status
from gittchi.ui.ascii_pets import get as get_kaomoji
from gittchi.state.pet import xp_for_next_level

console = Console()


def _xp_bar(xp: int, total: int = 100, width: int = 10) -> str:
    filled = round(xp / total * width)
    return "█" * filled + "░" * (width - filled)


def run() -> None:
    config = load_config()
    if not config.pet_name:
        console.print("[yellow]아직 초기화 안 됨. gittchi init 실행[/yellow]")
        return

    try:
        pet = load_pet()
    except TamperedError:
        console.print("[bold red]⚠️  변조 감지[/bold red] — gittchi init으로 재시작하세요.")
        return

    if pet is None:
        console.print("[yellow]펫 데이터 없음. gittchi init 실행[/yellow]")
        return

    status_name, status_emoji = compute_status(pet.last_commit_at, pet.streak_days)
    if pet.is_angry:
        status_name, status_emoji = "화남", "😤"
    kaomoji = get_kaomoji(config.pet_type, status_name)

    console.print(
        Panel(
            f"[bold]{config.pet_name}[/bold]  Lv.{pet.level}  {kaomoji}\n"
            f"{status_emoji}  {status_name}\n\n"
            f"XP  {_xp_bar(pet.xp, total=xp_for_next_level(pet.level))}  {pet.xp}/{xp_for_next_level(pet.level)}\n"
            f"총 커밋 {pet.total_commits}  |  연속 {pet.streak_days}일",
            title="🐾 펫 상태",
            border_style="yellow",
            padding=(0, 1),
        )
    )
