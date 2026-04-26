from dataclasses import dataclass
from datetime import datetime


@dataclass
class Achievement:
    id: str
    emoji: str
    name: str
    desc: str


ACHIEVEMENTS: list[Achievement] = [
    Achievement("first_commit", "🌱", "첫 발걸음",     "첫 커밋"),
    Achievement("streak_3",     "🔥", "불꽃 개발자",   "3일 연속 커밋"),
    Achievement("streak_7",     "💪", "불굴의 의지",   "7일 연속 커밋"),
    Achievement("commits_10",   "📦", "시작이 반",     "커밋 10개 달성"),
    Achievement("commits_100",  "🏆", "백전백승",      "커밋 100개 달성"),
    Achievement("test_lover",   "🧪", "테스트 전도사", "test 커밋 5개 이상"),
    Achievement("night_coder",  "🌙", "새벽 코더",     "자정~새벽 4시 커밋"),
    Achievement("level_5",      "⭐", "레벨업 고수",   "Lv.5 달성"),
]

_ACHIEVEMENT_MAP = {a.id: a for a in ACHIEVEMENTS}


def get(achievement_id: str) -> Achievement | None:
    return _ACHIEVEMENT_MAP.get(achievement_id)


def check_new(pet, memory) -> list[Achievement]:
    """새로 달성한 업적 반환 + memory.unlocked_achievements 갱신."""
    from gittchi.state.memory import Memory

    unlocked = set(memory.unlocked_achievements)
    local_hour = datetime.now().hour

    test_count = sum(1 for r in memory.short_term if r.commit_type == "test")

    conditions: dict[str, bool] = {
        "first_commit": pet.total_commits >= 1,
        "streak_3":     pet.streak_days >= 3,
        "streak_7":     pet.streak_days >= 7,
        "commits_10":   pet.total_commits >= 10,
        "commits_100":  pet.total_commits >= 100,
        "test_lover":   test_count >= 5,
        "night_coder":  0 <= local_hour <= 4,
        "level_5":      pet.level >= 5,
    }

    new: list[Achievement] = []
    for achievement in ACHIEVEMENTS:
        if achievement.id not in unlocked and conditions.get(achievement.id, False):
            new.append(achievement)
            memory.unlocked_achievements.append(achievement.id)

    return new
