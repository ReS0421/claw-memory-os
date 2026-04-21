# MEMORY.md — Master MOC
> Last updated: YYYY-MM-DD
> Session-start entry point. Keep this file pointer-first and lightweight.

---

## Identity
- **User**: _(name / timezone / key preferences)_
- **Agent**: _(name / first boot / role)_

---

## Domain State
> Load the relevant `Memory/State/{domain}.md` file when the request matches that domain.

| Domain | One-line status | Updated | State file |
|---|---|---|---|
| Example domain | Current status summary | MM-DD | Memory/State/example.md |

---

## Current Operating Note
- _(optional: current model/runtime/provider note)_

## System Pointers
- Channels → `Channels/`
- Tickets → `Tickets/INDEX.md`
- Topics → `Topics/`
- System rules → `System/` or workspace `System/`

---

## Patterns & Cases
- Learned Patterns → `Memory/Patterns/`
- Learned Cases → `Memory/Patterns/`

---

## Key Log
- Milestones → `Memory/Log/YYYY-MM.md`
- Intake queue → `Memory/MEMORY_INBOX.md`

---

> Current tasks/TODOs belong in `Tickets/`, not here.
