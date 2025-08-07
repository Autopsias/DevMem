#!/bin/bash

# Memory Manager - Unified Interface
# Purpose: Single entry point for all memory maintenance operations
# Usage: ./memory_manager.sh <command> [options]

set -euo pipefail

# Configuration
readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly SCRIPTS_DIR="${PROJECT_ROOT}/scripts/memory"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/memory_manager.log"

# Get script for command
get_script_for_command() {
    case "$1" in
        "maintenance") echo "auto_maintenance.sh" ;;
        "validate") echo "validate_memory.sh" ;;
        "setup-periodic") echo "setup_periodic_maintenance.sh" ;;
        "dashboard"|"status"|"monitor"|"alerts") echo "memory_dashboard.sh" ;;
        "edit") echo "memory_editor.sh" ;;
        "safety") echo "memory_safety_framework.sh" ;;
        "help") echo "" ;;
        *) echo "" ;;
    esac
}

# Get description for command
get_description_for_command() {
    case "$1" in
        "maintenance") echo "Run memory maintenance (full, periodic, post-quality)" ;;
        "validate") echo "Validate memory structure and content [--fix] [--report]" ;;
        "setup-periodic") echo "Setup/manage periodic maintenance [--enable|--disable|--status]" ;;
        "dashboard") echo "Show memory system dashboard" ;;
        "status") echo "Show current memory system status" ;;
        "monitor") echo "Live memory monitoring dashboard" ;;
        "alerts") echo "Check for memory system alerts" ;;
        "edit") echo "Safe memory file editing with validation [file] [--editor] [--force]" ;;
        "safety") echo "Advanced safety checks and recovery [operation] [--emergency]" ;;
        "help") echo "Show this help message" ;;
        *) echo "" ;;
    esac
}

# Available commands
readonly AVAILABLE_COMMANDS="maintenance validate setup-periodic dashboard status monitor alerts edit safety help"

# Color codes
readonly GREEN='\033[0;32m'
readonly BLUE='\033[0;34m'
readonly YELLOW='\033[1;33m'
readonly RED='\033[0;31m'
readonly NC='\033[0m'
readonly BOLD='\033[1m'

# Logging
log_manager() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] MANAGER: $1" >> "$LOG_FILE"
}

# Print colored status
print_status() {
    local level="$1"
    local message="$2"
    case "$level" in
        "SUCCESS") echo -e "${GREEN} $message${NC}" ;;
        "INFO") echo -e "${BLUE}9 $message${NC}" ;;
        "WARNING") echo -e "${YELLOW}� $message${NC}" ;;
        "ERROR") echo -e "${RED}L $message${NC}" ;;
        *) echo "$message" ;;
    esac
}

# Show help
show_help() {
    cat << 'EOF'
Memory Manager - Unified Memory System Interface

USAGE:
    ./memory_manager.sh <command> [options]

COMMANDS:
EOF

    echo
    for cmd in $AVAILABLE_COMMANDS; do
        printf "    ${BLUE}%-15s${NC} %s\n" "$cmd" "$(get_description_for_command "$cmd")"
    done
    
    cat << 'EOF'

EXAMPLES:
    ./memory_manager.sh maintenance full       # Run full maintenance
    ./memory_manager.sh validate --fix         # Validate and fix issues
    ./memory_manager.sh setup-periodic --enable # Enable automated maintenance
    ./memory_manager.sh dashboard              # Show system dashboard
    ./memory_manager.sh monitor                # Live monitoring
    ./memory_manager.sh alerts                 # Check for alerts

SHORTCUTS:
    make memory-status          # Show dashboard
    make memory-validate        # Validate memory
    make memory-maintenance     # Run maintenance
    
For detailed command help, use:
    ./memory_manager.sh <command> --help

EOF
}

