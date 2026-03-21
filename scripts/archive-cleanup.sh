#!/bin/bash
# Archive cleanup — manual trigger
# Usage: bash scripts/archive-cleanup.sh

VAULT="${VAULT:-$HOME/vaults/workspace}"
TODAY=$(date +%Y-%m-%d)
YEAR=$(date +%Y)
MONTH=$(date +%Y-%m)
CHANGED=0

# 1. Done Tickets → Archive/tickets/YYYY-MM/
# Only tickets marked done for 30+ days
mkdir -p "$VAULT/Archive/tickets/$MONTH"
for f in "$VAULT/Tickets/"T-*.md; do
  [ -f "$f" ] || continue
  status=$(grep -m1 "^status:" "$f" 2>/dev/null | sed 's/status: //')
  if [ "$status" = "done" ]; then
    updated=$(grep -m1 "^updated:" "$f" 2>/dev/null | sed 's/updated: //')
    if [ -z "$updated" ]; then
      updated=$(grep -m1 "^created:" "$f" 2>/dev/null | sed 's/created: //')
    fi
    if [ -n "$updated" ]; then
      days_ago=$(( ($(date -d "$TODAY" +%s) - $(date -d "$updated" +%s)) / 86400 ))
      if [ "$days_ago" -ge 30 ]; then
        name=$(basename "$f")
        mv "$f" "$VAULT/Archive/tickets/$MONTH/$name"
        echo "| $TODAY | Tickets/$name | Archive/tickets/$MONTH/$name | done 30+ days |" >> "$VAULT/Archive/archive-log.md"
        echo "archived: $name ($days_ago days)"
        CHANGED=1
      fi
    fi
  fi
done

# 2. Old Daily → Archive/daily/YYYY/
mkdir -p "$VAULT/Archive/daily/$YEAR"
for f in "$VAULT/Daily/"*.md; do
  [ -f "$f" ] || continue
  name=$(basename "$f" .md)
  if [ -n "$name" ]; then
    days_ago=$(( ($(date -d "$TODAY" +%s) - $(date -d "$name" +%s 2>/dev/null || echo 0)) / 86400 )) 2>/dev/null
    if [ "$days_ago" -ge 30 ]; then
      mv "$f" "$VAULT/Archive/daily/$YEAR/$(basename $f)"
      echo "| $TODAY | Daily/$(basename $f) | Archive/daily/$YEAR/$(basename $f) | 30+ days |" >> "$VAULT/Archive/archive-log.md"
      echo "archived: $(basename $f) ($days_ago days)"
      CHANGED=1
    fi
  fi
done

# 3. Old Sessions → Archive/sessions/YYYY/
mkdir -p "$VAULT/Archive/sessions/$YEAR"
for f in "$VAULT/Sessions/"*.md; do
  [ -f "$f" ] || continue
  name=$(basename "$f" .md)
  date_part=$(echo "$name" | grep -oP '^\d{4}-\d{2}-\d{2}')
  if [ -n "$date_part" ]; then
    days_ago=$(( ($(date -d "$TODAY" +%s) - $(date -d "$date_part" +%s)) / 86400 ))
    if [ "$days_ago" -ge 60 ]; then
      mv "$f" "$VAULT/Archive/sessions/$YEAR/$(basename $f)"
      echo "| $TODAY | Sessions/$(basename $f) | Archive/sessions/$YEAR/$(basename $f) | 60+ days |" >> "$VAULT/Archive/archive-log.md"
      echo "archived: $(basename $f) ($days_ago days)"
      CHANGED=1
    fi
  fi
done

if [ "$CHANGED" -eq 0 ]; then
  echo "Nothing to archive"
else
  cd "$VAULT" && git add -A && git commit -m "archive: cleanup $TODAY" && git push
  echo "Archive complete + git push"
fi
