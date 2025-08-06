#!/bin/bash

# Essential Security Hook - Streamlined from bash_security.sh
# Purpose: Critical bash command security validation only
# Simplified for Claude Code native integration

set -euo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/security.log"

# Simple logging function
log_security() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SECURITY: $1" >> "$LOG_FILE"
}

# Validate bash command security - ESSENTIAL ONLY
validate_bash_command() {
    local command="${CLAUDE_TOOL_PARAMETER_command:-${1:-}}"

    if [[ -z "$command" ]]; then
        return 0
    fi

    # CRITICAL: Block dangerous system commands
    # Pattern matches: rm -rf /, format, del /, rmdir /, sudo rm -rf
    if [[ "$command" =~ (rm[[:space:]]+-rf[[:space:]]+/|format[[:space:]]+|del[[:space:]]+/|rmdir[[:space:]]+/|sudo[[:space:]]+rm[[:space:]]+-rf) ]]; then
        log_security "BLOCKED: Dangerous command: $command"
        echo "🚨 BLOCKED: Dangerous system command detected"
        echo "  Command: $command"
        exit 1  # Block execution
    fi

    # CRITICAL: Validate privileged operations 
    if [[ "$command" =~ (sudo[[:space:]]+|chmod[[:space:]]+777|chown[[:space:]]+-R) ]]; then
        log_security "PRIVILEGED: $command"
        echo "⚠️ Privileged operation detected: Verify necessity"
        # Don't block, just alert
    fi

    log_security "VALIDATED: $command"
    return 0
}

# Main security handler - STREAMLINED
main() {
    validate_bash_command "$@"
    
    # Simple log rotation
    if [[ -f "$LOG_FILE" && $(wc -l < "$LOG_FILE" 2>/dev/null || echo "0") -gt 100 ]]; then
        tail -n 50 "$LOG_FILE" > "${LOG_FILE}.tmp" 2>/dev/null && mv "${LOG_FILE}.tmp" "$LOG_FILE" 2>/dev/null || true
    fi
    
    exit 0
}

main "$@"