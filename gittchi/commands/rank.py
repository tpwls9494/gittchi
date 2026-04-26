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
    from gittchi.config import load_config
    config = load_config()
    my_username = config.github_username or config.pet_name

    try:
        resp = requests.get(
            f"{SUPABASE_URL}/rest/v1/rankings",
            params={"select": "*", "order": "level.desc,xp.desc", "limit": "200"},
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

    total = len(rows)

    # 10명 이하면 전체 표시
    if total <= 10:
        show_indices = set(range(total))
    else:
        my_idx = next((i for i, r in enumerate(rows) if r["username"] == my_username), None)
        # 상위 5명
        show_indices = set(range(min(5, total)))
        # 내 주변 ±1
        if my_idx is not None:
            for i in range(max(0, my_idx - 1), min(total, my_idx + 2)):
                show_indices.add(i)

    # 표시할 항목 + "..." 구분선 계산
    sorted_indices = sorted(show_indices)
    display: list[int | None] = []
    prev = -1
    for idx in sorted_indices:
        if idx > prev + 1:
            display.append(None)  # "..." 구분선
        display.append(idx)
        prev = idx
    if prev < total - 1:
        display.append(None)  # 뒤에 더 있음

    # 렌더링
    my_idx_global = next((i for i, r in enumerate(rows) if r["username"] == my_username), None)

    table = Table(title=f"🏆 Gittchi 글로벌 랭킹  ({total}명)", border_style="yellow")
    table.add_column("#", style="dim", width=4)
    table.add_column("유저", style="bold")
    table.add_column("펫", style="cyan")
    table.add_column("레벨", justify="center")
    table.add_column("XP", justify="center")
    table.add_column("연속", justify="center")

    for item in display:
        if item is None:
            table.add_row("...", "...", "", "", "", "")
            continue
        row = rows[item]
        rank = item + 1
        is_me = row["username"] == my_username
        style = "bold yellow" if is_me else ""
        me_mark = " ◀" if is_me else ""
        table.add_row(
            str(rank),
            row.get("username", "?") + me_mark,
            row.get("pet_name", "?"),
            f"Lv.{row.get('level', 0)}",
            str(row.get("xp", 0)),
            f"{row.get('streak_days', 0)}일",
            style=style,
        )

    console.print()
    console.print(table)
    if my_idx_global is None:
        console.print("[dim]내 정보 등록: gittchi sync[/dim]")
    else:
        console.print(f"[dim]내 순위: {my_idx_global + 1}위  |  정보 갱신: gittchi sync[/dim]")
    console.print()
