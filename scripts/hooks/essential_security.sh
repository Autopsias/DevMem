#!/bin/bash

# Essential Security & Validation Framework - Consolidated
# Purpose: Critical security validation, memory validation, system health security
# Consolidates: bash_security.sh, validate_memory.sh, system_health.sh security components
# Simplified for Claude Code native integration

set -euo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/security.log"
readonly MEMORY_DIR="${PROJECT_ROOT}/.claude/memory"
readonly CONFIG_FILE="${PROJECT_ROOT}/.claude/settings.json"

# Security thresholds
readonly MAX_MEMORY_SIZE_MB=5
readonly MAX_LOG_SIZE_LINES=500

# Enhanced logging function
log_security() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SECURITY: $1" >> "$LOG_FILE"
}

# Memory security validation - consolidated from validate_memory.sh
validate_memory_security() {
    if [[ ! -d "$MEMORY_DIR" ]]; then
        log_security "Memory directory missing: $MEMORY_DIR"
        return 1
    fi
    
    # Check memory size limits
    local total_size_mb=0
    if command -v du >/dev/null 2>&1; then
        total_size_mb=$(du -sm "$MEMORY_DIR" 2>/dev/null | cut -f1 || echo "0")
    fi
    
    if [[ "$total_size_mb" -gt "$MAX_MEMORY_SIZE_MB" ]]; then
        log_security "Memory size exceeded: ${total_size_mb}MB > ${MAX_MEMORY_SIZE_MB}MB"
        return 1
    fi
    
    # Validate memory file permissions
    find "$MEMORY_DIR" -type f -name "*.md" | while read -r file; do
        if [[ ! -r "$file" ]]; then
            log_security "Memory file not readable: $file"
            return 1
        fi
    done
    
    log_security "Memory security validation passed"
    return 0
}

# System health security check - consolidated from system_health.sh
validate_system_security() {
    # Check configuration file security
    if [[ -f "$CONFIG_FILE" ]]; then
        local permissions
        permissions=$(stat -f "%OLp" "$CONFIG_FILE" 2>/dev/null || echo "644")
        if [[ "$permissions" != "644" && "$permissions" != "600" ]]; then
            log_security "Insecure config permissions: $CONFIG_FILE ($permissions)"
            return 1
        fi
    fi
    
    # Check log file security
    if [[ -f "$LOG_FILE" ]]; then
        local log_lines
        log_lines=$(wc -l < "$LOG_FILE" 2>/dev/null || echo "0")
        if [[ "$log_lines" -gt "$MAX_LOG_SIZE_LINES" ]]; then
            log_security "Log file too large: $log_lines lines > $MAX_LOG_SIZE_LINES"
            # Auto-rotate for security
            tail -n $(( MAX_LOG_SIZE_LINES / 2 )) "$LOG_FILE" > "${LOG_FILE}.tmp" 2>/dev/null && mv "${LOG_FILE}.tmp" "$LOG_FILE" 2>/dev/null || true
        fi
    fi
    
    log_security "System security validation passed"
    return 0
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

# Comprehensive security validation - CONSOLIDATED
main() {
    local mode="${1:-command}"
    
    case "$mode" in
        "command")
            validate_bash_command "${@:2}"
            ;;
        "memory")
            validate_memory_security
            ;;
        "system")
            validate_system_security
            ;;
        "full")
            validate_bash_command "${@:2}"
            validate_memory_security
            validate_system_security
            ;;
        *)
            validate_bash_command "$@"
            ;;
    esac
    
    # Enhanced log rotation
    if [[ -f "$LOG_FILE" && $(wc -l < "$LOG_FILE" 2>/dev/null || echo "0") -gt 200 ]]; then
        tail -n 100 "$LOG_FILE" > "${LOG_FILE}.tmp" 2>/dev/null && mv "${LOG_FILE}.tmp" "$LOG_FILE" 2>/dev/null || true
    fi
    
    exit 0
}

main "$@"