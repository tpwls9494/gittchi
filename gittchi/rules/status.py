from datetime import datetime, timezone

# 방치 기반 (days since last commit) — 우선순위 높음
DECAY_THRESHOLDS: list[tuple[int, str, str]] = [
    (10, "위중",   "😷"),
    (7,  "아픔",   "🤒"),
    (5,  "슬픔",   "😢"),
    (2,  "배고픔", "😮‍💨"),
]

# 연속 커밋 기반 (streak days)
STREAK_THRESHOLDS: list[tuple[int, str, str]] = [
    (7, "최고", "🥰"),
    (3, "신남", "😄"),
    (1, "행복", "😊"),
]


def compute_status(last_commit_at: float, streak_days: int) -> tuple[str, str]:
    """(상태명, 이모지) 반환. 방치 상태가 streak보다 우선."""
    if last_commit_at <= 0:
        return "보통", "😐"

    now = datetime.now(timezone.utc).timestamp()
    days_since = (now - last_commit_at) / 86400

    for threshold, name, emoji in DECAY_THRESHOLDS:
        if days_since >= threshold:
            return name, emoji

    for threshold, name, emoji in STREAK_THRESHOLDS:
        if streak_days >= threshold:
            return name, emoji

    return "보통", "😐"
