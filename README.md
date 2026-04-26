# 🐾 Gittchi

**커밋할 때마다 반응하고, 나의 개발 여정을 기억하는 AI 동반자**

[![PyPI version](https://img.shields.io/pypi/v/gittchi?color=blue)](https://pypi.org/project/gittchi)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

혼자 사이드 프로젝트를 하다 보면 아무도 봐주지 않고, 반응도 없고, 결국 동기부여가 사라져 포기하게 된다.

Gittchi는 **git commit을 먹이로 자라는 AI 펫**이다. 커밋 횟수가 아닌 **내용을 읽고**, 과거 레포를 분석해 **나를 기억한다**. 단순한 도구가 아닌, 혼자 개발하는 사람의 유일한 동반자.

```
기존 툴: "커밋 감사해요! +10 행복"
Gittchi: "오 드디어 그 인증 버그 고쳤네. 저번에 힘들어 보였는데."
```

---

## 차별점

기존 펫 툴들은 커밋 횟수를 세는 단순한 다마고치다.

Gittchi는 다르다:
- **커밋 내용을 읽는다** — 숫자가 아닌 맥락을 이해
- **개발자를 기억한다** — 과거 레포 분석으로 나를 파악
- **시간이 쌓일수록 나를 더 잘 안다** — 단순 도구가 아닌 동반자

---

## 대상 사용자

- 사이드 프로젝트를 혼자 진행하는 개발자
- 꾸준히 커밋하는 습관을 만들고 싶은 개발자
- 포트폴리오 자동 정리가 필요한 취준생

---

## 설치

```bash
pip install gittchi
```

---

## 시작하기

```bash
gittchi init
```

```
🥚 Gittchi에 오신 걸 환영합니다!
펫의 이름을 지어주세요: > 코코

어떤 펫으로 키울까요?
[🐶 강아지] [🐱 고양이] [🐰 토끼] [🐻 곰]
> 🐱

GitHub username: > tpwls9494
AI API 키를 입력해주세요 (Gemini/Claude/GPT): > ...

코코: "...생각보다 열심히 했네. Python이 제일 많고 주로 새벽에 코딩하더라."
```

이후 모든 레포에서 커밋하면 자동으로 반응한다. 별도 설정 없음.

```bash
$ git commit -m "feat: 로그인 기능 추가"

코코: "오 드디어 로그인 됐어? 저번에 힘들어 보였는데. 나쁘지 않아."
      [😊 행복] [창의력 XP +15] [Lv.3 → Lv.4]
```

---

## 커맨드

```bash
gittchi init        # 최초 설정 + global hook 자동 설치
gittchi hello       # 펫과 대화
gittchi status      # 펫 상태 확인
gittchi petinfo     # 내 개발자 프로필 + 포트폴리오 자동 생성
gittchi attach      # 특정 레포에 추가로 hook 설치
gittchi uninstall   # 작별 인사 후 삭제
```

---

## 펫 종류

| 펫 | 성격 | 특징 |
|----|------|------|
| 🐶 강아지 | 열정형 | 커밋마다 폭발적 반응, 오랜만에 오면 난리남 |
| 🐱 고양이 | 츤데레 | 칭찬 아끼지만 은근 응원, 오랜만에 오면 슬며시 다가옴 |
| 🐰 토끼 | 감성형 | 섬세하고 공감 잘함, 새벽 커밋에 걱정해줌 |
| 🐻 곰 | 듬직형 | 과묵하지만 깊은 응원, 묵묵히 옆에 있어줌 |

---

## 상태 시스템

| 상태 | 이모지 | 트리거 |
|------|--------|--------|
| 행복 | 😊 | feat 커밋, 꾸준한 커밋 |
| 화남 | 😤 | 커밋 메시지 없음, 같은 버그 반복 |
| 배고픔 | 😮‍💨 | 마지막 커밋 2일 이상 |
| 슬픔 | 😢 | 마지막 커밋 5일 이상 |
| 아픔 | 🤒 | 마지막 커밋 7일 이상 |
| 위중 | 😷 | 마지막 커밋 10일 이상 |

**회복:** 어떤 커밋이든 하면 회복됨 (feat/fix → 빠른 회복, chore/docs → 느린 회복)

---

## 커밋할수록 더 잘 알아간다

커밋 내용을 읽고 맥락을 기억한다. 시간이 쌓일수록 대화가 달라진다.

```bash
$ gittchi hello
코코: "왜 불렀어"
> 오늘 뭐 할까?
코코: "어제 feat 커밋하고 오늘 아무것도 안 했잖아. 그 기능 테스트는 짰어?"
> 아직...
코코: "...그럴 줄 알았어. Python은 잘하면서 테스트는 항상 미루더라."
```

방치하면 펫이 아파간다. 다시 커밋하면 회복된다.

```bash
$ gittchi hello
코코: "...왔어?"
      "...딱히 기다린 건 아니거든."
      [😢 슬픔 — 커밋하면 회복됩니다]
```

---

## 커밋 타입별 효과

[Conventional Commits](https://www.conventionalcommits.org) 규약을 쓸수록 XP 혜택이 크다.

| 커밋 | 비유 | 효과 |
|------|------|------|
| `feat` | 🍖 영양식 | 창의력 +15 |
| `fix` | 💊 약 | 문제해결 +15 |
| `refactor` | 🥗 건강식 | 완성도 +12 |
| `test` | 🥦 보약 | 신뢰도 +20 |
| `docs` | 🍵 차 | 소통력 +8 |
| `chore` | 🍬 간식 | 소량 회복 |
| 규약 없는 메시지 | 🍺 정크푸드 | 최소 XP |
| 빈 메시지 | ☠️ 독 | XP 없음 + 화남 |

---

## `/petinfo` — 포트폴리오 자동 생성

```bash
$ gittchi petinfo

╔══════════════════════════════════════════════╗
║  🐱 코코 (Lv.12)          주인: tpwls9494   ║
║  함께한 기간: 127일        총 커밋: 342개    ║
╚══════════════════════════════════════════════╝

🧠 Developer DNA
  "AI 백엔드 빌더 — 빠른 프로토타입과 LLM에 강점"
  주로 새벽에 집중, 아이디어를 빠르게 MVP로 만드는 스타일

🛠 Tech Stack
  ┌─────────────────────────────────────┐
  │ Python      ████████░░  82%  Expert │
  │ FastAPI     ███████░░░  71%  Strong │
  │ LangChain   ███████░░░  68%  Strong │
  │ React       █████░░░░░  53%  Mid    │
  │ Docker      ████░░░░░░  41%  Basic  │
  └─────────────────────────────────────┘

⚡ 강점
  · LLM/RAG 파이프라인 설계 (프로젝트 4개)
  · 빠른 MVP 구현 (평균 2주 내 배포)
  · API 설계 및 백엔드 아키텍처

⚠️  개선 포인트
  · 테스트 코드 비율 3% (업계 평균 20%)
  · 프론트엔드 커밋 비율 낮음

📅 활동 패턴
  · 주 활동: 화~목 / 주로 오후 10시~새벽 2시
  · 평균 커밋 간격: 1.2일
  · 가장 많이 쓰는 커밋: feat (41%), fix (28%)

📁 대표 프로젝트
  ┌─────────────────────────────────────────────────┐
  │ PASS       AI 특허 명세서 자동 생성 시스템      │
  │            Python · FastAPI · Qwen3 · FAISS     │
  │                                                 │
  │ Shop-RAG   이커머스 AI 고객 상담 플랫폼         │
  │            LangGraph · FastAPI · Supabase       │
  │                                                 │
  │ Zivo       한일 항공권 최저가 조합 서비스        │
  │            Next.js · FastAPI · PostgreSQL       │
  └─────────────────────────────────────────────────┘

🏷️  한줄 소개 (포트폴리오용)
  "LLM/RAG 기반 AI 백엔드 개발자.
   아이디어를 빠르게 프로덕트로 만드는 것을 좋아하며
   Python과 FastAPI로 3개 이상의 AI 서비스를 배포한 경험 보유."
```

---

## AI 프로바이더

직접 API 키를 제공한다 (BYOK). 커밋당 1회 호출.

```bash
gittchi init --model gemini/gemini-2.5-flash  # 기본값
gittchi init --model claude-sonnet-4-6
gittchi init --model gpt-4o
```

---

## 메모리 시스템

```
단기 기억  →  최근 커밋 50개 (상세)
중기 기억  →  월별 활동 요약 (최근 6개월)
장기 기억  →  개발자 프로필 (압축된 핵심 특성)
대화 기억  →  최근 10턴

커밋 50개 초과 → 월별 요약으로 자동 압축
월별 요약 6개 초과 → 분기 요약으로 압축
```

---

## 파일 구조

```
~/.gittchi/
├── pet.json          # 펫 상태 (HMAC 서명 포함)
├── memory.json       # 커밋 기억 (3단계)
└── config.json       # API 키, 모델 설정

~/.config/git/hooks/
└── post-commit       # global hook (gittchi init 시 자동 설치)
```

---

## 변조 감지

- `pet.json` HMAC 서명으로 직접 XP/레벨 수정 감지
- 변조 감지 시 펫 초기화
- 재설치 = 새 펫 시작 (이전 펫과 작별)

---

## 기술 스택

```
Python + Typer    → CLI 인터페이스
Rich              → 터미널 UI (ASCII 펫, 색상, 패널)
LiteLLM           → AI 멀티 프로바이더 (Gemini, Claude, GPT 등)
GitPython         → 로컬 git 히스토리/diff 읽기
requests          → GitHub API 호출
python-dotenv     → 환경변수 관리
HMAC + JSON       → 상태 저장 + 변조 감지
pyproject.toml    → pip 패키지 빌드
```

---

## 라이선스

MIT