# Quick status check
show_quick_status() {
    local memory_dir="${PROJECT_ROOT}/.claude/memory"
    local file_count=0
    local total_size=0
    
    if [[ -d "$memory_dir" ]]; then
        file_count=$(find "$memory_dir" -name "*.md" -type f | wc -l)
        total_size=$(find "$memory_dir" -name "*.md" -type f -exec wc -c {} + 2>/dev/null | tail -n1 | awk '{print $1}' || echo "0")
    fi
    
    echo -e "${BOLD}Memory System Quick Status${NC}"
    echo "=========================="
    echo -e "${BLUE}Files:${NC} $file_count"
    echo -e "${BLUE}Size:${NC} $total_size bytes ($((total_size / 1024))KB)"
    
    # Check for issues
    if [[ $file_count -eq 0 ]]; then
        print_status "WARNING" "No memory files found"
    elif [[ $file_count -gt 15 ]]; then
        print_status "WARNING" "High file count - consider maintenance"
    elif [[ $total_size -gt $((3 * 1024 * 1024)) ]]; then
        print_status "WARNING" "High memory usage - consider cleanup"
    else
        print_status "SUCCESS" "Memory system healthy"
    fi
    
    echo
    echo "For detailed analysis, run: ./memory_manager.sh dashboard"
}

# Execute command
execute_command() {
    local command="$1"
    shift
    
    case "$command" in
        "maintenance")
            local script="${SCRIPTS_DIR}/$(get_script_for_command "$command")"
            log_manager "Running maintenance: $*"
            exec bash "$script" "$@"
            ;;
        "validate")
            local script="${SCRIPTS_DIR}/$(get_script_for_command "$command")"
            log_manager "Running validation: $*"
            exec bash "$script" "$@"
            ;;
        "setup-periodic")
            local script="${SCRIPTS_DIR}/$(get_script_for_command "$command")"
            log_manager "Managing periodic setup: $*"
            exec bash "$script" "$@"
            ;;
        "dashboard")
            local script="${SCRIPTS_DIR}/$(get_script_for_command "$command")"
            log_manager "Showing dashboard"
            exec bash "$script" dashboard
            ;;
        "status")
            if [[ $# -eq 0 ]]; then
                show_quick_status
            else
                local script="${SCRIPTS_DIR}/$(get_script_for_command "$command")"
                exec bash "$script" dashboard
            fi
            ;;
        "monitor")
            local script="${SCRIPTS_DIR}/$(get_script_for_command "$command")"
            log_manager "Starting live monitoring"
            exec bash "$script" --live
            ;;
        "alerts")
            local script="${SCRIPTS_DIR}/$(get_script_for_command "$command")"
            log_manager "Checking alerts"
            exec bash "$script" --alerts
            ;;
        "edit")
            local script="${SCRIPTS_DIR}/$(get_script_for_command "$command")"
            log_manager "Memory editing: $*"
            exec bash "$script" "$@"
            ;;
        "safety")
            local script="${SCRIPTS_DIR}/$(get_script_for_command "$command")"
            log_manager "Safety operations: $*"
            exec bash "$script" "$@"
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            print_status "ERROR" "Unknown command: $command"
            echo
            show_help
            exit 1
            ;;
    esac
}

# Validate environment
validate_environment() {
    # Check if scripts directory exists
    if [[ ! -d "$SCRIPTS_DIR" ]]; then
        print_status "ERROR" "Scripts directory not found: $SCRIPTS_DIR"
        exit 1
    fi
    
    # Check if required scripts exist
    local missing_scripts=()
    for cmd in $AVAILABLE_COMMANDS; do
        local script_name="$(get_script_for_command "$cmd")"
        if [[ -n "$script_name" ]]; then
            local script_path="${SCRIPTS_DIR}/$script_name"
            if [[ ! -f "$script_path" ]]; then
                missing_scripts+=("$script_name")
            elif [[ ! -x "$script_path" ]]; then
                chmod +x "$script_path" 2>/dev/null || missing_scripts+=("$script_name (not executable)")
            fi
        fi
    done
    
    if [[ ${#missing_scripts[@]} -gt 0 ]]; then
        print_status "ERROR" "Missing or non-executable scripts:"
        for script in "${missing_scripts[@]}"; do
            echo "  - $script"
        done
        exit 1
    fi
    
    # Create memory directory if it doesn't exist
    mkdir -p "${PROJECT_ROOT}/.claude/memory"
    
    log_manager "Environment validation completed"
}

# Main function
main() {
    if [[ $# -eq 0 ]]; then
        show_quick_status
        exit 0
    fi
    
    local command="$1"
    shift
    
    # Validate environment before executing commands
    validate_environment
    
    # Execute the command
    execute_command "$command" "$@"
}

# Execute main function
main "$@"