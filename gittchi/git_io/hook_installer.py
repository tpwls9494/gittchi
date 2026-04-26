import subprocess
from gittchi.paths import hooks_dir, post_commit_hook
from gittchi.git_io.hook_template import render


def _to_git_path(path: str) -> str:
    """Windows 백슬래시 → Git이 인식하는 포워드슬래시."""
    return path.replace("\\", "/")


def get_current_hooks_path() -> str:
    try:
        result = subprocess.run(
            ["git", "config", "--global", "core.hooksPath"],
            capture_output=True, text=True,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def install(prev_hooks_path: str = "") -> None:
    hdir = hooks_dir()
    hdir.mkdir(parents=True, exist_ok=True)

    hook = post_commit_hook()
    hook.write_text(render(prev_hooks_path), encoding="utf-8")
    hook.chmod(0o755)  # Windows에서는 no-op이지만 오류 없음

    subprocess.run(
        ["git", "config", "--global", "core.hooksPath", _to_git_path(str(hdir))],
        check=True,
    )


def uninstall(prev_hooks_path: str = "") -> None:
    hook = post_commit_hook()
    if hook.exists():
        hook.unlink()

    if prev_hooks_path:
        subprocess.run(
            ["git", "config", "--global", "core.hooksPath", _to_git_path(prev_hooks_path)],
            check=True,
        )
    else:
        subprocess.run(
            ["git", "config", "--global", "--unset", "core.hooksPath"],
            check=False,
        )
