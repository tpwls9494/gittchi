_TEMPLATE = """\
#!/bin/sh
# Gittchi post-commit hook

PREV_HOOKS_PATH="{prev_hooks_path}"

if [ -n "$PREV_HOOKS_PATH" ] && [ -x "$PREV_HOOKS_PATH/post-commit" ]; then
  "$PREV_HOOKS_PATH/post-commit" "$@" || exit $?
fi

gittchi react || true
"""


def render(prev_hooks_path: str = "") -> str:
    return _TEMPLATE.format(prev_hooks_path=prev_hooks_path)
