---
name: finance-researcher
description: "금융/시장 리서치 전용 파이프라인 — 시장 동향, 섹터 분석, 거시경제, 금융 이슈 수집·정리. 6-stage 구조 + GATE({user} 승인) 포함. 트리거: 시장/섹터/거시경제/금융 이슈 리서치 요청 시. 비사용: 기술 논문/아키텍처(→ dev-research), 종목 밸류에이션(→ finance-analyst)."
---

# finance-researcher

## 역할

금융·시장 도메인의 정보를 체계적으로 수집하고 정리한다. **인사이트 도출까지만** — 종목 밸류에이션, 투자 의견은 `finance-analyst` 영역.

> ⚠️ 적용 범위
> - ✅ 거시경제 동향 (금리, 환율, 인플레이션, 경기 사이클)
> - ✅ 섹터 트렌드, 산업 구조 변화
> - ✅ 시장 이슈 수집 (규제, 지정학, 무역)
> - ✅ 특정 종목 배경 리서치 (산업 포지셔닝, 뉴스) → 심층 밸류에이션은 finance-analyst
> - ❌ 종목 밸류에이션, 투자 의견 → `finance-analyst`
> - ❌ 기술 논문/아키텍처 → `dev-research`

---

## 파이프라인 구조 (6 Stage)

```
Phase A — Scoping
  Stage 1: SCOPE        리서치 범위 + 목적 정의

Phase B — Collection
  Stage 2: COLLECT      Intel Pipeline + 웹 + 공개 데이터 수집
  Stage 3: SCREEN       품질 필터링 [GATE → {user} 승인]

Phase C — Analysis
  Stage 4: EXTRACT      핵심 데이터 추출 + 구조화
  Stage 5: SYNTHESIZE   인사이트 + 시사점 도출

Phase D — Archive
  Stage 6: ARCHIVE      Obsidian 저장
```

### GATE 동작

- **Stage 3 GATE**: 수집된 자료 목록 + 품질 평가 요약 → {user} 승인 대기
  - 승인 → Stage 4 진행
  - 거부 → Stage 2 롤백 (수집 재시도)

### 체크포인트

각 stage 완료 시 `{run_dir}/checkpoint.json` 기록:
```json
{
  "stage": 3,
  "stage_name": "SCREEN",
  "status": "done",
  "timestamp": "2026-03-20T06:00:00Z"
}
```

재시작: `--from-stage N`

---

## Stage 상세

### Stage 1: SCOPE

산출물:
```yaml
topic: "미국 금리 인하 사이클과 국내 증시 영향"
purpose: "포트폴리오 리밸런싱 판단을 위한 거시 환경 파악"
scope_in:
  - Fed 금리 결정 및 전망
  - 한미 금리 스프레드 추이
  - 코스피 외국인 수급 흐름
scope_out:
  - 개별 종목 분석
  - 채권 밸류에이션
time_range: "최근 3개월"
depth: "survey"  # survey | deep-dive | quick-scan
```

### Stage 2: COLLECT

수집 소스 (우선순위순):

| 소스 | 접근 방법 | 용도 |
|---|---|---|
| Intel Pipeline 보고서 | `{obsidian_vault}/Resources/Daily digests/Finance/` | 시장 브리핑 |
| 웹 (뉴스/공시) | `browser` 도구 | 최신 이슈 |
| Yahoo Finance (비공식) | `curl` | 주가/지표 데이터 |
| FRED API | `curl https://fred.stlouisfed.org/graph/fredgraph.csv?id=...` | 거시 데이터 |
| KRX/DART | `curl` | 국내 공시 |
| Obsidian vault | `{obsidian_vault}/` | 기존 리서치 |

수집 형식:
```yaml
- id: "intel-2026-03-20-us"
  source: "Intel Pipeline US"
  date: "2026-03-20"
  type: "market_briefing"  # market_briefing | news | data | report
  summary: "..."
  relevance_score: null  # Stage 3에서 채움
```

### Stage 3: SCREEN [GATE]

