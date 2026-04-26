import sys
import subprocess
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm

console = Console()


def _get_local_hooks_path(repo_root: Path) -> str:
    """레포 로컬 core.hooksPath 반환. 없으면 ""."""
    result = subprocess.run(
        ["git", "config", "--local", "core.hooksPath"],
        cwd=str(repo_root), capture_output=True, text=True,
    )
    return result.stdout.strip()


def _set_local_hooks_path(repo_root: Path, path: str) -> None:
    subprocess.run(
        ["git", "config", "--local", "core.hooksPath", path],
        cwd=str(repo_root), check=True,
    )


def run() -> None:
    """현재 레포에 Gittchi hook 설치 (로컬 core.hooksPath 설정으로 글로벌 우선)."""
    try:
        import git
        repo = git.Repo(search_parent_directories=True)
    except Exception:
        console.print("[red]git 레포를 찾을 수 없어요. git 레포 안에서 실행해주세요.[/red]")
        return

    python_exe = sys.executable.replace("\\", "/")
    git_dir = Path(repo.git_dir)
    repo_root = Path(repo.working_dir)

    local_hooks_path = _get_local_hooks_path(repo_root)

    if local_hooks_path:
        # ── 이미 로컬 hooksPath 있음 (husky / lefthook 등) ──────────────────
        hooks_dir = (
            Path(local_hooks_path) if Path(local_hooks_path).is_absolute()
            else repo_root / local_hooks_path
        )
        hook = hooks_dir / "post-commit"
        console.print(f"[yellow]로컬 core.hooksPath 발견[/yellow]: [dim]{hooks_dir}[/dim]")

        if hook.exists():
            if not Confirm.ask(
                "기존 post-commit hook과 체이닝할까요?",
                default=True,
            ):
                console.print("[dim]취소됐습니다.[/dim]")
                return

            prev_hook = hooks_dir / "post-commit.prev"
            if prev_hook.exists():
                console.print("[yellow]post-commit.prev 이미 존재해요. 덮어씁니다.[/yellow]")
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
            console.print(f"[dim]기존 hook → post-commit.prev[/dim]")
        else:
            hooks_dir.mkdir(parents=True, exist_ok=True)
            hook.write_text(
                f'#!/bin/sh\n"{python_exe}" -m gittchi react || true\n',
                encoding="utf-8",
            )
            hook.chmod(0o755)
            console.print(f"[bold green]✓[/bold green] hook 설치 완료")

    else:
        # ── 로컬 hooksPath 없음 → .git/hooks 를 로컬로 지정 ─────────────────
        # 글로벌 core.hooksPath(~/.gittchi/hooks)를 이 레포에서만 오버라이드
        hooks_dir = git_dir / "hooks"
        hooks_dir.mkdir(exist_ok=True)
        hook = hooks_dir / "post-commit"

        hooks_path_str = str(hooks_dir).replace("\\", "/")
        _set_local_hooks_path(repo_root, hooks_path_str)

        if hook.exists():
            if not Confirm.ask(
                "기존 post-commit hook과 체이닝할까요?",
                default=True,
            ):
                _set_local_hooks_path(repo_root, "")  # 방금 설정한 로컬 값 되돌리기
                console.print("[dim]취소됐습니다.[/dim]")
                return

            prev_hook = hooks_dir / "post-commit.prev"
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
        else:
            hook.write_text(
                f'#!/bin/sh\n"{python_exe}" -m gittchi react || true\n',
                encoding="utf-8",
            )
            hook.chmod(0o755)
            console.print(f"[bold green]✓[/bold green] hook 설치 완료")

        console.print(f"[dim]로컬 core.hooksPath → {hooks_path_str}[/dim]")
        console.print("[dim](글로벌 설정보다 이 레포 설정이 우선 적용됩니다)[/dim]")

    console.print(f"[dim]{hook}[/dim]")
    console.print("[dim]이 레포에서 커밋하면 자동으로 반응합니다.[/dim]")
