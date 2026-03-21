---
title: Channel Archiving Rules
created: 2026-03-21
updated: 2026-03-21
---

# Channel Archiving Rules

> Channel 파일 비대화 방지를 위한 아카이빙 정책. 정본.
> secretary wrap-up + daily-log cron이 이 규칙을 따른다.

## 원칙
- Channel 파일은 **현재 상태 + 최근 맥락**만 유지
- 과거 이력은 Sessions/로 이관
- Channel은 "지금 열면 현황 파악 가능"한 상태를 유지

## 트리밍 기준

### Recent Decisions
- **유지:** 최근 2주 이내 항목 (최대 10개)
- **이관:** 2주 초과 → Sessions/{날짜}-{채널명}.md로 이동
- **예외:** Open Loops에서 참조하는 결정은 2주 넘어도 유지

### 완료 섹션
- **유지:** 최근 1주 이내 완료 항목
- **이관:** 1주 초과 → Sessions/로 이동
- **이관 시:** 완료 일자 + 한 줄 요약만 Sessions에 기록

### Open Loops
- 트리밍 대상 아님 — 해결될 때까지 유지
- 해결 시 → 완료 섹션으로 이동 (1주 후 트리밍 대상)

## 트리밍 타이밍

### 자동 (daily-log cron, 매일 05:00)
- Channel 파일 스캔: `Recent Decisions` 내 2주 초과 항목 감지
- 감지만 하고, Daily에 `⚠️ trim-candidate` 행으로 기록
- 실제 트리밍은 하지 않음 (데이터 손실 방지)

### 수동 (secretary wrap-up)
- wrap-up 시 해당 채널의 Recent Decisions 10개 초과 확인
- 초과 시 오래된 것부터 Sessions/로 이관 후 Channel에서 제거
- 이관 파일명: `Sessions/{날짜}-{채널명}-archive.md`
- 이관 시 Channel에 `> 이전 기록: Sessions/{파일명}` 링크 추가

## Sessions/ 아카이브 형식

```markdown
---
title: "{채널명} archived decisions"
date: YYYY-MM-DD
channel: {채널명}
type: channel-archive
---

# {채널명} — Archived Decisions

## From Recent Decisions (archived YYYY-MM-DD)
- [원본 날짜] 결정 내용
- ...

## From 완료 (archived YYYY-MM-DD)  
- 완료 항목
- ...
```

## 크기 경고선
- **1.5KB 초과:** 트리밍 권장 (daily-log가 감지)
- **3KB 초과:** 즉시 트리밍 (secretary가 wrap-up 시 강제)

## 트리밍 금지 대상
- frontmatter (abstract, purpose, current_focus, last_updated)
- Open Loops 섹션 전체
- Related Tickets 섹션 전체
