from dataclasses import dataclass, asdict, field, fields
from gittchi.paths import memory_json
from gittchi.state import store

SHORT_TERM_MAX = 50


@dataclass
class CommitRecord:
    timestamp: float
    message: str
    commit_type: str
    xp_gained: int


@dataclass
class LongTermProfile:
    github_username: str = ""
    top_languages: list[str] = field(default_factory=list)
    language_pct: dict[str, float] = field(default_factory=dict)
    notable_repos: list[str] = field(default_factory=list)
    ai_summary: str = ""  # LLM이 생성한 개발자 DNA 한두 문장


@dataclass
class Memory:
    short_term: list[CommitRecord] = field(default_factory=list)
    long_term: LongTermProfile = field(default_factory=LongTermProfile)
    # mid_term: Stage 4 (월별 압축)


def load_memory() -> Memory:
    """store.TamperedError 가능."""
    data = store.load(memory_json())
    if data is None:
        return Memory()

    records = [CommitRecord(**r) for r in data.get("short_term", [])]

    lt_data = data.get("long_term", {})
    valid_lt = {f.name for f in fields(LongTermProfile)}
    long_term = LongTermProfile(**{k: v for k, v in lt_data.items() if k in valid_lt})

    return Memory(short_term=records, long_term=long_term)


def save_memory(memory: Memory) -> None:
    store.save(memory_json(), {
        "short_term": [asdict(r) for r in memory.short_term],
        "long_term": asdict(memory.long_term),
    })


def add_commit(memory: Memory, record: CommitRecord) -> Memory:
    memory.short_term.append(record)
    # Stage 4에서 50개 초과 시 월별 요약으로 압축 예정
    if len(memory.short_term) > SHORT_TERM_MAX:
        memory.short_term = memory.short_term[-SHORT_TERM_MAX:]
    return memory


def recent_messages(memory: Memory, n: int = 10) -> list[str]:
    return [r.message for r in memory.short_term[-n:]]
