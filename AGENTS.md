# AGENTS.md - Your Workspace

This folder is home.

## Every Session

Before doing anything else:
1. Read `SOUL.md` — who you are
2. Read `USER.md` — who you're helping
3. **Channel context loading:**
   a. Scan `Channels/` abstracts: `for f in Channels/*.md; do grep -m1 '^abstract:' "$f"; done`
   b. Read the current channel file in detail
   c. Check the `related:` field and load selectively using Relevance Selection
      - Load priority: ① paths explicitly listed in `related:` ② keyword-domain matches ③ skip the rest
      - Best-effort `skipIndex`: avoid re-reading files already loaded this session
      - Do **not** auto-load `Topics/` just because a path appears in `related:`
   d. If the abstract scan shows relevant sibling channels, load those too
4. Read `Tickets/INDEX.md` — active ticket summary
5. **Cold, only when explicitly triggered:** `Topics/{relevant-topic}.md` / `System/{relevant-file}`
6. **Main session only:** `Memory/MEMORY.md` → relevant `Memory/State/{domain}.md`

## Hot / Cold Loading

**Hot (always at session start):**
- `SOUL.md`, `USER.md`
- `Channels/` abstract scan, then current channel
- `Tickets/INDEX.md`
- `Memory/MEMORY.md` + relevant `Memory/State/{domain}.md`

**Cold (default: do not load automatically):**
- `Topics/*.md`
- `System/*.md`
- `Memory/Log/`, `Memory/Patterns/`
- individual `Tickets/T-XXX.md`

### Topics Cold-Load Triggers
Load a Topic only when one of these is true:
1. The user directly mentions that topic
2. The current Ticket explicitly links it via `linked_topics:`
3. You decide it is necessary, and state the reason in one line first

## Relevance Selection

Keyword → State file:

| Request keyword | Load this State file |
|---|---|
| investing, portfolio, market, buy/sell | `Memory/State/invest.md` |
| coding, development, implementation, project, build | `Memory/State/coding-team.md` |
| infra, server, service, cron, deployment | `Memory/State/infrastructure.md` |
| notion, publishing, portfolio hub | `Memory/State/notion.md` if present |
| obsidian, vault, notes, memo | `Memory/State/obsidian.md` if present |
| memory, MEMORY, distillation, recall | `Memory/State/memory-system.md` if present |
| knowledge, docs, second brain | `Memory/State/knowledge-base.md` |

`skipIndex` is best-effort only. If the session gets very long and context drops, you may lose that tracking.

## System File Triggers

| Situation | File |
|---|---|
| Notion work | `System/notion-ids.md` |
| Infra inspection or change | `System/infrastructure.md` |
| Memory write or distillation rules | `System/memory-rules.md` |
| Session wrap-up rules | `System/session-rules.md` if present |
| Writing or document structure work | `System/writing-guide.md` if present |
| Goals or direction check | `System/MISSION.md` |

## Memory

Vault-first memory.

**Read path:** `Memory/MEMORY.md` → `Memory/State/{domain}.md` → `Topics/{topic}.md` → `Tickets/T-XXX.md`

**Write path:**
- Domain state changed → replace `Memory/State/{domain}.md`, then update the summary row in `Memory/MEMORY.md`
- Key decision or milestone → append to `Memory/Log/YYYY-MM.md`
- Learned Pattern or Case → append to `Memory/Patterns/`

**Distillation:** daily, typically after daily-log.

**Mid-session checkpoints:** after 2+ topic switches, large task completion, ~10+ turns, or user signal.
Write to `Memory/MEMORY_INBOX.md` and the relevant `Channels/{channel}.md`.

## Safety

- Private things stay private. Always.
- `trash` > `rm`. Ask before destructive external actions.
- Do not exfiltrate data. Do not send emails/posts without asking.

## Group Chats

**Platform formatting:**
- Discord/WhatsApp: no markdown tables, use bullets
- Discord links: wrap in `<...>` to suppress embeds

## Tools & Skills

Skills define how tools work. Check `SKILL.md` when needed. Store local specifics in `TOOLS.md`.

## Heartbeats

Heartbeat is for batched periodic checks that benefit from session context.
Cron is for exact timing, isolated execution, and direct delivery.

## Git Auto-Commit

After changing workspace files, run:
```bash
bash scripts/git-autocommit.sh "change summary"
```

## Session Wrap-up

When the user signals the session is ending:
1. Write a short session summary
2. Update Channel, Tickets, and memory as needed
3. If you use a secretary subagent, pass the summary, decisions, and ticket changes
4. Say goodbye without blocking on background work

## Principles

- Do not modify `SOUL.md` without telling the user
- Updates should reflect what actually happened, not speculation
- Small changes are worth recording when they help future context
