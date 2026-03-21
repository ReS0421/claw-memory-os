# 🧠 claw-memory-os

**A persistent memory system for AI agents built on [OpenClaw](https://github.com/openclaw/openclaw).**

AI agents forget everything between sessions. This project gives them structured, file-based memory that survives restarts — without databases, embeddings, or vector stores. Just markdown files with clear rules.

## What This Is

A complete operating system for AI agent memory:

- **Session continuity** — agents read their memory files at startup and update them before shutdown
- **Structured recall** — channels, tickets, topics, and long-term memory each have their place
- **Automatic distillation** — daily cron separates signal from noise, keeping memory lean
- **Multi-agent orchestration** — org chart with specialized subagents (coder team, investment team, research pipeline, secretary)
- **Checkpoint system** — mid-session writing prevents memory loss during long conversations

## Architecture

```
workspace/
├── SOUL.md              # Agent identity and personality
├── USER.md              # About your human (learned over time)
├── AGENTS.md            # Session rules, org chart, workflows
├── HEARTBEAT.md         # Periodic health checks
├── BOOTSTRAP.md         # Reading guide (where to find what)
├── TOOLS.md             # Local environment notes
│
├── System/              # Operational rules (source of truth)
│   ├── memory-rules.md          # Distillation rules
│   ├── channel-archiving-rules.md  # Channel trimming policy
│   ├── design-review-checklist.md  # System design verification
│   ├── skills-registry.md      # Skill catalog + org chart
│   ├── infrastructure.md       # Infra, paths, services
│   ├── notion-ids.md           # Notion ID reference
│   └── MISSION.md              # Top-level goals
│
├── skills/              # Subagent skills (SKILL.md per role)
│   ├── openclaw-secretary/     # Ops docs, memory, daily logs
│   ├── coder-*/                # Coding team (architect → planner → ACP → reviewer)
│   ├── invest-*/               # Investment team (4-agent chain)
│   ├── finance-*/              # Research pipelines
│   ├── knowledge-ops/          # Obsidian ↔ Notion dual system
│   └── ...
│
├── scripts/             # Automation utilities
│   ├── git-autocommit.sh       # Auto-commit workspace changes
│   ├── vault-backup.sh         # Git-based vault sync
│   ├── cost-tracker.sh         # Token usage tracking
│   └── ...
│
└── vault-template/      # Starter structure for your vault
    ├── Channels/        # Conversation state (one file per channel)
    ├── Tickets/         # Task tracking (T-001, T-002, ...)
    ├── Topics/          # Long-lived knowledge docs
    ├── Memory/          # MEMORY.md + INBOX + review log
    ├── Sessions/        # Archived session records
    └── Daily/           # Daily logs (one per day)
```

## Key Concepts

### Memory Hierarchy
1. **MEMORY.md** — Long-term curated memory ("will this matter in 6 months?")
2. **Channels/** — Current state per conversation thread
3. **Topics/** — Mature knowledge promoted from channels
4. **Tickets/** — Active tasks with INDEX.md overview
5. **Daily/** — Time-axis event log
6. **Sessions/** — Archived channel history

### Two-Path Memory Intake
- **Immediate** — infrastructure changes, key decisions, confirmed patterns → straight to MEMORY.md
- **Inbox** — uncertain items → MEMORY_INBOX.md → daily distillation cron decides

### Channel Lifecycle
Channels track conversation state. When they grow too large (>10 decisions or >3KB), old entries archive to Sessions/. Frontmatter `abstract` enables fast scanning at session start.

### Subagent Orchestration
The org chart in AGENTS.md defines specialized roles. Each skill folder contains a SKILL.md that gets injected into the subagent's task at spawn time.

## Getting Started

1. **Install [OpenClaw](https://github.com/openclaw/openclaw)** if you haven't already

2. **Copy the workspace files** to your OpenClaw workspace:
   ```bash
   cp -r SOUL.md USER.md AGENTS.md HEARTBEAT.md BOOTSTRAP.md TOOLS.md IDENTITY.md ~/.openclaw/workspace/
   cp -r System/ skills/ scripts/ ~/.openclaw/workspace/
   ```

3. **Set up your vault** (the memory storage):
   ```bash
   cp -r vault-template/ ~/vaults/my-workspace/
   cd ~/vaults/my-workspace && git init
   ```

4. **Customize**:
   - Edit `SOUL.md` — give your agent a name and personality
   - Edit `System/MISSION.md` — define your goals
   - Edit `System/infrastructure.md` — map your setup
   - Review `AGENTS.md` — adjust the org chart to your needs

5. **Set up crons** (optional but recommended):
   - Daily log: `05:00`
   - Memory distillation: `05:30`
   - Vault backup: `03:00`

## Design Principles

- **Files over databases.** Everything is markdown. Git gives you history.
- **Single source of truth.** Each piece of info lives in exactly one place. Everything else is a pointer.
- **Separation of axes.** State (Channels, Tickets) vs. time (Daily, Sessions) never mix.
- **Automatic trimming.** Memory grows; rules keep it bounded.
- **Distillation over accumulation.** Not everything deserves to be remembered.

## Skills Included

| Category | Skills | Purpose |
|---|---|---|
| **Operations** | secretary, skill-creator | Docs, memory, auditing |
| **Knowledge** | knowledge-ops, obsidian-governance, notion-*, second-brain-operator | Dual knowledge system |
| **Research** | finance-researcher, finance-analyst, dev-research | Structured research pipelines |
| **Investment** | invest-portfolio-manager, invest-analyst, invest-operator, invest-da, invest-risk-manager | 4-agent investment chain |
| **Coding** | coder-architect, coder-planner, coder-developer (reviewer), coder-designer, coder-spec, repo-scanner | Multi-tier coding orchestration |

## Contributing

This system was built for real daily use. If you find improvements, open an issue or PR.

## License

MIT

---

Built with [OpenClaw](https://github.com/openclaw/openclaw) 🐾
