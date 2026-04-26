from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def xp_bar(xp: int, total: int = 100, width: int = 10) -> str:
    filled = round(xp / total * width)
    return "█" * filled + "░" * (width - filled)


def reaction_panel(
    pet_name: str,
    kaomoji: str,
    response: str,
    status_emoji: str,
    status_name: str,
    level: int,
    old_level: int,
    xp: int,
    xp_gain: int,
    leveled_up: bool,
    max_xp: int = 100,
) -> Panel:
    level_str = (
        f"[bold cyan]Lv.{old_level} → Lv.{level} ✨[/bold cyan]"
        if leveled_up
        else f"Lv.{level}"
    )
    bar = xp_bar(xp, total=max_xp)
    status_line = f"{status_emoji} {status_name}  {level_str}  XP {bar} +{xp_gain}/{max_xp}"

    body = Text()
    body.append(f"{kaomoji}  ", style="bold")
    body.append(f'{pet_name}: "{response}"\n')
    body.append(status_line, style="dim")

    return Panel(body, border_style="yellow", padding=(0, 1))
