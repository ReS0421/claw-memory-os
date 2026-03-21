#!/usr/bin/env bash
# git-autocommit.sh — auto-commit and push workspace changes
# Usage: bash scripts/git-autocommit.sh "change summary"

set -euo pipefail
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MSG="${1:-auto: workspace update $(date +%Y-%m-%d)}"

cd "$WORKSPACE"

# Remove only files that are tracked but now gitignored
# (safer than wiping the entire index)
ignored_tracked=$(git ls-files -ci --exclude-standard 2>/dev/null || true)
if [ -n "$ignored_tracked" ]; then
  echo "$ignored_tracked" | xargs git rm --cached --quiet --
fi

git add -A

if git diff --cached --quiet; then
  echo "No changes to commit"
  exit 0
fi

git commit -m "$MSG"
git push origin main 2>&1 && echo "[git] ✅ pushed: $MSG" || echo "[git] ⚠️ push failed (remote may be ahead — run git pull)"