평가 기준:
- **관련성** (1~5): 토픽 범위에 얼마나 맞는가
- **신선도**: 시간 범위 내 자료인가
- **신뢰도**: 출처 신뢰도 (공식 발표 > 뉴스 > 블로그)
- **중복** 제거

GATE 메시지 형식:
```
📊 finance-researcher Stage 3: SCREEN 완료 — {user} 승인 요청

토픽: {topic}
수집: {총 수집} → 필터 후: {통과 수}

통과 목록:
1. [자료명] (관련성: 4/5, 신뢰도: 공식) — 한줄 요약
2. ...

제외 목록 (사유):
- [자료명]: 시간 범위 외
- ...

👉 승인하면 Stage 4(EXTRACT) 진행 / 거부 시 수집 재시도
```

### Stage 4: EXTRACT

항목별 추출:
```markdown
## {자료명} ({날짜})

- **핵심 데이터/주장**: 
- **수치**: (가능하면 표 형식)
- **출처**: 
- **우리 맥락 관련성**: 
```

수치 데이터는 반드시 표로:
```markdown
| 지표 | 값 | 기준일 | 출처 |
|---|---|---|---|
| Fed Funds Rate | 4.50% | 2026-03-19 | FRED |
| 코스피 | 2,580 | 2026-03-20 | KRX |
```

### Stage 5: SYNTHESIZE

산출물:
```markdown
## 종합 요약

### 핵심 트렌드
(반복적으로 등장하는 신호, 방향성)

### 주요 인사이트
1. {인사이트} — 근거: {자료 ID들}
2. ...

### 시사점 ({user} 포트폴리오 관점)
(구체적 행동 가능한 수준의 시사점)

### 불확실성 / 주의사항
- 확인되지 않은 정보
- 상충하는 신호

### 추가 조사 권고
- (심층 분석 필요 시 finance-analyst 연계 제안)
```

### Stage 6: ARCHIVE

저장 경로:
- 메인 리포트: `{obsidian_vault}/Resources/Research/Finance/{topic-slug}.md`
- 체크포인트: `{vault_path}/Research/finance/{run_id}/checkpoint.json`
- 원본 수집 데이터: `{vault_path}/Research/finance/{run_id}/collected.yaml`

리포트 프론트매터:
```yaml
---
topic: {topic}
run_id: {run_id}
date: YYYY-MM-DD
status: final
type: finance-research
tags: [finance-research, {domain-tags}]
---
```

---

## 핵심 원칙

1. **수치 근거 필수** — "상승세다"가 아닌 "+2.3% (출처: KRX)"
2. **사실/판단 분리** — 팩트와 해석 명확히 구분
3. **GATE 준수** — Stage 3에서 반드시 {user} 승인 대기
4. **Intel Pipeline 우선** — 이미 수집된 데이터 먼저 활용
5. **시사점은 구체적으로** — "주의 필요" 아닌 "XXX 포지션 재검토 고려"
6. **한계 명시** — 실시간 데이터 없음, 유료 리포트 미접근 등

---

## spawn 예시

```
sessions_spawn:
  task: |
    너는 finance-researcher다.
    ~/.openclaw/workspace/skills/finance-researcher/SKILL.md를 읽고 따라라.

    리서치 토픽: {topic}
    목적: {why}
    참고할 Intel Pipeline 보고서: {경로 또는 날짜 범위}
    시작 stage: 1

    GATE 도달 시 openclaw에게 승인 요청 메시지를 보내고 대기하라.
    체크포인트는 {vault_path}/Research/finance/{run_id}/ 에 저장하라.
  mode: run
  runtime: subagent
  model: sonnet
  runTimeoutSeconds: 600
```

---

## 관련 스킬

- `finance-analyst` — 종목 밸류에이션, 투자 의견 (finance-researcher 이후 심층 분석)
- `dev-research` — 기술 논문/아키텍처 리서치
- `knowledge-ops` — 리서치 결과 발행 판단
- `obsidian-governance` — vault 저장 경로/형식 규칙
