# 🐾 Gittchi

**커밋할 때마다 반응하고, 나의 개발 여정을 기억하는 AI 동반자**

[![PyPI version](https://img.shields.io/pypi/v/gittchi?color=blue)](https://pypi.org/project/gittchi)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

혼자 사이드 프로젝트를 하다 보면 아무도 봐주지 않고, 반응도 없고, 결국 동기부여가 사라져 포기하게 된다.

Gittchi는 **git commit을 먹이로 자라는 AI 펫**이다. 커밋 횟수가 아닌 **내용을 읽고**, GitHub 레포를 분석해 **나를 기억한다**. 단순한 도구가 아닌, 혼자 개발하는 사람의 유일한 동반자.

```
기존 툴: "커밋 감사해요! +10 행복"
Gittchi: "오 드디어 그 인증 버그 고쳤네. 저번에 힘들어 보였는데."
```

---

## 데모

```
$ git commit -m "feat: 로그인 기능 추가"

╭─────────────────────────────────────────────────────╮
│ (っ≧▽≦)っ  람: "드디어 로그인이야! 저번에 막혔던    │
│ 거 해결했네. 진짜 대단한 거야!"                     │
│ 😊 행복  Lv.3 → Lv.4 ✨  XP ████░░░░░░ +15/400     │
╰─────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────╮
│ 🎉 업적 달성!  🔥 불꽃 개발자                       │
╰─────────────────────────────────────────────────────╯
```

```
$ gittchi status

╭──────────────── 🐾 펫 상태 ────────────────╮
│ 람  Lv.4  (っ≧▽≦)っ                        │
│ 😄  신남                                   │
│                                            │
│ XP  ████░░░░░░  42/400                     │
│ 총 커밋 23  |  연속 4일                    │
╰────────────────────────────────────────────╯
```

---

## 차별점

- **커밋 내용을 읽는다** — 숫자가 아닌 맥락을 이해
- **개발자를 기억한다** — GitHub 레포 분석으로 나를 파악
- **시간이 쌓일수록 나를 더 잘 안다** — 단순 도구가 아닌 동반자
- **Claude Code, cursor 등 AI 코딩 툴과 자동 연동** — 어디서 커밋해도 반응

---

## 설치

```bash
pip install gittchi
```

> **Windows:** Git for Windows + Windows Terminal 환경에서 네이티브 지원.  
> WSL2도 동일하게 사용 가능.

---

## 시작하기

```bash
gittchi init
```

```
🥚 Gittchi에 오신 걸 환영합니다!

펫의 이름을 지어주세요: > 람
어떤 펫으로 키울까요?  [1] 강아지  [2] 고양이  [3] 토끼  [4] 곰 > 1
GitHub username (선택): > tpwls9494
AI API 키 (Gemini/Claude/GPT): > ****
모델 [gemini/gemini-2.5-flash]: >

✓ 🐶 강아지 람 탄생!
람이 GitHub를 분석 중입니다...

람: "주인님! Python이랑 JS 많이 쓰네요! 빠르게 만드는 스타일이에요!"
```

이후 **모든 레포에서 커밋하면 자동으로 반응**한다. 별도 설정 없음.

### API 키 발급 (무료)

Gemini 무료 티어: [aistudio.google.com/apikey](https://aistudio.google.com/apikey) → "Get API key"  
→ 일 500회 무료 (커밋마다 1회, 1년 이상 무료 사용 가능)

---

## 커맨드

```bash
gittchi init                          # 최초 설정 + global hook 자동 설치
gittchi hello                         # 펫과 대화 (터미널 대화 모드)
gittchi hello "오늘 뭐 할까?"          # 단발 질문 (Claude Code 등 비인터랙티브 환경)
gittchi status                        # 펫 상태 · XP · 연속일 확인
gittchi petinfo                       # 내 개발자 프로필 + 포트폴리오 자동 생성
gittchi sync                          # 내 레벨·XP를 글로벌 랭킹에 등록 (opt-in)
gittchi rank                          # 글로벌 랭킹 확인
gittchi config                        # 현재 설정 확인
gittchi config --pet-type cat         # 펫 종류 변경 (dog|cat|rabbit|bear)
gittchi config --model gpt-4o-mini    # 모델 변경
gittchi config --api-key KEY          # API 키 변경
gittchi attach                        # 특정 레포에 추가로 hook 설치 (팀 레포 등)
gittchi uninstall                     # 작별 인사 후 삭제
```

---

## 펫 종류

| 펫 | 성격 | 특징 |
|----|------|------|
| 🐶 강아지 | 열정형 | 커밋마다 폭발적 반응, 오랜만에 오면 난리남 |
| 🐱 고양이 | 츤데레 | 칭찬 아끼지만 은근 응원, 오랜만에 오면 슬며시 다가옴 |
| 🐰 토끼 | 감성형 | 섬세하게 공감, 새벽 커밋에 걱정해줌 |
| 🐻 곰 | 듬직형 | 과묵하지만 깊은 응원, 묵묵히 옆에 있어줌 |

---

## 상태 시스템

매일 커밋하면 기뻐하고, 방치하면 아파한다.

| 상태 | 이모지 | 트리거 |
|------|--------|--------|
| 보통 | 😐 | 기본 |
| 행복 | 😊 | 오늘 커밋 |
| 신남 | 😄 | 3일 연속 |
| 최고 | 🥰 | 7일 연속 |
| 배고픔 | 😮‍💨 | 2일 이상 방치 |
| 슬픔 | 😢 | 5일 이상 |
| 아픔 | 🤒 | 7일 이상 |
| 위중 | 😷 | 10일 이상 |
| 화남 *(일시적)* | 😤 | 빈 커밋 메시지 |

---

## 레벨 시스템

레벨이 높아질수록 더 많은 XP가 필요하다.

```
Lv.1 → Lv.2 : 100 XP   (feat 커밋 약 7회)
Lv.2 → Lv.3 : 200 XP
Lv.5 → Lv.6 : 500 XP
Lv.10 → Lv.11 : 1000 XP
```

---

## 업적

| 업적 | 조건 |
|------|------|
| 🌱 첫 발걸음 | 첫 커밋 |
| 🔥 불꽃 개발자 | 3일 연속 |
| 💪 불굴의 의지 | 7일 연속 |
| 📦 시작이 반 | 커밋 10개 |
| 🏆 백전백승 | 커밋 100개 |
| 🧪 테스트 전도사 | test 커밋 5개 |
| 🌙 새벽 코더 | 자정~새벽 4시 커밋 |
| ⭐ 레벨업 고수 | Lv.5 달성 |

---

## 커밋 타입별 XP

[Conventional Commits](https://www.conventionalcommits.org) 규약을 쓸수록 혜택이 크다.

| 커밋 | XP |
|------|-----|
| `test` | +20 |
| `feat` / `fix` | +15 |
| `refactor` | +12 |
| `docs` | +8 |
| `chore` / 규약 없음 | +4 |
| 빈 메시지 | 0 + 화남 |

---

## 글로벌 랭킹

```bash
gittchi sync   # 내 레벨·XP 등록 (opt-in, 커밋 내용 미포함)
gittchi rank   # 리더보드 확인
```

```
        🏆 Gittchi 글로벌 랭킹  (42명)
┌─────┬───────────┬────┬──────┬────┬──────┐
│  1  │ devmaster │ 람 │ Lv.8 │ 80 │ 12일 │
│  2  │ codekim   │ 냥 │ Lv.7 │ 50 │  7일 │
│  3  │ park_dev  │ 몽 │ Lv.6 │ 30 │  3일 │
│  4  │ ...       │ ...│ ...  │ ...│ ...  │
│  5  │ ...       │ ...│ ...  │ ...│ ...  │
│ ... │ ...       │    │      │    │      │
│ 11  │ you-1     │    │ Lv.3 │ 90 │  1일 │
│ 12  │ tpwls9494 ◀│ 람 │ Lv.3 │ 40 │  1일 │
│ 13  │ you+1     │    │ Lv.3 │ 10 │  0일 │
│ ... │ ...       │    │      │    │      │
└─────┴───────────┴────┴──────┴────┴──────┘
```

---

## Claude Code / AI 도구와 함께

`gittchi init`만 해두면 Claude Code, cursor 등 AI 코딩 도구가 `git commit`을 실행할 때도 자동으로 반응한다.

```bash
# Claude Code 안에서도 바로 사용 가능
gittchi hello "오늘 테스트 코드 짜야 할까?"
# 람: "어제 feat 커밋하고 test는 한 개도 없잖아. 지금 짜."
```

---

## 메모리 시스템

```
단기 기억  →  최근 커밋 50개
중기 기억  →  월별 활동 요약 (자동 압축)
장기 기억  →  GitHub 레포 분석 기반 개발자 프로필
대화 기억  →  최근 10턴 (세션 간 유지, 펫 변경 시 초기화)
```

---

## 변조 감지

`pet.json`을 직접 수정해 XP·레벨을 올리면 HMAC 서명 불일치로 즉시 감지되고 펫이 초기화된다.

---

## 기술 스택

```
Python + Typer    → CLI 인터페이스
Rich              → 터미널 UI (카오모지, 색상, 패널)
LiteLLM           → AI 멀티 프로바이더 (Gemini, Claude, GPT 등)
GitPython         → 로컬 git 히스토리/diff 읽기
requests          → GitHub API · Supabase 랭킹
HMAC + JSON       → 상태 저장 + 변조 감지
```

---

## 라이선스

MIT
