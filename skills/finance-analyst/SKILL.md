---
name: finance-analyst
description: "투자 분석 전용 파이프라인 — 펀더멘털 기반 종목/섹터 분석, 밸류에이션, Bull/Bear 시나리오. 7-stage 구조 + GATE({user} 승인) 포함. 트리거: 종목/섹터 밸류에이션, 투자 의견, 심층 분석 요청 시. 비사용: 거시/시장 트렌드 수집(→ finance-researcher)."
---

# finance-analyst

## 역할

펀더멘털 기반 바이사이드 리서치를 수행한다. 종목/섹터 심층 분석, 밸류에이션, 투자 논리 구축.

> ⚠️ 적용 범위
> - ✅ 종목 펀더멘털 분석 (사업 이해, 재무, 밸류에이션)
> - ✅ 섹터 구조 분석 + 선호 종목 도출
> - ✅ Bull/Bear 시나리오, 리스크 분석
> - ✅ 핵심 모니터링 지표 설정
> - ❌ 거시/시장 트렌드 수집 → `finance-researcher` (선행 작업으로 활용)
> - ❌ 기술 리서치 → `dev-research`

> ⚠️ 면책 고지: 모든 산출물은 분석 목적이며 투자 조언이 아닙니다.

---

## 파이프라인 구조 (7 Stage)

```
Phase A — Scoping
  Stage 1: SCOPE         분석 대상 + 목적 + 맥락 정의

Phase B — Data
  Stage 2: DATA_COLLECT  재무/주가/공시 데이터 수집
  Stage 3: FUNDAMENTAL   사업 이해 + 재무 분석

Phase C — Valuation
  Stage 4: VALUATION     밸류에이션 산정 [GATE → {user} 승인]

Phase D — Scenario
  Stage 5: SCENARIO      Bull/Bear 시나리오 + 리스크 분석

Phase E — Finalization
  Stage 6: REVIEW        {user} 최종 리뷰 [GATE]
  Stage 7: ARCHIVE       Obsidian 저장
```

### GATE 동작

- **Stage 4 GATE**: 밸류에이션 산정 결과 + 핵심 가정 → {user} 승인 대기
  - 승인 → Stage 5 진행
  - 거부(가정 수정 요청) → Stage 3 또는 4 롤백
- **Stage 6 GATE**: 전체 분석 요약 → {user} 최종 리뷰
  - 승인 → Stage 7 저장
  - 수정 요청 → 해당 stage 롤백

### 체크포인트

각 stage 완료 시 `{run_dir}/checkpoint.json` 기록.
재시작: `--from-stage N`

---

## Stage 상세

### Stage 1: SCOPE

산출물:
```yaml
target: "삼성전자 (005930)"  # 또는 섹터명
market: "KRX"  # KRX | NYSE | NASDAQ
analysis_type: "company"  # company | sector
purpose: "반도체 사이클 회복 구간에서 매수 타이밍 판단"
context:
  - "finance-researcher 보고서: {경로 또는 요약}"
  - "Intel Pipeline 최근 관련 내용"
time_horizon: "6~12개월"
```

### Stage 2: DATA_COLLECT

수집 데이터:

| 항목 | 소스 | 접근 방법 |
|---|---|---|
| 주가/시가총액 | Yahoo Finance (비공식) | `curl` |
| 재무제표 (KRX) | DART | `curl https://opendart.fss.or.kr/api/...` |
| 재무제표 (US) | Financial Modeling Prep / Yahoo | `curl` |
| 공시/IR | DART / 기업 IR 페이지 | `browser` |
| 증권사 컨센서스 | 네이버/인포스탁 (가능 범위) | `browser` |
| Intel Pipeline | `{obsidian_vault}/Resources/Daily digests/Finance/` | `exec` |
| 기존 분석 노트 | `{obsidian_vault}/` | `exec` |

수집 불가 데이터는 "데이터 없음 (출처 제한)" 명시.

### Stage 3: FUNDAMENTAL

**사업 이해:**
```markdown
## 사업 개요
- 핵심 사업: 
- 수익 구조 (세그먼트별 비중):
- 경쟁 우위 (Moat):
- 주요 고객/시장:
```

**재무 분석:**
```markdown
## 재무 분석
| 지표 | FY-2 | FY-1 | FY0(TTM/E) | YoY |
|---|---|---|---|---|
| 매출 | | | | |
| 영업이익 | | | | |
| 순이익 | | | | |
| 영업이익률 | | | | |
| ROE | | | | |
| 부채비율 | | | | |
| FCF | | | | |

### 재무 품질 체크
- 이익의 질: (현금흐름 vs 순이익 괴리 여부)
- 부채 구조: (단기/장기, 이자보상배율)
- 배당/자사주: 
```

### Stage 4: VALUATION [GATE]

