# 🐾 GitGotchi

**커밋할 때마다 반응하고, 나의 개발 여정을 기억하는 AI 동반자**

[![PyPI version](https://img.shields.io/pypi/v/gitgotchi?color=blue)](https://pypi.org/project/gitgotchi)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

혼자 사이드 프로젝트를 하다 보면 아무도 봐주지 않고, 반응도 없고, 결국 동기부여가 사라져 포기하게 된다.

GitGotchi는 **git commit을 먹이로 자라는 AI 펫**이다. 커밋 횟수가 아닌 **내용을 읽고**, 과거 레포를 분석해 **나를 기억한다**. 단순한 도구가 아닌, 혼자 개발하는 사람의 유일한 동반자.

```
기존 툴: "커밋 감사해요! +10 행복"
GitGotchi: "오 드디어 그 인증 버그 고쳤네. 저번에 힘들어 보였는데."
```

---

## 설치

```bash
pip install gitgotchi
```

---

## 시작하기

```bash
gitgotchi init
```

```
🥚 GitGotchi에 오신 걸 환영합니다!
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
gitgotchi init        # 최초 설정 + global hook 자동 설치
gitgotchi hello       # 펫과 대화
gitgotchi status      # 펫 상태 확인
gitgotchi petinfo     # 내 개발자 프로필 + 포트폴리오 자동 생성
gitgotchi attach      # 특정 레포에 추가로 hook 설치
gitgotchi uninstall   # 작별 인사 후 삭제
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

## 커밋할수록 더 잘 알아간다

커밋 내용을 읽고 맥락을 기억한다. 시간이 쌓일수록 대화가 달라진다.

```bash
$ gitgotchi hello
코코: "왜 불렀어"
> 오늘 뭐 할까?
코코: "어제 feat 커밋하고 오늘 아무것도 안 했잖아. 그 기능 테스트는 짰어?"
> 아직...
코코: "...그럴 줄 알았어. Python은 잘하면서 테스트는 항상 미루더라."
```

방치하면 펫이 아파간다. 다시 커밋하면 회복된다.

```bash
$ gitgotchi hello
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
$ gitgotchi petinfo

╔══════════════════════════════════════════════╗
║  🐱 코코 (Lv.12)          주인: tpwls9494   ║
║  함께한 기간: 127일        총 커밋: 342개    ║
╚══════════════════════════════════════════════╝

🧠 Developer DNA
  "AI 백엔드 빌더 — 빠른 프로토타입과 LLM에 강점"

🛠 Tech Stack
  │ Python      ████████░░  82%  Expert │
  │ FastAPI     ███████░░░  71%  Strong │
  │ LangChain   ███████░░░  68%  Strong │

⚡ 강점
  · LLM/RAG 파이프라인 설계 (프로젝트 4개)
  · 빠른 MVP 구현 (평균 2주 내 배포)

🏷️  한줄 소개 (포트폴리오용)
  "LLM/RAG 기반 AI 백엔드 개발자.
   아이디어를 빠르게 프로덕트로 만드는 것을 좋아하며
   Python과 FastAPI로 3개 이상의 AI 서비스를 배포한 경험 보유."
```

---

## AI 프로바이더

직접 API 키를 제공한다 (BYOK). 커밋당 1회 호출.

```bash
gitgotchi init --model gemini/gemini-2.5-flash  # 기본값 (무료 티어 활용 가능)
gitgotchi init --model claude-sonnet-4-6
gitgotchi init --model gpt-4o
```

---

## 기술 스택

```
Python + Typer    → CLI 인터페이스
Rich              → 터미널 UI (ASCII 펫, 색상, 패널)
LiteLLM           → AI 멀티 프로바이더
GitPython         → 로컬 git 히스토리/diff 읽기
requests          → GitHub API 호출
HMAC + JSON       → 상태 저장 + 변조 감지
```

---

## 라이선스

MIT
