from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from gittchi.config import load_config, save_config

console = Console()

PET_TYPES = {"dog", "cat", "rabbit", "bear"}
PET_LABELS = {"dog": "🐶 강아지", "cat": "🐱 고양이", "rabbit": "🐰 토끼", "bear": "🐻 곰"}


def run(model: str | None = None, api_key: str | None = None, pet_type: str | None = None) -> None:
    config = load_config()

    if model is None and api_key is None and pet_type is None:
        masked_key = (config.api_key[:8] + "..." + config.api_key[-4:]) if len(config.api_key) > 12 else ("설정됨" if config.api_key else "없음")
        console.print(Panel(
            f"펫:    [bold]{config.pet_name}[/bold] ({PET_LABELS.get(config.pet_type, config.pet_type)})\n"
            f"모델:  [cyan]{config.model}[/cyan]\n"
            f"키:    [dim]{masked_key}[/dim]\n"
            f"GitHub: [dim]{config.github_username or '미연동'}[/dim]",
            title="⚙️  현재 설정",
            border_style="blue",
            padding=(0, 1),
        ))
        console.print("[dim]변경: --model 모델명  /  --api-key 키  /  --pet-type dog|cat|rabbit|bear[/dim]")
        return

    changed = []

    if pet_type:
        if pet_type not in PET_TYPES:
            console.print(f"[red]유효하지 않은 펫 종류: {pet_type}[/red]")
            console.print(f"[dim]선택 가능: {' | '.join(PET_TYPES)}[/dim]")
            return
        if pet_type == config.pet_type:
            console.print(f"[dim]이미 {PET_LABELS[pet_type]}이에요.[/dim]")
            return

        console.print(
            f"[yellow]⚠️  펫 종류를 {PET_LABELS[config.pet_type]} → {PET_LABELS[pet_type]}으로 바꿉니다.[/yellow]\n"
            "[dim]대화 기억이 초기화됩니다. XP·레벨은 유지됩니다.[/dim]"
        )
        if not Confirm.ask("계속하시겠어요?", default=False):
            console.print("[dim]취소됐습니다.[/dim]")
            return

        config.pet_type = pet_type

        # 대화 기억 초기화
        try:
            from gittchi.state.memory import load_memory, save_memory
            memory = load_memory()
            memory.chat_history = []
            memory.chat_pet_type = pet_type
            save_memory(memory)
        except Exception:
            pass

        changed.append(f"펫 종류 → {PET_LABELS[pet_type]}")

    if model:
        config.model = model
        changed.append(f"모델 → [cyan]{model}[/cyan]")

    if api_key:
        config.api_key = api_key
        changed.append("API 키 업데이트")

    save_config(config)
    for msg in changed:
        console.print(f"[bold green]✓[/bold green] {msg}")
