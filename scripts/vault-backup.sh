#!/usr/bin/env bash
# vault-backup.sh — Obsidian + workspace vault 자동 git sync
# 경로: ~/vaults/ (git 기반, SMB 독립)
set -euo pipefail

sync_vault() {
    local path="$1"
    local name="$2"

    if [ ! -d "$path/.git" ]; then
        echo "[$name] git 미초기화 — skip"
        return 1
    fi

    cd "$path"

    # 1. 원격 최신 반영 (pull first)
    git pull origin main --rebase --quiet 2>&1 && echo "[$name] pull ✅" || echo "[$name] pull 충돌 — push만 시도"

    # 2. 변경사항 확인
    if git diff --quiet HEAD 2>/dev/null && [ -z "$(git ls-files --others --exclude-standard)" ]; then
        echo "[$name] 변경 없음 — skip push"
        return 0
    fi

    # 3. commit & push
    git add -A
    git commit -m "auto: backup $(date +%Y-%m-%d)"
    git push origin main 2>&1
    echo "[$name] push ✅"
}

echo "=== Vault Sync $(date '+%Y-%m-%d %H:%M') ==="

if [ ! -d "${OBSIDIAN_VAULT:-$HOME/vaults/obsidian}" ] || [ ! -d "${WORKSPACE_VAULT:-$HOME/vaults/workspace}" ]; then
    echo "❌ ~/vaults/ 경로 없음"
    exit 1
fi

sync_vault "${OBSIDIAN_VAULT:-$HOME/vaults/obsidian}" "Obsidian"
sync_vault "${WORKSPACE_VAULT:-$HOME/vaults/workspace}" "Workspace-vault"

echo "=== 완료 ==="
