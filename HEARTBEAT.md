# HEARTBEAT.md

## Active Tasks

- If the vault mount is down, alert.
- Scan stale tickets: `find ~/vaults/my-workspace/Tickets/ -name "T-*.md" -mtime +7` and report active ones.
- Run `bash ~/.openclaw/workspace/scripts/cost-tracker.sh today` and alert if daily cost exceeds your threshold.
- Memory scale check: `cat ~/vaults/my-workspace/Memory/MEMORY.md ~/vaults/my-workspace/Channels/*.md ~/vaults/my-workspace/Topics/*.md 2>/dev/null | wc -l` and alert if total lines exceed 5,000.
- State freshness check: warn if any `Memory/State/*.md` has not been updated for 30+ days.
- If nothing needs attention, reply `HEARTBEAT_OK`.
