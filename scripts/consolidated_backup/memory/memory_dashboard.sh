#!/bin/bash

# Memory Dashboard Script
# Purpose: Real-time memory system monitoring and health dashboard
# Usage: ./memory_dashboard.sh [--live|--report|--alerts]

set -euo pipefail

# Configuration
readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly MEMORY_DIR="${PROJECT_ROOT}/.claude/memory"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/memory_dashboard.log"
readonly DASHBOARD_REPORT="${PROJECT_ROOT}/.claude/memory_dashboard_report.md"

# Dashboard configuration
readonly REFRESH_INTERVAL=5  # seconds for live mode
readonly ALERT_THRESHOLD_MB=3  # Memory usage alert threshold
readonly FILE_COUNT_THRESHOLD=12  # File count alert threshold

# Color codes for terminal output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color
readonly BOLD='\033[1m'

# Logging function
log_dashboard() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] DASHBOARD: $1" >> "$LOG_FILE"
}

# Colored output functions
print_status() {
    local status="$1"
    local message="$2"
    case "$status" in
        "OK") echo -e "${GREEN} $message${NC}" ;;
        "WARNING") echo -e "${YELLOW}� $message${NC}" ;;
        "ERROR") echo -e "${RED}L $message${NC}" ;;
        "INFO") echo -e "${BLUE}9 $message${NC}" ;;
        *) echo "$message" ;;
    esac
}

print_header() {
    echo -e "${BOLD}${BLUE}$1${NC}"
    echo -e "${BLUE}$(printf '=%.0s' $(seq 1 ${#1}))${NC}"
}

# System information gathering
get_memory_stats() {
    local total_size=0
    local file_count=0
    local avg_file_size=0
    local largest_file_size=0
    local largest_file_name=""
    
    if [[ -d "$MEMORY_DIR" ]]; then
        while IFS= read -r -d '' file; do
            local size=$(wc -c < "$file" 2>/dev/null || echo "0")
            total_size=$((total_size + size))
            ((file_count++))
            
            if [[ $size -gt $largest_file_size ]]; then
                largest_file_size=$size
                largest_file_name=$(basename "$file")
            fi
        done < <(find "$MEMORY_DIR" -name "*.md" -type f -print0 2>/dev/null)
        
        if [[ $file_count -gt 0 ]]; then
            avg_file_size=$((total_size / file_count))
        fi
    fi
    
    # Return as JSON-like structure
    cat << EOF
{
    "total_size_bytes": $total_size,
    "total_size_mb": $((total_size / 1024 / 1024)),
    "file_count": $file_count,
    "avg_file_size": $avg_file_size,
    "largest_file_size": $largest_file_size,
    "largest_file_name": "$largest_file_name"
}
EOF
}

# Performance metrics
get_performance_metrics() {
    local maintenance_log="${PROJECT_ROOT}/.claude/memory_maintenance.log"
    local quality_log="${PROJECT_ROOT}/.claude/quality.log"
    
    local last_maintenance="Never"
    local maintenance_frequency=0
    local quality_events=0
    
    if [[ -f "$maintenance_log" ]]; then
        last_maintenance=$(tail -n 1 "$maintenance_log" 2>/dev/null | cut -d']' -f1 | tr -d '[' || echo "Never")
        maintenance_frequency=$(grep -c "MEMORY:" "$maintenance_log" 2>/dev/null || echo "0")
    fi
    
    if [[ -f "$quality_log" ]]; then
        quality_events=$(grep -c "QUALITY:" "$quality_log" 2>/dev/null || echo "0")
    fi
    
    cat << EOF
{
    "last_maintenance": "$last_maintenance",
    "maintenance_frequency": $maintenance_frequency,
    "quality_events": $quality_events
}
EOF
}

