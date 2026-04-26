import requests
from rich.console import Console
from rich.table import Table

console = Console()

SUPABASE_URL = "https://yfzgmshcmgtnzwhjywve.supabase.co"
SUPABASE_KEY = "sb_publishable_5AiAHIbXduF-m6dwVFIwvQ_DQjehYQ1"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}


def run() -> None:
    try:
        resp = requests.get(
            f"{SUPABASE_URL}/rest/v1/rankings",
            params={"select": "*", "order": "level.desc,xp.desc", "limit": "10"},
            headers=HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        rows = resp.json()
    except Exception as e:
        console.print(f"[red]랭킹 불러오기 실패: {e}[/red]")
        return

    if not rows:
        console.print("[dim]아직 등록된 유저가 없어요. gittchi sync로 먼저 등록하세요.[/dim]")
        return

    table = Table(title="🏆 Gittchi 글로벌 랭킹", border_style="yellow")
    table.add_column("#", style="dim", width=3)
    table.add_column("유저", style="bold")
    table.add_column("펫", style="cyan")
    table.add_column("레벨", justify="center")
    table.add_column("XP", justify="center")
    table.add_column("연속", justify="center")
    table.add_column("총 커밋", justify="center")

    for i, row in enumerate(rows, 1):
        table.add_row(
            str(i),
            row.get("username", "?"),
            row.get("pet_name", "?"),
            f"Lv.{row.get('level', 0)}",
            str(row.get("xp", 0)),
            f"{row.get('streak_days', 0)}일",
            str(row.get("total_commits", 0)),
        )

    console.print()
    console.print(table)
    console.print("[dim]내 정보 등록: gittchi sync[/dim]\n")
