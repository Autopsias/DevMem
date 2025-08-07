#!/bin/bash

# Automated Memory Maintenance Script
# Purpose: Streamlined memory maintenance for Claude Code Agent Framework
# Integration: Hooks into quality enforcement and periodic maintenance

set -euo pipefail

# Configuration
readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly MEMORY_DIR="${PROJECT_ROOT}/.claude/memory"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/memory_maintenance.log"
readonly CONFIG_FILE="${PROJECT_ROOT}/.claude/settings.json"
readonly MAINTENANCE_LOCK="${PROJECT_ROOT}/.claude/.maintenance_lock"

# Memory maintenance configuration
readonly MAX_MEMORY_FILES=15
readonly MAX_LOG_SIZE_LINES=500
readonly CLEANUP_OLDER_THAN_DAYS=7
readonly PERFORMANCE_LOG_RETENTION_DAYS=3

# Logging function
log_maintenance() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] MEMORY: $1" >> "$LOG_FILE"
}

# Lock management for concurrent execution prevention
acquire_lock() {
    if [[ -f "$MAINTENANCE_LOCK" ]]; then
        local lock_age
        lock_age=$(($(date +%s) - $(stat -f %m "$MAINTENANCE_LOCK" 2>/dev/null || echo 0)))
        if [[ $lock_age -lt 300 ]]; then  # 5 minutes max lock
            log_maintenance "Maintenance already running, skipping"
            exit 0
        else
            log_maintenance "Stale lock detected, removing"
            rm -f "$MAINTENANCE_LOCK"
        fi
    fi
    echo $$ > "$MAINTENANCE_LOCK"
}

release_lock() {
    rm -f "$MAINTENANCE_LOCK"
}

# Cleanup function to ensure lock is released
cleanup() {
    release_lock
    exit "${1:-0}"
}

trap cleanup EXIT INT TERM

# Memory file consolidation - prevent memory fragmentation
consolidate_memory_files() {
    log_maintenance "Starting memory file consolidation"
    
    # Count current memory files
    local memory_file_count
    memory_file_count=$(find "$MEMORY_DIR" -name "*.md" -type f | wc -l)
    log_maintenance "Found $memory_file_count memory files"
    
    if [[ $memory_file_count -gt $MAX_MEMORY_FILES ]]; then
        log_maintenance "Memory file count exceeds limit ($memory_file_count > $MAX_MEMORY_FILES)"
        
        # Archive old files instead of deleting
        local archive_dir="${MEMORY_DIR}/archive/$(date +%Y%m%d)"
        mkdir -p "$archive_dir"
        
        # Move files older than retention period to archive
        find "$MEMORY_DIR" -name "*.md" -type f -mtime "+$CLEANUP_OLDER_THAN_DAYS" \
            -not -path "*/archive/*" \
            -not -name "agent-coordination-patterns.md" \
            -not -name "*testing-patterns*.md" \
            -not -name "*infrastructure-patterns*.md" \
            -not -name "*security-patterns*.md" \
            -exec mv {} "$archive_dir/" \;
        
        log_maintenance "Archived old memory files to $archive_dir"
    fi
}

# Log rotation and cleanup
rotate_logs() {
    log_maintenance "Starting log rotation"
    
    # Rotate memory maintenance log
    if [[ -f "$LOG_FILE" && $(wc -l < "$LOG_FILE" 2>/dev/null || echo "0") -gt $MAX_LOG_SIZE_LINES ]]; then
        tail -n $((MAX_LOG_SIZE_LINES / 2)) "$LOG_FILE" > "${LOG_FILE}.tmp"
        mv "${LOG_FILE}.tmp" "$LOG_FILE"
        log_maintenance "Rotated maintenance log (kept $((MAX_LOG_SIZE_LINES / 2)) lines)"
    fi
    
    # Rotate quality enforcement log
    local quality_log="${PROJECT_ROOT}/.claude/quality.log"
    if [[ -f "$quality_log" && $(wc -l < "$quality_log" 2>/dev/null || echo "0") -gt $MAX_LOG_SIZE_LINES ]]; then
        tail -n $((MAX_LOG_SIZE_LINES / 2)) "$quality_log" > "${quality_log}.tmp"
        mv "${quality_log}.tmp" "$quality_log"
        log_maintenance "Rotated quality log"
    fi
    
    # Clean old performance logs
    find "${PROJECT_ROOT}/.claude" -name "*.log" -type f -mtime "+$PERFORMANCE_LOG_RETENTION_DAYS" \
        -not -name "memory_maintenance.log" \
        -not -name "quality.log" \
        -delete 2>/dev/null || true
    
    log_maintenance "Log rotation completed"
}

