#!/bin/bash

# System Health Check Script for Simplified Claude Code Framework
# Purpose: Comprehensive health monitoring of essential system components
# Integration: Core maintenance and monitoring procedures

set -euo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/system_health.log"
readonly CONFIG_FILE="${PROJECT_ROOT}/.claude/settings.json"

# Health scoring weights
readonly MEMORY_WEIGHT=40
readonly CONFIG_WEIGHT=25
readonly LOG_WEIGHT=20
readonly SECURITY_WEIGHT=15

# Health thresholds
readonly MEMORY_WARNING_MB=${MEMORY_WARNING_THRESHOLD_MB:-3}
readonly LOG_WARNING_LINES=${LOG_WARNING_THRESHOLD_LINES:-200}
readonly HEALTH_WARNING_THRESHOLD=${HEALTH_SCORE_WARNING_THRESHOLD:-70}

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly ORANGE='\033[0;33m'
readonly NC='\033[0m' # No Color

# Logging function
log_health() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] HEALTH: $1" >> "$LOG_FILE"
}

# Health score calculation
calculate_health_score() {
    local memory_score=$1
    local config_score=$2
    local log_score=$3
    local security_score=$4
    
    local total_score=$(( (memory_score * MEMORY_WEIGHT + config_score * CONFIG_WEIGHT + 
                          log_score * LOG_WEIGHT + security_score * SECURITY_WEIGHT) / 100 ))
    echo "$total_score"
}

# Memory health check
check_memory_health() {
    local score=100
    local issues=0
    local status="EXCELLENT"
    
    # Check memory directory exists
    if [[ ! -d "${PROJECT_ROOT}/.claude/memory" ]]; then
        ((score -= 25))
        ((issues++))
        echo "L Memory directory missing"
    fi
    
    # Check memory usage
    local memory_usage_mb=0
    if [[ -d "${PROJECT_ROOT}/.claude/memory" ]]; then
        memory_usage_mb=$(du -sm "${PROJECT_ROOT}/.claude/memory" 2>/dev/null | cut -f1 || echo "0")
        if [[ $memory_usage_mb -gt $MEMORY_WARNING_MB ]]; then
            ((score -= 30))
            ((issues++))
            echo "� Memory usage: ${memory_usage_mb}MB (threshold: ${MEMORY_WARNING_MB}MB)"
        fi
    fi
    
    # Check memory file count
    local file_count=0
    if [[ -d "${PROJECT_ROOT}/.claude/memory" ]]; then
        file_count=$(find "${PROJECT_ROOT}/.claude/memory" -name "*.md" | wc -l)
        if [[ $file_count -gt 12 ]]; then
            ((score -= 20))
            ((issues++))
            echo "� Memory files: $file_count (threshold: 12)"
        fi
    fi
    
    # Check required memory files
    local required_files=(
        ".claude/memory/agent-coordination-patterns.md"
        ".claude/memory/domains/testing-patterns.md"
        ".claude/memory/domains/infrastructure-patterns.md"
        ".claude/memory/domains/security-patterns.md"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "${PROJECT_ROOT}/$file" ]]; then
            ((score -= 25))
            ((issues++))
            echo "L Missing required file: $file"
        fi
    done
    
    # Determine status
    if [[ $score -ge 90 ]]; then
        status="EXCELLENT"
    elif [[ $score -ge 75 ]]; then
        status="GOOD"
    elif [[ $score -ge 60 ]]; then
        status="WARNING"
    else
        status="CRITICAL"
    fi
    
    echo "$score:$status:$issues:${memory_usage_mb}MB:$file_count"
}

