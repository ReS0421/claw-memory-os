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
workspace/                          ← OpenClaw workspace (~/.openclaw/workspace/)
├── SOUL.md                         # Agent identity and personality
├── USER.md                         # About your human (learned over time)
├── AGENTS.md                       # Session rules, memory workflows, vault path
├── BOOTSTRAP.md                    # First-run setup ritual (delete after use)
├── IDENTITY.md                     # Agent name, creature, vibe, emoji
├── HEARTBEAT.md                    # Periodic health check tasks
├── TOOLS.md                        # Local environment notes
├── CONTRIBUTING.md                 # Contribution guidelines
├── LICENSE                         # MIT License
│
├── System/                         # Operational rules (source of truth)
│   ├── memory-rules.md             # Distillation rules
│   ├── channel-archiving-rules.md  # Channel trimming policy
│   ├── design-review-checklist.md  # System design verification
│   ├── infrastructure.md           # Infra, paths, services
│   ├── notion-ids.md               # External service ID reference
│   └── MISSION.md                  # Top-level goals
│
├── skills/
│   └── openclaw-secretary/         # Memory management, distillation, daily logs
│
├── scripts/                        # Automation utilities
│   ├── git-autocommit.sh           # Auto-commit workspace changes
│   ├── vault-backup.sh             # Git-based vault sync
│   ├── archive-cleanup.sh          # Move old Tickets/Daily/Sessions into Archive/
│   └── cost-tracker.sh             # Token usage tracking
│
└── docs/
    └── deployment.md               # Server/cloud deployment guides

vault/                              ← Separate git repo (your memory storage)
├── Archive/                        # Archived tickets, daily logs, sessions
├── Channels/                       # Conversation state (one file per channel)
├── Daily/                          # Daily logs (one per day)
├── Memory/                         # MEMORY.md + INBOX + review log
├── Sessions/                       # Archived session records
├── System/                         # Optional local copies / pointers to workspace System/
├── Tickets/                        # Task tracking (T-001, T-002, ...)
└── Topics/                         # Long-lived knowledge docs
```

> **Workspace vs. Vault:** The workspace holds agent config and rules. The vault holds your actual memory data. They're separate git repos — you can share the workspace (this repo) without exposing your memory.

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

When a session ends:
1. Update relevant Channel files
2. Move confirmed learnings to MEMORY.md or MEMORY_INBOX.md
3. Update Tickets if task states changed
4. Refresh Channel `abstract` frontmatter

## Getting Started

### 1. Install OpenClaw

Follow the [OpenClaw installation guide](https://github.com/openclaw/openclaw).

### 2. Set up your workspace

**Option A — Clone as workspace (recommended):**

Use this repo directly as your OpenClaw workspace. This lets `git-autocommit.sh` track changes automatically.

```bash
git clone https://github.com/ReS0421/claw-memory-os.git ~/.openclaw/workspace
```

**Option B — Copy files (if you manage workspace separately):**

```bash
git clone https://github.com/ReS0421/claw-memory-os.git
cd claw-memory-os
cp SOUL.md USER.md AGENTS.md BOOTSTRAP.md IDENTITY.md HEARTBEAT.md TOOLS.md ~/.openclaw/workspace/
cp -r System/ skills/ scripts/ docs/ ~/.openclaw/workspace/
```

> With Option B, `git-autocommit.sh` will only work if your workspace is independently a git repo. If not, the script skips silently.

### 3. Set up your vault

```bash
# Create vault from template
cp -r vault-template/ ~/vaults/my-workspace/
cd ~/vaults/my-workspace && git init && git add -A && git commit -m "init: memory vault"

# (Optional) Add a remote for backup/sync
# git remote add origin <your-private-repo-url>
# git push -u origin main
```

> All scripts default to `~/vaults/my-workspace/`. To use a different path, set `VAULT_PATH` (or `VAULT`) before running them.

### 4. First run

Start a session with your agent. `BOOTSTRAP.md` will guide the first conversation:
- Name your agent, set its personality
- Fill in `USER.md` with your info
- Set goals in `System/MISSION.md`
- Update `AGENTS.md` with your vault path

After setup, the agent deletes `BOOTSTRAP.md` — it's a one-time ritual.

### 5. Set up crons (recommended)

```
daily-log         05:00    # Write daily summary
memory-distill    05:30    # Distill INBOX → MEMORY.md
vault-backup      03:00    # Git commit + push vault
```

See OpenClaw docs for cron configuration.

### Deployment Options

Running on a dedicated PC? Want to access your vault from multiple devices via SMB or git sync? See [docs/deployment.md](docs/deployment.md) for setup guides.

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
| > 5,000 lines | More aggressive archiving, topic consolidation, or semantic search. |

`HEARTBEAT.md` includes an optional memory scale check — uncomment it after setting up your vault.

## Contributing

This system was built for real daily use over weeks of iteration. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT

---

Built with [OpenClaw](https://github.com/openclaw/openclaw) 🐾
