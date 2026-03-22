---
title: Channel Archiving Rules
---

# Channel Archiving Rules

> Archiving policy to prevent Channel file bloat. Source of truth.
> Both secretary wrap-up and daily-log cron follow these rules.

## Principle
- Channel files maintain **current state + recent context** only
- Past history moves to Sessions/
- A Channel should answer "what's happening now?" when opened

## Trimming Criteria

### Recent Decisions
- **Keep:** items within the last 2 weeks (max 10)
- **Archive:** items older than 2 weeks → `Sessions/{date}-{channel}-archive.md`
- **Exception:** decisions referenced by Open Loops stay even if older than 2 weeks

### Completed Items
- **Keep:** items completed within the last 1 week
- **Archive:** older than 1 week → Sessions/
- **When archiving:** record completion date + one-line summary in Sessions

### Open Loops
- Never trimmed — stay until resolved
- When resolved → move to completed section (trimming target after 1 week)

## Trimming Timing

### Automatic (daily-log cron)
- Scan Channel files: detect items older than 2 weeks in `Recent Decisions`
- Detection only — log `⚠️ trim-candidate` in Daily
- Does not perform actual trimming (data loss prevention)

### Manual (secretary wrap-up)
- Check if Recent Decisions exceeds 10 during wrap-up
- If exceeded: move oldest to Sessions/, remove from Channel
- Archive filename: `Sessions/{date}-{channel}-archive.md`
- Add `> Previous records: Sessions/{filename}` link in Channel

## Sessions/ Archive Format

```markdown
---
title: "{channel} archived decisions"
date: YYYY-MM-DD
channel: {channel}
type: channel-archive
---

# {channel} — Archived Decisions

## From Recent Decisions (archived YYYY-MM-DD)
- [original date] decision content
- ...

## From Completed (archived YYYY-MM-DD)
- completed item
- ...
```

## Size Warnings
- **Over 1.5KB:** trimming recommended (daily-log detects)
- **Over 3KB:** immediate trimming (secretary enforces during wrap-up)

## Never Trim
- Frontmatter (abstract, purpose, current_focus, last_updated)
- Open Loops section (entire)
- Related Tickets section (entire)
