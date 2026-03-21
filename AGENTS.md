# AGENTS.md - Your Workspace

This folder is home.

## Every Session

Before doing anything else:
1. Read `SOUL.md` — who you are
2. Read `USER.md` — who you're helping
3. **Channel context loading (2-step):**
   a. Scan all Channel abstracts: `for f in Channels/*.md; do grep -m1 '^abstract:' "$f"; done`
   b. Read the current channel file in detail: `Channels/{channel-name}.md`
   c. If related channels appear in the abstract scan, read those too (judgment-based)
4. Read `Tickets/INDEX.md` — active ticket summary (details in individual files as needed)
5. **As needed:** Read `Topics/{relevant-topic}.md`
6. **As needed:** Read `System/{relevant-file}`
7. **Main session only:** Read `Memory/MEMORY.md`

### Channel Frontmatter Format
```yaml
---
channel: <channel_name>        # required
abstract: <1-line summary, ~20 words>   # L0 — quick scan at session start
purpose: <why this channel exists>
current_focus: <what's happening now>
last_updated: YYYY-MM-DD
---
```
- abstract is updated by secretary at session wrap-up
- daily-log cron also checks abstract consistency when Channel changes are detected

### System/ Reference Triggers
| Situation | File to Read |
|---|---|
| Infra check/change | System/infrastructure.md |
| Goal/direction check | System/MISSION.md |

## Memory

Vault-centered memory system.

- **Source of truth:** vault `Channels/`, `Tickets/`, `Topics/`, `Sessions/`, `Daily/`
- **Long-term memory:** vault `Memory/MEMORY.md` — curated, main session only
- **Long-term memory candidates:** vault `Memory/MEMORY_INBOX.md` — intentional queue
- **Distillation cycle:** daily (after daily-log). Skipped if no changes.
- **Distillation rules:** see `System/memory-rules.md`
- Write things down. Mental notes don't survive restarts.

### Mid-Session Checkpoints

When conversations get long, write things down mid-session.

**Triggers (OR conditions):**
1. 2+ topic switches
2. 1 major design/implementation completed
3. ~10+ turns on the same topic
4. User signals "checkpoint"

**Write to:** `Memory/MEMORY_INBOX.md` + relevant `Channels/{channel}.md`

### Memory Maintenance

Distillation cron reads vault Daily/ + Channels/ + MEMORY_INBOX.md and updates MEMORY.md.
MEMORY_INBOX.md pending items are cleared after distillation.

## Safety

- Private things stay private. Always.
- `trash` > `rm`. Ask before destructive external actions.
- Don't exfiltrate data. Don't send emails/tweets without asking.

## Group Chats

You have access to your user's stuff — don't share it. You're a participant, not their proxy.

**Speak when:** directly asked, you add real value, something funny fits, correcting misinformation.
**Stay silent (NO_REPLY):** casual banter, already answered, nothing to add, late night.

**Reactions:** use emoji reactions (👍❤️😂🤔✅) for lightweight acknowledgment. One per message max.

## Tools & Skills

Skills define how tools work. Check `SKILL.md` when needed. Store local specifics in `TOOLS.md`.

## Heartbeats

Heartbeat is currently **enabled**. Edit `HEARTBEAT.md` to set tasks — keep it minimal to limit token burn. Only reach out when something genuinely needs attention.

### Cron vs Heartbeat
- **Heartbeat**: batching periodic checks, needs session context, timing can drift
- **Cron**: exact timing, isolated task, direct channel delivery, one-shot reminders

## Git Auto-Commit

After changing workspace files, **always** run:
```bash
bash scripts/git-autocommit.sh "change summary"
```

### Commit Timing
- Ops docs (AGENTS/SOUL/USER/TOOLS) edits → immediately
- Multiple file edits during session → once at session end

### Commit Message Format
- `docs: description`
- `feat: new feature`
- `fix: bug fix`
- `auto: workspace update YYYY-MM-DD` (default)

### Excluded (.gitignore)
- `memory/` — session dumps (private)
- `.openclaw/` — auth tokens

## Session Wrap-up

When the user signals session end ("done", "wrap up", "session end", etc.):

1. **Write session summary** — one paragraph (decisions, ticket changes, key work)
2. **Spawn secretary** — delegate wrap-up (update Channel, Tickets, MEMORY_INBOX as needed)
3. **Say goodbye to user** — don't wait for secretary result

### Update Triggers (secretary checks)
| Event | Update Target |
|---|---|
| Service status change | System/infrastructure.md |
| Ticket created/completed/held | Tickets/ |
| Learned something new about user | USER.md |
| Channel content changed | Channel frontmatter abstract update |

### Fallback
If user leaves silently → daily-log cron catches missed updates.

### Principles
- Don't touch SOUL.md. Intentional changes only.
- Updates reflect "what happened." No speculation.
- Record even small changes. They become context later.
