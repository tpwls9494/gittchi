import sys

_TEMPLATE = """\
#!/bin/sh
# Gittchi post-commit hook

PREV_HOOKS_PATH="{prev_hooks_path}"
PYTHON="{python_exe}"

if [ -n "$PREV_HOOKS_PATH" ] && [ -x "$PREV_HOOKS_PATH/post-commit" ]; then
  "$PREV_HOOKS_PATH/post-commit" "$@" || exit $?
fi

"$PYTHON" -m gittchi react || true
"""


def render(prev_hooks_path: str = "", python_exe: str = "") -> str:
    exe = python_exe or sys.executable
    # Git Bash (Windows 포함)에서 경로 구분자는 포워드슬래시여야 함
    exe = exe.replace("\\", "/")
    prev = prev_hooks_path.replace("\\", "/")
    return _TEMPLATE.format(prev_hooks_path=prev, python_exe=exe)
