---
name: dev-research
description: "기술 리서치 전용 파이프라인 — AI/ML 논문, 기술 트렌드, 라이브러리, 아키텍처 조사. 8-stage 구조 + GATE({user} 승인) 포함. 트리거: 기술 논문/트렌드/아키텍처 리서치 요청 시. 비사용: 투자/시장/경쟁사 분석(→ finance-researcher/finance-analyst 사용)."
---

# dev-research

## 역할

기술 도메인 리서치를 체계적으로 수행한다. AI/ML 논문, 기술 트렌드, 오픈소스 라이브러리, 아키텍처 패턴 등 **개발·기술 관련 리서치 전용**.

> ⚠️ 이 스킬의 적용 범위
> - ✅ AI/ML 논문, 기술 트렌드, 아키텍처 패턴, 오픈소스 라이브러리
> - ✅ Laplace / OSSCA 등 기술 프로젝트 리서치 지원
> - ❌ 투자/시장/경쟁사 분석 → `finance-researcher` 사용
> - ❌ 종목/섹터 분석 → `finance-analyst` 사용

---

## 파이프라인 구조 (8 Stage)

```
Phase A — Scoping
  Stage 1: TOPIC_SCOPE     토픽 정의 + 범위/목적 명확화
  Stage 2: SEARCH_PLAN     키워드 + 소스 전략 수립

Phase B — Collection
  Stage 3: COLLECT         arXiv API + 웹 수집
  Stage 4: SCREEN          품질 필터링 [GATE → {user} 승인]

Phase C — Synthesis
  Stage 5: EXTRACT         핵심 지식 추출 + 구조화
  Stage 6: SYNTHESIZE      합성 + 인사이트/가설 생성
  Stage 7: REVIEW          {user} 최종 리뷰 [GATE]

Phase D — Archive
  Stage 8: ARCHIVE         Obsidian 저장 (+ Notion General 선택)
```

### GATE 동작

GATE 단계에서는 작업을 **중단하고 {user}에게 승인 요청**을 보낸다.
- Stage 4 GATE: 수집된 논문/자료 목록 + 각 항목 품질 평가 요약 전달
- Stage 7 GATE: 최종 리서치 결과 전체 요약 전달
- {user}가 승인하면 다음 단계 진행 / 거부하면 이전 단계로 롤백

### 체크포인트

각 stage 완료 시 `{run_dir}/checkpoint.json`에 기록:
```json
{
  "stage": 4,
  "stage_name": "SCREEN",
  "status": "done",
  "timestamp": "2026-03-20T06:00:00Z"
}
```

재시작 시 `--from-stage N` 옵션으로 중간부터 재개.

---

## Stage 상세

### Stage 1: TOPIC_SCOPE

**목표:** 리서치 범위를 명확하게 정의한다.

산출물:
```yaml
topic: "GraphRAG for personal knowledge management"
purpose: "Laplace 설계를 위한 지식 그래프 기반 RAG 아키텍처 조사"
scope_in:
  - Knowledge Graph 기반 RAG 아키텍처
  - Neo4j + LLM 연동 패턴
  - Personal Knowledge Management (PKM) 적용 사례
scope_out:
  - Enterprise-scale GraphRAG (Microsoft 제품군)
  - 실시간 스트리밍 KB
time_range: "2023~2025"
depth: "survey"  # survey | deep-dive | quick-scan
```

### Stage 2: SEARCH_PLAN

**목표:** 수집 전략을 수립한다.

산출물:
```yaml
keywords:
  primary: ["GraphRAG", "knowledge graph RAG", "graph-based retrieval"]
  secondary: ["personal knowledge management", "PKM AI", "note-taking AI"]
sources:
  - arxiv: true
  - semantic_scholar: true
  - web: ["github.com", "blog posts", "official docs"]
filters:
  min_year: 2023
  min_citations: 0  # 최신 논문은 인용수 낮을 수 있음
  languages: ["en", "ko"]
target_count: 15  # 수집 목표 문헌 수
```

### Stage 3: COLLECT

**목표:** 실제 자료를 수집한다.

수집 방법:
- **arXiv API**: `curl "https://export.arxiv.org/api/query?search_query=...&max_results=20"`
- **Semantic Scholar API**: `curl "https://api.semanticscholar.org/graph/v1/paper/search?query=..."`
- **웹**: `browser` 도구로 GitHub, 블로그, 공식 문서 수집
- **Obsidian vault**: 기존 관련 노트 참조 (`{obsidian_vault}/`)

수집 형식:
```yaml
- id: "arxiv:2404.xxxxx"
  title: "..."
  authors: [...]
  year: 2024
  abstract: "..."
  url: "..."
  relevance_score: null  # Stage 4에서 채움
  quality_score: null
```

### Stage 4: SCREEN [GATE]

