# Topics/

Long-lived knowledge and design documents.

## Role in MEMOS v3
- Topics are **cold by default**
- Load them only when directly relevant
- Use them for durable concepts, designs, and reference material

## TTL
Temporary Topics can declare:

```yaml
archive_after: YYYY-MM-DD
```

Expired files can be moved to `Archive/deprecated-topics/` by periodic cleanup.
