#!/usr/bin/env bash
# git-autocommit.sh — auto-commit and push workspace changes
# Usage: bash scripts/git-autocommit.sh "change summary"

set -euo pipefail
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MSG="${1:-auto: workspace update $(date +%Y-%m-%d)}"

cd "$WORKSPACE"

# 1. Remove gitignored files from index if cached
git rm -r --cached --quiet . 2>/dev/null || true

# 2. Add all (respects .gitignore — untracked files won't re-add)
git add -A

# 3. Exit if no changes
if git diff --cached --quiet; then
  echo "No changes to commit"
  exit 0
fi

git commit -m "$MSG"
git push origin main 2>&1 && echo "Push ✅" || echo "Push failed (remote may be ahead)"
