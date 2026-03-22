#!/usr/bin/env bash
# vault-backup.sh — git-based vault sync
# Usage: bash scripts/vault-backup.sh
#
# Supports both local-only vaults (no remote) and remote-backed vaults.
# Set VAULT_PATH (or VAULT) to override the default path.

set -euo pipefail

VAULT="${VAULT_PATH:-${VAULT:-$HOME/vaults/my-workspace}}"

sync_vault() {
    local path="$1"
    local name="$2"

    if [ ! -d "$path/.git" ]; then
        echo "[$name] git not initialized — skip"
        return 1
    fi

    cd "$path"

    has_remote=false
    if git remote get-url origin >/dev/null 2>&1; then
        has_remote=true
    fi

    # 1. Pull remote changes first (only if remote exists)
    if $has_remote; then
        git pull origin main --rebase --quiet 2>&1 && echo "[$name] pull ✅" || echo "[$name] pull conflict — attempting local commit only"
    fi

    # 2. Check for changes
    if git diff --quiet HEAD 2>/dev/null && [ -z "$(git ls-files --others --exclude-standard)" ]; then
        echo "[$name] no changes — skip"
        return 0
    fi

    # 3. Commit & push (or commit only)
    git add -A
    git commit -m "auto: backup $(date +%Y-%m-%d)"

    if $has_remote; then
        git push origin main 2>&1 && echo "[$name] push ✅" || echo "[$name] ⚠️ push failed — committed locally"
    else
        echo "[$name] ✅ committed locally (no remote configured)"
    fi
}

echo "=== Vault Sync $(date '+%Y-%m-%d %H:%M') ==="

if [ ! -d "$VAULT" ]; then
    echo "❌ Vault directory not found: $VAULT"
    echo "Set VAULT_PATH env var or update the default path in this script."
    exit 1
fi

sync_vault "$VAULT" "vault"

echo "=== Done ==="
