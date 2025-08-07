#!/bin/bash

# Essential Quality Hook - Streamlined from code_quality_enforcer.sh  
# Purpose: Critical code quality enforcement only
# Simplified for Claude Code native integration

set -euo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/quality.log"

# Simple logging function
log_quality() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] QUALITY: $1" >> "$LOG_FILE"
}

# Extract file path from Claude Code parameters
extract_file_path() {
    if [[ -n "${CLAUDE_TOOL_PARAMETER_file_path:-}" ]]; then
        echo "${CLAUDE_TOOL_PARAMETER_file_path}"
    elif [[ -n "${1:-}" ]]; then
        echo "$1" 
    else
        echo ""
    fi
}

# Check if file is Python - EARLY EXIT
is_python_file() {
    local file_path="${1:-}"
    [[ "$file_path" =~ \.py$ ]]
}

# Check file size limits - ESSENTIAL REQUIREMENT
check_file_size_limits() {
    local file_path="$1"
    local line_count
    line_count=$(wc -l < "$file_path" 2>/dev/null || echo "0")
    
    # File size limits per project standards:
    # Test files: 1000 lines max, Implementation files: 750 lines max
    local limit=750
    if [[ "$file_path" =~ (test.*\.py$|.*_test\.py$|tests/.*\.py$) ]]; then
        limit=1000  # Test files get higher limit
    fi
    
    if [[ "$line_count" -gt "$limit" ]]; then
        echo "❌ File size violation: $file_path has $line_count lines (max $limit)"
        return 1
    fi
    
    return 0
}

# Run essential linting - CORE QUALITY GATES
run_essential_linting() {
    local file_path="$1"
    local issues=0
    
    # Essential: ruff check (if available)
    if command -v ruff >/dev/null 2>&1; then
        if ! timeout 15 ruff check "$file_path" >/dev/null 2>&1; then
            echo "⚠️ Ruff linting issues in $file_path"
            ((issues++))
        fi
    fi
    
    # Essential: black formatting (if available)  
    if command -v black >/dev/null 2>&1; then
        if ! timeout 15 black --check --quiet "$file_path" >/dev/null 2>&1; then
            echo "⚠️ Black formatting needed in $file_path"
            ((issues++))
        fi
    fi
    
    return $issues
}

# Main quality enforcement - STREAMLINED
main() {
    local file_path
    file_path=$(extract_file_path "$@")
    
    # Early exit if no file path or not Python
    if [[ -z "$file_path" ]] || ! is_python_file "$file_path"; then
        exit 0
    fi
    
    # Skip if file doesn't exist
    if [[ ! -f "$file_path" ]]; then
        log_quality "File does not exist: $file_path"
        exit 0
    fi
    
    log_quality "Checking: $file_path"
    
    # Essential checks only
    local issues=0
    
    if ! check_file_size_limits "$file_path"; then
        ((issues++))
    fi
    
    if ! run_essential_linting "$file_path"; then
        ((issues++))
    fi
    
    if [[ $issues -eq 0 ]]; then
        log_quality "PASSED: $file_path"
    else
        log_quality "ISSUES: $file_path ($issues violations)"
    fi
    
    # Simple log rotation
    if [[ -f "$LOG_FILE" && $(wc -l < "$LOG_FILE" 2>/dev/null || echo "0") -gt 100 ]]; then
        tail -n 50 "$LOG_FILE" > "${LOG_FILE}.tmp" 2>/dev/null && mv "${LOG_FILE}.tmp" "$LOG_FILE" 2>/dev/null || true
    fi
    
    # Trigger light memory maintenance after quality enforcement
    if [[ "${CLAUDE_MEMORY_MAINTENANCE_ENABLED:-true}" == "true" ]]; then
        local maintenance_script="$PROJECT_ROOT/scripts/memory/auto_maintenance.sh"
        if [[ -f "$maintenance_script" && -x "$maintenance_script" ]]; then
            log_quality "Triggering post-quality memory maintenance"
            timeout 30 bash "$maintenance_script" post-quality >/dev/null 2>&1 || true
        fi
    fi
    
    exit 0
}

main "$@"