# Configuration health check
check_config_health() {
    local score=100
    local issues=0
    local status="EXCELLENT"
    
    # Check settings.json exists and is valid JSON
    if [[ ! -f "$CONFIG_FILE" ]]; then
        ((score -= 50))
        ((issues++))
        echo "L Settings.json missing"
    else
        if ! python -m json.tool "$CONFIG_FILE" >/dev/null 2>&1; then
            ((score -= 40))
            ((issues++))
            echo "L Settings.json invalid JSON"
        fi
    fi
    
    # Check essential hooks configuration
    local essential_hooks=(
        "scripts/hooks/essential_security.sh"
        "scripts/hooks/essential_quality.sh"
    )
    
    for hook in "${essential_hooks[@]}"; do
        if [[ ! -f "${PROJECT_ROOT}/$hook" ]]; then
            ((score -= 25))
            ((issues++))
            echo "L Missing essential hook: $hook"
        elif [[ ! -x "${PROJECT_ROOT}/$hook" ]]; then
            ((score -= 15))
            ((issues++))
            echo "� Hook not executable: $hook"
        fi
    done
    
    # Check environment variables
    local required_vars=(
        "CLAUDE_AGENT_FRAMEWORK_ENABLED"
        "QUALITY_GATES_ENABLED"
        "SECURITY_SCANNING_ENABLED"
    )
    
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            ((score -= 10))
            ((issues++))
            echo "� Environment variable not set: $var"
        fi
    done
    
    # Determine status
    if [[ $score -ge 90 ]]; then
        status="EXCELLENT"
    elif [[ $score -ge 75 ]]; then
        status="GOOD"
    elif [[ $score -ge 60 ]]; then
        status="WARNING"
    else
        status="CRITICAL"
    fi
    
    echo "$score:$status:$issues"
}

# Log health check
check_log_health() {
    local score=100
    local issues=0
    local status="EXCELLENT"
    
    # Check essential log files
    local log_files=(
        ".claude/security.log"
        ".claude/quality.log"
        ".claude/memory_maintenance.log"
    )
    
    for log_file in "${log_files[@]}"; do
        if [[ -f "${PROJECT_ROOT}/$log_file" ]]; then
            local line_count
            line_count=$(wc -l < "${PROJECT_ROOT}/$log_file" 2>/dev/null || echo "0")
            if [[ $line_count -gt $LOG_WARNING_LINES ]]; then
                ((score -= 15))
                ((issues++))
                echo "� Large log file: $log_file ($line_count lines)"
            fi
        fi
    done
    
    # Check log permissions
    for log_file in "${log_files[@]}"; do
        if [[ -f "${PROJECT_ROOT}/$log_file" ]]; then
            local perms
            perms=$(stat -f "%Mp%Lp" "${PROJECT_ROOT}/$log_file" 2>/dev/null || echo "000")
            if [[ ! "$perms" =~ ^-rw.* ]]; then
                ((score -= 10))
                ((issues++))
                echo "� Incorrect log permissions: $log_file"
            fi
        fi
    done
    
    # Check for recent errors in logs
    local recent_errors=0
    for log_file in "${log_files[@]}"; do
        if [[ -f "${PROJECT_ROOT}/$log_file" ]]; then
            local recent_error_count
            recent_error_count=$(tail -n 20 "${PROJECT_ROOT}/$log_file" 2>/dev/null | grep -c "ERROR\|FAILED\|CRITICAL" 2>/dev/null || echo "0")
            recent_error_count=$((recent_error_count + 0))  # Ensure it's treated as a number
            recent_errors=$((recent_errors + recent_error_count))
        fi
    done
    
    if [[ $recent_errors -gt 5 ]]; then
        ((score -= 20))
        ((issues++))
        echo "� Recent errors in logs: $recent_errors"
    fi
    
    # Determine status
    if [[ $score -ge 90 ]]; then
        status="EXCELLENT"
    elif [[ $score -ge 75 ]]; then
        status="GOOD"
    elif [[ $score -ge 60 ]]; then
        status="WARNING"
    else
        status="CRITICAL"
    fi
    
    echo "$score:$status:$issues"
}

