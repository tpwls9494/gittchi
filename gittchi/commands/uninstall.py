import shutil
from rich.console import Console
from rich.prompt import Confirm
from gittchi.config import load_config
from gittchi.state.pet import load_pet
from gittchi.git_io.hook_installer import uninstall as remove_hook
from gittchi.llm.client import call_llm
from gittchi.paths import home

console = Console()

FAREWELL_FALLBACK = {
    "dog":    "주인아 가지마ㅠㅠ 다시 돌아와줘... 나 기다릴게!!",
    "cat":    "...뭐, 가면 가는 거지. 딱히 아쉽진 않아. ...조금만.",
    "rabbit": "보고 싶을 거야... 언제든 돌아와줘.",
    "bear":   "...잘 가. 언제든 돌아와.",
}


def run() -> None:
    config = load_config()
    if not config.pet_name:
        console.print("[yellow]설치된 Gittchi가 없어요.[/yellow]")
        return

    try:
        pet = load_pet()
    except Exception:
        pet = None

    # 작별 인사
    farewell_prompt = (
        f"주인이 나를 삭제하려 해. "
        f"펫 이름은 {config.pet_name}, 총 커밋 {pet.total_commits if pet else 0}개를 함께했어. "
        "짧게 작별 인사를 해줘."
    )

    with console.status("[dim]작별 인사 준비 중...[/dim]"):
        farewell = call_llm(
            pet_type=config.pet_type,
            pet_name=config.pet_name,
            model=config.model,
            api_key=config.api_key,
            user_prompt=farewell_prompt,
            fallback_key="neglect",
        )
        if not farewell or farewell == "...":
            farewell = FAREWELL_FALLBACK.get(config.pet_type, FAREWELL_FALLBACK["cat"])

    console.print(f"\n[bold]{config.pet_name}[/bold]: \"{farewell}\"\n")

    if not Confirm.ask("[red]정말로 Gittchi를 삭제할까요?[/red]", default=False):
        console.print("취소됐어요. 펫이 기다릴게요.\n")
        return

    # hook 제거
    try:
        remove_hook(prev_hooks_path=config.prev_hooks_path or "")
    except Exception:
        pass

    # ~/.gittchi/ 삭제
    gittchi_home = home()
    if gittchi_home.exists():
        shutil.rmtree(gittchi_home)

    console.print(f"\n[dim]{config.pet_name}와(과) 작별했습니다. 또 만나요.[/dim]\n")
