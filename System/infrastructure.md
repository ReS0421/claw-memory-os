---
title: Infrastructure Overview
updated: YYYY-MM-DD
---

# Infrastructure Overview

## Architecture

```
Host Machine
├── OpenClaw Gateway  :18789
├── Agent: _(your agent name)_
├── workspace: ~/.openclaw/workspace/
└── (your services here)
```

## Key Paths

- Workspace: `~/.openclaw/workspace/`
- Vault: `~/vaults/my-workspace/` _(update to match your VAULT_PATH)_
- OpenClaw Config: `~/.openclaw/openclaw.json`
- Skills: `workspace/skills/`

## Running Services

| Service | Schedule | Status |
|---|---|---|
| daily-log | daily 05:00 | enabled / disabled |
| memory-distill | daily 05:30 | enabled / disabled |
| vault-backup | daily 03:00 | enabled / disabled |
| heartbeat | _(interval)_ | enabled / disabled |

## External Integrations

- Discord: _(channel info)_
- Notion: _(workspace info)_
- GitHub: _(repo info)_

## Known Issues / Tech Debt

→ See `Tickets/`
