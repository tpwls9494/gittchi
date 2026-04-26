from gittchi.llm.client import call_llm
from gittchi.state.memory import Memory
from gittchi.state.pet import Pet


def petinfo_prompt(
    github_username: str,
    days_together: int,
    total_commits: int,
    ai_summary: str,
    language_pct: dict[str, float],
    notable_repos: list[str],
    commit_type_counts: dict[str, int],
) -> str:
    langs = ", ".join(f"{k} {v}%" for k, v in list(language_pct.items())[:5]) or "정보 없음"
    repos = ", ".join(notable_repos[:3]) or "정보 없음"
    types = ", ".join(f"{k} {v}회" for k, v in sorted(commit_type_counts.items(), key=lambda x: -x[1])[:4]) or "정보 없음"
    profile = f"개발자 특성: {ai_summary}\n" if ai_summary else ""

    return (
        f"개발자 정보:\n"
        f"GitHub: {github_username or '(미연동)'}\n"
        f"펫과 함께한 날: {days_together}일  총 커밋: {total_commits}개\n"
        f"주요 언어: {langs}\n"
        f"최근 레포: {repos}\n"
        f"커밋 패턴: {types}\n"
        f"{profile}\n"
        "아래 항목을 줄바꿈으로 구분해서 출력해줘 (JSON 없이):\n\n"
        "[강점]\n· (2가지)\n\n"
        "[개선 포인트]\n· (1-2가지)\n\n"
        "[한줄 소개]\n\"...\""
    )


def count_commit_types(memory: Memory) -> dict[str, int]:
    counts: dict[str, int] = {}
    for r in memory.short_term:
        counts[r.commit_type] = counts.get(r.commit_type, 0) + 1
    return counts


def generate(
    pet_type: str,
    pet_name: str,
    model: str,
    api_key: str,
    pet: Pet,
    memory: Memory,
    github_username: str,
    days_together: int,
) -> str:
    lt = memory.long_term
    commit_counts = count_commit_types(memory)

    prompt = petinfo_prompt(
        github_username=github_username,
        days_together=days_together,
        total_commits=pet.total_commits,
        ai_summary=lt.ai_summary,
        language_pct=lt.language_pct,
        notable_repos=lt.notable_repos,
        commit_type_counts=commit_counts,
    )
    return call_llm(
        pet_type=pet_type,
        pet_name=pet_name,
        model=model,
        api_key=api_key,
        user_prompt=prompt,
    )
