#!/usr/bin/env bash
# git-autocommit.sh — workspace 변경사항 자동 커밋 + push

set -euo pipefail
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MSG="${1:-auto: workspace update $(date '+%Y-%m-%d %H:%M')}"

cd "$WORKSPACE"

# 1. gitignore 대상이 cached에 남아있으면 제거
git rm -r --cached memory/ .openclaw/ .trash/ IDENTITY.md intel_pipeline/ 2>/dev/null || true

# 2. add (gitignore 적용됨 — 위에서 untrack했으므로 re-add 안 됨)
git add .

# 3. 변경사항 없으면 종료
if git diff --cached --quiet; then
  echo "[git] nothing to commit"
  exit 0
fi

git commit -m "$MSG"
git push
echo "[git] ✅ pushed: $MSG"
