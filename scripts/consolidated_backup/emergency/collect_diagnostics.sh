#!/bin/bash

# Emergency Diagnostics Collection Script
# Purpose: Collect comprehensive diagnostic information during emergencies
# Usage: ./collect_diagnostics.sh [--output-dir=/path/to/output]

set -euo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly TIMESTAMP=$(date +%Y%m%d_%H%M%S)
readonly DEFAULT_OUTPUT_DIR="${PROJECT_ROOT}/.claude/diagnostics_${TIMESTAMP}"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/emergency_diagnostics.log"

# Parse command line arguments
OUTPUT_DIR="$DEFAULT_OUTPUT_DIR"
while [[ $# -gt 0 ]]; do
    case $1 in
        --output-dir=*)
            OUTPUT_DIR="${1#*=}"
            shift
            ;;
        --help)
            echo "Emergency Diagnostics Collection"
            echo "Usage: $0 [--output-dir=/path/to/output]"
            echo "Collects comprehensive diagnostic information for troubleshooting."
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Logging function
log_emergency() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] EMERGENCY: $1" >> "$LOG_FILE"
    echo "=¨ $1"
}

# Create output directory
create_output_dir() {
    mkdir -p "$OUTPUT_DIR"
    log_emergency "Created diagnostics directory: $OUTPUT_DIR"
}

# Collect system information
collect_system_info() {
    log_emergency "Collecting system information..."
    
    cat > "$OUTPUT_DIR/system_info.txt" << EOF
=== System Information ===
Generated: $(date)
Host: $(hostname)
OS: $(uname -a)
User: $(whoami)
Working Directory: $(pwd)
Project Root: $PROJECT_ROOT

=== Environment Variables ===
$(env | grep CLAUDE | sort)

=== Disk Usage ===
$(df -h "$PROJECT_ROOT")

=== Directory Structure ===
$(find "$PROJECT_ROOT" -type d -name ".claude" -o -name "scripts" -o -name "docs" | head -20)

=== Process Information ===
$(ps aux | grep -E "(python|claude|bash)" | grep -v grep || echo "No relevant processes found")
EOF

    log_emergency "System information collected"
}

# Collect configuration files
collect_config_files() {
    log_emergency "Collecting configuration files..."
    
    mkdir -p "$OUTPUT_DIR/config"
    
    # Claude Code settings
    if [[ -f "$PROJECT_ROOT/.claude/settings.json" ]]; then
        cp "$PROJECT_ROOT/.claude/settings.json" "$OUTPUT_DIR/config/" 2>/dev/null || true
    fi
    
    # Essential hooks
    if [[ -d "$PROJECT_ROOT/scripts/hooks" ]]; then
        cp -r "$PROJECT_ROOT/scripts/hooks" "$OUTPUT_DIR/config/" 2>/dev/null || true
    fi
    
    # Project configuration files
    for config_file in "Makefile" "pyproject.toml" "requirements.txt" "CLAUDE.md" ".gitignore"; do
        if [[ -f "$PROJECT_ROOT/$config_file" ]]; then
            cp "$PROJECT_ROOT/$config_file" "$OUTPUT_DIR/config/" 2>/dev/null || true
        fi
    done
    
    log_emergency "Configuration files collected"
}

