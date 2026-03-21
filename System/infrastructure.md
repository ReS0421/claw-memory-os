---
title: Infrastructure Overview
updated: YYYY-MM-DD
---

# Infrastructure Overview

## Architecture

```
Host Machine
├── OpenClaw Gateway  :18789
├── Agent: research (single)
├── workspace: ~/.openclaw/workspace/
└── (your services here)
```

## Key Paths

- Workspace: `~/.openclaw/workspace/`
- Vault: `~/vaults/your-vault/`
- OpenClaw Config: `~/.openclaw/openclaw.json`
- Skills: `workspace/skills/`

## Running Services

| Service | Schedule | Status |
|---|---|---|
| daily-log | daily 05:00 | ✅ |
| memory-distill | daily 05:30 | ✅ |
| vault-backup | daily 03:00 | ✅ |
| heartbeat | 6h interval | ✅ |

## External Integrations

- Discord: _(channel info)_
- Notion: _(workspace info)_
- GitHub: _(repo info)_

## Known Issues / Tech Debt

→ See `Tickets/`
