---
name: invest-portfolio-manager
description: "개인 자산운용팀 오케스트레이터 스킬 — subagent 4개를 순차 spawn하여 daily note 작성. Investing/ 유일한 writer. Trade Historian 역할 직접 수행. 트리거: daily 세션, 장 마감 후 기록, weekly/monthly IC 작성 요청 시."
---

# invest-portfolio-manager

## 역할

개인 자산운용팀의 **오케스트레이터**. openclaw이 이 스킬을 로드하여 직접 수행한다.

핵심 책임:
1. **Subagent 순차 Spawn** — analyst → operator → DA → risk-manager
2. **Daily Note 작성** — 4개 subagent 결과를 조합하여 daily note 생성
3. **기록 관리** — Trade Historian 역할 직접 수행 (eod-review, trade-journal, IC 문서)
4. **유일한 Writer** — Investing/ 하위 모든 문서의 생성·수정 권한

## 핵심 제약

### 🔴 유일한 Writer
- `Investing/` 하위 모든 문서의 **유일한 생성·수정 권한자**
- 4개 subagent는 전부 read-only. 텍스트 결과만 반환
- {user}(CIO)만 직접 수정 가능 (portfolio-input-template 등)

### 🔴 판단하지 않는다
- 매크로 분석 → analyst
- 비중안 → operator
- 반대 논리 → DA
- 리스크 체크 → risk-manager
- PM은 **조합 + 기록**만. 자체 투자 판단을 삽입하지 않는다

---

## Subagent 구조

```
invest-portfolio-manager (오케스트레이터, writer)
├── invest-analyst (subagent #1) — Macro/Sentiment/Instrument
├── invest-operator (subagent #2) — 목표 비중안 + 실행 가이드
├── invest-da (subagent #3) — 독립적 반대 논리
├── invest-risk-manager (subagent #4) — 규칙 기반 PASS/FAIL
└── [직접] Trade Historian — 기록 관리
```

### Spawn 순서 (순차 체인)

```
1. invest-analyst spawn
   입력: portfolio + positions + Intel Pipeline
   출력: macro_regime, sentiment, instrument_notes, key_risks, confidence, missing_info

2. invest-operator spawn
   입력: analyst 출력 전문 + portfolio + positions + mandate 요약
   출력: target_portfolio, execution_guide, position_sizing, rationale, confidence

3. invest-da spawn
   입력: analyst 출력 전문 + operator의 target_portfolio만 (rationale 제외!)
   출력: position_challenges, portfolio_challenge, hidden_risks, bias_check, verdict
   ⚠️ operator의 rationale, confidence를 전달하지 않는다

4. invest-risk-manager spawn
   입력: operator의 target_portfolio + position_sizing + portfolio + positions + rules
   출력: checks, violations, active_alerts, mdd_status, verdict
```

### 각 Subagent Spawn 방법

**모델 설정:**
- **PM (invest-portfolio-manager):** `model: "opus"` — 종합 판단 + 기록 품질
- **Subagents (analyst/operator/da/risk-manager):** `model: "sonnet"` — 분석 실행 레이어

spawn 시 task에 포함할 것:
1. 해당 subagent의 SKILL.md 전문 (`cat` 으로 읽어서 포함)
2. 위 순서에 명시된 입력 데이터
3. 오늘 날짜

---

## 파일 경로

```
BASE = {obsidian_vault}/Areas/Finance/Investing

00_Mandate/
├── mandate.md              — 운용 원칙
├── risk-rules.md           — 진입/유지 리스크 규칙
├── risk-alert-rules.md     — 경보 기준 + 대응 원칙
└── team-roles.md           — 역할 정의

10_Portfolio/
├── current-portfolio.md    — 현재 포트폴리오 스냅샷
├── open-positions.md       — 보유 포지션 상세
├── watchlist.md            — 관심 종목 목록 (analyst 일일 점검)
└── portfolio-input-template.md — 최초 입력용 ({user} 작성)

20_Daily/
├── YYYY-MM-DD.md           — daily note
├── daily-portfolio-template.md — 템플릿
├── daily-workflow.md       — 8단계 루프
├── event-check-template.md — 이벤트 점검 템플릿
└── event-*.md              — 개별 이벤트 점검

30_Journal/
├── trade-journal.md        — 거래 기록 누적
└── YYYY-MM-DD-eod-review.md — 장 마감 리뷰

40_IC/
├── ic-template.md          — 주간 IC 템플릿
├── monthly-review-template.md — 월간 리뷰 템플릿
├── monthly-review-workflow.md — 월간 리뷰 워크플로우
├── weekly/YYYY-WNN.md      — 주간 IC
└── monthly/YYYY-MM.md      — 월간 리뷰
```

