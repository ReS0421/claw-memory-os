#!/bin/bash
# Claude ACP wrapper - HOME을 Windows 사용자 경로로 오버라이드
# Claude Code 인증 파일이 Windows 경로에 있어서 필요
export HOME="${ACP_HOME:-$HOME}"
exec "${CLAUDE_ACP_BIN:-claude-agent-acp}" "$@"