**목표:** 수집된 자료를 품질 필터링하고 {user} 승인을 받는다.

평가 기준:
- **관련성** (1~5): 토픽 범위에 얼마나 맞는가
- **품질** (1~5): 방법론/출처 신뢰도
- **신선도**: 시간 범위 내인가
- **중복** 제거

GATE 메시지 형식:
```
📋 dev-research Stage 4: SCREEN 완료 — {user} 승인 요청

토픽: {topic}
수집: {총 수집} → 필터 후: {통과 수}

통과 목록:
1. [논문/자료 제목] (관련성: 4/5, 품질: 3/5) — 한줄 요약
2. ...

제외 목록 (사유):
- [제목]: 관련성 낮음 (1/5)
- ...

👉 승인하면 Stage 5(EXTRACT) 진행 / 거부 메시지와 함께 수집 재시도
```

### Stage 5: EXTRACT

**목표:** 각 자료에서 핵심 지식을 추출하고 구조화한다.

항목별 추출:
```markdown
## {논문/자료 제목}

- **핵심 기여**: 
- **방법론**: 
- **주요 결과**: 
- **한계**: 
- **우리 맥락 관련성**: (Laplace / OSSCA 등에 어떻게 적용 가능한가)
- **인용 가능 포인트**: 
```

### Stage 6: SYNTHESIZE

**목표:** 추출된 지식을 합성하여 인사이트와 가설을 생성한다.

산출물 구조:
```markdown
## 합성 요약

### 트렌드 및 패턴
(반복적으로 등장하는 개념, 방법론의 흐름)

### 주요 인사이트
1. {인사이트} — 근거: {논문 ID들}
2. ...

### 가설 / 설계 방향
(우리 프로젝트에 적용 시 가설 또는 설계 방향 제안)

### 미해결 질문 / 추가 조사 필요
- ...

### 한계 / 주의사항
- ...
```

### Stage 7: REVIEW [GATE]

**목표:** {user} 최종 리뷰를 받는다.

GATE 메시지: Stage 6 합성 결과 전체 + 핵심 인사이트 요약 전달.

{user} 피드백 반영:
- 수정 요청 → Stage 5 또는 6으로 롤백
- 추가 수집 요청 → Stage 3으로 롤백
- 승인 → Stage 8 진행

### Stage 8: ARCHIVE

**목표:** 리서치 결과를 Obsidian에 저장한다. Notion General은 {user} 지시 시에만.

저장 경로:
- 메인 리포트: `{obsidian_vault}/Resources/Research/{topic-slug}.md`
- 체크포인트: `{vault_path}/Research/{run_id}/checkpoint.json`
- 원본 수집 데이터: `{vault_path}/Research/{run_id}/collected.yaml`

리포트 형식:
```markdown
---
topic: {topic}
run_id: {run_id}
date: YYYY-MM-DD
status: final
tags: [dev-research, {domain-tags}]
---

# {topic} 리서치 리포트

## 요약 (3줄 이내)

## 스코프
- 목적: 
- 범위: 
- 기간: 

## 문헌 목록
(통과한 자료 목록)

## 핵심 추출

## 합성 + 인사이트

## 가설 / 설계 방향

## 미해결 질문

## 한계

## 출처
```

---

## 핵심 원칙

1. **출처 필수** — 모든 주장에 출처(논문 ID, URL 등). 추측은 "추정" 명시
2. **사실과 판단 분리** — 팩트/의견 구분
3. **GATE 준수** — Stage 4, 7에서 반드시 {user} 승인 대기. 임의 진행 금지
4. **체크포인트 기록** — 각 stage 완료 시 기록
5. **기술 맥락 연결** — 단순 요약이 아닌 "우리 프로젝트에 어떻게 쓰나" 관점 유지
6. **한계 인정** — 모르는 것은 모른다고 씀

---

## spawn 예시

```
sessions_spawn:
  task: |
    너는 dev-research 파이프라인 실행자다.
    ~/.openclaw/workspace/skills/dev-research/SKILL.md를 읽고 따라라.

    리서치 토픽: {topic}
    목적: {why}
    프로젝트 맥락: {Laplace / OSSCA / etc.}
    시작 stage: 1 (또는 --from-stage N으로 재시작)

    GATE 도달 시 openclaw에게 승인 요청 메시지를 보내고 대기하라.
    체크포인트는 {vault_path}/Research/{run_id}/ 에 저장하라.
  mode: run
  runtime: subagent
  model: sonnet
  runTimeoutSeconds: 600
```

---

## 관련 스킬

- `finance-researcher` — 금융/시장 리서치 (거시경제, 섹터, 이슈)
- `finance-analyst` — 투자 분석 (종목/섹터 펀더멘털, 밸류에이션)
- `knowledge-ops` — 리서치 결과 발행 판단
- `obsidian-governance` — vault 저장 경로/형식 규칙
