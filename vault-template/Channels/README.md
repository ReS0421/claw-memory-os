# Channels/

Current conversation state, one file per channel or thread.

## Role
- Keep **current state + recent context** here
- Keep long-lived knowledge in `Topics/`
- Keep active execution state in `Tickets/`
- Archive older detail into `Sessions/`

## Typical contents
- frontmatter: `channel`, `abstract`, `purpose`, `current_focus`, `last_updated`, optional `related`
- recent decisions
- open loops
- related tickets

Scan abstracts first, then load the current channel in detail.
