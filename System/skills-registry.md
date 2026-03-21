---
title: Skills Registry
updated: 2026-03-20
---

# Skills Registry

로컬 스킬 목록 및 역할 정의. 상세 구현은 각 SKILL.md 참조.

## 로컬 스킬 (`~/.openclaw/workspace/skills/`)

| 스킬 | 경로 | 역할 |
|---|---|---|
| knowledge-ops | `skills/knowledge-ops/` | Obsidian↔Notion 이중 운영 상위 규칙 |
| notion-portfolio-api | `skills/notion-portfolio-api/` | Notion DB 스키마/블록 구문 레퍼런스 |
| notion-general | `skills/notion-general/` | Notion General 공간 운영 (내부 정제 레이어) |
| obsidian-governance | `skills/obsidian-governance/` | vault 내부 운영 규칙 |
| intel-x-post | `skills/intel-x-post/` | Intel Pipeline 보고서 → X 포스트 변환 |
| openclaw-secretary | `skills/openclaw-secretary/` | 운영 문서, 기억, 로그 관리 |
| second-brain-operator | `skills/second-brain-operator/` | Second Brain 운영 (Obsidian/Notion) |
| finance-researcher | `skills/finance-researcher/` | 금융·시장 리서치 파이프라인 (거시경제, 섹터, 이슈) |
| finance-analyst | `skills/finance-analyst/` | 투자 분석 파이프라인 (종목/섹터 펀더멘털, 밸류에이션) |
| dev-research | `skills/dev-research/` | 기술 리서치 파이프라인 (AI/ML 논문, 트렌드, 아키텍처) |
| skill-creator | `skills/skill-creator/` | 스킬 작성 및 감사/개선 |
| coder-architect | `skills/coder-architect/` | 시스템 설계 + 기능 명세 통합 (복잡한 프로젝트) |
| coder-planner | `skills/coder-planner/` | 구현 계획/파일 구조/태스크 분해 + ACP 직접 위임 |
| coder-designer | `skills/coder-designer/` | UI/UX 구조 설계 (ui-spec.md 단일 산출) |
| coder-developer | `skills/coder-developer/` | diff 리뷰/스펙 대조/테스트 검증 (reviewer, 코드 수정 금지) |
| coder-spec | `skills/coder-spec/` | 기능 명세 전담 (확장형, architect에서 분리 시) |
| repo-scanner | `skills/repo-scanner/` | 기존 코드베이스 구조 분석 |

## Org Chart

```
openclaw (CEO / 총괄)
├── openclaw-secretary
├── second-brain-operator
├── finance-researcher
├── finance-analyst
├── dev-research
├── skill-creator
└── coder/
    ├── architect       — 시스템 설계 (복잡한 프로젝트)
    ├── planner         — 구현 계획 + ACP 직접 위임
    ├── reviewer        — diff 리뷰/검증 (coder-developer 스킬)
    ├── [ACP]           — Claude Code 런타임
    ├── repo-scanner    — 기존 코드 분석 (확장형)
    ├── spec-writer     — 기능 명세 전담 (확장형)
    └── designer        — UI/UX 구조 설계 (확장형, UI 프로젝트만)
```

## 코딩 팀 워크플로우

```
[architect →] planner → ACP (런타임) ── reviewer (독립)
```

- **최소형:** architect(선택) + planner + ACP + reviewer
- **확장형:** + repo-scanner → + spec-writer → + designer
- **planner → ACP 직접 위임** (depth 2, runTimeoutSeconds: 0) — openclaw 승인 후
- **openclaw 역할:** 승인 게이트 + reviewer spawn (중간 릴레이 최소화)
- **reviewer:** read-only, 코드 수정 금지
- 설계 문서: `{vault_path}/Designs/{project}/`
- 프로젝트 코드: `~/projects/{project}/`

> 상세 워크플로우: `skills/coder-workflow.md`

## 자산운용팀 (Investing)

| 스킬 | 경로 | 역할 |
|---|---|---|
| invest-portfolio-manager | `skills/invest-portfolio-manager/` | 오케스트레이터 + Investing/ 유일한 writer + Trade Historian |
| invest-analyst | `skills/invest-analyst/` | Macro/Sentiment/Instrument 분석 (read-only) |
| invest-operator | `skills/invest-operator/` | 목표 비중안 + 실행 가이드 (read-only) |
| invest-da | `skills/invest-da/` | 독립적 반대 논리 (read-only) |
| invest-risk-manager | `skills/invest-risk-manager/` | 규칙 기반 PASS/FAIL (read-only) |

### 운용 구조

```
openclaw (invest-portfolio-manager 스킬 로드)
├── invest-analyst (subagent #1) — Macro/Sentiment/Instrument
├── invest-operator (subagent #2) — 비중안 (analyst 결과 입력)
├── invest-da (subagent #3) — 반대 논리 (operator rationale 미전달)
├── invest-risk-manager (subagent #4) — PASS/FAIL (순수 룰 기반)
└── [직접] Trade Historian — 기록 관리
```

### 원칙
- `invest-portfolio-manager` = 오케스트레이터 + 유일한 writer. 자체 투자 판단 삽입 금지
- 4개 subagent = 전부 read-only, 고정 출력 형식
- DA에 operator rationale 미전달 (편향 전염 방지)
- Risk Manager FAIL → CIO 오버라이드 없으면 실행 불가
- CIO({user}) = 최종 승인 + 주문 집행