# Security health check
check_security_health() {
    local score=100
    local issues=0
    local status="EXCELLENT"
    
    # Check security hook is active
    if [[ ! -x "${PROJECT_ROOT}/scripts/hooks/essential_security.sh" ]]; then
        ((score -= 30))
        ((issues++))
        echo "L Security hook not executable"
    fi
    
    # Check for dangerous commands in recent logs
    if [[ -f "${PROJECT_ROOT}/.claude/security.log" ]]; then
        local dangerous_commands
        dangerous_commands=$(tail -n 50 "${PROJECT_ROOT}/.claude/security.log" 2>/dev/null | grep -c "BLOCKED\|DANGEROUS" 2>/dev/null || echo "0")
        dangerous_commands=$((dangerous_commands + 0))  # Ensure it's treated as a number
        if [[ $dangerous_commands -gt 3 ]]; then
            ((score -= 25))
            ((issues++))
            echo "⚠️ Recent dangerous command attempts: $dangerous_commands"
        fi
    fi
    
    # Check .claude directory permissions
    if [[ -d "${PROJECT_ROOT}/.claude" ]]; then
        local claude_perms
        claude_perms=$(stat -f "%Mp%Lp" "${PROJECT_ROOT}/.claude" 2>/dev/null || echo "000")
        if [[ ! "$claude_perms" =~ ^drwx.*$ ]]; then
            ((score -= 20))
            ((issues++))
            echo "� Incorrect .claude directory permissions"
        fi
    fi
    
    # Check for sensitive files in wrong locations
    local sensitive_patterns=("*.key" "*.pem" "*password*" "*secret*")
    local sensitive_found=0
    
    for pattern in "${sensitive_patterns[@]}"; do
        local found_files
        found_files=$(find "${PROJECT_ROOT}" -name "$pattern" -not -path "*/.claude/secrets/*" -not -path "*/.git/*" 2>/dev/null | wc -l)
        sensitive_found=$((sensitive_found + found_files))
    done
    
    if [[ $sensitive_found -gt 0 ]]; then
        ((score -= 30))
        ((issues++))
        echo "� Sensitive files in unprotected locations: $sensitive_found"
    fi
    
    # Determine status
    if [[ $score -ge 90 ]]; then
        status="EXCELLENT"
    elif [[ $score -ge 75 ]]; then
        status="GOOD"
    elif [[ $score -ge 60 ]]; then
        status="WARNING"
    else
        status="CRITICAL"
    fi
    
    echo "$score:$status:$issues"
}

# Display health status with color
display_status() {
    local status="$1"
    local score="$2"
    local component="$3"
    
    case "$status" in
        "EXCELLENT")
            echo -e "${GREEN} $component: $status ($score/100)${NC}"
            ;;
        "GOOD")
            echo -e "${YELLOW}=� $component: $status ($score/100)${NC}"
            ;;
        "WARNING")
            echo -e "${ORANGE}=� $component: $status ($score/100)${NC}"
            ;;
        "CRITICAL")
            echo -e "${RED}=4 $component: $status ($score/100)${NC}"
            ;;
    esac
}

