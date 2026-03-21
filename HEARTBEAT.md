# HEARTBEAT.md

## Active Tasks

- If vault mount is down, reply with the alert.
- Scan Tickets: `find Tickets/ -name "T-*.md" -mtime +7` then check which ones have `status: active`. List stale ones (7+ days no update) in reply if any.
- Run `bash scripts/cost-tracker.sh today` — if today's cost exceeds $20, reply with a cost alert.
- Memory scale check: `cat Memory/MEMORY.md Channels/*.md Topics/*.md 2>/dev/null | wc -l` — if over 5,000 lines, alert about memory growth.
- If nothing needs attention, reply HEARTBEAT_OK.

## Notes
- Daily log → cron (daily 05:00)
- MEMORY.md distillation → cron (daily 05:30)
- Vault backup → cron (daily 03:00)
- Above tasks are excluded from heartbeat
