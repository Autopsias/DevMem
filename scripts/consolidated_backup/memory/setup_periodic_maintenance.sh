#!/bin/bash

# Periodic Memory Maintenance Setup Script
# Purpose: Setup automated memory maintenance via cron or launchd
# Usage: ./setup_periodic_maintenance.sh [--enable|--disable|--status]

set -euo pipefail

# Configuration
readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly MAINTENANCE_SCRIPT="${PROJECT_ROOT}/scripts/memory/auto_maintenance.sh"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/maintenance_setup.log"

# macOS launchd configuration
readonly LAUNCHD_LABEL="com.claude.devmem.memory-maintenance"
readonly LAUNCHD_PLIST_DIR="$HOME/Library/LaunchAgents"
readonly LAUNCHD_PLIST_FILE="${LAUNCHD_PLIST_DIR}/${LAUNCHD_LABEL}.plist"

# Cron configuration (fallback)
readonly CRON_COMMENT="# Claude DevMem Memory Maintenance"

# Logging function
log_setup() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SETUP: $1" >> "$LOG_FILE"
}

# Detect operating system
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

# Create launchd plist for macOS
create_launchd_plist() {
    log_setup "Creating launchd plist for periodic maintenance"
    
    mkdir -p "$LAUNCHD_PLIST_DIR"
    
    cat > "$LAUNCHD_PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LAUNCHD_LABEL}</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>${MAINTENANCE_SCRIPT}</string>
        <string>periodic</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>${PROJECT_ROOT}</string>
    
    <key>StartInterval</key>
    <integer>3600</integer>
    
    <key>StandardOutPath</key>
    <string>${PROJECT_ROOT}/.claude/periodic_maintenance.log</string>
    
    <key>StandardErrorPath</key>
    <string>${PROJECT_ROOT}/.claude/periodic_maintenance_error.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>CLAUDE_PROJECT_DIR</key>
        <string>${PROJECT_ROOT}</string>
        <key>CLAUDE_MEMORY_MAINTENANCE_ENABLED</key>
        <string>true</string>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin</string>
    </dict>
    
    <key>RunAtLoad</key>
    <false/>
    
    <key>KeepAlive</key>
    <false/>
    
    <key>ProcessType</key>
    <string>Background</string>
    
    <key>LowPriorityIO</key>
    <true/>
</dict>
</plist>
EOF
    
    log_setup "Created launchd plist: $LAUNCHD_PLIST_FILE"
}

# Setup cron job (Linux fallback)
setup_cron() {
    log_setup "Setting up cron job for periodic maintenance"
    
    local cron_entry="0 * * * * cd ${PROJECT_ROOT} && ${MAINTENANCE_SCRIPT} periodic >> ${PROJECT_ROOT}/.claude/periodic_maintenance.log 2>&1"
    
    # Check if cron entry already exists
    if crontab -l 2>/dev/null | grep -q "$MAINTENANCE_SCRIPT"; then
        log_setup "Cron job already exists, skipping"
        return 0
    fi
    
    # Add new cron entry
    (crontab -l 2>/dev/null; echo "$CRON_COMMENT"; echo "$cron_entry") | crontab -
    
    log_setup "Added cron job for memory maintenance"
}

# Enable periodic maintenance
enable_maintenance() {
    local os_type
    os_type=$(detect_os)
    
    log_setup "Enabling periodic memory maintenance for $os_type"
    
    # Validate maintenance script exists and is executable
    if [[ ! -f "$MAINTENANCE_SCRIPT" ]]; then
        echo "ERROR: Maintenance script not found: $MAINTENANCE_SCRIPT"
        exit 1
    fi
    
    if [[ ! -x "$MAINTENANCE_SCRIPT" ]]; then
        chmod +x "$MAINTENANCE_SCRIPT"
        log_setup "Made maintenance script executable"
    fi
    
    case "$os_type" in
        "macos")
            create_launchd_plist
            
            # Load the launchd job
            if launchctl load "$LAUNCHD_PLIST_FILE" 2>/dev/null; then
                log_setup "Successfully loaded launchd job"
                echo " Periodic memory maintenance enabled via launchd"
                echo "   Runs every hour in background"
                echo "   Logs: ${PROJECT_ROOT}/.claude/periodic_maintenance.log"
            else
                log_setup "Failed to load launchd job, trying bootstrap"
                # Try bootstrap for newer macOS versions
                if launchctl bootstrap gui/$(id -u) "$LAUNCHD_PLIST_FILE" 2>/dev/null; then
                    log_setup "Successfully bootstrapped launchd job"
                    echo " Periodic memory maintenance enabled via launchd (bootstrap)"
                else
                    log_setup "Failed to setup launchd, falling back to manual instructions"
                    echo "  Could not automatically enable launchd job"
                    echo "   Please run manually: launchctl load $LAUNCHD_PLIST_FILE"
                fi
            fi
            ;;
        "linux")
            setup_cron
            echo " Periodic memory maintenance enabled via cron"
            echo "   Runs every hour"
            echo "   Logs: ${PROJECT_ROOT}/.claude/periodic_maintenance.log"
            ;;
        *)
            log_setup "Unsupported OS: $os_type"
            echo "L Unsupported operating system: $os_type"
            echo "   Please set up periodic maintenance manually"
            echo "   Command: ${MAINTENANCE_SCRIPT} periodic"
            exit 1
            ;;
    esac
    
    # Run initial maintenance
    echo "=' Running initial memory maintenance..."
    bash "$MAINTENANCE_SCRIPT" full
    echo " Initial maintenance completed"
}

