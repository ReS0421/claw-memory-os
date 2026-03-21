<div align="center">

# 🧠 claw-memory-os

**A persistent memory system for AI agents built on [OpenClaw](https://github.com/openclaw/openclaw).**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/ReS0421/claw-memory-os)](https://github.com/ReS0421/claw-memory-os/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/ReS0421/claw-memory-os)](https://github.com/ReS0421/claw-memory-os/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/ReS0421/claw-memory-os)](https://github.com/ReS0421/claw-memory-os/issues)

</div>

---


AI agents forget everything between sessions. This project gives them structured, file-based memory that survives restarts — without databases, embeddings, or vector stores. Just markdown files with clear rules.

## The Problem

Every time an AI agent starts a new session, it starts from zero. It doesn't know what you discussed yesterday, what decisions were made, or what tasks are in progress. Context windows help within a session, but across sessions? Gone.

## The Solution

A file-based memory architecture where:
- The agent **reads** its memory files at session start
- **Writes** updates during and after each session
- A **distillation cron** separates signal from noise daily
- **Archiving rules** keep memory bounded and lean

No vector databases. No embeddings. No RAG pipeline. Just markdown files with structure and discipline.

## Architecture

```
workspace/
├── SOUL.md              # Agent identity and personality
├── USER.md              # About your human (learned over time)
├── AGENTS.md            # Session rules, memory workflows
├── HEARTBEAT.md         # Periodic health checks
├── BOOTSTRAP.md         # Reading guide (where to find what)
├── TOOLS.md             # Local environment notes
│
├── System/              # Operational rules (source of truth)
│   ├── memory-rules.md          # Distillation rules
│   ├── channel-archiving-rules.md  # Channel trimming policy
│   ├── design-review-checklist.md  # System design verification
│   ├── infrastructure.md       # Infra, paths, services
│   ├── notion-ids.md           # External service ID reference
│   └── MISSION.md              # Top-level goals
│
├── skills/
│   └── openclaw-secretary/     # Memory management, distillation, logs
│
├── scripts/             # Automation utilities
│   ├── git-autocommit.sh       # Auto-commit workspace changes
│   ├── vault-backup.sh         # Git-based vault sync
│   ├── archive-cleanup.sh      # Channel archive trimming
│   └── cost-tracker.sh         # Token usage tracking
│
└── vault-template/      # Starter structure for your memory vault
    ├── Channels/        # Conversation state (one file per channel)
    ├── Tickets/         # Task tracking (T-001, T-002, ...)
    ├── Topics/          # Long-lived knowledge docs
    ├── Memory/          # MEMORY.md + INBOX + review log
    ├── Sessions/        # Archived session records
    └── Daily/           # Daily logs (one per day)
```

## Key Concepts

### Memory Hierarchy

```
MEMORY.md          ← Long-term (curated, "will this matter in 6 months?")
  ↑ distilled from
Channels/          ← Current state per conversation thread
Topics/            ← Mature knowledge promoted from Channels
Tickets/           ← Active tasks with INDEX.md overview
  ↑ logged in
Daily/             ← Time-axis event log (one per day)
Sessions/          ← Archived channel history
```

### Two-Path Memory Intake

Not everything deserves to be remembered. Two paths handle this:

1. **Immediate path** — infrastructure changes, key decisions, confirmed patterns → straight to MEMORY.md
2. **Inbox path** — uncertain items → MEMORY_INBOX.md → daily distillation cron decides (promote / discard / hold)

Every decision is logged in `Memory/review-log.md` for auditability.

### Channel Lifecycle

Channels track conversation state with structured frontmatter:

```yaml
---
channel: feature-discussion
abstract: Designing new auth flow. Waiting on API spec.
purpose: Authentication redesign project
current_focus: OAuth2 provider selection
last_updated: 2026-03-21
---
```

When channels grow too large (>10 decisions or >3KB), old entries archive to Sessions/. The `abstract` field enables fast scanning at session start without reading full files.

### Mid-Session Checkpoints

Long conversations risk memory loss. Checkpoint triggers:
- 2+ topic switches
- Major design/implementation completed
- ~10+ turns on same topic
- User explicitly signals "checkpoint"

### Distillation Rules

The distillation cron (see `System/memory-rules.md`) follows strict rules:
- **Promote** items that pass the "6-month test"
- **Replace** outdated info (don't accumulate)
- **Never** put active tasks in MEMORY.md (that's Tickets' job)
- **Learned Patterns** require 2+ observations or high impact
- **Learned Cases** need a concrete problem→solution pair
- Keep Patterns and Cases under 10 each; merge or discard old ones

### Session Wrap-up

When a session ends, the secretary:
1. Updates relevant Channel files
2. Moves confirmed learnings to MEMORY.md or MEMORY_INBOX.md
3. Updates Tickets if task states changed
4. Refreshes Channel `abstract` frontmatter

## Getting Started

1. **Install [OpenClaw](https://github.com/openclaw/openclaw)** if you haven't already

2. **Copy workspace files:**
   ```bash
   cp SOUL.md USER.md AGENTS.md HEARTBEAT.md BOOTSTRAP.md TOOLS.md IDENTITY.md ~/.openclaw/workspace/
   cp -r System/ skills/ scripts/ ~/.openclaw/workspace/
   ```

3. **Set up your vault** (memory storage):
   ```bash
   cp -r vault-template/ ~/vaults/my-workspace/
   cd ~/vaults/my-workspace && git init
   ```

4. **Customize:**
   - `SOUL.md` — give your agent a name and personality
   - `System/MISSION.md` — define your goals
   - `System/infrastructure.md` — map your setup
   - `AGENTS.md` — adjust session rules to your workflow

5. **Set up crons** (recommended):
   - Daily log generation
   - Memory distillation (after daily log)
   - Vault backup (git-based)

## Design Principles

- **Files over databases.** Everything is markdown. Git gives you history for free.
- **Single source of truth.** Each piece of info lives in exactly one place. Everything else is a pointer.
- **State vs. time separation.** Current state (Channels, Tickets) and historical record (Daily, Sessions) never mix.
- **Bounded growth.** Archiving rules and distillation keep memory from growing unboundedly.
- **Distillation over accumulation.** Not everything deserves to be remembered. Active curation beats passive storage.

## How It Scales

| Memory Size | Approach |
|---|---|
| < 1,000 lines | Just works. Read everything at session start. |
| 1,000–5,000 lines | Channel abstracts for fast scanning. Read details on demand. |
| > 5,000 lines | Time to evaluate: more aggressive archiving, topic consolidation, or semantic search. |

The system includes a heartbeat check that alerts when total memory exceeds 5,000 lines.

## Contributing

This system was built for real daily use over weeks of iteration. If you find improvements, open an issue or PR.

## License

MIT

---

Built with [OpenClaw](https://github.com/openclaw/openclaw) 🐾
