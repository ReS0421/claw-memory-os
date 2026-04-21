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

It has evolved beyond a simple `MEMORY.md` note. The current model is **MEMOS v2 + Relevance Selection + Hot/Cold loading + TTL archiving**.

## What this system does

- reads a small, structured memory surface at session start
- loads deeper context only when relevant
- keeps current state and historical record separate
- distills noisy session output into durable memory
- archives aging Topic docs before the vault sprawls

## Current Architecture

### Workspace

```text
workspace/
├── SOUL.md
├── USER.md
├── AGENTS.md
├── BOOTSTRAP.md
├── IDENTITY.md
├── HEARTBEAT.md
├── TOOLS.md
├── System/
│   ├── memory-rules.md
│   ├── channel-archiving-rules.md
│   ├── infrastructure.md
│   ├── notion-ids.md
│   └── MISSION.md
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

## Core Model

### 1. MEMOS v2

Instead of one growing memory file, memory is split by role:

- `Memory/MEMORY.md` for the pointer-first master overview
- `Memory/State/*.md` for current domain state
- `Memory/Log/YYYY-MM.md` for append-only milestones
- `Memory/Patterns/` for reusable learned patterns and cases
- `Memory/MEMORY_INBOX.md` for pre-distillation intake

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

## Scaling Notes

| Memory size | Suggested behavior |
|---|---|
| under 1k lines | read almost everything |
| 1k to 5k | rely on channel abstracts and selective state loading |
| 5k+ | tighten archive rules, consolidate Topics, consider semantic retrieval |

## Repo Scope

This repository is the **public template / operating model**.

Your real vault is separate, private, and should contain your actual:
- Channels
- Tickets
- Topics
- Logs
- durable memory

## License

MIT

---

Built with [OpenClaw](https://github.com/openclaw/openclaw) 🐾
