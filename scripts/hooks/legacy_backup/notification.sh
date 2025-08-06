#!/bin/bash

# Universal Notification Handler
# Purpose: Lightweight notification system for Claude Code operations
# Usage: Called automatically by Claude Code notification hooks

set -euo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/notifications.log"

# Logging function
log_notification() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] NOTIFICATION: $1" >> "$LOG_FILE"
}

# Play notification sound if available and enabled
play_notification_sound() {
    local sound_type="${1:-default}"
    
    if [[ "${CLAUDE_AUDIO_ALERTS:-false}" == "true" ]]; then
        if command -v afplay &> /dev/null; then
            case "$sound_type" in
                "success")
                    afplay /System/Library/Sounds/Glass.aiff 2>/dev/null &
                    ;;
                "warning")
                    afplay /System/Library/Sounds/Sosumi.aiff 2>/dev/null &
                    ;;
                "error")
                    afplay /System/Library/Sounds/Basso.aiff 2>/dev/null &
                    ;;
                *)
                    afplay /System/Library/Sounds/Ping.aiff 2>/dev/null &
                    ;;
            esac
        fi
    fi
}

# Send desktop notification if available
send_desktop_notification() {
    local title="$1"
    local message="$2"
    local type="${3:-info}"
    
    # Try different notification systems
    if command -v osascript &> /dev/null; then
        # macOS notification
        osascript -e "display notification \"$message\" with title \"$title\"" 2>/dev/null || true
    elif command -v notify-send &> /dev/null; then
        # Linux notification
        notify-send "$title" "$message" 2>/dev/null || true
    fi
}

# Handle different types of notifications
handle_notification() {
    local notification_type="${1:-}"
    local notification_text="${CLAUDE_NOTIFICATION_TEXT:-${2:-}}"
    
    case "$notification_type" in
        "edit_complete")
            log_notification "File edit completed"
            echo "📝 File edit completed successfully"
            play_notification_sound "success"
            send_desktop_notification "Claude Code" "File edit completed" "success"
            ;;
        "write_complete")
            log_notification "File write completed"
            echo "✍️ File write completed successfully"
            play_notification_sound "success"
            send_desktop_notification "Claude Code" "File write completed" "success"
            ;;
        "quality_check")
            log_notification "Quality check completed: $notification_text"
            echo "🔍 Quality check: $notification_text"
            play_notification_sound "default"
            send_desktop_notification "Claude Code Quality" "$notification_text" "info"
            ;;
        "security_alert")
            log_notification "Security alert: $notification_text"
            echo "🔒 Security alert: $notification_text"
            play_notification_sound "warning"
            send_desktop_notification "Claude Code Security" "$notification_text" "warning"
            ;;
        "agent_suggestion")
            log_notification "Agent suggestion: $notification_text"
            echo "🤖 Agent suggestion: $notification_text"
            play_notification_sound "default"
            send_desktop_notification "Claude Code Agents" "$notification_text" "info"
            ;;
        "task_complete")
            log_notification "Task completed: $notification_text"
            echo "✅ Task completed: $notification_text"
            play_notification_sound "success"
            send_desktop_notification "Claude Code" "Task completed: $notification_text" "success"
            ;;
        "error")
            log_notification "Error: $notification_text"
            echo "❌ Error: $notification_text"
            play_notification_sound "error"
            send_desktop_notification "Claude Code Error" "$notification_text" "error"
            ;;
        "warning")
            log_notification "Warning: $notification_text"
            echo "⚠️ Warning: $notification_text"
            play_notification_sound "warning"
            send_desktop_notification "Claude Code Warning" "$notification_text" "warning"
            ;;
        *)
            log_notification "General notification: $notification_text"
            echo "💬 $notification_text"
            play_notification_sound "default"
            send_desktop_notification "Claude Code" "$notification_text" "info"
            ;;
    esac
}

# Check for environment-based notifications
check_environment_notifications() {
    # Check for approval requirements
    if [[ "${CLAUDE_BASH_NEEDS_APPROVAL:-false}" == "true" ]]; then
        handle_notification "security_alert" "Command requires approval: ${CLAUDE_BASH_APPROVAL_COMMAND:-unknown}"
    fi
    
    # Check for interactive commands
    if [[ "${CLAUDE_INTERACTIVE_COMMAND:-false}" == "true" ]]; then
        handle_notification "warning" "Interactive command detected: ${CLAUDE_INTERACTIVE_COMMAND_TEXT:-unknown}"
    fi
    
    # Check for quality enforcement suggestions
    if [[ -n "${CLAUDE_QUALITY_SUGGESTION:-}" ]]; then
        handle_notification "agent_suggestion" "$CLAUDE_QUALITY_SUGGESTION"
    fi
}

# Display helpful tips based on context
show_context_tips() {
    local context="${1:-general}"
    
    case "$context" in
        "first_run")
            echo ""
            echo "💡 Claude Code Framework Tips:"
            echo "  • Use natural language to describe problems instead of calling agents directly"
            echo "  • Try '/digdeep [problem]' for complex technical investigations"
            echo "  • Use '/testfix' for test failures and '/commit' for intelligent commits"
            echo "  • Quality enforcement runs automatically on file edits"
            ;;
        "quality_issues")
            echo ""
            echo "💡 Quality Improvement Tips:"
            echo "  • Describe quality issues naturally: 'I have linting errors that need fixing'"
            echo "  • For systematic issues: 'I need comprehensive code quality analysis'"
            echo "  • The framework will automatically suggest appropriate agents"
            ;;
        "testing")
            echo ""
            echo "💡 Testing Tips:"
            echo "  • For test failures: 'My tests are failing with async/mock issues'"
            echo "  • For coverage: 'I need to improve test coverage and identify gaps'"
            echo "  • The test-specialist will coordinate with other agents as needed"
            ;;
    esac
}

# Main notification handler
main() {
    local notification_type="${1:-}"
    local notification_text="${2:-}"
    
    # Handle specific notification
    if [[ -n "$notification_type" ]]; then
        handle_notification "$notification_type" "$notification_text"
    fi
    
    # Check for environment-based notifications
    check_environment_notifications
    
    # Show context tips for first-time users
    if [[ ! -f "${PROJECT_ROOT}/.claude/framework_initialized" ]]; then
        show_context_tips "first_run"
        touch "${PROJECT_ROOT}/.claude/framework_initialized" 2>/dev/null || true
    fi
    
    # Keep notification log manageable
    if [[ -f "$LOG_FILE" && $(wc -l < "$LOG_FILE" 2>/dev/null || echo "0") -gt 200 ]]; then
        tail -n 100 "$LOG_FILE" > "${LOG_FILE}.tmp" 2>/dev/null && mv "${LOG_FILE}.tmp" "$LOG_FILE" 2>/dev/null || true
    fi
    
    exit 0
}

# Run main function
main "$@"