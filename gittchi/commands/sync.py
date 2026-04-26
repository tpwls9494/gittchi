from datetime import datetime, timezone
import requests
from rich.console import Console
from rich.prompt import Confirm
from gittchi.config import load_config
from gittchi.state.pet import load_pet
from gittchi.state.store import TamperedError

console = Console()

SUPABASE_URL = "https://yfzgmshcmgtnzwhjywve.supabase.co"
SUPABASE_KEY = "sb_publishable_5AiAHIbXduF-m6dwVFIwvQ_DQjehYQ1"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates",
}


def run() -> None:
    config = load_config()
    if not config.pet_name:
        console.print("[yellow]gittchi init 먼저 실행하세요.[/yellow]")
        return

    try:
        pet = load_pet()
    except TamperedError:
        console.print("[red]변조 감지 — 동기화 불가.[/red]")
        return

    if pet is None:
        console.print("[yellow]펫 데이터 없음. gittchi init 실행하세요.[/yellow]")
        return

    username = config.github_username or config.pet_name
    console.print(
        f"[dim]랭킹에 등록할 정보:[/dim]\n"
        f"  유저: [bold]{username}[/bold]  "
        f"Lv.{pet.level}  XP {pet.xp}  연속 {pet.streak_days}일\n"
        "[dim](커밋 내용은 전송되지 않습니다)[/dim]"
    )

    if not Confirm.ask("글로벌 랭킹에 등록할까요?", default=True):
        console.print("[dim]취소됐습니다.[/dim]")
        return

    data = {
        "username": username,
        "pet_name": config.pet_name,
        "level": pet.level,
        "xp": pet.xp,
        "streak_days": pet.streak_days,
        "total_commits": pet.total_commits,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        resp = requests.post(
            f"{SUPABASE_URL}/rest/v1/rankings",
            json=data,
            headers=HEADERS,
            timeout=10,
        )
        if resp.ok:
            console.print(f"[bold green]✓[/bold green] 랭킹 등록 완료: [bold]{username}[/bold] Lv.{pet.level}")
        else:
            console.print(f"[red]등록 실패: {resp.status_code} {resp.text[:100]}[/red]")
    except Exception as e:
        console.print(f"[red]네트워크 오류: {e}[/red]")