# Main health check function
main() {
    local detailed=false
    local json_output=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --detailed)
                detailed=true
                shift
                ;;
            --json)
                json_output=true
                shift
                ;;
            *)
                echo "Usage: $0 [--detailed] [--json]"
                exit 1
                ;;
        esac
    done
    
    log_health "Starting system health check"
    
    # Run health checks
    local memory_result
    memory_result=$(check_memory_health)
    local memory_score=$(echo "$memory_result" | cut -d: -f1)
    local memory_status=$(echo "$memory_result" | cut -d: -f2)
    local memory_issues=$(echo "$memory_result" | cut -d: -f3)
    local memory_usage=$(echo "$memory_result" | cut -d: -f4)
    local memory_files=$(echo "$memory_result" | cut -d: -f5)
    
    local config_result
    config_result=$(check_config_health)
    local config_score=$(echo "$config_result" | cut -d: -f1)
    local config_status=$(echo "$config_result" | cut -d: -f2)
    local config_issues=$(echo "$config_result" | cut -d: -f3)
    
    local log_result
    log_result=$(check_log_health)
    local log_score=$(echo "$log_result" | cut -d: -f1)
    local log_status=$(echo "$log_result" | cut -d: -f2)
    local log_issues=$(echo "$log_result" | cut -d: -f3)
    
    local security_result
    security_result=$(check_security_health)
    local security_score=$(echo "$security_result" | cut -d: -f1)
    local security_status=$(echo "$security_result" | cut -d: -f2)
    local security_issues=$(echo "$security_result" | cut -d: -f3)
    
    # Calculate overall health score
    local total_score
    total_score=$(calculate_health_score "$memory_score" "$config_score" "$log_score" "$security_score")
    local total_status="EXCELLENT"
    
    if [[ $total_score -ge 90 ]]; then
        total_status="EXCELLENT"
    elif [[ $total_score -ge 75 ]]; then
        total_status="GOOD"
    elif [[ $total_score -ge 60 ]]; then
        total_status="WARNING"
    else
        total_status="CRITICAL"
    fi
    
    # Output results
    if [[ "$json_output" == true ]]; then
        cat << EOF
{
  "overall": {
    "score": $total_score,
    "status": "$total_status",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  },
  "components": {
    "memory": {
      "score": $memory_score,
      "status": "$memory_status",
      "issues": $memory_issues,
      "usage_mb": $(echo "$memory_usage" | sed 's/MB//'),
      "file_count": $memory_files
    },
    "configuration": {
      "score": $config_score,
      "status": "$config_status",
      "issues": $config_issues
    },
    "logs": {
      "score": $log_score,
      "status": "$log_status",
      "issues": $log_issues
    },
    "security": {
      "score": $security_score,
      "status": "$security_status",
      "issues": $security_issues
    }
  }
}
EOF
    else
        echo
        echo "=== System Health Report ==="
        echo "Generated: $(date)"
        echo
        
        display_status "$total_status" "$total_score" "Overall System Health"
        echo
        
        if [[ "$detailed" == true ]]; then
            echo "Component Health:"
            display_status "$memory_status" "$memory_score" "Memory System"
            echo "  =� Memory Files: $memory_files"
            echo "  =� Memory Usage: $memory_usage"
            echo "  =' Issues: $memory_issues"
            echo
            
            display_status "$config_status" "$config_score" "Configuration"
            echo "  =' Issues: $config_issues"
            echo
            
            display_status "$log_status" "$log_score" "Log System"
            echo "  =' Issues: $log_issues"
            echo
            
            display_status "$security_status" "$security_score" "Security"
            echo "  =' Issues: $security_issues"
        else
            echo "Quick Status:"
            echo "  =� Memory Files: $memory_files"
            echo "  =� Memory Usage: $memory_usage"
            echo "  � Last Check: $(date '+%H:%M')"
        fi
        
        echo
        
        # Health recommendations
        if [[ $total_score -lt $HEALTH_WARNING_THRESHOLD ]]; then
            echo "� Health Score Below Threshold ($HEALTH_WARNING_THRESHOLD)"
            echo "Recommended Actions:"
            
            if [[ $memory_score -lt 70 ]]; then
                echo "  " Run: make memory-maintenance"
            fi
            
            if [[ $config_score -lt 70 ]]; then
                echo "  " Validate configuration: python scripts/validate_native_config.py"
            fi
            
            if [[ $log_score -lt 70 ]]; then
                echo "  " Check logs: tail -f .claude/security.log"
            fi
            
            if [[ $security_score -lt 70 ]]; then
                echo "  " Review security: ./scripts/system/security_audit.sh"
            fi
        fi
    fi
    
    log_health "System health check completed - Score: $total_score ($total_status)"
    
    # Return appropriate exit code
    if [[ $total_score -lt 60 ]]; then
        exit 2  # Critical
    elif [[ $total_score -lt $HEALTH_WARNING_THRESHOLD ]]; then
        exit 1  # Warning
    else
        exit 0  # OK
    fi
}

main "$@"