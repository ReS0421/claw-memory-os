<div align="center">

# 🧠 claw-memory-os

**A persistent memory OS for AI agents built on [OpenClaw](https://github.com/openclaw/openclaw).**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/ReS0421/claw-memory-os)](https://github.com/ReS0421/claw-memory-os/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/ReS0421/claw-memory-os)](https://github.com/ReS0421/claw-memory-os/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/ReS0421/claw-memory-os)](https://github.com/ReS0421/claw-memory-os/issues)

🇰🇷 [한국어](README.ko.md)
</div>

---

AI agents forget between sessions. This repo gives them durable, file-based memory without databases, embeddings, or vector search by default.

It has evolved beyond a simple `MEMORY.md` note. The current model is **MEMOS v3: Relevance Selection + Hot/Cold loading + TTL archiving**.

## What this system does

- reads a small, structured memory surface at session start
- loads deeper context only when relevant
- keeps current state and historical record separate
- distills noisy session output into durable memory
- archives aging Topic docs before the vault sprawls

Recent versions of this system also split memory into distinct layers: a master index (`MEMORY.md`), per-domain state files, append-only logs, reusable patterns/cases, and an inbox for distillation.

## Architecture

### Workspace

```text
workspace/                          ← OpenClaw workspace (~/.openclaw/workspace/)
├── SOUL.md                         # Agent identity and personality
├── USER.md                         # About your human
├── AGENTS.md                       # Session rules, memory workflows, vault path
├── BOOTSTRAP.md                    # First-run setup guide
├── IDENTITY.md                     # Agent identity pointer
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
├── scripts/
└── docs/
```

### Vault

```text
vault/
├── Archive/
├── Channels/
├── Daily/
├── Memory/
│   ├── MEMORY.md
│   ├── MEMORY_INBOX.md
│   ├── State/
│   ├── Log/
│   └── Patterns/
├── Sessions/
├── System/
├── Tickets/
└── Topics/
```

## Key Concepts

### Memory Hierarchy

```text
MEMORY.md                ← Master index / long-term navigation layer
State/{domain}.md        ← Current state per domain (replace-in-place)
Log/YYYY-MM.md           ← Append-only key decisions
Patterns/                ← Reusable patterns and concrete cases
MEMORY_INBOX.md          ← Pending distillation buffer

Channels/                ← Current state per conversation thread
Topics/                  ← Mature knowledge promoted from Channels
Tickets/                 ← Active tasks with INDEX.md overview
Daily/                   ← Time-axis event log (one per day)
Sessions/                ← Archived channel history
```

## Core Model

### 1. MEMOS v3

Instead of one growing memory file, memory is split by role:

- `Memory/MEMORY.md` for the pointer-first master overview
- `Memory/State/*.md` for current domain state
- `Memory/Log/YYYY-MM.md` for append-only milestones
- `Memory/Patterns/` for reusable learned patterns and cases
- `Memory/MEMORY_INBOX.md` for pre-distillation intake

Two intake paths coexist:
1. **Immediate path** — stable state changes, infrastructure changes, confirmed patterns/cases, or key decisions → update the appropriate long-term file directly
2. **Inbox path** — uncertain items → `MEMORY_INBOX.md` → daily distillation decides (promote / discard / hold)

A practical rule of thumb: keep `MEMORY.md` as an index, keep current domain truth in `State/`, and keep historical decisions in append-only `Log/`.

### 2. Relevance Selection

The agent should not load everything every session.

Typical startup flow:
1. scan Channel abstracts
2. read the current channel
3. read `Tickets/INDEX.md`
4. read `Memory/MEMORY.md`
5. load only relevant `Memory/State/{domain}.md`
6. keep `Topics/` and most `System/` docs cold unless explicitly needed

This reduces context waste and keeps session start lean.

### 3. Hot / Cold Loading

**Hot:** identity, user, channel scan, current channel, ticket index, master memory, relevant state files.

**Cold:** Topics, detailed System docs, monthly logs, pattern libraries, individual ticket files.

Topics should load only when:
- the user directly mentions the topic
- the active ticket explicitly links it
- the agent decides it is necessary and states why

### 4. TTL Archiving

Some Topic docs are temporary by nature. Add:

```yaml
archive_after: YYYY-MM-DD
```

Then a periodic cleanup can move expired Topics into `Archive/deprecated-topics/`.

This keeps design residue from silently bloating active memory.

## Design Principles

- **Files over databases**
- **Single source of truth**
- **Current state vs historical record separation**
- **Distillation over accumulation**
- **Bounded growth**
- **Canonical-first references**

### Distillation Rules

The distillation cron (see `System/memory-rules.md`) follows strict rules:
- **Promote** only what still matters long-term
- **Replace** current-state files instead of accumulating stale summaries
- **Append** historical decisions to monthly logs instead of rewriting history
- **Never** put active tasks in long-term memory files (that's Tickets' job)
- **Promote patterns/cases** only when repetition or impact justifies it
- Prefer pointers and structure over duplication

### Session Wrap-up

When a session ends:
1. Update relevant Channel files
2. Move confirmed learnings to MEMORY.md or MEMORY_INBOX.md
3. Update Tickets if task states changed
4. Refresh Channel `abstract` frontmatter

## Getting Started

### 1. Clone the workspace

```bash
git clone https://github.com/ReS0421/claw-memory-os.git ~/.openclaw/workspace
```

### 2. Create a private vault

```bash
cp -r vault-template/ ~/vaults/my-workspace/
cd ~/vaults/my-workspace
git init
git add -A
git commit -m "init: memory vault"
```

> Your vault repo should be private. It contains real memory data.

### 3. Set your session rules

Customize:
- `SOUL.md`
- `USER.md`
- `AGENTS.md`
- `System/MISSION.md`

### 4. Add automation

Recommended recurring jobs:
- daily-log
- memory-distill
- vault-backup
- archive-cleanup

## Vault Template Quick Tour

If you open `vault-template/` for the first time, start here:

- `Memory/MEMORY.md` → the lightweight master entry point
- `Memory/State/` → current truth by domain
- `Memory/Log/` → append-only monthly milestones
- `Memory/Patterns/` → reusable patterns and problem→solution cases
- `Memory/MEMORY_INBOX.md` → pre-distillation queue
- `Channels/` → current conversation state
- `Tickets/` → active execution state
- `Topics/` → durable design and knowledge docs

A simple rule of thumb:
- **current truth** → `State/`
- **historical milestones** → `Log/`
- **reusable lessons** → `Patterns/`
- **uncertain intake** → `MEMORY_INBOX.md`

That split is the heart of MEMOS v3.