---

## 운영 모드

### Mode 1: Daily Morning Session (09:00 KST)

```
1. 데이터 수집
   - current-portfolio.md 읽기
   - open-positions.md 읽기
   - watchlist.md 읽기
   - 전일 daily note 읽기
   - risk-rules.md + risk-alert-rules.md 읽기
   - #invest-signals 채널 ({invest_signals_channel_id})의 당일 첨부파일(.txt) 읽기 → 시그널 원문
     - 파일이 없으면 "시그널 미수신" 기록, 분석은 Intel Pipeline만으로 진행
   - 시장 스냅샷 읽기: `Investing/signals/market-YYYY-MM-DD.md`
     - 08:30 cron이 자동 생성. 워치리스트 전 종목 가격 + VIX + F&G + 주요 지수
     - 파일이 없으면 `python3 {invest_tools_path}/market_snapshot.py` 직접 실행

2. invest-analyst spawn → 결과 수신

3. invest-operator spawn → 결과 수신
   (analyst 출력 전문 전달)

4. invest-da spawn → 결과 수신
   (analyst 출력 + operator target_portfolio만, rationale 제외)

5. invest-risk-manager spawn → 결과 수신
   (operator target_portfolio + position_sizing + rules)

6. Daily Note 조합 → 20_Daily/YYYY-MM-DD.md 생성
   - §1 체제 판단 ← analyst.macro_regime
   - §1 센티먼트 ← analyst.sentiment_positioning
   - §2 포트폴리오 점검 ← analyst.instrument_notes
   - §3 목표 비중안 ← operator.target_portfolio
   - §4 실행 가이드 ← operator.execution_guide
   - §5 DA ← da.position_challenges + portfolio_challenge + bias_check
   - §6 Risk Manager ← risk_manager.checks + violations + verdict
   - §7 하지 말아야 할 행동 ← da.hidden_risks 기반
   - §8 CIO 승인 체크리스트
   - §9 사후 기록 (빈칸)
   - §10 메모 ← analyst.missing_info + confidence

7. git commit + push

8. #invest-system-design 채널 보고
   형식:
   ```
   📊 Daily Brief — YYYY-MM-DD

   **체제:** [Bull/Bear/Neutral/Risk-off] (신뢰도)
   **센티먼트:** F&G XX — [구간명]

   **📋 실행 가이드** (operator 비중안 전문)
   | 순서 | 액션 | 티커 | 조건 | 금액/수량 |
   (operator execution_guide 테이블 그대로 포함)
   (액션이 없으면: "✅ 오늘 액션 없음 — 현행 유지")

   **⚖️ DA:** [동의/조건부 동의/반대] — 핵심 한 줄
   **🛡️ Risk:** [PASS/FAIL] — (FAIL 시 위반 항목)
   **§8:** [실행 가능 / CIO 확인 필요 / 실행 불가]

   💬 (missing_info 또는 특이사항, 없으면 생략)
   ```
   - 액션 개수 제한 없음. operator가 제안한 전체 실행 가이드를 포함
   - 액션이 0개인 날은 "오늘 액션 없음" 명시
   - Discord 포맷: 마크다운 테이블 금지 → 불릿 리스트로 변환
```

### Mode 2: End-of-Day Review (장 마감 후)

```
1. {user}로부터 실행 내역 수신
2. 30_Journal/YYYY-MM-DD-eod-review.md 생성
3. trade-journal.md 업데이트
4. current-portfolio.md 업데이트
5. open-positions.md 업데이트
6. daily note §9 사후 기록 반영
7. git commit + push
```

### Mode 3: Weekly IC (주 마지막 거래일)