# Memory consistency validation
validate_memory_consistency() {
    log_maintenance "Starting memory consistency validation"
    
    local issues=0
    
    # Check for required memory files
    local required_files=(
        "agent-coordination-patterns.md"
    )
    
    for required_file in "${required_files[@]}"; do
        if [[ ! -f "${MEMORY_DIR}/${required_file}" ]]; then
            log_maintenance "WARNING: Required memory file missing: $required_file"
            ((issues++))
        fi
    done
    
    # Validate domain patterns if they exist
    if [[ -d "${MEMORY_DIR}/domains" ]]; then
        local domain_files=(
            "domains/testing-patterns.md"
            "domains/infrastructure-patterns.md"
            "domains/security-patterns.md"
        )
        
        for domain_file in "${domain_files[@]}"; do
            if [[ -f "${MEMORY_DIR}/${domain_file}" ]]; then
                # Basic validation: check file isn't empty and has proper structure
                if [[ ! -s "${MEMORY_DIR}/${domain_file}" ]]; then
                    log_maintenance "WARNING: Domain pattern file is empty: $domain_file"
                    ((issues++))
                fi
            fi
        done
    fi
    
    if [[ $issues -eq 0 ]]; then
        log_maintenance "Memory consistency validation passed"
    else
        log_maintenance "Memory consistency validation found $issues issues"
    fi
    
    return $issues
}

# Performance optimization
optimize_memory_performance() {
    log_maintenance "Starting memory performance optimization"
    
    # Remove duplicate content in memory files (basic deduplication)
    local processed_files=0
    
    for memory_file in "$MEMORY_DIR"/*.md; do
        if [[ -f "$memory_file" ]]; then
            # Simple deduplication: remove consecutive duplicate lines
            awk '!seen[$0]++' "$memory_file" > "${memory_file}.tmp" && \
            mv "${memory_file}.tmp" "$memory_file"
            ((processed_files++))
        fi
    done
    
    log_maintenance "Optimized $processed_files memory files"
}

# Memory health monitoring
monitor_memory_health() {
    log_maintenance "Starting memory health monitoring"
    
    # Calculate memory usage statistics
    local total_memory_size
    total_memory_size=$(find "$MEMORY_DIR" -name "*.md" -type f -exec wc -c {} + 2>/dev/null | tail -n1 | awk '{print $1}' || echo "0")
    
    local file_count
    file_count=$(find "$MEMORY_DIR" -name "*.md" -type f | wc -l)
    
    local avg_file_size=0
    if [[ $file_count -gt 0 ]]; then
        avg_file_size=$((total_memory_size / file_count))
    fi
    
    log_maintenance "Memory health: $file_count files, ${total_memory_size} bytes total, ${avg_file_size} bytes average"
    
    # Alert if memory usage is excessive
    local max_total_size=$((1024 * 1024))  # 1MB limit for memory files
    if [[ $total_memory_size -gt $max_total_size ]]; then
        log_maintenance "WARNING: Memory usage excessive (${total_memory_size} > ${max_total_size} bytes)"
        return 1
    fi
    
    return 0
}

# Configuration validation
validate_configuration() {
    log_maintenance "Validating memory configuration"
    
    # Check if settings.json has proper memory configuration
    if [[ -f "$CONFIG_FILE" ]]; then
        if ! python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
            log_maintenance "ERROR: Invalid JSON in settings.json"
            return 1
        fi
        
        # Check for required memory configuration sections
        local required_sections=("agents" "memory_hierarchy")
        for section in "${required_sections[@]}"; do
            if ! python3 -c "import json; config=json.load(open('$CONFIG_FILE')); exit(0 if '$section' in config.get('agents', {}) else 1)" 2>/dev/null; then
                log_maintenance "WARNING: Missing configuration section: agents.$section"
            fi
        done
    else
        log_maintenance "WARNING: Configuration file not found: $CONFIG_FILE"
    fi
}

# Main maintenance function
run_maintenance() {
    local maintenance_type="${1:-full}"
    
    log_maintenance "Starting maintenance: $maintenance_type"
    
    case "$maintenance_type" in
        "post-quality")
            # Light maintenance after quality enforcement
            rotate_logs
            ;;
        "periodic")
            # Regular periodic maintenance
            consolidate_memory_files
            rotate_logs
            validate_memory_consistency
            optimize_memory_performance
            ;;
        "full"|*)
            # Full maintenance cycle
            consolidate_memory_files
            rotate_logs
            validate_memory_consistency
            optimize_memory_performance
            monitor_memory_health
            validate_configuration
            ;;
    esac
    
    log_maintenance "Maintenance completed: $maintenance_type"
}

# Main execution
main() {
    local maintenance_type="${1:-full}"
    
    # Skip maintenance in certain conditions
    if [[ "${CLAUDE_MEMORY_MAINTENANCE_ENABLED:-true}" != "true" ]]; then
        log_maintenance "Memory maintenance disabled, skipping"
        exit 0
    fi
    
    # Acquire lock to prevent concurrent execution
    acquire_lock
    
    # Run the requested maintenance
    run_maintenance "$maintenance_type"
    
    log_maintenance "Memory maintenance session completed successfully"
}

# Execute main function with all arguments
main "$@"