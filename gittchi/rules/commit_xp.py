XP_TABLE: dict[str, int] = {
    "feat":     15,
    "fix":      15,
    "refactor": 12,
    "test":     20,
    "docs":      8,
    "chore":     4,
    "unknown":   4,  # conventional commit 미사용
}


def commit_xp(commit_type: str, message: str) -> int:
    if not message.strip():
        return 0  # 빈 메시지 → XP 없음
    return XP_TABLE.get(commit_type, XP_TABLE["unknown"])
