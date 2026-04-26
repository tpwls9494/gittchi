from dataclasses import dataclass, asdict, fields
from datetime import datetime, timezone, date
from gittchi.paths import pet_json
from gittchi.state import store

XP_PER_LEVEL = 100


@dataclass
class Pet:
    level: int = 1
    xp: int = 0
    total_commits: int = 0
    last_commit_at: float = 0.0
    created_at: float = 0.0      # init 시 설정, 이후 변경 없음
    streak_days: int = 0
    last_commit_date: str = ""   # YYYY-MM-DD
    is_angry: bool = False


def load_pet() -> Pet | None:
    """None = 미초기화. store.TamperedError = 변조 감지."""
    data = store.load(pet_json())
    if data is None:
        return None
    valid = {f.name for f in fields(Pet)}
    return Pet(**{k: v for k, v in data.items() if k in valid})


def save_pet(pet: Pet) -> None:
    store.save(pet_json(), asdict(pet))


def new_pet() -> Pet:
    now = datetime.now(timezone.utc).timestamp()
    return Pet(last_commit_at=now, created_at=now)


def apply_commit(pet: Pet, xp_gain: int, is_bad_commit: bool) -> tuple[Pet, int, bool]:
    """커밋 적용 후 (updated_pet, old_level, leveled_up) 반환."""
    now = datetime.now(timezone.utc)
    today = now.date().isoformat()

    # 이전 커밋의 화남 상태 해제 → 이번 커밋으로 재평가
    pet.is_angry = False

    # streak 계산
    if pet.last_commit_date:
        diff = (now.date() - date.fromisoformat(pet.last_commit_date)).days
        if diff == 1:
            pet.streak_days += 1
        elif diff > 1:
            pet.streak_days = 1
        # diff == 0: 같은 날 여러 커밋, streak 유지
    else:
        pet.streak_days = 1

    pet.last_commit_date = today
    pet.last_commit_at = now.timestamp()
    pet.total_commits += 1

    if is_bad_commit:
        pet.is_angry = True

    old_level = pet.level
    pet.xp += xp_gain
    while pet.xp >= XP_PER_LEVEL:
        pet.xp -= XP_PER_LEVEL
        pet.level += 1

    return pet, old_level, pet.level > old_level
