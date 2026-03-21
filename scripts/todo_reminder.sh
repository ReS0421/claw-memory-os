#!/bin/bash
# TODO 미완료 항목 Discord #obsidian-and-notion 채널로 알림

TODO_FILE="${TODO_FILE:-$HOME/vaults/obsidian/Areas/TODO.md}"

# vault 마운트 확인
if [ ! -f "$TODO_FILE" ]; then
  echo "TODO 파일 없음 or vault 미마운트" >&2
  exit 1
fi

# 미완료 항목 추출
ITEMS=$(grep "^- \[ \]" "$TODO_FILE" | sed 's/^- \[ \] /• /')
COUNT=$(echo "$ITEMS" | wc -l)

MESSAGE="📋 **TODO 미완료 항목 (${COUNT}개)**

$ITEMS


echo "$MESSAGE"