# Collect recent logs
collect_logs() {
    log_emergency "Collecting recent logs..."
    
    mkdir -p "$OUTPUT_DIR/logs"
    
    # Essential log files
    local log_files=(
        ".claude/security.log"
        ".claude/quality.log"
        ".claude/memory_maintenance.log"
        ".claude/system_health.log"
        ".claude/bash_security.log"
        ".claude/code_quality_enforcement.log"
    )
    
    for log_file in "${log_files[@]}"; do
        if [[ -f "$PROJECT_ROOT/$log_file" ]]; then
            # Copy last 500 lines of each log
            tail -n 500 "$PROJECT_ROOT/$log_file" > "$OUTPUT_DIR/logs/$(basename "$log_file")" 2>/dev/null || true
        fi
    done
    
    # Create log summary
    cat > "$OUTPUT_DIR/logs/log_summary.txt" << EOF
=== Log Summary ===
Generated: $(date)

EOF
    
    for log_file in "${log_files[@]}"; do
        if [[ -f "$PROJECT_ROOT/$log_file" ]]; then
            local line_count=$(wc -l < "$PROJECT_ROOT/$log_file" 2>/dev/null || echo "0")
            local file_size=$(du -h "$PROJECT_ROOT/$log_file" 2>/dev/null | cut -f1 || echo "0")
            local last_modified=$(stat -f "%Sm" "$PROJECT_ROOT/$log_file" 2>/dev/null || echo "unknown")
            
            echo "$log_file: $line_count lines, $file_size, modified: $last_modified" >> "$OUTPUT_DIR/logs/log_summary.txt"
        else
            echo "$log_file: NOT FOUND" >> "$OUTPUT_DIR/logs/log_summary.txt"
        fi
    done
    
    log_emergency "Recent logs collected"
}

# Collect memory system status
collect_memory_status() {
    log_emergency "Collecting memory system status..."
    
    mkdir -p "$OUTPUT_DIR/memory"
    
    # Memory directory structure
    if [[ -d "$PROJECT_ROOT/.claude/memory" ]]; then
        find "$PROJECT_ROOT/.claude/memory" -type f -name "*.md" | head -20 > "$OUTPUT_DIR/memory/memory_files.txt"
        du -sh "$PROJECT_ROOT/.claude/memory" > "$OUTPUT_DIR/memory/memory_usage.txt" 2>/dev/null || echo "Unable to calculate memory usage" > "$OUTPUT_DIR/memory/memory_usage.txt"
    else
        echo "Memory directory not found" > "$OUTPUT_DIR/memory/memory_status.txt"
    fi
    
    # Run memory validation if available
    if [[ -x "$PROJECT_ROOT/scripts/memory/validate_memory.sh" ]]; then
        timeout 30 "$PROJECT_ROOT/scripts/memory/validate_memory.sh" > "$OUTPUT_DIR/memory/memory_validation.txt" 2>&1 || echo "Memory validation timed out or failed" > "$OUTPUT_DIR/memory/memory_validation.txt"
    fi
    
    log_emergency "Memory system status collected"
}

# Run health checks
collect_health_status() {
    log_emergency "Running health checks..."
    
    mkdir -p "$OUTPUT_DIR/health"
    
    # System health check
    if [[ -x "$PROJECT_ROOT/scripts/system/system_health.sh" ]]; then
        timeout 30 "$PROJECT_ROOT/scripts/system/system_health.sh" --detailed > "$OUTPUT_DIR/health/system_health.txt" 2>&1 || echo "System health check failed or timed out" > "$OUTPUT_DIR/health/system_health.txt"
        timeout 30 "$PROJECT_ROOT/scripts/system/system_health.sh" --json > "$OUTPUT_DIR/health/system_health.json" 2>&1 || echo "{\"error\": \"Health check failed\"}" > "$OUTPUT_DIR/health/system_health.json"
    fi
    
    # Memory status
    if command -v make >/dev/null 2>&1 && [[ -f "$PROJECT_ROOT/Makefile" ]]; then
        timeout 30 make memory-status > "$OUTPUT_DIR/health/memory_status.txt" 2>&1 || echo "Memory status check failed" > "$OUTPUT_DIR/health/memory_status.txt"
    fi
    
    log_emergency "Health checks completed"
}

