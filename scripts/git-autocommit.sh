#!/usr/bin/env bash
# git-autocommit.sh — auto-commit and push workspace changes
# Usage: bash scripts/git-autocommit.sh "change summary"
#
# If the workspace is not a git repo, exits silently (exit 0).
# If no remote is configured, commits locally without pushing.

set -euo pipefail
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MSG="${1:-auto: workspace update $(date +%Y-%m-%d)}"

cd "$WORKSPACE"

# Not a git repo? That's fine — just skip.
if [ ! -d ".git" ]; then
  echo "[git-autocommit] Not a git repo — skipping"
  exit 0
fi

# Remove only files that are tracked but now gitignored
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

# Push only if a remote is configured
if git remote get-url origin >/dev/null 2>&1; then
  # Resolve current branch name (fallback to main if detached)
  BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "main")
  git push origin "$BRANCH" 2>&1 \
    && echo "[git] ✅ pushed: $MSG" \
    || echo "[git] ⚠️ push failed (remote may be ahead — run git pull)"
else
  echo "[git] ✅ committed locally: $MSG (no remote configured)"
fi
