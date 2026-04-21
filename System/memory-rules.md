---
title: Memory Rules (MEMOS v3)
---

# Memory Rules — MEMOS v3

> Source of truth for memory distillation, routing, and bounded growth.
> Both cron flows and session wrap-up should follow this file.

## Core Principle

Ask: **Will this still matter in 6 months?**

## MEMOS v3 Structure

| Layer | Role | Write pattern |
|---|---|---|
| `Memory/MEMORY.md` | Master MOC, pointer-first overview | replace summaries only |
| `Memory/State/{domain}.md` | Current domain state | full replace |
| `Memory/Log/YYYY-MM.md` | Milestones and key decisions | append only |
| `Memory/Patterns/` | Learned patterns and cases | append or merge |
| `Memory/MEMORY_INBOX.md` | Pre-distillation queue | clear after processing |

## Two Intake Paths

### 1. Immediate Path
Write directly when any of these apply:
- infrastructure change
- key design or architecture decision
- new tool, pipeline, or automation
- project state transition
- system structure change
- confirmed Learned Pattern or Case

When writing immediately:
- replace old state instead of duplicating it
- keep details in source docs, not in `MEMORY.md`
- log the decision in `Memory/review-log.md` as `immediate`

### 2. Inbox Path
Default path for uncertain or lower-signal items.
- add to `Memory/MEMORY_INBOX.md`
- distillation later decides: promote / discard / hold

## Distillation Cycle

- usually daily, after daily-log
- can skip quietly if nothing changed
- even light days should still update `Memory/review-log.md`

## Distillation Rules

1. Process `pending` INBOX items first
2. Extract only decisions, state changes, config changes, and durable insights from Daily and Channels
3. Do not duplicate existing content
4. Replace stale facts instead of accumulating them
5. Detect repeated patterns or concrete problem→solution pairs and promote them to `Patterns/`

## Prohibited

1. Never put active tasks or TODOs in `MEMORY.md`
2. Never put short-lived operational noise in Key Log
3. Never copy full contents from `System/`, `Channels/`, or other source files into memory
4. Keep Patterns and Cases bounded, merge or prune when they sprawl

## v3 Additions

### Relevance Selection + skipIndex
- Use AGENTS loading rules to select only relevant State files
- `skipIndex` is best-effort session-local tracking to avoid redundant reads
- Revisit the approach if State files reach ~20+ or Topics reach ~50+

### Storage Ban Filter
Do not promote to durable memory:
- one-off fixes already captured in Daily
- transient chat details with no durable value
- duplicate references to existing canonical docs

### Staleness Checks
Heartbeat can warn when `Memory/State/*.md` files have not been updated for 30+ days.

## TTL Archive Policy

### `archive_after` field
- Topic files may declare `archive_after: YYYY-MM-DD`
- once expired, `archive-cleanup` moves them to `Archive/deprecated-topics/`
- missing `archive_after` can be treated as a lint warning for Topics that should be time-bounded

### TTL Guidelines
| State | Suggested TTL |
|---|---|
| short-lived implementation plan | 2 to 6 weeks |
| temporary comparison or audit note | 1 to 3 months |
| core canonical design | no TTL or very long TTL |

### Automation
- `archive-cleanup` can run monthly
- record archive moves in an archive log if your setup uses one
- extending TTL is allowed when a Topic is still actively referenced

## Hot / Cold Loading

Hot load at session start:
- `SOUL.md`, `USER.md`
- Channel abstracts, current channel
- `Tickets/INDEX.md`
- `Memory/MEMORY.md` and relevant `Memory/State/*.md`

Cold load only on explicit trigger:
- `Topics/*.md`
- `System/*.md`
- `Memory/Log/`, `Memory/Patterns/`
- individual Tickets

## Archive Reference Rules

- archive files are valid references, but they are not current canon
- current docs may cite archive docs as history or reference
- do not treat archive docs as active source of truth unless explicitly reactivated

## Review Log

Every promote / discard / hold / immediate decision should be logged in `Memory/review-log.md`.
Recommended columns:

| date | item | decision | reason |
|---|---|---|---|
