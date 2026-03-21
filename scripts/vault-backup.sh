#!/usr/bin/env bash
# vault-backup.sh — git-based vault sync
# Usage: bash scripts/vault-backup.sh
set -euo pipefail

sync_vault() {
    local path="$1"
    local name="$2"

    if [ ! -d "$path/.git" ]; then
        echo "[$name] git not initialized — skip"
        return 1
    fi

    cd "$path"

    # 1. Pull remote changes first
    git pull origin main --rebase --quiet 2>&1 && echo "[$name] pull ✅" || echo "[$name] pull conflict — attempting push only"

    # 2. Check for changes
    if git diff --quiet HEAD 2>/dev/null && [ -z "$(git ls-files --others --exclude-standard)" ]; then
        echo "[$name] no changes — skip push"
        return 0
    fi

    # 3. Commit & push
    git add -A
    git commit -m "auto: backup $(date +%Y-%m-%d)"
    git push origin main 2>&1
    echo "[$name] push ✅"
}

echo "=== Vault Sync $(date '+%Y-%m-%d %H:%M') ==="

VAULT_1="${OBSIDIAN_VAULT:-$HOME/vaults/obsidian}"
VAULT_2="${WORKSPACE_VAULT:-$HOME/vaults/workspace}"

if [ ! -d "$VAULT_1" ] && [ ! -d "$VAULT_2" ]; then
    echo "❌ No vault directories found"
    exit 1
fi

[ -d "$VAULT_1" ] && sync_vault "$VAULT_1" "Vault-1"
[ -d "$VAULT_2" ] && sync_vault "$VAULT_2" "Vault-2"

echo "=== Done ==="
