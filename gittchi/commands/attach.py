import sys
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm

console = Console()


def run() -> None:
    """현재 레포의 .git/hooks/post-commit에 Gittchi hook 설치."""
    try:
        import git
        repo = git.Repo(search_parent_directories=True)
    except Exception:
        console.print("[red]git 레포를 찾을 수 없어요. git 레포 안에서 실행해주세요.[/red]")
        return

    hdir = Path(repo.git_dir) / "hooks"
    hdir.mkdir(exist_ok=True)
    hook = hdir / "post-commit"
    python_exe = sys.executable.replace("\\", "/")

    if hook.exists():
        console.print(f"[yellow]기존 post-commit hook 발견[/yellow]: [dim]{hook}[/dim]")

        if not Confirm.ask(
            "기존 hook과 체이닝할까요? (기존 hook 먼저 실행 → gittchi react)",
            default=True,
        ):
            console.print("[dim]취소됐습니다.[/dim]")
            return

        # 기존 hook 백업
        prev_hook = hdir / "post-commit.prev"
        if prev_hook.exists():
            console.print("[yellow]post-commit.prev 이미 존재해요. 기존 백업을 덮어씁니다.[/yellow]")
        hook.rename(prev_hook)
        prev_hook.chmod(0o755)

        prev_path = str(prev_hook).replace("\\", "/")
        hook.write_text(
            f'#!/bin/sh\n'
            f'# Gittchi post-commit hook (chained)\n\n'
            f'PREV_HOOK="{prev_path}"\n\n'
            f'if [ -n "$PREV_HOOK" ] && [ -x "$PREV_HOOK" ]; then\n'
            f'  "$PREV_HOOK" "$@" || exit $?\n'
            f'fi\n\n'
            f'"{python_exe}" -m gittchi react || true\n',
            encoding="utf-8",
        )
        hook.chmod(0o755)
        console.print(f"[bold green]✓[/bold green] 체이닝 hook 설치 완료")
        console.print(f"[dim]기존 hook → post-commit.prev / 새 hook → post-commit[/dim]")
    else:
        hook.write_text(
            f'#!/bin/sh\n"{python_exe}" -m gittchi react || true\n',
            encoding="utf-8",
        )
        hook.chmod(0o755)
        console.print(f"[bold green]✓[/bold green] hook 설치 완료")

    console.print(f"[dim]{hook}[/dim]")
    console.print("[dim]이 레포에서 커밋하면 자동으로 반응합니다.[/dim]")