# Collect security status
collect_security_status() {
    log_emergency "Collecting security status..."
    
    mkdir -p "$OUTPUT_DIR/security"
    
    # Check essential hooks
    cat > "$OUTPUT_DIR/security/hook_status.txt" << EOF
=== Essential Hook Status ===
Generated: $(date)

Security Hook:
EOF
    
    if [[ -f "$PROJECT_ROOT/scripts/hooks/essential_security.sh" ]]; then
        if [[ -x "$PROJECT_ROOT/scripts/hooks/essential_security.sh" ]]; then
            echo " Present and executable" >> "$OUTPUT_DIR/security/hook_status.txt"
        else
            echo "  Present but not executable" >> "$OUTPUT_DIR/security/hook_status.txt"
        fi
    else
        echo "L Missing" >> "$OUTPUT_DIR/security/hook_status.txt"
    fi
    
    echo "" >> "$OUTPUT_DIR/security/hook_status.txt"
    echo "Quality Hook:" >> "$OUTPUT_DIR/security/hook_status.txt"
    
    if [[ -f "$PROJECT_ROOT/scripts/hooks/essential_quality.sh" ]]; then
        if [[ -x "$PROJECT_ROOT/scripts/hooks/essential_quality.sh" ]]; then
            echo " Present and executable" >> "$OUTPUT_DIR/security/hook_status.txt"
        else
            echo "  Present but not executable" >> "$OUTPUT_DIR/security/hook_status.txt"
        fi
    else
        echo "L Missing" >> "$OUTPUT_DIR/security/hook_status.txt"
    fi
    
    # Recent security events
    if [[ -f "$PROJECT_ROOT/.claude/security.log" ]]; then
        echo "=== Recent Security Events ===" > "$OUTPUT_DIR/security/recent_events.txt"
        grep -E "BLOCKED|DANGEROUS|SECURITY|ERROR" "$PROJECT_ROOT/.claude/security.log" | tail -n 20 >> "$OUTPUT_DIR/security/recent_events.txt" 2>/dev/null || echo "No recent security events found" >> "$OUTPUT_DIR/security/recent_events.txt"
    fi
    
    # File permissions check
    echo "=== Critical File Permissions ===" > "$OUTPUT_DIR/security/permissions.txt"
    echo ".claude directory: $(ls -ld "$PROJECT_ROOT/.claude" 2>/dev/null || echo "NOT FOUND")" >> "$OUTPUT_DIR/security/permissions.txt"
    echo "settings.json: $(ls -l "$PROJECT_ROOT/.claude/settings.json" 2>/dev/null || echo "NOT FOUND")" >> "$OUTPUT_DIR/security/permissions.txt"
    echo "essential_security.sh: $(ls -l "$PROJECT_ROOT/scripts/hooks/essential_security.sh" 2>/dev/null || echo "NOT FOUND")" >> "$OUTPUT_DIR/security/permissions.txt"
    echo "essential_quality.sh: $(ls -l "$PROJECT_ROOT/scripts/hooks/essential_quality.sh" 2>/dev/null || echo "NOT FOUND")" >> "$OUTPUT_DIR/security/permissions.txt"
    
    log_emergency "Security status collected"
}

# Collect performance metrics
collect_performance_metrics() {
    log_emergency "Collecting performance metrics..."
    
    mkdir -p "$OUTPUT_DIR/performance"
    
    # System resource usage
    cat > "$OUTPUT_DIR/performance/system_resources.txt" << EOF
=== System Resource Usage ===
Generated: $(date)

Memory Usage:
$(ps aux --sort=-%mem | head -10)

CPU Usage:
$(ps aux --sort=-%cpu | head -10)

Disk Space:
$(df -h)

Load Average:
$(uptime)
EOF
    
    # Performance log files
    if [[ -d "$PROJECT_ROOT/.claude/performance_results" ]]; then
        cp -r "$PROJECT_ROOT/.claude/performance_results" "$OUTPUT_DIR/performance/" 2>/dev/null || true
    fi
    
    log_emergency "Performance metrics collected"
}