# Health assessment
assess_health() {
    local stats
    stats=$(get_memory_stats)
    
    local total_size_mb
    total_size_mb=$(echo "$stats" | grep -o '"total_size_mb": [0-9]*' | cut -d':' -f2 | tr -d ' ')
    
    local file_count
    file_count=$(echo "$stats" | grep -o '"file_count": [0-9]*' | cut -d':' -f2 | tr -d ' ')
    
    local health_score=100
    local health_issues=()
    
    # Check memory usage
    if [[ $total_size_mb -gt $ALERT_THRESHOLD_MB ]]; then
        health_score=$((health_score - 30))
        health_issues+=("High memory usage: ${total_size_mb}MB")
    fi
    
    # Check file count
    if [[ $file_count -gt $FILE_COUNT_THRESHOLD ]]; then
        health_score=$((health_score - 20))
        health_issues+=("Too many memory files: $file_count")
    fi
    
    # Check for required files
    if [[ ! -f "${MEMORY_DIR}/agent-coordination-patterns.md" ]]; then
        health_score=$((health_score - 25))
        health_issues+=("Missing required file: agent-coordination-patterns.md")
    fi
    
    # Check maintenance activity
    local maintenance_log="${PROJECT_ROOT}/.claude/memory_maintenance.log"
    if [[ -f "$maintenance_log" ]]; then
        local last_maintenance_epoch
        last_maintenance_epoch=$(stat -f %m "$maintenance_log" 2>/dev/null || echo "0")
        local current_epoch
        current_epoch=$(date +%s)
        local hours_since_maintenance=$(( (current_epoch - last_maintenance_epoch) / 3600 ))
        
        if [[ $hours_since_maintenance -gt 24 ]]; then
            health_score=$((health_score - 15))
            health_issues+=("No maintenance in $hours_since_maintenance hours")
        fi
    else
        health_score=$((health_score - 10))
        health_issues+=("No maintenance log found")
    fi
    
    local health_status
    if [[ $health_score -ge 90 ]]; then
        health_status="EXCELLENT"
    elif [[ $health_score -ge 75 ]]; then
        health_status="GOOD"
    elif [[ $health_score -ge 60 ]]; then
        health_status="WARNING"
    else
        health_status="CRITICAL"
    fi
    
    cat << EOF
{
    "health_score": $health_score,
    "health_status": "$health_status",
    "issues": [$(if [[ ${#health_issues[@]} -gt 0 ]]; then printf '"%s",' "${health_issues[@]}" | sed 's/,$//'; fi)]
}
EOF
}

# Display dashboard
show_dashboard() {
    clear
    
    print_header "Claude Code Memory System Dashboard"
    echo
    echo -e "${BLUE}Project:${NC} DevMem"
    echo -e "${BLUE}Memory Directory:${NC} $MEMORY_DIR"
    echo -e "${BLUE}Updated:${NC} $(date '+%Y-%m-%d %H:%M:%S')"
    echo
    
    # Memory Statistics
    print_header "Memory Statistics"
    local stats
    stats=$(get_memory_stats)
    
    local total_size_mb
    total_size_mb=$(echo "$stats" | grep -o '"total_size_mb": [0-9]*' | cut -d':' -f2 | tr -d ' ')
    
    local total_size_bytes
    total_size_bytes=$(echo "$stats" | grep -o '"total_size_bytes": [0-9]*' | cut -d':' -f2 | tr -d ' ')
    
    local file_count
    file_count=$(echo "$stats" | grep -o '"file_count": [0-9]*' | cut -d':' -f2 | tr -d ' ')
    
    local avg_file_size
    avg_file_size=$(echo "$stats" | grep -o '"avg_file_size": [0-9]*' | cut -d':' -f2 | tr -d ' ')
    
    local largest_file_name
    largest_file_name=$(echo "$stats" | grep -o '"largest_file_name": "[^"]*"' | cut -d':' -f2 | tr -d ' "')
    
    echo -e "${GREEN}=� Total Files:${NC} $file_count"
    echo -e "${GREEN}=� Total Size:${NC} ${total_size_bytes} bytes (${total_size_mb}MB)"
    echo -e "${GREEN}=� Average File Size:${NC} ${avg_file_size} bytes"
    echo -e "${GREEN}=� Largest File:${NC} $largest_file_name"
    echo
    
    # Health Assessment
    print_header "System Health"
    local health
    health=$(assess_health)
    
    local health_score
    health_score=$(echo "$health" | grep -o '"health_score": [0-9]*' | cut -d':' -f2 | tr -d ' ')
    
    local health_status
    health_status=$(echo "$health" | grep -o '"health_status": "[^"]*"' | cut -d':' -f2 | tr -d ' "')
    
    case "$health_status" in
        "EXCELLENT") print_status "OK" "Health Score: ${health_score}/100 ($health_status)" ;;
        "GOOD") print_status "OK" "Health Score: ${health_score}/100 ($health_status)" ;;
        "WARNING") print_status "WARNING" "Health Score: ${health_score}/100 ($health_status)" ;;
        "CRITICAL") print_status "ERROR" "Health Score: ${health_score}/100 ($health_status)" ;;
    esac
    
    # Show issues if any
    local issues
    issues=$(echo "$health" | grep -o '"issues": \[[^]]*\]' | sed 's/"issues": \[\(.*\)\]/\1/' | tr -d '"')
    if [[ -n "$issues" ]]; then
        echo
        echo -e "${YELLOW}Issues found:${NC}"
        echo "$issues" | tr ',' '\n' | while read -r issue; do
            if [[ -n "$issue" ]]; then
                print_status "WARNING" "$(echo "$issue" | xargs)"
            fi
        done
    fi
    echo
    
    # Performance Metrics
    print_header "Performance Metrics"
    local perf
    perf=$(get_performance_metrics)
    
    local last_maintenance
    last_maintenance=$(echo "$perf" | grep -o '"last_maintenance": "[^"]*"' | cut -d':' -f2 | tr -d ' "')
    
    local maintenance_frequency
    maintenance_frequency=$(echo "$perf" | grep -o '"maintenance_frequency": [0-9]*' | cut -d':' -f2 | tr -d ' ')
    
    local quality_events
    quality_events=$(echo "$perf" | grep -o '"quality_events": [0-9]*' | cut -d':' -f2 | tr -d ' ')
    
    echo -e "${BLUE}=' Last Maintenance:${NC} $last_maintenance"
    echo -e "${BLUE}=� Maintenance Events:${NC} $maintenance_frequency"
    echo -e "${BLUE} Quality Events:${NC} $quality_events"
    echo
    
    # File breakdown
    print_header "File Breakdown"
    if [[ -d "$MEMORY_DIR" ]]; then
        find "$MEMORY_DIR" -name "*.md" -type f 2>/dev/null | while read -r file; do
            local filename=$(basename "$file")
            local size=$(wc -c < "$file" 2>/dev/null || echo "0")
            local size_kb=$((size / 1024))
            echo -e "${GREEN}=�${NC} $filename: ${size} bytes (${size_kb}KB)"
        done | head -10
        
        local total_files
        total_files=$(find "$MEMORY_DIR" -name "*.md" -type f 2>/dev/null | wc -l)
        if [[ $total_files -gt 10 ]]; then
            echo -e "${BLUE}... and $((total_files - 10)) more files${NC}"
        fi
    else
        print_status "ERROR" "Memory directory not found"
    fi
}

# Generate report
generate_report() {
    log_dashboard "Generating memory dashboard report"
    
    cat > "$DASHBOARD_REPORT" << 'EOF'
# Memory System Dashboard Report

EOF
    
    echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')" >> "$DASHBOARD_REPORT"
    echo >> "$DASHBOARD_REPORT"
    
    # Add statistics
    echo "## Memory Statistics" >> "$DASHBOARD_REPORT"
    echo >> "$DASHBOARD_REPORT"
    
    local stats
    stats=$(get_memory_stats)
    echo "- **Total Files:** $(echo "$stats" | grep -o '"file_count": [0-9]*' | cut -d':' -f2 | tr -d ' ')" >> "$DASHBOARD_REPORT"
    echo "- **Total Size:** $(echo "$stats" | grep -o '"total_size_bytes": [0-9]*' | cut -d':' -f2 | tr -d ' ') bytes" >> "$DASHBOARD_REPORT"
    echo "- **Average File Size:** $(echo "$stats" | grep -o '"avg_file_size": [0-9]*' | cut -d':' -f2 | tr -d ' ') bytes" >> "$DASHBOARD_REPORT"
    echo >> "$DASHBOARD_REPORT"
    
    # Add health assessment
    echo "## Health Assessment" >> "$DASHBOARD_REPORT"
    echo >> "$DASHBOARD_REPORT"
    
    local health
    health=$(assess_health)
    local health_score
    health_score=$(echo "$health" | grep -o '"health_score": [0-9]*' | cut -d':' -f2 | tr -d ' ')
    local health_status
    health_status=$(echo "$health" | grep -o '"health_status": "[^"]*"' | cut -d':' -f2 | tr -d ' "')
    
    echo "**Health Score:** ${health_score}/100 ($health_status)" >> "$DASHBOARD_REPORT"
    echo >> "$DASHBOARD_REPORT"
    
    # Add file listing
    echo "## File Listing" >> "$DASHBOARD_REPORT"
    echo >> "$DASHBOARD_REPORT"
    
    if [[ -d "$MEMORY_DIR" ]]; then
        find "$MEMORY_DIR" -name "*.md" -type f 2>/dev/null | while read -r file; do
            local filename=$(basename "$file")
            local size=$(wc -c < "$file" 2>/dev/null || echo "0")
            echo "- \`$filename\`: ${size} bytes" >> "$DASHBOARD_REPORT"
        done
    fi
    
    echo >> "$DASHBOARD_REPORT"
    echo "---" >> "$DASHBOARD_REPORT"
    echo "Report generated by Claude Code Memory Dashboard" >> "$DASHBOARD_REPORT"
    
    echo "Dashboard report generated: $DASHBOARD_REPORT"
}

# Check for alerts
check_alerts() {
    log_dashboard "Checking for memory system alerts"
    
    local alerts=()
    local stats
    stats=$(get_memory_stats)
    local health
    health=$(assess_health)
    
    # Check memory usage alert
    local total_size_mb
    total_size_mb=$(echo "$stats" | grep -o '"total_size_mb": [0-9]*' | cut -d':' -f2 | tr -d ' ')
    if [[ $total_size_mb -gt $ALERT_THRESHOLD_MB ]]; then
        alerts+=("HIGH_MEMORY_USAGE: ${total_size_mb}MB exceeds threshold")
    fi
    
    # Check file count alert
    local file_count
    file_count=$(echo "$stats" | grep -o '"file_count": [0-9]*' | cut -d':' -f2 | tr -d ' ')
    if [[ $file_count -gt $FILE_COUNT_THRESHOLD ]]; then
        alerts+=("HIGH_FILE_COUNT: $file_count files exceeds threshold")
    fi
    
    # Check health score alert
    local health_score
    health_score=$(echo "$health" | grep -o '"health_score": [0-9]*' | cut -d':' -f2 | tr -d ' ')
    if [[ $health_score -lt 70 ]]; then
        alerts+=("LOW_HEALTH_SCORE: ${health_score}/100 below acceptable level")
    fi
    
    if [[ ${#alerts[@]} -gt 0 ]]; then
        print_status "ERROR" "Memory System Alerts:"
        for alert in "${alerts[@]}"; do
            print_status "WARNING" "$alert"
            log_dashboard "ALERT: $alert"
        done
        return 1
    else
        print_status "OK" "No alerts - system healthy"
        return 0
    fi
}

# Live monitoring mode
live_mode() {
    echo "Starting live memory monitoring (Ctrl+C to exit)..."
    echo "Refresh interval: ${REFRESH_INTERVAL}s"
    echo
    
    while true; do
        show_dashboard
        echo
        print_status "INFO" "Live monitoring active - Press Ctrl+C to exit"
        sleep $REFRESH_INTERVAL
    done
}

# Main function
main() {
    local mode="${1:-dashboard}"
    
    case "$mode" in
        "--live"|"live")
            live_mode
            ;;
        "--report"|"report")
            generate_report
            ;;
        "--alerts"|"alerts")
            check_alerts
            ;;
        "--dashboard"|"dashboard"|*)
            show_dashboard
            ;;
    esac
}

# Handle Ctrl+C gracefully
trap 'echo -e "\n${BLUE}Memory dashboard stopped${NC}"; exit 0' INT

# Execute main function
main "$@"