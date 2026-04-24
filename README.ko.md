<div align="center">

# 🧠 claw-memory-os

**[OpenClaw](https://github.com/openclaw/openclaw) 기반 AI 에이전트 영구 메모리 OS.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/ReS0421/claw-memory-os)](https://github.com/ReS0421/claw-memory-os/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/ReS0421/claw-memory-os)](https://github.com/ReS0421/claw-memory-os/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/ReS0421/claw-memory-os)](https://github.com/ReS0421/claw-memory-os/issues)

🇺🇸 [English](README.md)

</div>

---

AI 에이전트는 세션이 끝나면 잊는다. 이 레포는 데이터베이스, 임베딩, 벡터 검색 없이도 세션을 넘어 유지되는 파일 기반 메모리 운영체계를 제공한다.

지금의 구조는 단순한 `MEMORY.md` 하나가 아니다. 현재 운영 모델은 **MEMOS v3: Relevance Selection + Hot/Cold 로드 + TTL Archive** 다.

## 이 시스템이 하는 일

- 세션 시작 시 작은 정제된 메모리 표면만 읽는다
- 관련 있을 때만 깊은 문맥을 추가 로드한다
- 현재 상태와 이력 기록을 분리한다
- 세션 산출물을 증류해 durable memory로 승격한다
- 오래된 Topic 문서를 자동 아카이브해 vault 팽창을 막는다

최근 버전에서는 메모리를 `MEMORY.md`(마스터 인덱스), 도메인별 State 파일, append-only 로그, 재사용 가능한 패턴/케이스, 증류용 INBOX로 더 명확히 분리한다.

## 아키텍처

### Workspace

```text
workspace/                          ← OpenClaw 워크스페이스 (~/.openclaw/workspace/)
├── SOUL.md                         # 에이전트 정체성과 성격
├── USER.md                         # 사용자에 대한 정보
├── AGENTS.md                       # 세션 규칙, 메모리 워크플로우, vault 경로
├── BOOTSTRAP.md                    # 최초 설정 가이드
├── IDENTITY.md                     # 에이전트 정체성 포인터
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
├── scripts/
└── docs/
```

### Vault

```text
vault/
├── Archive/
├── Channels/
├── Daily/
├── Memory/
│   ├── MEMORY.md
│   ├── MEMORY_INBOX.md
│   ├── State/
│   ├── Log/
│   └── Patterns/
├── Sessions/
├── System/
├── Tickets/
└── Topics/
```

## 핵심 개념

### 메모리 계층 구조

```text
MEMORY.md                ← 마스터 인덱스 / 장기 기억 진입점
State/{domain}.md        ← 도메인별 현재 상태 (교체형)
Log/YYYY-MM.md           ← append-only 핵심 결정 로그
Patterns/                ← 재사용 가능한 패턴/케이스
MEMORY_INBOX.md          ← 증류 전 임시 버퍼

Channels/                ← 대화 스레드별 현재 상태
Topics/                  ← Channels에서 성숙된 후 승격된 지식
Tickets/                 ← 활성 태스크 (INDEX.md 개요 포함)
Daily/                   ← 시간축 이벤트 로그 (하루에 하나)
Sessions/                ← 아카이빙된 채널 히스토리
```

## 핵심 운영 모델

### 1. MEMOS v3

하나의 거대한 메모리 파일 대신 역할별로 분리한다.

- `Memory/MEMORY.md` 는 pointer-first 마스터 진입점
- `Memory/State/*.md` 는 도메인별 현재 상태
- `Memory/Log/YYYY-MM.md` 는 append-only 마일스톤
- `Memory/Patterns/` 는 재사용 가능한 패턴과 케이스
- `Memory/MEMORY_INBOX.md` 는 증류 전 intake 버퍼

두 가지 intake path를 함께 쓴다.
1. **즉시 경로** — 안정된 상태 변화, 인프라 변경, 확정된 패턴/케이스, 핵심 결정 → 적절한 장기 파일에 즉시 반영
2. **인박스 경로** — 불확실한 항목 → `MEMORY_INBOX.md` → 일일 증류가 판단 (승격 / 폐기 / 보류)

실전 운영에서는 `MEMORY.md`는 인덱스, 현재 상태는 `State/`, 이력은 `Log/`에 두는 식으로 역할을 분리하는 것이 좋다.

### 2. Relevance Selection

매 세션마다 전부 읽지 않는다.

일반적인 시작 흐름:
1. Channel abstract 스캔
2. 현재 채널 상세 읽기
3. `Tickets/INDEX.md` 읽기
4. `Memory/MEMORY.md` 읽기
5. 관련 `Memory/State/{domain}.md` 만 선택 로드
6. `Topics/` 와 대부분의 `System/` 문서는 cold 유지

이렇게 해야 컨텍스트 낭비를 줄이고 시작 비용을 낮출 수 있다.

### 3. Hot / Cold 로드

**Hot:** identity, user, channel scan, current channel, ticket index, master memory, relevant state files.

**Cold:** Topics, 상세 System 문서, 월별 로그, pattern library, 개별 ticket 파일.

Topics는 아래 중 하나일 때만 로드한다.
- 사용자가 해당 주제를 직접 언급
- 현재 ticket이 `linked_topics:` 로 명시
- 에이전트가 필요하다고 판단하고 이유를 한 줄로 먼저 밝힘

### 4. TTL Archive

일부 Topic 문서는 임시 산출물 성격이 강하다. 이런 경우 frontmatter에 다음을 둔다.

```yaml
archive_after: YYYY-MM-DD
```

주기 작업이 만료된 문서를 `Archive/deprecated-topics/` 로 이동시켜 active memory 팽창을 막는다.

## 설계 원칙

- **데이터베이스보다 파일**
- **단일 정본**
- **현재 상태와 이력 분리**
- **누적보다 증류**
- **경계 있는 성장**
- **canonical-first 참조**

### 증류 규칙

증류 크론 (`System/memory-rules.md` 참조)은 엄격한 규칙을 따른다:
- **승격**: 장기적으로 유지할 가치가 있는 것만
- **교체**: 현재 상태 파일은 누적보다 교체
- **append**: 과거 결정은 월별 로그에 append-only로 기록
- **절대 금지**: 활성 태스크를 장기 기억 파일에 넣지 않기 (그건 Tickets의 역할)
- **패턴/케이스 승격**: 반복성 또는 임팩트가 있을 때만
- 중복보다 포인터와 구조를 우선

### 세션 마무리

세션이 끝날 때:
1. 관련 Channel 파일 업데이트
2. 확인된 학습 내용을 MEMORY.md 또는 MEMORY_INBOX.md로 이동
3. 태스크 상태 변경 시 Tickets 업데이트
4. Channel `abstract` 프론트매터 갱신

## 시작하기

### 1. 워크스페이스 클론

```bash
git clone https://github.com/ReS0421/claw-memory-os.git ~/.openclaw/workspace
```

### 2. private vault 생성

```bash
cp -r vault-template/ ~/vaults/my-workspace/
cd ~/vaults/my-workspace
git init
git add -A
git commit -m "init: memory vault"
```

> vault 레포는 private 이어야 한다. 실제 메모리 데이터가 들어간다.

### 3. 세션 규칙 커스터마이즈

다음을 수정한다.
- `SOUL.md`
- `USER.md`
- `AGENTS.md`
- `System/MISSION.md`

### 4. 자동화 추가

권장 주기 작업:
- daily-log
- memory-distill
- vault-backup
- archive-cleanup

## Vault Template Quick Tour

`vault-template/`를 처음 열면 아래 순서로 보면 된다.

- `Memory/MEMORY.md` → 가벼운 마스터 진입점
- `Memory/State/` → 도메인별 현재 진실
- `Memory/Log/` → 월별 append-only 마일스톤
- `Memory/Patterns/` → 재사용 가능한 패턴과 문제→해결 케이스
- `Memory/MEMORY_INBOX.md` → 증류 전 intake 큐
- `Channels/` → 현재 대화 상태
- `Tickets/` → 활성 실행 상태
- `Topics/` → 장기 설계/지식 문서

간단한 기준은 이렇다.
- **현재 진실** → `State/`
- **히스토리 마일스톤** → `Log/`
- **재사용 교훈** → `Patterns/`
- **불확실한 intake** → `MEMORY_INBOX.md`

이 분리가 MEMOS v3의 핵심이다.
