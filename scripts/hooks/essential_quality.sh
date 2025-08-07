#!/bin/bash

# Essential Quality & Memory Management Framework - Consolidated
# Purpose: Critical quality enforcement, memory management, system health, troubleshooting
# Consolidates: code_quality_enforcer.sh, memory_manager.sh, system_health.sh, auto_maintenance.sh
# Simplified for Claude Code native integration

set -euo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/quality.log"
readonly MEMORY_DIR="${PROJECT_ROOT}/.claude/memory"
readonly MAINTENANCE_LOG="${PROJECT_ROOT}/.claude/maintenance.log"
readonly HEALTH_LOG="${PROJECT_ROOT}/.claude/system_health.log"

# Quality and memory thresholds
readonly MAX_MEMORY_FILES=50
readonly MAX_FILE_SIZE_KB=100
readonly HEALTH_CHECK_INTERVAL_HOURS=24

# Enhanced logging functions
log_quality() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] QUALITY: $1" >> "$LOG_FILE"
}

log_maintenance() {
    mkdir -p "$(dirname "$MAINTENANCE_LOG")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] MAINT: $1" >> "$MAINTENANCE_LOG"
}

log_health() {
    mkdir -p "$(dirname "$HEALTH_LOG")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] HEALTH: $1" >> "$HEALTH_LOG"
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

# Memory management - consolidated from memory_manager.sh and auto_maintenance.sh
run_memory_maintenance() {
    local trigger="${1:-manual}"
    log_maintenance "Starting memory maintenance: $trigger"
    
    # Memory cleanup - remove empty files and old logs
    if [[ -d "$MEMORY_DIR" ]]; then
        find "$MEMORY_DIR" -type f -empty -delete 2>/dev/null || true
        find "$MEMORY_DIR" -name "*.tmp" -mtime +1 -delete 2>/dev/null || true
    fi
    
    # Memory size validation
    local memory_file_count=0
    if [[ -d "$MEMORY_DIR" ]]; then
        memory_file_count=$(find "$MEMORY_DIR" -type f -name "*.md" | wc -l)
    fi
    
    if [[ "$memory_file_count" -gt "$MAX_MEMORY_FILES" ]]; then
        log_maintenance "Memory file count warning: $memory_file_count > $MAX_MEMORY_FILES"
    fi
    
    # Log rotation for all logs
    rotate_logs
    
    log_maintenance "Memory maintenance completed: $trigger"
}

# System health check - consolidated from system_health.sh
run_system_health_check() {
    log_health "Starting system health check"
    
    local health_score=100
    
    # Check memory health
    if [[ -d "$MEMORY_DIR" ]]; then
        local memory_size_mb
        memory_size_mb=$(du -sm "$MEMORY_DIR" 2>/dev/null | cut -f1 || echo "0")
        if [[ "$memory_size_mb" -gt 3 ]]; then
            ((health_score-=20))
            log_health "Memory size warning: ${memory_size_mb}MB"
        fi
    else
        ((health_score-=30))
        log_health "Memory directory missing"
    fi
    
    # Check log health
    for log_file in "$LOG_FILE" "$MAINTENANCE_LOG" "$HEALTH_LOG"; do
        if [[ -f "$log_file" ]]; then
            local log_lines
            log_lines=$(wc -l < "$log_file" 2>/dev/null || echo "0")
            if [[ "$log_lines" -gt 200 ]]; then
                ((health_score-=10))
                log_health "Large log file: $log_file ($log_lines lines)"
            fi
        fi
    done
    
    # Check configuration
    if [[ ! -f "$PROJECT_ROOT/.claude/settings.json" ]]; then
        ((health_score-=15))
        log_health "Missing configuration file"
    fi
    
    log_health "System health score: $health_score/100"
    
    if [[ "$health_score" -lt 70 ]]; then
        echo "⚠️ System health warning: $health_score/100"
        return 1
    fi
    
    return 0
}

# Log rotation - consolidated functionality
rotate_logs() {
    for log_file in "$LOG_FILE" "$MAINTENANCE_LOG" "$HEALTH_LOG"; do
        if [[ -f "$log_file" && $(wc -l < "$log_file" 2>/dev/null || echo "0") -gt 200 ]]; then
            tail -n 100 "$log_file" > "${log_file}.tmp" 2>/dev/null && mv "${log_file}.tmp" "$log_file" 2>/dev/null || true
        fi
    done
}

# Troubleshooting and diagnostics - consolidated from collect_diagnostics.sh
run_diagnostics() {
    local output_file="${1:-$PROJECT_ROOT/.claude/diagnostics_$(date +%Y%m%d_%H%M%S).txt}"
    
    {
        echo "=== Claude Code Framework Diagnostics ==="
        echo "Generated: $(date)"
        echo ""
        
        echo "=== System Health ==="
        run_system_health_check 2>&1 || true
        echo ""
        
        echo "=== Memory Status ==="
        if [[ -d "$MEMORY_DIR" ]]; then
            echo "Memory directory: $MEMORY_DIR"
            echo "Memory files: $(find "$MEMORY_DIR" -type f -name "*.md" | wc -l)"
            echo "Memory size: $(du -sh "$MEMORY_DIR" 2>/dev/null || echo "0B")"
        else
            echo "Memory directory missing: $MEMORY_DIR"
        fi
        echo ""
        
        echo "=== Recent Quality Log ==="
        if [[ -f "$LOG_FILE" ]]; then
            tail -n 20 "$LOG_FILE" 2>/dev/null || echo "No quality log entries"
        else
            echo "Quality log missing: $LOG_FILE"
        fi
        echo ""
        
        echo "=== Configuration Status ==="
        if [[ -f "$PROJECT_ROOT/.claude/settings.json" ]]; then
            echo "Configuration exists: $PROJECT_ROOT/.claude/settings.json"
        else
            echo "Configuration missing: $PROJECT_ROOT/.claude/settings.json"
        fi
        
    } > "$output_file"
    
    log_quality "Diagnostics collected: $output_file"
    echo "Diagnostics saved to: $output_file"
}

# Quality check function (renamed from original main)
run_quality_check() {
    local file_path
    file_path=$(extract_file_path "$@")
    
    # Early exit if no file path or not Python
    if [[ -z "$file_path" ]] || ! is_python_file "$file_path"; then
        return 0
    fi
    
    # Skip if file doesn't exist
    if [[ ! -f "$file_path" ]]; then
        log_quality "File does not exist: $file_path"
        return 0
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
    
    # Integrated memory maintenance - consolidated from auto_maintenance.sh
    if [[ "${CLAUDE_MEMORY_MAINTENANCE_ENABLED:-true}" == "true" ]]; then
        run_memory_maintenance "post-quality"
    fi
}

# Main quality and maintenance handler - CONSOLIDATED
main() {
    local mode="${1:-quality}"
    
    case "$mode" in
        "quality")
            run_quality_check "${@:2}"
            ;;
        "maintenance")
            run_memory_maintenance "${2:-manual}"
            ;;
        "health")
            run_system_health_check
            ;;
        "diagnostics")
            run_diagnostics "${2:-}"
            ;;
        "full")
            run_quality_check "${@:2}"
            run_memory_maintenance "full-check"
            run_system_health_check
            ;;
        *)
            run_quality_check "$@"
            ;;
    esac
    
    exit 0
}

main "$@"