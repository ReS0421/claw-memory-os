---
title: Memory Rules
created: 2026-03-21
updated: 2026-03-21
---

# Memory Rules

> MEMORY.md 증류 및 INBOX 운영 규칙. 정본.
> cron(memory-distill) + secretary wrap-up 모두 이 규칙을 따른다.

## 적재 기준
"6개월 뒤에도 알아야 하는가?"

## MEMORY.md 섹션 구조

| 섹션 | 내용 | 갱신 방식 |
|------|------|----------|
| **About {user}** | 사용자 프로필 + Preferences | 추가/교체 |
| **About Me** | 에이전트 프로필 | 변경 시 교체 |
| **시스템 구성** | 인프라 포인터 | 포인터 유지, 상세는 System/ |
| **도메인별 상태** | Notion/Obsidian/Intel/투자/코딩팀/메모리 | 교체 (최신만 유지) |
| **Learned Patterns** | 반복 확인된 운영 패턴 | 추가 (중복 시 병합) |
| **Learned Cases** | 구체적 문제→해결 쌍 | 추가 (유사 시 병합) |
| **Key Decisions** | 시간순 핵심 결정 | 추가만 |

### Learned Patterns 적재 기준
- **2회 이상** 같은 패턴이 관찰되었을 때
- 또는 1회라도 impact가 커서(시간 낭비 30분+, 데이터 손실 위험 등) 기록할 가치가 있을 때
- 형식: 한 줄, "상황 → 교훈" 구조

### Learned Cases 적재 기준
- 구체적 문제 + 해결 방법이 쌍으로 존재
- 재발 가능성이 있는 것만
- 형식: 한 줄, "문제: 원인 → 해결"

## 두 가지 적재 경로

### 1. 즉시 반영 (secretary wrap-up 시)
확실한 장기 기억은 INBOX를 거치지 않고 MEMORY.md에 직접 반영한다.

**기준 (하나라도 해당 시):**
- 인프라 변경 (서비스, cron, 경로)
- 핵심 설계 결정 (아키텍처, 운영 체계)
- 새 도구/파이프라인 도입
- 프로젝트 상태 전환 (착수, 완료, 중단)
- 시스템 구조 변경 (메모리 체계, vault 구조)
- Learned Pattern/Case 확정

review-log에 `decision: immediate` 로 기록.

### 2. INBOX 경로 (기존)
판단이 필요한 것, 애매한 것은 INBOX pending에 적재.
증류 cron(매일 05:30)이 처리.

## INBOX 구조
- `pending` — 증류 cron이 처리 (승격/폐기/hold)
- `hold` — 건드리지 않음. 4주 초과 시 강제 판단

## 증류 주기
- **매일 05:30 KST** (daily-log 05:00 직후)
- 변동 없는 날은 조용히 종료 (MEMORY.md 미수정)
- 변동 적은 날은 INBOX 처리 + 날짜 업데이트만으로 충분
- 소량 변경에도 review-log는 반드시 기록

## 증류 규칙
1. pending 확인 → MEMORY.md 반영(승격) / 폐기 / hold 이동
2. Daily(어제) + Channels(어제 수정분)에서 새 결정, 설정 변경, 상태 변화, 핵심 인사이트만 추출
3. 이미 있는 내용은 중복 추가하지 않음
4. 오래된 정보가 바뀌었으면 교체 (추가 아님)
5. **Patterns/Cases 추출:** 세션에서 반복된 패턴이나 문제→해결 쌍을 감지하면 해당 섹션에 추가

## 금지 사항
1. **진행 중인 작업/TODO를 MEMORY.md에 넣지 마라.** 현재 상태는 Tickets/INDEX.md가 담당.
2. **단기 이벤트를 Key Decisions에 넣지 마라.** "설정 복원", "에러 수정"은 Daily에 있으면 충분.
3. **다른 폴더 정본을 MEMORY에 복사하지 마라.** System/, Channels/ 정보는 포인터만 유지.
4. **Patterns/Cases를 과하게 넣지 마라.** 각 10개 이내 유지. 초과 시 오래된 것부터 병합 또는 폐기.

## review-log
모든 승격/폐기/hold/즉시반영 판단은 `Memory/review-log.md`에 기록:
| date | item | decision | reason |

- 즉시 반영: `decision: immediate`
- 증류 승격: `decision: promote`
- 폐기: `decision: discard`
- hold: `decision: hold`
