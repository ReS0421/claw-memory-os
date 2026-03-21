---
title: Memory Rules
---

# Memory Rules

> Distillation and INBOX management rules for MEMORY.md. Source of truth.
> Both cron (memory-distill) and secretary wrap-up follow these rules.

## Intake Criteria
"Will this still matter in 6 months?"

## MEMORY.md Section Structure

| Section | Content | Update Method |
|---------|---------|---------------|
| **About {user}** | User profile + preferences | Add/replace |
| **About Me** | Agent profile | Replace on change |
| **System Overview** | Infra pointers | Maintain pointers, details in System/ |
| **Domain Status** | Per-domain state summaries | Replace (keep latest only) |
| **Learned Patterns** | Repeatedly confirmed operational patterns | Add (merge if duplicate) |
| **Learned Cases** | Specific problem→solution pairs | Add (merge if similar) |
| **Key Decisions** | Chronological key decisions | Append only |

### Learned Patterns Intake Criteria
- **2+ occurrences** of the same pattern observed
- Or even 1 occurrence if impact is high (30+ min wasted, data loss risk, etc.)
- Format: one line, "situation → lesson" structure

### Learned Cases Intake Criteria
- Concrete problem + solution must exist as a pair
- Only if reoccurrence is likely
- Format: one line, "problem: cause → solution"

## Two Intake Paths

### 1. Immediate Path (during secretary wrap-up)
Certain long-term memories skip the INBOX and go directly to MEMORY.md.

**Criteria (if any apply):**
- Infrastructure change (services, cron, paths)
- Key design decision (architecture, system design)
- New tool/pipeline introduced
- Project state transition (started, completed, paused)
- System structure change (memory system, vault structure)

Log as `decision: immediate` in review-log.

### 2. Inbox Path (default)
Items that need judgment go to INBOX pending.
Distillation cron processes them.

## INBOX Structure
- `pending` — processed by distillation cron (promote/discard/hold)
- `hold` — untouched. Force-decided after 4 weeks.

## Distillation Cycle
- **Daily** (after daily-log)
- Skip quietly if no changes
- Light days: INBOX processing + date update is sufficient
- Always write review-log, even for small changes

## Distillation Rules
1. Check pending → promote to MEMORY.md / discard / move to hold
2. From Daily (yesterday) + Channels (yesterday's edits): extract only decisions, config changes, state changes, key insights
3. Don't duplicate existing content
4. If old info has changed → replace (not add)
5. **Extract Patterns/Cases:** detect repeated patterns or problem→solution pairs from sessions → add to relevant section

## Prohibited
1. **Never put active tasks/TODOs in MEMORY.md.** Current state belongs in Tickets/INDEX.md.
2. **Never put short-term events in Key Decisions.** "Config restored", "error fixed" — Daily is enough.
3. **Never copy other folder contents into MEMORY.** System/, Channels/ info → pointers only.
4. **Don't over-fill Patterns/Cases.** Keep each under 10. Merge or discard oldest when exceeded.

## Review Log
All promote/discard/hold/immediate decisions logged in `Memory/review-log.md`:
| date | item | decision | reason |

- Immediate: `decision: immediate`
- Promote: `decision: promote`
- Discard: `decision: discard`
- Hold: `decision: hold`
