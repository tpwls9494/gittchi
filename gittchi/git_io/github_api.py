from dataclasses import dataclass, field
import requests

BASE = "https://api.github.com"
TIMEOUT = 6


@dataclass
class GithubProfile:
    username: str
    language_bytes: dict[str, int] = field(default_factory=dict)  # 언어 → 총 바이트
    notable_repos: list[str] = field(default_factory=list)        # 최근 레포 이름 top 5


def fetch(username: str, token: str = "", max_repos: int = 30) -> GithubProfile | None:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        resp = requests.get(
            f"{BASE}/users/{username}/repos",
            params={"sort": "updated", "per_page": max_repos},
            headers=headers,
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        repos = resp.json()
    except Exception:
        return None

    language_bytes: dict[str, int] = {}
    notable_repos: list[str] = []

    for repo in repos[:15]:  # 언어 수집은 15개만 (API 호출 수 제한)
        notable_repos.append(repo["name"])
        try:
            lang_resp = requests.get(
                f"{BASE}/repos/{username}/{repo['name']}/languages",
                headers=headers,
                timeout=TIMEOUT,
            )
            if lang_resp.ok:
                for lang, count in lang_resp.json().items():
                    language_bytes[lang] = language_bytes.get(lang, 0) + count
        except Exception:
            continue

    return GithubProfile(
        username=username,
        language_bytes=language_bytes,
        notable_repos=notable_repos[:5],
    )


# GitHub 언어 바이트 보정 계수
# Jupyter Notebook: output/이미지가 실제 코드보다 훨씬 크므로 ×0.1 후 Python으로 합산
# HTML/CSS: 프레임워크 boilerplate가 많아 실력 대비 과대평가
_DEFLATION: dict[str, float] = {
    "Jupyter Notebook": 0.1,
    "HTML":             0.3,
    "CSS":              0.4,
    "SCSS":             0.4,
}
# 보정 후 다른 언어로 합산할 언어
_MERGE_INTO: dict[str, str] = {
    "Jupyter Notebook": "Python",
}


def _normalize(raw: dict[str, int]) -> dict[str, int]:
    result: dict[str, int] = {}
    for lang, count in raw.items():
        factor = _DEFLATION.get(lang, 1.0)
        target = _MERGE_INTO.get(lang, lang)
        result[target] = result.get(target, 0) + int(count * factor)
    return result


def language_percentages(profile: GithubProfile, top_n: int = 8) -> dict[str, float]:
    normalized = _normalize(profile.language_bytes)
    total = sum(normalized.values())
    if not total:
        return {}
    sorted_langs = sorted(normalized.items(), key=lambda x: -x[1])
    return {k: round(v / total * 100, 1) for k, v in sorted_langs[:top_n]}
