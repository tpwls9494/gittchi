from rich.console import Console
from rich.panel import Panel
from gittchi.config import load_config, save_config

console = Console()


def run(model: str | None = None, api_key: str | None = None) -> None:
    config = load_config()

    if model is None and api_key is None:
        # 현재 설정 표시
        masked_key = (config.api_key[:8] + "..." + config.api_key[-4:]) if len(config.api_key) > 12 else ("설정됨" if config.api_key else "없음")
        console.print(Panel(
            f"펫:    [bold]{config.pet_name}[/bold] ({config.pet_type})\n"
            f"모델:  [cyan]{config.model}[/cyan]\n"
            f"키:    [dim]{masked_key}[/dim]\n"
            f"GitHub: [dim]{config.github_username or '미연동'}[/dim]",
            title="⚙️  현재 설정",
            border_style="blue",
            padding=(0, 1),
        ))
        console.print("[dim]변경: gittchi config --model 모델명  /  --api-key 키[/dim]")
        return

    changed = []
    if model:
        config.model = model
        changed.append(f"모델 → [cyan]{model}[/cyan]")
    if api_key:
        config.api_key = api_key
        changed.append("API 키 업데이트")

    save_config(config)
    for msg in changed:
        console.print(f"[bold green]✓[/bold green] {msg}")
