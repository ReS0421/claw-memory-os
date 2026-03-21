---
name: intel-x-post
description: "Intel Pipeline 보고서(KR/US Pre-Open)를 X 단일 포스트로 변환하는 전용 스킬. 저작권 안전 처리, 팩트 라인 형식, 출처 표기 규칙 포함. 트리거: Intel Pipeline 보고서를 X에 올려줘, intel 보고서 X 포스트 작성 요청 시."
---

# Intel X Post Writer

Intel Pipeline 보고서 → X 공개 포스트 변환 규칙.

## 저작권 원칙

팩트·수치엔 저작권 없음(한국 저작권법 제7조). 문장 전재는 금지.

| 채널 유형 | 처리 방식 |
|---|---|
| 증권사 공식 리서치 (하나·미래에셋·신한·메리츠·한화·키움·대신·DAOL) | 팩트+수치 자유 인용, 출처 표기 |
| 독립 리서치 / 유료 채널 (그로쓰리서치, Plan G Research 등) | 팩트·수치만 추출, 문장 전재 금지, 출처 표기 |
| 개인 채널 (루팡, 특파원 김씨, 사제콩이 등) | 팩트·수치만 추출, 문장 전재 금지, 출처 표기 |
| 연합인포맥스(einfomax) | 기사 본문 전재 절대 금지, 제목+링크만 또는 팩트 요약 |
| 외신(Bloomberg, Reuters, WSJ 등) | 팩트 요약 인용, 원문 링크 첨부 |

## 포스트 형식 규칙

### 구조
```
[헤더 이모지] [날짜] [시장] [브리프 제목]

━━━━━━━━━━━━━━━━━
[섹션 이모지] [섹션명]
━━━━━━━━━━━━━━━━━
◾ [팩트 라인]
◾ [팩트 라인]

━━━━━━━━━━━━━━━━━
[섹션 이모지] [섹션명]
━━━━━━━━━━━━━━━━━
◾ [팩트 라인]

━━━━━━━━━━━━━━━━━
📎 출처
━━━━━━━━━━━━━━━━━
[출처명] [URL]
```

### 필수 규칙
- **단일 포스트** — 스레드로 나누지 않음
- **언어**: 한국어 (종목·지수·기관명은 영문 병기 허용)
- **수치 표기**: 단위 명시 ($93.63, +7.31%, 213K, 148.7만)
- ✅ / ❌ — 예상 대비 서프라이즈/미스 표기
- ◾ — 팩트 불릿
- ━━━ — 섹션 구분선
- 섹션 이모지: 🛢유가 ⚔️전황 📊지표 📈증시 📋종목 🌏무역 💡코멘트 📎출처

### 팩트 라인 작성 원칙
- 주어(누가/무엇이) + 수치/행동 + 맥락(왜 중요한가) 순
- 한 줄에 하나의 팩트
- 배경 설명 금지 — 팩트만
- 예측·전망은 출처 명시 필수 ("골드만삭스: ...")
- 중립 톤 유지 — 투자 권유 표현 금지

### 출처 섹션
- 반드시 원문 URL 첨부
- 텔레그램 채널 직접 링크 허용 (https://t.me/채널명)
- einfomax 기사 링크 허용
- 여러 출처는 줄바꿈으로 나열

## 섹션 선택 기준

보고서에 해당 내용이 있을 때만 섹션 포함. 없으면 생략.

| 보고서 내용 | 포함 섹션 |
|---|---|
| 유가/에너지 이슈 | 🛢 유가/에너지 |
| 지정학·전쟁·분쟁 | ⚔️ 전황 |
| 미국 경제지표 (CPI, 고용, 주택 등) | 📊 경제지표 |
| 뉴욕 증시 마감/선물 | 📈 뉴욕 증시 |
| 프리마켓 개별 종목 | 📋 프리마켓 종목 |
| 관세·무역·통상 | 🌏 무역/관세 |
| 기관 코멘트·전망 | 💡 주목 코멘트 |

## 품질 체크리스트

포스트 작성 후 확인:
- [ ] 단일 포스트인가
- [ ] 문장 전재 없이 팩트·수치만 인용했는가
- [ ] 출처 URL이 모두 첨부됐는가
- [ ] 투자 권유 표현이 없는가
- [ ] ✅/❌ 로 서프라이즈/미스가 명시됐는가
- [ ] 빈 섹션이 없는가

## Intel Pipeline 연동

보고서 파일 위치: `/mnt/vault/Resources/Daily digests/Finance/[KR|US]/YYYY-MM-DD.md`
Raw DB: `~/workspace/intel_pipeline/data/dedup.db`

보고서 내용이 부실할 경우 — DB에서 직접 팩트 추가 추출 후 보강:
```python
import sqlite3, json
conn = sqlite3.connect("~/workspace/intel_pipeline/data/dedup.db")
cur = conn.cursor()
cur.execute("""
    SELECT source_container, canonical_url, judge_result
    FROM events WHERE first_seen >= 'YYYY-MM-DD' AND accepted = 1
    ORDER BY (json_extract(judge_result,'$.relevance') +
              json_extract(judge_result,'$.importance') +
              json_extract(judge_result,'$.novelty')) DESC
    LIMIT 60
""")
```

자세한 채널별 저작권 분류는 `references/channel-copyright.md` 참조.

---

## spawn 예시

```
sessions_spawn:
  task: |
    너는 intel-x-post 작성자다.
    ~/.openclaw/workspace/skills/intel-x-post/SKILL.md를 읽고 따라라.

    보고서 경로: {파일 경로}
    시장: {KR 또는 US}
    날짜: {YYYY-MM-DD}

    품질 체크리스트를 모두 통과한 단일 포스트를 작성하라.
    출처 URL을 반드시 포함하라.
  mode: run
  runtime: subagent
  model: sonnet
  runTimeoutSeconds: 300
```
