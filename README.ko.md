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

## 현재 아키텍처

### Workspace

```text
workspace/
├── SOUL.md
├── USER.md
├── AGENTS.md
├── BOOTSTRAP.md
├── IDENTITY.md
├── HEARTBEAT.md
├── TOOLS.md
├── System/
│   ├── memory-rules.md
│   ├── channel-archiving-rules.md
│   ├── infrastructure.md
│   ├── notion-ids.md
│   └── MISSION.md
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

## 핵심 운영 모델

### 1. MEMOS v3

하나의 거대한 메모리 파일 대신 역할별로 분리한다.

- `Memory/MEMORY.md` 는 pointer-first 마스터 진입점
- `Memory/State/*.md` 는 도메인별 현재 상태
- `Memory/Log/YYYY-MM.md` 는 append-only 마일스톤
- `Memory/Patterns/` 는 재사용 가능한 패턴과 케이스
- `Memory/MEMORY_INBOX.md` 는 증류 전 intake 버퍼

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

## 규모 대응

| 메모리 규모 | 권장 동작 |
|---|---|
| 1천 줄 이하 | 거의 전부 읽기 |
| 1천~5천 | channel abstract + selective state loading |
| 5천 이상 | archive 강화, Topics 통합, semantic retrieval 검토 |

## 레포 범위

이 레포는 **공개 템플릿 / 운영 모델** 이다.

실제 운영 vault는 별도 private 레포로 두고, 그 안에 실제:
- Channels
- Tickets
- Topics
- Logs
- durable memory
를 저장하는 방식이 권장된다.

## 라이선스

MIT

---

[OpenClaw](https://github.com/openclaw/openclaw) 🐾 로 구축됨
