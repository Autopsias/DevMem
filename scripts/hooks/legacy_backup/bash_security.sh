#!/bin/bash

# Universal Bash Security Handler
# Purpose: Lightweight security check for Bash operations in any Python project
# Usage: Called automatically by Claude Code bash hooks

set -euo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/bash_security.log"

# Logging function
log_security() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] BASH_SECURITY: $1" >> "$LOG_FILE"
}

# Check if command typically requires user approval
check_approval_needed() {
    local command="${1:-}"

    # Commands that typically need user approval or confirmation
    if [[ "$command" =~ (git\s+push|git\s+commit|git\s+merge|git\s+rebase) ]] || \
       [[ "$command" =~ (rm\s+.*\.(env|config|key|pem|crt)|rm\s+.*important) ]] || \
       [[ "$command" =~ (pip\s+install|poetry\s+add|npm\s+install|yarn\s+add) ]] || \
       [[ "$command" =~ (docker\s+run|docker-compose\s+up|make\s+deploy) ]] || \
       [[ "$command" =~ (chmod\s+.*\.(sh|py|js)|mv\s+.*\.(env|config)) ]] || \
       [[ "$command" =~ (curl.*install|wget.*install|bash.*install) ]]; then
        return 0  # Approval needed
    fi

    return 1  # No approval needed
}

# Check if command is likely to trigger interactive prompts
check_interactive_command() {
    local command="${1:-}"

    # Interactive command patterns that typically prompt for user input
    if [[ "$command" =~ timeout\s+[0-9]+.*pytest ]] || \
       [[ "$command" =~ timeout\s+[0-9]+.*python.*test ]] || \
       [[ "$command" =~ timeout.*tests/(integration|performance|e2e) ]] || \
       [[ "$command" =~ python.*test.*integration ]] || \
       [[ "$command" =~ make.*test-(coverage|integration|e2e) ]] || \
       [[ "$command" =~ \./scripts/.*runner\.sh ]] || \
       [[ "$command" =~ docker-compose.*up.*-d ]] || \
       [[ "$command" =~ make.*docker-up ]] || \
       [[ "$command" =~ kubectl.*apply ]] || \
       [[ "$command" =~ gh.*workflow.*run ]]; then
        return 0  # Interactive prompt likely
    fi

    return 1  # No interactive prompt expected
}

# Trigger approval alert for commands that need confirmation
trigger_approval_alert() {
    local command="$1"
    local alert_reason="$2"

    # Set environment variable for other hooks to detect
    export CLAUDE_BASH_NEEDS_APPROVAL="true"
    export CLAUDE_BASH_APPROVAL_COMMAND="$command"
    export CLAUDE_BASH_APPROVAL_REASON="$alert_reason"

    # Immediate sound alert if audio is enabled
    if [[ "${CLAUDE_AUDIO_ALERTS:-false}" == "true" ]]; then
        if command -v afplay &> /dev/null; then
            # Play distinctive approval sound
            afplay /System/Library/Sounds/Sosumi.aiff 2>/dev/null &
        fi
    fi

    # Log approval requirement
    log_security "APPROVAL_NEEDED: $command ($alert_reason)"
    echo "🔔 Approval Required: $alert_reason"
    echo "  - Command: $command"
    echo "  - Please confirm this action"
}

# Trigger interactive alert for commands likely to prompt for user input
trigger_interactive_alert() {
    local command="$1"
    local alert_reason="$2"

    # Set environment variable for other hooks to detect
    export CLAUDE_INTERACTIVE_COMMAND="true"
    export CLAUDE_INTERACTIVE_COMMAND_TEXT="$command"
    export CLAUDE_INTERACTIVE_REASON="$alert_reason"

    # Play attention sound if audio is enabled (proactive notification)
    if [[ "${CLAUDE_AUDIO_ALERTS:-false}" == "true" ]]; then
        if command -v afplay &> /dev/null; then
            # Play attention sound to alert user of upcoming interactive prompt
            afplay /System/Library/Sounds/Ping.aiff 2>/dev/null &
            sleep 0.3
            # Follow with distinctive Sosumi for user input scenarios
            afplay /System/Library/Sounds/Sosumi.aiff 2>/dev/null &
        fi
    fi

    # Log interactive command detection
    log_security "INTERACTIVE_COMMAND: $command ($alert_reason)"
    echo "🔔 Interactive Command Detected: $alert_reason"
    echo "  - Command: $command"
    echo "  - Expect user input prompt during execution"
}

# Basic security validation for bash commands
validate_bash_command() {
    local command="${CLAUDE_TOOL_PARAMETER_command:-${1:-}}"

    if [[ -z "$command" ]]; then
        log_security "No command provided - allowing"
        return 0
    fi

    # Check for dangerous patterns
    if [[ "$command" =~ (rm\s+-rf\s+/|format\s+|del\s+/|rmdir\s+/|sudo\s+rm) ]]; then
        log_security "BLOCKED: Dangerous command pattern: $command"
        echo "🚨 Security: BLOCKED dangerous bash command"
        echo "  - Command: $command"
        echo "  - Reason: Potential system damage"
        trigger_approval_alert "$command" "Dangerous system operation"
        return 1
    fi

    # Check for excessive privileges
    if [[ "$command" =~ (sudo|su\s+|chmod\s+777|chown\s+-R) ]]; then
        log_security "WARNING: Privileged command: $command"
        echo "⚠️ Security: Privileged command detected"
        echo "  - Command: $command"
        echo "  - Recommendation: Verify necessity"
        trigger_approval_alert "$command" "Privileged operation"
    fi

    # Check if command needs approval (non-blocking)
    if check_approval_needed "$command"; then
        trigger_approval_alert "$command" "User confirmation recommended"
    fi

    # Check if command is likely to be interactive (non-blocking notification)
    if check_interactive_command "$command"; then
        trigger_interactive_alert "$command" "Command may prompt for user input"
    fi

    log_security "Command validated: $command"
    return 0
}

# Main security handler
main() {
    # Validate bash command security
    if validate_bash_command "$@"; then
        log_security "Bash command security check passed"
    else
        log_security "Bash command security check failed"
        exit 2  # Blocking error
    fi

    # Keep log manageable with safe atomic rotation
    if [[ -f "$LOG_FILE" && $(wc -l < "$LOG_FILE" 2>/dev/null || echo "0") -gt 200 ]]; then
        local temp_file="${LOG_FILE}.tmp.$$"
        if tail -n 100 "$LOG_FILE" > "$temp_file" 2>/dev/null; then
            if mv "$temp_file" "$LOG_FILE" 2>/dev/null; then
                # Log rotation successful - add entry directly to avoid recursion
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] BASH_SECURITY: Log rotated successfully" >> "$LOG_FILE"
            else
                # Failed to move - clean up temp file silently
                rm -f "$temp_file" 2>/dev/null
            fi
        else
            # Failed to create temp file - clean up silently
            rm -f "$temp_file" 2>/dev/null
        fi
    fi

    exit 0
}

# Run main function
main "$@"