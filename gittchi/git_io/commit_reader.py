from dataclasses import dataclass


KNOWN_TYPES = ["feat", "fix", "refactor", "test", "docs", "chore"]


@dataclass
class CommitInfo:
    message: str
    diff_summary: str
    commit_type: str  # feat, fix, refactor, test, docs, chore, unknown


def read_last_commit() -> CommitInfo:
    try:
        import git
        repo = git.Repo(search_parent_directories=True)
        commit = repo.head.commit
        message = commit.message.strip()

        changed = list(commit.stats.files.keys())
        if changed:
            preview = ", ".join(changed[:5])
            suffix = f" 외 {len(changed) - 5}개" if len(changed) > 5 else ""
            diff_summary = f"{len(changed)}개 파일 변경: {preview}{suffix}"
        else:
            diff_summary = "첫 커밋"

        return CommitInfo(
            message=message,
            diff_summary=diff_summary,
            commit_type=_parse_type(message),
        )
    except Exception:
        return CommitInfo(message="(알 수 없음)", diff_summary="", commit_type="unknown")


def _parse_type(message: str) -> str:
    lower = message.lower()
    for t in KNOWN_TYPES:
        if lower.startswith(f"{t}:") or lower.startswith(f"{t}("):
            return t
    return "unknown"