# Create diagnostic summary
create_diagnostic_summary() {
    log_emergency "Creating diagnostic summary..."
    
    cat > "$OUTPUT_DIR/DIAGNOSTIC_SUMMARY.md" << EOF
# Emergency Diagnostic Report

**Generated:** $(date)
**Location:** \`$OUTPUT_DIR\`
**Project:** $(basename "$PROJECT_ROOT")

## Quick Assessment

### System Status
- **Host:** $(hostname)
- **User:** $(whoami)
- **OS:** $(uname -s)
- **Project Root:** $PROJECT_ROOT

### Critical Files Status
- **Settings.json:** $([ -f "$PROJECT_ROOT/.claude/settings.json" ] && echo " Present" || echo "L Missing")
- **Security Hook:** $([ -x "$PROJECT_ROOT/scripts/hooks/essential_security.sh" ] && echo " Present & Executable" || echo "L Missing or Not Executable")
- **Quality Hook:** $([ -x "$PROJECT_ROOT/scripts/hooks/essential_quality.sh" ] && echo " Present & Executable" || echo "L Missing or Not Executable")
- **Memory Directory:** $([ -d "$PROJECT_ROOT/.claude/memory" ] && echo " Present" || echo "L Missing")

### Recent Activity
- **Last Security Log Entry:** $([ -f "$PROJECT_ROOT/.claude/security.log" ] && tail -n 1 "$PROJECT_ROOT/.claude/security.log" | cut -d' ' -f1-2 || echo "No security log")
- **Last Quality Log Entry:** $([ -f "$PROJECT_ROOT/.claude/quality.log" ] && tail -n 1 "$PROJECT_ROOT/.claude/quality.log" | cut -d' ' -f1-2 || echo "No quality log")

## Collected Information

### =Á Directories
- \`config/\` - Configuration files and settings
- \`logs/\` - Recent log files (last 500 lines each)
- \`memory/\` - Memory system status and validation
- \`health/\` - System health check results
- \`security/\` - Security status and recent events
- \`performance/\` - Performance metrics and resource usage

### =Ë Key Files
- \`system_info.txt\` - Comprehensive system information
- \`DIAGNOSTIC_SUMMARY.md\` - This summary (you are here)

## Recommended Next Steps

1. **Review Health Status:** Check \`health/system_health.txt\` for overall system status
2. **Check Recent Logs:** Review files in \`logs/\` directory for recent errors
3. **Validate Configuration:** Examine \`config/settings.json\` for configuration issues
4. **Security Assessment:** Review \`security/\` directory for security concerns
5. **Performance Analysis:** Check \`performance/\` directory for resource issues

## Emergency Contacts

If this is a critical issue:
1. Check the troubleshooting guide: \`docs/MAINTENANCE.md\`
2. Run emergency recovery procedures if needed
3. Document any actions taken for post-incident review

---
*This diagnostic report was automatically generated by the emergency diagnostics system.*
EOF

    log_emergency "Diagnostic summary created"
}

# Main diagnostic collection function
main() {
    echo
    echo "=¨ Emergency Diagnostic Collection Started"
    echo "=========================================="
    echo "Timestamp: $(date)"
    echo "Output Directory: $OUTPUT_DIR"
    echo
    
    log_emergency "Emergency diagnostic collection started"
    
    # Create output directory
    create_output_dir
    
    # Collect all diagnostic information
    collect_system_info
    collect_config_files
    collect_logs
    collect_memory_status
    collect_health_status
    collect_security_status
    collect_performance_metrics
    
    # Create summary
    create_diagnostic_summary
    
    # Create archive
    local archive_name="${PROJECT_ROOT}/.claude/diagnostics_${TIMESTAMP}.tar.gz"
    if command -v tar >/dev/null 2>&1; then
        tar -czf "$archive_name" -C "$(dirname "$OUTPUT_DIR")" "$(basename "$OUTPUT_DIR")" 2>/dev/null || {
            log_emergency "Failed to create archive, but diagnostics collected in: $OUTPUT_DIR"
        }
        
        if [[ -f "$archive_name" ]]; then
            log_emergency "Diagnostics archived: $archive_name"
            echo
            echo " Diagnostic collection completed successfully"
            echo "=æ Archive: $archive_name"
            echo "=Á Directory: $OUTPUT_DIR"
        else
            echo "  Archive creation failed, but diagnostics available in: $OUTPUT_DIR"
        fi
    else
        echo "  tar not available, diagnostics collected in: $OUTPUT_DIR"
    fi
    
    echo
    echo "=Ë Summary report: $OUTPUT_DIR/DIAGNOSTIC_SUMMARY.md"
    echo
    echo "= To review the diagnostics:"
    echo "   cat $OUTPUT_DIR/DIAGNOSTIC_SUMMARY.md"
    echo "   ls -la $OUTPUT_DIR/"
    echo
    
    log_emergency "Emergency diagnostic collection completed successfully"
}

main "$@"