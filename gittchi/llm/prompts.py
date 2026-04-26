def commit_reaction_prompt(
    pet_name: str,
    commit_msg: str,
    diff_summary: str,
    recent_commits: list[str],
    status: str,
) -> str:
    recent = "\n".join(f"- {c}" for c in recent_commits[-5:]) if recent_commits else "없음"
    return (
        f"펫 이름: {pet_name}\n"
        f"현재 상태: {status}\n\n"
        f"최근 커밋 기록:\n{recent}\n\n"
        f"방금 한 커밋:\n"
        f"메시지: {commit_msg}\n"
        f"변경 요약: {diff_summary}\n\n"
        "위 커밋에 반응해줘. 최근 기록을 참고해서 맥락 있게."
    )


def first_impression_prompt(pet_name: str, github_username: str) -> str:
    if github_username:
        return (
            f"나는 {pet_name}야. 주인의 GitHub는 {github_username}야. "
            "처음 만나는 인사를 짧게 해줘."
        )
    return f"나는 {pet_name}야. 주인을 처음 만나는 인사를 짧게 해줘."


def first_impression_with_profile_prompt(pet_name: str, developer_summary: str) -> str:
    return (
        f"나는 {pet_name}야. 주인에 대해 알게 됐어: {developer_summary}\n"
        "이걸 바탕으로 주인을 처음 만나는 짧은 인사를 해줘."
    )


def profile_generation_prompt(
    username: str,
    language_pct: dict[str, float],
    notable_repos: list[str],
) -> str:
    lang_str = ", ".join(f"{k} {v}%" for k, v in list(language_pct.items())[:5])
    repo_str = ", ".join(notable_repos[:5]) if notable_repos else "없음"
    return (
        f"GitHub 개발자 분석:\n"
        f"유저명: {username}\n"
        f"주요 언어: {lang_str}\n"
        f"최근 레포: {repo_str}\n\n"
        "이 개발자의 특징을 한두 문장으로 요약해줘. "
        "어떤 분야, 어떤 스타일인지 간결하게. 한국어로."
    )


def hello_system_context(
    recent_commits: list[str],
    long_term_summary: str,
    status: str,
) -> str:
    recent = "\n".join(f"- {c}" for c in recent_commits) if recent_commits else "없음"
    profile = f"\n주인 정보: {long_term_summary}" if long_term_summary else ""
    return (
        f"현재 상태: {status}{profile}\n\n"
        f"최근 커밋 기록:\n{recent}"
    )
