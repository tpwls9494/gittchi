from dataclasses import dataclass, asdict, field, fields
from gittchi.paths import memory_json
from gittchi.state import store

SHORT_TERM_MAX = 50
MID_TERM_MAX = 6


@dataclass
class CommitRecord:
    timestamp: float
    message: str
    commit_type: str
    xp_gained: int


@dataclass
class MonthlySummary:
    year_month: str           # "2025-04"
    commit_count: int
    top_types: dict[str, int] # {"feat": 10, "fix": 5}


@dataclass
class LongTermProfile:
    github_username: str = ""
    top_languages: list[str] = field(default_factory=list)
    language_pct: dict[str, float] = field(default_factory=dict)
    notable_repos: list[str] = field(default_factory=list)
    ai_summary: str = ""


@dataclass
class Memory:
    short_term: list[CommitRecord] = field(default_factory=list)
    mid_term: list[MonthlySummary] = field(default_factory=list)
    long_term: LongTermProfile = field(default_factory=LongTermProfile)
    chat_history: list[dict] = field(default_factory=list)          # hello 대화 기억 (최근 10턴)
    unlocked_achievements: list[str] = field(default_factory=list)  # 달성 업적 ID 목록


# ── 로드 / 저장 ──────────────────────────────────────────────────────────────

def load_memory() -> Memory:
    """store.TamperedError 가능."""
    data = store.load(memory_json())
    if data is None:
        return Memory()

    short = [CommitRecord(**r) for r in data.get("short_term", [])]

    mid = [
        MonthlySummary(**m)
        for m in data.get("mid_term", [])
    ]

    lt_data = data.get("long_term", {})
    valid_lt = {f.name for f in fields(LongTermProfile)}
    long_term = LongTermProfile(**{k: v for k, v in lt_data.items() if k in valid_lt})

    chat_history = data.get("chat_history", [])
    unlocked_achievements = data.get("unlocked_achievements", [])

    return Memory(
        short_term=short, mid_term=mid, long_term=long_term,
        chat_history=chat_history, unlocked_achievements=unlocked_achievements,
    )


def save_memory(memory: Memory) -> None:
    store.save(memory_json(), {
        "short_term":   [asdict(r) for r in memory.short_term],
        "mid_term":     [asdict(m) for m in memory.mid_term],
        "long_term":    asdict(memory.long_term),
        "chat_history":          memory.chat_history,
        "unlocked_achievements": memory.unlocked_achievements,
    })


# ── 커밋 추가 + 압축 ─────────────────────────────────────────────────────────

def add_commit(memory: Memory, record: CommitRecord) -> Memory:
    memory.short_term.append(record)
    if len(memory.short_term) > SHORT_TERM_MAX:
        memory = _compress_short_term(memory)
    return memory


def _compress_short_term(memory: Memory) -> Memory:
    """오래된 커밋 20개를 월별 요약으로 압축."""
    to_compress = memory.short_term[:20]
    memory.short_term = memory.short_term[20:]

    # 월별 그룹화
    from datetime import datetime, timezone
    monthly: dict[str, list[CommitRecord]] = {}
    for r in to_compress:
        ym = datetime.fromtimestamp(r.timestamp, tz=timezone.utc).strftime("%Y-%m")
        monthly.setdefault(ym, []).append(r)

    for ym, records in sorted(monthly.items()):
        type_counts: dict[str, int] = {}
        for r in records:
            type_counts[r.commit_type] = type_counts.get(r.commit_type, 0) + 1

        # 같은 달 요약이 있으면 합산
        existing = next((m for m in memory.mid_term if m.year_month == ym), None)
        if existing:
            existing.commit_count += len(records)
            for t, c in type_counts.items():
                existing.top_types[t] = existing.top_types.get(t, 0) + c
        else:
            memory.mid_term.append(MonthlySummary(
                year_month=ym,
                commit_count=len(records),
                top_types=type_counts,
            ))

    # 중기 기억도 6개 초과 시 오래된 것 제거
    if len(memory.mid_term) > MID_TERM_MAX:
        memory.mid_term = memory.mid_term[-MID_TERM_MAX:]

    return memory


# ── 헬퍼 ─────────────────────────────────────────────────────────────────────

def recent_messages(memory: Memory, n: int = 10) -> list[str]:
    return [r.message for r in memory.short_term[-n:]]
