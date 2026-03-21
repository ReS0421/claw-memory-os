# Contributing to claw-memory-os

Thanks for your interest! This project is built for real daily use, and contributions that improve the memory system are welcome.

## How to Contribute

### Reporting Issues
- Use the [issue templates](https://github.com/ReS0421/claw-memory-os/issues/new/choose)
- Include your OpenClaw version and setup context

### Pull Requests
1. Fork the repo
2. Create a branch (`git checkout -b improve-distillation-rules`)
3. Make your changes
4. Test with an actual OpenClaw agent if possible
5. Submit a PR with a clear description of what changed and why

### What We're Looking For
- Improvements to memory rules (distillation, archiving, trimming)
- Better session startup/shutdown workflows
- New automation scripts for memory management
- Documentation improvements
- Bug fixes in existing scripts

### Guidelines
- Keep files in markdown — no databases, no complex dependencies
- Maintain the single-source-of-truth principle
- Test your changes in a real agent workflow when possible
- Use clear commit messages (`docs:`, `feat:`, `fix:`)

## Structure

See [README.md](README.md) for the full architecture overview. Key files:
- `System/memory-rules.md` — core distillation rules
- `System/channel-archiving-rules.md` — channel trimming policy
- `AGENTS.md` — session workflow rules
- `skills/openclaw-secretary/SKILL.md` — memory management automation

## Questions?

Open an issue or join the [OpenClaw Discord](https://discord.com/invite/clawd).
