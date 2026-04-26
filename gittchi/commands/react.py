import time
from rich.console import Console
from rich.panel import Panel
from gittchi.config import load_config
from gittchi.git_io.commit_reader import read_last_commit
from gittchi.llm.client import call_llm
from gittchi.llm.prompts import commit_reaction_prompt
from gittchi.state.pet import load_pet, save_pet, new_pet, apply_commit
from gittchi.state.memory import load_memory, save_memory, add_commit, recent_messages, CommitRecord
from gittchi.state.store import TamperedError
from gittchi.rules.commit_xp import commit_xp
from gittchi.rules.status import compute_status

console = Console()


def run(dry_run: bool = False) -> None:
    try:
        _react(dry_run)
    except Exception:
        pass  # 펫 버그가 git 워크플로를 막으면 안 됨


def _react(dry_run: bool) -> None:
    config = load_config()
    if not config.pet_name:
        return

    commit = read_last_commit()
    if dry_run:
        console.print(f"[dim][dry-run] 커밋: {commit.message}[/dim]")

    # 상태 로드 (변조 시 초기화)
    try:
        pet = load_pet()
    except TamperedError:
        console.print(Panel("[bold red]⚠️  변조 감지[/bold red] 펫이 초기화됩니다.", border_style="red"))
        pet = None
    pet = pet or new_pet()

    try:
        memory = load_memory()
    except TamperedError:
        from gittchi.state.memory import Memory
        memory = Memory()

    # XP 계산
    is_bad = not commit.message.strip() or commit.message.strip() == "(알 수 없음)"
    xp_gain = commit_xp(commit.commit_type, commit.message)

    # 펫 상태 업데이트
    pet, old_level, leveled_up = apply_commit(pet, xp_gain, is_bad)

    # 메모리 업데이트
    record = CommitRecord(
        timestamp=time.time(),
        message=commit.message,
        commit_type=commit.commit_type,
        xp_gained=xp_gain,
    )
    memory = add_commit(memory, record)

    # 상태 계산
    status_name, status_emoji = compute_status(pet.last_commit_at, pet.streak_days)
    if pet.is_angry:
        status_name, status_emoji = "화남", "😤"

    # LLM 호출
    recent = recent_messages(memory, n=10)[:-1]  # 방금 추가한 커밋 제외
    prompt = commit_reaction_prompt(
        pet_name=config.pet_name,
        commit_msg=commit.message,
        diff_summary=commit.diff_summary,
        recent_commits=recent,
        status=status_name,
    )
    response = call_llm(
        pet_type=config.pet_type,
        pet_name=config.pet_name,
        user_prompt=prompt,
        model=config.model,
        api_key=config.api_key,
    )

    # 출력
    xp_bar = "█" * round(pet.xp / 100 * 10) + "░" * (10 - round(pet.xp / 100 * 10))
    level_str = (
        f"[bold cyan]Lv.{old_level} → Lv.{pet.level}[/bold cyan]"
        if leveled_up
        else f"Lv.{pet.level}"
    )
    status_line = f"{status_emoji} {status_name}  {level_str}  XP {xp_bar} +{xp_gain}"

    console.print(
        Panel(
            f'[bold]{config.pet_name}[/bold]: "{response}"\n[dim]{status_line}[/dim]',
            border_style="yellow",
            padding=(0, 1),
        )
    )

    # 상태 저장 (출력 후 — 저장 실패해도 반응은 이미 출력됨)
    save_pet(pet)
    save_memory(memory)