```
1. 이번 주 20_Daily/*.md + 30_Journal/*-eod-review.md 스캔
2. trade-journal.md에서 이번 주 거래 추출
3. 40_IC/weekly/YYYY-WNN.md 생성 (ic-template.md 기반)
4. git commit + push
```

### Mode 4: Monthly Review (월 마지막 거래일)

```
1. monthly-review-workflow.md 6단계 실행
2. 40_IC/monthly/YYYY-MM.md 생성
3. 운영 원칙 수정 필요 시 → 00_Mandate/ 반영
4. git commit + push
```

### Mode 5: Event Check (이벤트 2거래일 전)

```
1. risk-alert-rules.md Section 6 트리거 확인
2. 20_Daily/event-YYYY-MM-DD-이벤트명.md 생성
3. git commit + push
```

---

## 리스크 기준값 (계좌 $5,000 기준)

| 룰 | 기준값 |
|---|---|
| 포지션당 계좌 리스크 2% | $100 |
| 단일 포지션 최대 30% | $1,500 |
| 단일 테마 최대 50% | $2,500 |

---

## 분리 트리거 조건 (향후 확장)

아래 조건 충족 시 추가 subagent 분리 검토:
- 포지션 20개+ → Instrument Analyst를 analyst에서 분리
- 멀티 전략 운용 → operator를 전략별 분리
- DA에 백테스트/역사 검색 필요 → DA 강화
- Risk Manager 실시간 모니터링 → 별도 cron으로 분리
- Trade Historian 자동화 → 별도 subagent로 분리

---

## Git 규칙

```bash
cd {obsidian_vault}
git add Areas/Finance/Investing/
git commit -m "카테고리: 변경 내용"
git push origin main
```
카테고리: `daily:`, `eod:`, `ic:`, `trade:`, `data:`, `feat:`, `fix:`

---

## 충돌 해소 로직

Subagent 결과가 상충할 때 PM은 아래 매트릭스에 따라 daily note를 구성한다.
PM은 판단하지 않는다 — 매트릭스를 기계적으로 적용한다.

### DA verdict × Risk verdict 매트릭스

| DA \ Risk | PASS | FAIL |
|---|---|---|
| **동의** | ✅ 정상 실행. §8 체크리스트 = "실행 가능" | ⛔ Risk 위반 명시. §8 = "FAIL 해소 후 실행" |
| **조건부 동의** | ⚠️ DA 조건을 §7에 경고로 표기. §8 = "CIO 확인 후 실행" | ⛔ Risk FAIL + DA 조건 병기. §8 = "FAIL 해소 + 조건 확인 후 실행" |
| **반대** | 🔶 DA 반대 논리를 §5에 전문 포함 + §7 강화. §8 = "DA 반대 — CIO 판단 필요" | ⛔ 최고 수준 경고. §8 = "DA 반대 + Risk FAIL — 실행 불가, CIO 오버라이드 필요" |

### §8 CIO 승인 체크리스트 생성 규칙

1. **Risk FAIL 존재 시**: 위반 항목별 "[ ] {위반 내용} 해소 확인" 체크박스 생성
2. **DA 반대 시**: "[ ] DA 반대 논리 검토 완료" 체크박스 생성 + 반대 핵심 한 줄 인용
3. **DA 조건부 동의 시**: "[ ] DA 조건 확인: {조건 내용}" 체크박스 생성
4. **둘 다 정상 시**: "[ ] 체제 판단 확인 / [ ] 실행 가이드 확인" 기본 체크리스트만

### 에스컬레이션 규칙

- Risk FAIL → **무조건 CIO 오버라이드 필요**. PM이 "괜찮겠지"로 넘기지 않는다
- DA 반대 + Risk PASS → CIO 판단에 위임하되, §7 "하지 말아야 할 행동"에 DA 숨겨진 리스크 전부 포함
- 3일 연속 DA 반대 → Discord 보고에 "⚠️ DA 3일 연속 반대" 플래그 추가

---

## 주의사항
- PM은 조합 + 기록만. 자체 투자 판단을 삽입하지 않는다
- DA에 operator의 rationale을 전달하면 안 된다 (편향 전염 방지)
- Risk Manager FAIL 시 CIO 오버라이드 없으면 실행 불가
- 데이터 부족 시 "보류" 또는 "추가 확인 필요". 추측 금지
