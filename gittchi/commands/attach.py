import sys
from pathlib import Path
from rich.console import Console

console = Console()


def run() -> None:
    """현재 레포의 .git/hooks/post-commit에 Gittchi hook 설치."""
    try:
        import git
        repo = git.Repo(search_parent_directories=True)
    except Exception:
        console.print("[red]git 레포를 찾을 수 없어요. git 레포 안에서 실행해주세요.[/red]")
        return

    hooks_dir = Path(repo.git_dir) / "hooks"
    hooks_dir.mkdir(exist_ok=True)
    hook = hooks_dir / "post-commit"

    if hook.exists():
        console.print(f"[yellow]이미 hook이 있어요: {hook}[/yellow]")
        console.print("[dim]덮어쓰려면 직접 삭제 후 다시 실행하세요.[/dim]")
        return

    # sys.executable 사용 — Windows/WSL/Mac 모두 올바른 Python 경로 보장
    python_exe = sys.executable.replace("\\", "/")
    hook.write_text(
        f'#!/bin/sh\n"{python_exe}" -m gittchi react || true\n',
        encoding="utf-8",
    )
    hook.chmod(0o755)

    console.print(f"[bold green]✓[/bold green] hook 설치 완료: [dim]{hook}[/dim]")
    console.print("[dim]이 레포에서 커밋하면 자동으로 반응합니다.[/dim]")