# Disable periodic maintenance
disable_maintenance() {
    local os_type
    os_type=$(detect_os)
    
    log_setup "Disabling periodic memory maintenance for $os_type"
    
    case "$os_type" in
        "macos")
            # Unload launchd job
            if launchctl unload "$LAUNCHD_PLIST_FILE" 2>/dev/null; then
                log_setup "Successfully unloaded launchd job"
            else
                # Try bootout for newer macOS versions
                launchctl bootout gui/$(id -u) "$LAUNCHD_PLIST_FILE" 2>/dev/null || true
                log_setup "Attempted to bootout launchd job"
            fi
            
            # Remove plist file
            if [[ -f "$LAUNCHD_PLIST_FILE" ]]; then
                rm -f "$LAUNCHD_PLIST_FILE"
                log_setup "Removed launchd plist file"
            fi
            
            echo " Periodic memory maintenance disabled"
            ;;
        "linux")
            # Remove cron job
            if crontab -l 2>/dev/null | grep -v "$MAINTENANCE_SCRIPT" | crontab -; then
                log_setup "Removed cron job"
                echo " Periodic memory maintenance disabled"
            else
                log_setup "Failed to remove cron job or no job found"
                echo "  Could not remove cron job automatically"
                echo "   Please check: crontab -e"
            fi
            ;;
        *)
            echo "L Unsupported operating system: $os_type"
            exit 1
            ;;
    esac
}

# Show maintenance status
show_status() {
    local os_type
    os_type=$(detect_os)
    
    echo "Memory Maintenance Status"
    echo "========================="
    echo
    echo "Operating System: $os_type"
    echo "Project Root: $PROJECT_ROOT"
    echo "Maintenance Script: $MAINTENANCE_SCRIPT"
    echo
    
    # Check if maintenance script exists and is executable
    if [[ -f "$MAINTENANCE_SCRIPT" && -x "$MAINTENANCE_SCRIPT" ]]; then
        echo " Maintenance script: Ready"
    else
        echo "L Maintenance script: Not found or not executable"
    fi
    
    case "$os_type" in
        "macos")
            echo "Scheduler: launchd"
            if [[ -f "$LAUNCHD_PLIST_FILE" ]]; then
                echo " Plist file: Exists"
                
                # Check if job is loaded
                if launchctl list | grep -q "$LAUNCHD_LABEL"; then
                    echo " Status: Running"
                else
                    echo "  Status: Installed but not loaded"
                fi
            else
                echo "L Status: Not installed"
            fi
            ;;
        "linux")
            echo "Scheduler: cron"
            if crontab -l 2>/dev/null | grep -q "$MAINTENANCE_SCRIPT"; then
                echo " Status: Installed"
                echo "Schedule: Hourly"
            else
                echo "L Status: Not installed"
            fi
            ;;
        *)
            echo "L Scheduler: Unsupported OS"
            ;;
    esac
    
    echo
    
    # Check recent maintenance activity
    local maintenance_log="${PROJECT_ROOT}/.claude/memory_maintenance.log"
    if [[ -f "$maintenance_log" ]]; then
        echo "Recent Activity:"
        tail -n 3 "$maintenance_log" | while read -r line; do
            echo "  $line"
        done
    else
        echo "No recent maintenance activity"
    fi
    
    echo
    echo "Log Files:"
    echo "  Setup: $LOG_FILE"
    echo "  Maintenance: ${PROJECT_ROOT}/.claude/memory_maintenance.log"
    echo "  Periodic: ${PROJECT_ROOT}/.claude/periodic_maintenance.log"
}

# Run immediate maintenance
run_immediate() {
    echo "=' Running immediate memory maintenance..."
    log_setup "Running immediate maintenance"
    
    if bash "$MAINTENANCE_SCRIPT" full; then
        echo " Immediate maintenance completed successfully"
        log_setup "Immediate maintenance completed successfully"
    else
        echo "L Immediate maintenance failed"
        log_setup "Immediate maintenance failed"
        exit 1
    fi
}

# Main function
main() {
    local action="${1:-status}"
    
    case "$action" in
        "--enable"|"enable")
            enable_maintenance
            ;;
        "--disable"|"disable")
            disable_maintenance
            ;;
        "--status"|"status")
            show_status
            ;;
        "--run"|"run")
            run_immediate
            ;;
        "-h"|"--help"|"help")
            echo "Usage: $0 [--enable|--disable|--status|--run]"
            echo
            echo "Options:"
            echo "  --enable   Enable periodic memory maintenance"
            echo "  --disable  Disable periodic memory maintenance"
            echo "  --status   Show current maintenance status"
            echo "  --run      Run immediate maintenance"
            echo "  --help     Show this help message"
            echo
            echo "The maintenance system runs automatically every hour when enabled."
            ;;
        *)
            echo "Unknown option: $action"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"