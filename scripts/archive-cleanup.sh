#!/usr/bin/env bash
# archive-cleanup.sh — move old tickets/daily/sessions to Archive/
# Usage: bash scripts/archive-cleanup.sh
#
# Compatibility: Linux (GNU date) and macOS (BSD date)
# Set VAULT_PATH (or VAULT) to override the default path.

set -euo pipefail

VAULT="${VAULT_PATH:-${VAULT:-$HOME/vaults/my-workspace}}"
TODAY=$(date +%Y-%m-%d)
YEAR=$(date +%Y)
MONTH=$(date +%Y-%m)
CHANGED=0

# ── Cross-platform date diff ──────────────────────────────────────────────────
days_since() {
    local target="$1"
    if date --version >/dev/null 2>&1; then
        # GNU date (Linux)
        echo $(( ($(date -d "$TODAY" +%s) - $(date -d "$target" +%s 2>/dev/null || echo 0)) / 86400 ))
    else
        # BSD date (macOS)
        local today_ts target_ts
        today_ts=$(date -j -f "%Y-%m-%d" "$TODAY" "+%s" 2>/dev/null || echo 0)
        target_ts=$(date -j -f "%Y-%m-%d" "$target" "+%s" 2>/dev/null || echo 0)
        echo $(( (today_ts - target_ts) / 86400 ))
    fi
}
# ─────────────────────────────────────────────────────────────────────────────

# 1. Done Tickets → Archive/tickets/YYYY-MM/  (30+ days since last update)
mkdir -p "$VAULT/Archive/tickets/$MONTH"
for f in "$VAULT/Tickets/"T-*.md; do
  [ -f "$f" ] || continue
  status=$(grep -m1 "^status:" "$f" 2>/dev/null | sed 's/status: //' | tr -d '[:space:]')
  if [ "$status" = "done" ]; then
    updated=$(grep -m1 "^updated:" "$f" 2>/dev/null | sed 's/updated: //' | tr -d '[:space:]')
    [ -z "$updated" ] && updated=$(grep -m1 "^created:" "$f" 2>/dev/null | sed 's/created: //' | tr -d '[:space:]')
    if [ -n "$updated" ]; then
      days_ago=$(days_since "$updated")
      if [ "$days_ago" -ge 30 ]; then
        name=$(basename "$f")
        mv "$f" "$VAULT/Archive/tickets/$MONTH/$name"
        echo "| $TODAY | Tickets/$name | Archive/tickets/$MONTH/$name | done ${days_ago}d |" >> "$VAULT/Archive/archive-log.md"
        echo "archived: $name ($days_ago days)"
        CHANGED=1
      fi
    fi
  fi
done

# 2. Old Daily → Archive/daily/YYYY/  (30+ days)
mkdir -p "$VAULT/Archive/daily/$YEAR"
for f in "$VAULT/Daily/"*.md; do
  [ -f "$f" ] || continue
  name=$(basename "$f" .md)
  # only process files named YYYY-MM-DD
  if [[ "$name" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    days_ago=$(days_since "$name")
    if [ "$days_ago" -ge 30 ]; then
      mv "$f" "$VAULT/Archive/daily/$YEAR/$(basename "$f")"
      echo "| $TODAY | Daily/$(basename $f) | Archive/daily/$YEAR/$(basename $f) | ${days_ago}d |" >> "$VAULT/Archive/archive-log.md"
      echo "archived: $(basename $f) ($days_ago days)"
      CHANGED=1
    fi
  fi
done

# 3. Old Sessions → Archive/sessions/YYYY/  (60+ days)
mkdir -p "$VAULT/Archive/sessions/$YEAR"
for f in "$VAULT/Sessions/"*.md; do
  [ -f "$f" ] || continue
  date_part=$(basename "$f" | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}' || true)
  if [ -n "$date_part" ]; then
    days_ago=$(days_since "$date_part")
    if [ "$days_ago" -ge 60 ]; then
      mv "$f" "$VAULT/Archive/sessions/$YEAR/$(basename "$f")"
      echo "| $TODAY | Sessions/$(basename $f) | Archive/sessions/$YEAR/$(basename $f) | ${days_ago}d |" >> "$VAULT/Archive/archive-log.md"
      echo "archived: $(basename $f) ($days_ago days)"
      CHANGED=1
    fi
  fi
done

if [ "$CHANGED" -eq 0 ]; then
  echo "Nothing to archive"
else
  cd "$VAULT"
  if [ -d ".git" ]; then
    git add -A && git commit -m "archive: cleanup $TODAY"
    if git remote get-url origin >/dev/null 2>&1; then
      git push && echo "Archive complete + git push"
    else
      echo "Archive complete (committed locally, no remote)"
    fi
  else
    echo "Archive complete (vault is not a git repo)"
  fi
fi
