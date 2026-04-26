# CLAUDE.md — Gittchi 핸드오프

> 새 세션이 cold-start로 작업하기 위한 구현 계약. 제품 스펙은 `PLAN.md`, 사용자 향은 `README.md`.

## 한 줄

git commit을 먹이로 자라는 AI 펫 CLI. 호들갑 떨지 않고, 짧고, 맥락을 안다.

## 스택

Python 3.10+ · Typer · Rich · LiteLLM · GitPython · requests · python-dotenv(선택)
빌드: `pyproject.toml`, dev install은 `pip install -e .`

## Repo 레이아웃

```
gittchi/                  # repo root
├── pyproject.toml
├── CLAUDE.md / PLAN.md / README.md / .gitignore
└── gittchi/              # Python 패키지
    ├── __init__.py
    ├── __main__.py            # python -m gittchi → cli.app()
    ├── cli.py                 # Typer app, thin wrapper
    ├── paths.py               # GITTCHI_HOME 등 경로 single source
    ├── config.py              # Config dataclass + load/save
    ├── commands/              # init, react, hello, status, petinfo, attach, uninstall
    ├── state/
    │   ├── pet.py             # Pet dataclass + XP/Lv 룰
    │   ├── memory.py          # 3단 메모리 + 압축
    │   ├── store.py           # JSON r/w + HMAC (단일 IO 경계)
    │   └── hmac_key.py
    ├── git_io/
    │   ├── hook_installer.py  # 설치/제거, 체이닝
    │   ├── hook_template.py   # 셸 스크립트 문자열
    │   ├── commit_reader.py   # GitPython 래퍼
    │   └── github_api.py      # init용 public repo 분석
    ├── llm/
    │   ├── client.py          # LiteLLM 래퍼, 타임아웃, fallback
    │   ├── prompts.py         # 이벤트별 템플릿
    │   └── personas.py        # 4종 펫 톤
    ├── rules/                 # commit_xp, status decay
    ├── ui/                    # render(Rich), ascii_pets
    └── portfolio/generator.py
```

원칙: IO 경계는 `state/store.py`, `git_io/`, `llm/`, `ui/` 네 곳뿐. `commands/*.py`는 한 파일 한 명령. `cli.py`는 선언만.

## 상태 저장 위치

`~/.gittchi/` 아래 (테스트는 `GITTCHI_HOME` 환경변수로 격리). 모든 경로는 `paths.py` 경유.

| 파일 | 소유 모듈 | 외부 직접 r/w |
|------|-----------|--------------|
| `pet.json` (HMAC 포함) | `state/store.py` | **금지** — HMAC 깨짐 |
| `memory.json` (HMAC 포함) | `state/store.py` | **금지** |
| `config.json` | `config.py` | 금지 |
| `.hmac_key` (chmod 600) | `state/hmac_key.py` | 금지 |
| `hooks/post-commit` | `git_io/hook_installer.py` | 금지 |

## Hook 아키텍처

`git config --global core.hooksPath ~/.gittchi/hooks` 로 단일 디렉터리 소유. `~/.config/git/hooks/`는 macOS에서 기본 활성 안 됨이라 사용 안 함.

`init` 시 직전 `core.hooksPath` 값을 `config.json` 의 `prev_hooks_path` 에 저장 (uninstall 복원 + 체이닝). Gittchi `post-commit`:

```sh
#!/bin/sh
if [ -n "$PREV_HOOK" ] && [ -x "$PREV_HOOK" ]; then
  "$PREV_HOOK" "$@" || exit $?
fi
gittchi react || true   # 펫이 죽어도 사용자 워크플로 안 막음
```

`gittchi react`는 `cli.py` 에서 `hidden=True`, `--dry-run` 지원, **어떤 예외에서도 exit 0** (git 워크플로 절대 차단 금지).

## LLM 계약

- 모든 호출은 `llm/client.py` 경유. `litellm` import는 함수 내부 lazy (모듈 최상단 import 시 CLI 시작 0.5s+ 느려짐)
- 타임아웃 6초 → 실패 시 페르소나별 정적 fallback 라인 (`personas.py` 의 `FALLBACK_LINES`)
- 프롬프트 템플릿은 `prompts.py` 에만 (f-string), 페르소나 톤 주입은 `personas.py` system message
- 기본 모델 `gemini/gemini-2.5-flash` (fallback `gemini/gemini-2.0-flash`). `GITTCHI_API_KEY` env 가 `config.json` 보다 우선

## HMAC 불변식

- `.hmac_key` 는 init 시 `os.urandom(32)`, `chmod 600`
- 서명 파일 구조: `{"data": {...}, "sig": "<hex>"}`
- 검증 실패 → 펫 초기화. **캐주얼 변조 감지 목적**, 결연한 우회 방어 아님

## 빌드 단계 (단계 완료 시 갱신)

- [x] **Stage 1** — Core loop: `init`(기본) + `react` + hook 설치 + LLM 반응
- [x] **Stage 2** — HMAC + 단기 기억 + status decay + hook 체이닝
- [x] **Stage 3** — GH 분석 + 장기 기억 + `hello` REPL
- [ ] **Stage 4** — `petinfo` + 메모리 압축 + `uninstall`/`attach` + ASCII

상세 산출물·결정 근거: `/Users/isejin/.claude/plans/enumerated-toasting-fern.md`

## 로컬 개발 루프

```bash
pip install -e .
gittchi react --dry-run                            # hook 없이 반응 테스트
GITTCHI_HOME=/tmp/gt-test gittchi init             # 격리 실험
```

각 Stage 끝에 실 git repo 에서 `git commit` → 반응 출력 1회 검증.

테스트 픽스처(Stage 2+): tempfile git repo, `gittchi.llm.client.completion` mock, `time.time` patch (status decay).

## 컨벤션 & 함정

- state는 dict 대신 `@dataclass`. 경로는 `paths.py` 경유 (하드코딩된 `~/.gittchi/...` 금지)
- 사용자 노출 한국어 문자열은 `prompts.py` / `ui/render.py` 에만 (톤 일관성)
- 사용자 노출 메시지에 이모지 OK, 코드 내부 로그/주석엔 금지
- 주석은 **WHY** 만. 의존성 추가 시 `pyproject.toml` + 이 문서 "스택" 동시 갱신
- `react`는 어떤 예외에서도 exit 0 — 펫 버그가 git 워크플로 차단하면 신뢰 즉사
