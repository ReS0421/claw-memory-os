<div align="center">

# 🧠 claw-memory-os

**[OpenClaw](https://github.com/openclaw/openclaw) 기반 AI 에이전트 영구 메모리 시스템.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/ReS0421/claw-memory-os)](https://github.com/ReS0421/claw-memory-os/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/ReS0421/claw-memory-os)](https://github.com/ReS0421/claw-memory-os/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/ReS0421/claw-memory-os)](https://github.com/ReS0421/claw-memory-os/issues)

🇺🇸 [English](README.md)

</div>

---

AI 에이전트는 세션이 끝나면 모든 것을 잊는다. 이 프로젝트는 데이터베이스, 임베딩, 벡터 스토어 없이 — 마크다운 파일과 명확한 규칙만으로 — 재시작 후에도 살아남는 구조화된 파일 기반 메모리를 제공한다.

## 문제

AI 에이전트는 새 세션을 시작할 때마다 제로에서 출발한다. 어제 무슨 얘기를 했는지, 어떤 결정을 내렸는지, 어떤 작업이 진행 중인지 알지 못한다. 컨텍스트 윈도우는 세션 내에서는 도움이 되지만, 세션을 넘어서면? 전부 사라진다.

## 해결책

파일 기반 메모리 아키텍처:
- 에이전트가 세션 시작 시 메모리 파일을 **읽는다**
- 세션 중/후에 업데이트를 **기록한다**
- **증류 크론**이 매일 신호와 노이즈를 분리한다
- **아카이빙 규칙**이 메모리를 일정 크기 이하로 유지한다

벡터 데이터베이스 없음. 임베딩 없음. RAG 파이프라인 없음. 구조와 규율이 있는 마크다운 파일뿐.

## 아키텍처

```
workspace/                          ← OpenClaw 워크스페이스 (~/.openclaw/workspace/)
├── SOUL.md                         # 에이전트 정체성과 성격
├── USER.md                         # 사용자에 대한 정보 (시간이 지나며 학습)
├── AGENTS.md                       # 세션 규칙, 메모리 워크플로우, vault 경로
├── BOOTSTRAP.md                    # 최초 설정 의식 (완료 후 삭제)
├── IDENTITY.md                     # 에이전트 이름, 캐릭터, 분위기, 이모지
├── HEARTBEAT.md                    # 주기적 상태 점검 태스크
├── TOOLS.md                        # 로컬 환경 메모
├── CONTRIBUTING.md                 # 기여 가이드라인
├── LICENSE                         # MIT 라이선스
│
├── System/                         # 운영 규칙 (단일 정본)
│   ├── memory-rules.md             # 증류 규칙
│   ├── channel-archiving-rules.md  # 채널 트리밍 정책
│   ├── design-review-checklist.md  # 시스템 설계 검증
│   ├── infrastructure.md           # 인프라, 경로, 서비스
│   ├── notion-ids.md               # 외부 서비스 ID 레퍼런스
│   └── MISSION.md                  # 최상위 목표
│
├── skills/
│   └── openclaw-secretary/         # 메모리 관리, 증류, 일일 로그
│
├── scripts/                        # 자동화 유틸리티
│   ├── git-autocommit.sh           # 워크스페이스 변경 자동 커밋
│   ├── vault-backup.sh             # git 기반 vault 동기화
│   ├── archive-cleanup.sh          # 오래된 Tickets/Daily/Sessions → Archive/로 이관
│   └── cost-tracker.sh             # 토큰 사용량 추적
│
└── docs/
    └── deployment.md               # 서버/클라우드 배포 가이드

vault/                              ← 별도 git 레포 (실제 메모리 저장소)
├── Archive/                        # 아카이빙된 티켓, 일일 로그, 세션
├── Channels/                       # 대화 상태 (채널당 파일 하나)
├── Daily/                          # 일일 로그 (하루에 하나)
├── Memory/                         # MEMORY.md + INBOX + 리뷰 로그
├── Sessions/                       # 아카이빙된 세션 기록
├── System/                         # 선택적 로컬 사본 / workspace System/ 포인터
├── Tickets/                        # 태스크 추적 (T-001, T-002, ...)
└── Topics/                         # 장기 지식 문서
```

> **Workspace vs. Vault:** 워크스페이스는 에이전트 설정과 규칙을 담는다. Vault는 실제 메모리 데이터를 담는다. 둘은 별도의 git 레포 — 메모리를 노출하지 않고 워크스페이스(이 레포)를 공유할 수 있다.

## 핵심 개념

### 메모리 계층 구조

```
MEMORY.md          ← 장기 기억 (큐레이션됨, "6개월 후에도 중요할까?")
  ↑ 증류됨
Channels/          ← 대화 스레드별 현재 상태
Topics/            ← Channels에서 성숙된 후 승격된 지식
Tickets/           ← 활성 태스크 (INDEX.md 개요 포함)
  ↑ 기록됨
Daily/             ← 시간축 이벤트 로그 (하루에 하나)
Sessions/          ← 아카이빙된 채널 히스토리
```

### 이중 경로 메모리 수집

모든 것이 기억될 자격이 있는 건 아니다. 두 경로가 이를 처리한다:

1. **즉시 경로** — 인프라 변경, 핵심 결정, 확인된 패턴 → MEMORY.md로 직행
2. **인박스 경로** — 불확실한 항목 → MEMORY_INBOX.md → 일일 증류 크론이 판단 (승격 / 폐기 / 보류)

모든 결정은 감사 가능성을 위해 `Memory/review-log.md`에 기록된다.

### 채널 라이프사이클

채널은 구조화된 프론트매터로 대화 상태를 추적한다:

```yaml
---
channel: feature-discussion
abstract: 새 인증 흐름 설계 중. API 스펙 대기.
purpose: 인증 리디자인 프로젝트
current_focus: OAuth2 공급자 선정
last_updated: 2026-03-21
---
```

채널이 너무 커지면 (결정 10개 초과 또는 3KB 초과), 오래된 항목은 Sessions/로 아카이빙된다. `abstract` 필드는 전체 파일을 읽지 않고도 세션 시작 시 빠른 스캔을 가능하게 한다.

### 세션 중 체크포인트

긴 대화는 메모리 손실 위험이 있다. 체크포인트 트리거:
- 주제 전환 2회 이상
- 주요 설계/구현 완료
- 같은 주제 10턴 이상
- 사용자가 명시적으로 "체크포인트" 신호

### 증류 규칙

증류 크론 (`System/memory-rules.md` 참조)은 엄격한 규칙을 따른다:
- **승격**: "6개월 테스트"를 통과한 항목
- **교체**: 오래된 정보 (누적하지 않음)
- **절대 금지**: MEMORY.md에 활성 태스크 넣기 (그건 Tickets의 역할)
- **학습된 패턴**: 2회 이상 관찰 또는 높은 임팩트 필요
- **학습된 케이스**: 구체적인 문제→해결 쌍 필요
- Patterns와 Cases는 각 10개 이하 유지; 오래된 것은 병합하거나 폐기

### 세션 마무리

세션이 끝날 때:
1. 관련 Channel 파일 업데이트
2. 확인된 학습 내용을 MEMORY.md 또는 MEMORY_INBOX.md로 이동
3. 태스크 상태 변경 시 Tickets 업데이트
4. Channel `abstract` 프론트매터 갱신

## 시작하기

### 1. OpenClaw 설치

[OpenClaw 설치 가이드](https://github.com/openclaw/openclaw)를 따른다.

### 2. 워크스페이스 설정

**옵션 A — 워크스페이스로 클론 (권장):**

이 레포를 OpenClaw 워크스페이스로 직접 사용한다. `git-autocommit.sh`가 변경 사항을 자동으로 추적한다.

```bash
git clone https://github.com/ReS0421/claw-memory-os.git ~/.openclaw/workspace
```

**옵션 B — 파일 복사 (워크스페이스를 별도로 관리하는 경우):**

```bash
git clone https://github.com/ReS0421/claw-memory-os.git
cd claw-memory-os
cp SOUL.md USER.md AGENTS.md BOOTSTRAP.md IDENTITY.md HEARTBEAT.md TOOLS.md ~/.openclaw/workspace/
cp -r System/ skills/ scripts/ docs/ ~/.openclaw/workspace/
```

> 옵션 B의 경우, `git-autocommit.sh`는 워크스페이스가 독립적인 git 레포일 때만 작동한다. 아닌 경우 스크립트는 조용히 건너뛴다.

### 3. Vault 설정

```bash
# 템플릿에서 vault 생성
cp -r vault-template/ ~/vaults/my-workspace/
cd ~/vaults/my-workspace && git init && git add -A && git commit -m "init: memory vault"

# (선택) 백업/동기화를 위한 원격 추가
# ⚠️  VAULT 레포는 반드시 PRIVATE으로 설정 — 개인 메모리 데이터를 담고 있다.
# 절대 공개 레포를 vault에 사용하지 말 것.
# git remote add origin <your-PRIVATE-repo-url>
# git push -u origin main
```

> 모든 스크립트는 기본적으로 `~/vaults/my-workspace/`를 사용한다. 다른 경로를 사용하려면 실행 전에 `VAULT_PATH` (또는 `VAULT`)를 설정한다.

> **레포 공개 범위 규칙:**
> - `claw-memory-os` (이 워크스페이스 템플릿) — 공개 OK
> - 실제 운영 워크스페이스 레포 — 비공개 권장
> - Vault 레포 — **비공개 필수** (개인 메모리 데이터 포함)

### 4. 첫 실행

에이전트와 세션을 시작한다. `BOOTSTRAP.md`가 첫 대화를 안내한다:
- 에이전트 이름 짓기, 성격 설정
- `USER.md`에 본인 정보 입력
- `System/MISSION.md`에 목표 설정
- `AGENTS.md`에 vault 경로 업데이트

설정 완료 후 에이전트가 `BOOTSTRAP.md`를 삭제한다 — 일회성 의식이다.

### 5. 크론 설정 (권장)

```
daily-log         05:00    # 일일 요약 작성
memory-distill    05:30    # INBOX → MEMORY.md 증류
vault-backup      03:00    # Vault git 커밋 + push
```

크론 설정은 OpenClaw 문서를 참고한다.

### 배포 옵션

전용 PC에서 운영 중인가? SMB나 git 동기화로 여러 기기에서 vault에 접근하고 싶은가? 설정 가이드는 [docs/deployment.md](docs/deployment.md)를 참고한다.

## 설계 원칙

- **데이터베이스보다 파일.** 모든 것이 마크다운이다. git이 히스토리를 무료로 제공한다.
- **단일 정본.** 각 정보는 정확히 한 곳에만 존재한다. 나머지는 포인터다.
- **상태와 시간 분리.** 현재 상태 (Channels, Tickets)와 히스토리 기록 (Daily, Sessions)은 절대 섞이지 않는다.
- **경계 있는 성장.** 아카이빙 규칙과 증류가 메모리의 무한 증가를 막는다.
- **누적보다 증류.** 모든 것이 기억될 자격이 있는 건 아니다. 능동적 큐레이션이 수동적 저장을 이긴다.

## 규모별 대응

| 메모리 크기 | 접근 방식 |
|---|---|
| 1,000줄 미만 | 그냥 된다. 세션 시작 시 전부 읽기. |
| 1,000~5,000줄 | 빠른 스캔을 위한 채널 abstract. 세부 내용은 필요 시 읽기. |
| 5,000줄 초과 | 더 적극적인 아카이빙, 토픽 통합, 또는 시맨틱 검색. |

`HEARTBEAT.md`에 선택적 메모리 규모 체크가 포함되어 있다 — vault 설정 완료 후 활성화한다.

## 기여

이 시스템은 수주간의 반복을 거쳐 실제 일상 사용을 위해 구축되었다. 가이드라인은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참고한다.

## 라이선스

MIT

---

[OpenClaw](https://github.com/openclaw/openclaw) 🐾 로 만들어짐