**밸류에이션 방법 (적용 가능한 방법 선택):**

```markdown
## 밸류에이션

### Relative Valuation
| 지표 | 현재 | 5년 평균 | 피어 평균 | 해석 |
|---|---|---|---|---|
| PER | | | | |
| PBR | | | | |
| EV/EBITDA | | | | |
| PSR | | | | |

### Absolute Valuation (DCF, 가능 시)
| 가정 | 값 |
|---|---|
| 성장률 (5년) | |
| Terminal growth rate | |
| WACC | |
| 산출 내재가치 | |

### 종합 적정 가치 범위
- 보수적: ₩/$ {A}
- 중립: ₩/$ {B}
- 낙관: ₩/$ {C}
- 현재가 대비 업사이드/다운사이드: {%}
```

GATE 메시지:
```
📈 finance-analyst Stage 4: VALUATION 완료 — {user} 승인 요청

대상: {ticker/sector}
현재가: ₩/$
산출 적정가치 범위: ₩/$ A ~ C (중립: B)
핵심 가정: 성장률 X%, WACC Y%

👉 가정 수정 필요하면 거부 + 수정 내용 / 승인하면 시나리오 분석 진행
```

### Stage 5: SCENARIO

```markdown
## Bull Case
- 전제 조건:
- 기대 수익률: +X%
- 핵심 촉매:

## Base Case
- 전제 조건:
- 기대 수익률: +X%

## Bear Case
- 전제 조건:
- 기대 수익률: -X%
- 핵심 리스크:

## 리스크 분석
| 리스크 | 발생 가능성 | 영향도 | 모니터링 방법 |
|---|---|---|---|
| 업황 악화 | 중 | 상 | 분기 실적 |
| 규제 변화 | 하 | 중 | 공시 모니터링 |

## 핵심 모니터링 지표
(보유 중 주기적으로 확인할 지표 3~5개)
1. {지표}: {기준값} / {체크 주기}
```

### Stage 6: REVIEW [GATE]

전체 분석 요약 + 투자 논지 1~2줄 → {user} 최종 리뷰.

GATE 메시지:
```
📋 finance-analyst 분석 완료 — {user} 최종 리뷰 요청

대상: {ticker/sector}
핵심 논지: (1~2줄)
적정가치: ₩/$ B (현재가 대비 +X%)
투자 의견: Overweight / Neutral / Underweight

주요 Bull: {한줄}
주요 Bear: {한줄}

👉 승인하면 Obsidian 저장 / 수정 요청 시 해당 단계 롤백
```

### Stage 7: ARCHIVE

저장 경로:
- 종목 분석: `{obsidian_vault}/Resources/Research/Finance/equities/{ticker}-analysis.md`
- 섹터 분석: `{obsidian_vault}/Resources/Research/Finance/sectors/{sector}-analysis.md`
- 체크포인트: `{vault_path}/Research/finance/{run_id}/checkpoint.json`

리포트 프론트매터:
```yaml
---
ticker: {종목코드}
company: {회사명}
market: KRX/NYSE/NASDAQ
run_id: {run_id}
date: YYYY-MM-DD
analyst: openclaw
status: final
type: finance-analysis
tags: [finance-analyst, {sector-tags}]
---
```

---

## 핵심 원칙

1. **수치 없으면 주장 없음** — "좋아 보인다" 금지. 반드시 수치 근거
2. **Bull/Bear 양면 필수** — 한쪽만 보는 분석은 분석이 아님
3. **가정 투명성** — 밸류에이션 가정은 모두 명시
4. **리스크 우선** — 업사이드보다 다운사이드를 먼저
5. **GATE 준수** — Stage 4(밸류에이션), Stage 6(최종)에서 반드시 승인 대기
6. **데이터 한계 명시** — 접근 불가 데이터는 "없음" 명시, 추정 시 "추정" 표기
7. **면책 고지** — 모든 산출물 하단에 "분석 목적이며 투자 조언이 아님" 명시

---

## spawn 예시

```
sessions_spawn:
  task: |
    너는 finance-analyst다.
    ~/.openclaw/workspace/skills/finance-analyst/SKILL.md를 읽고 따라라.

    분석 대상: {ticker 또는 sector}
    시장: {KRX / NYSE / NASDAQ}
    목적: {왜 이 분석이 필요한지}
    참고 자료:
      - Intel Pipeline: {경로 또는 요약}
      - finance-researcher 보고서: {경로} (있을 경우)
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

- `finance-researcher` — 거시/시장 트렌드 수집 (종목 분석 선행 작업)
- `dev-research` — 기술 리서치 (종목의 기술적 배경 조사 필요 시)
- `knowledge-ops` — 분석 결과 발행 판단
- `obsidian-governance` — vault 저장 경로/형식 규칙
