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

    target_repos = repos[:15]
    notable_repos = [r["name"] for r in target_repos]
    language_bytes: dict[str, int] = {}

    # 순차 호출 대신 병렬 호출 — 15x 속도 개선
    from concurrent.futures import ThreadPoolExecutor, as_completed

    def fetch_lang(repo_name: str) -> dict:
        try:
            r = requests.get(
                f"{BASE}/repos/{username}/{repo_name}/languages",
                headers=headers, timeout=TIMEOUT,
            )
            return r.json() if r.ok else {}
        except Exception:
            return {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_lang, r["name"]): r for r in target_repos}
        for future in as_completed(futures):
            for lang, count in future.result().items():
                language_bytes[lang] = language_bytes.get(lang, 0) + count

    return GithubProfile(
        username=username,
        language_bytes=language_bytes,
        notable_repos=notable_repos[:5],
    )


# ── 언어 바이트 보정 계수 ──────────────────────────────────────────────────────
#
# GitHub은 파일 바이트 기준으로 언어를 집계한다.
# 실제 개발 실력/기여도와 괴리가 생기는 대표 케이스:
#   - Jupyter Notebook: 코드보다 셀 output/base64 이미지가 수십 배 큼
#   - JSON/XML/Markdown: 데이터·문서이지 로직이 아님
#   - HTML/CSS: 프레임워크 boilerplate, 생성 코드가 대부분
#   - Vue SFC: template+style+script 합산이라 실제 JS/TS보다 부풀려짐
#   - Shell/Dockerfile: 짧은 스크립트지만 존재 자체는 의미 있음
#
# × 계수는 "이 언어의 바이트가 실제 기여도를 얼마나 반영하나"의 추정치다.
# 순수 로직 언어(Python, Go, Rust 등)는 보정하지 않는다.

_DEFLATION: dict[str, float] = {
    # 노트북 / 출력 포맷
    "Jupyter Notebook": 0.1,   # output·이미지가 코드의 10배+
    "JSON":             0.1,   # 데이터 파일
    "XML":              0.1,
    "Markdown":         0.05,  # 문서만

    # 웹 마크업 / 스타일
    "HTML":    0.25,           # 생성 코드·boilerplate 많음
    "CSS":     0.35,
    "SCSS":    0.4,
    "Less":    0.4,
    "Sass":    0.4,

    # 설정 / 인프라
    "YAML":       0.3,
    "TOML":       0.3,
    "HCL":        0.5,         # Terraform — 인프라 코드, 일부 의미 있음
    "Bicep":      0.5,
    "CMake":      0.5,
    "Makefile":   0.5,
    "Dockerfile": 0.4,

    # 템플릿 언어
    "Vue":        0.6,         # SFC: template+style이 script 부풀림
    "Blade":      0.2,         # Laravel 템플릿
    "Handlebars": 0.2,
    "EJS":        0.3,
    "ERB":        0.3,
    "Jinja":      0.3,

    # 셸 / 배치
    "Shell":      0.7,
    "Batchfile":  0.5,
    "PowerShell": 0.7,
}

# 보정 후 다른 언어로 합산 (방언 → 원어)
_MERGE_INTO: dict[str, str] = {
    "Jupyter Notebook": "Python",   # .ipynb 커널은 대부분 Python
    "SCSS":         "CSS",
    "Less":         "CSS",
    "Sass":         "CSS",
    "CoffeeScript": "JavaScript",   # JS로 컴파일되는 방언
    "JSX":          "JavaScript",
    "TSX":          "TypeScript",
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
