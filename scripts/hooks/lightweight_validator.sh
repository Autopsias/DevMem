#!/bin/bash

# Lightweight Validator for Read Operations
# Purpose: Fast validation for read-only operations without Claude usage
# Usage: Called automatically by Claude Code hooks

set -euo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/lightweight_validation.log"

# Logging function
log_validation() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] LIGHTWEIGHT_VALIDATOR: $1" >> "$LOG_FILE"
}

# Validate file path is within workspace
validate_workspace_confinement() {
    local file_path="$1"

    # Resolve absolute paths
    local abs_path
    abs_path=$(realpath "$file_path" 2>/dev/null || echo "$file_path")
    local abs_project_root
    abs_project_root=$(realpath "$PROJECT_ROOT")

    # Allow /tmp for testing purposes
    if [[ "$abs_path" =~ ^/tmp/ ]]; then
        log_validation "ALLOWED: Temporary file access for testing: $file_path"
        return 0
    fi

    # Check if path is within project
    if [[ "$abs_path" != "$abs_project_root"* ]]; then
        log_validation "BLOCKED: Path traversal attempt: $file_path"
        echo "🚨 Security Validator: BLOCKED - Path outside workspace"
        echo "  - Attempted: $file_path"
        echo "  - Policy: All operations must stay within project workspace"
        return 1
    fi

    return 0
}

# Check for dangerous patterns in file paths
check_dangerous_patterns() {
    local file_path="$1"

    # Dangerous path patterns
    if [[ "$file_path" =~ \.\./|/etc/|/var/|/usr/bin|/usr/sbin ]]; then
        log_validation "BLOCKED: Dangerous path pattern: $file_path"
        echo "🚨 Security Validator: BLOCKED - Dangerous path pattern"
        echo "  - Pattern: System directory access attempt"
        echo "  - File: $file_path"
        return 1
    fi

    # Check for sensitive file patterns
    if [[ "$file_path" =~ \.(key|pem|p12|pfx)$ ]]; then
        log_validation "WARNING: Sensitive file access: $file_path"
        echo "⚠️ Security Validator: Sensitive file access detected"
        echo "  - File: $file_path"
        echo "  - Type: Potential credential file"
    fi

    return 0
}

# Quick file size validation
validate_file_size() {
    local file_path="$1"

    if [[ -f "$file_path" ]]; then
        local file_size_mb
        file_size_mb=$(du -m "$file_path" | cut -f1)

        if (( file_size_mb > 100 )); then
            log_validation "WARNING: Large file access: $file_path ($file_size_mb MB)"
            echo "⚠️ Lightweight Validator: Large file detected"
            echo "  - File: $file_path"
            echo "  - Size: ${file_size_mb}MB"
            echo "  - Consider: File may require special handling"
        fi
    fi

    return 0
}

# Main validation function
main() {
    local file_path="${CLAUDE_TOOL_PARAMETER_file_path:-${CLAUDE_TOOL_PARAMETER_path:-}}"

    # Ensure log directory exists
    mkdir -p "$(dirname "$LOG_FILE")"
    touch "$LOG_FILE"

    # If no file path provided, exit successfully (not all operations have file paths)
    if [[ -z "$file_path" ]]; then
        log_validation "No file path provided - skipping validation"
        exit 0
    fi

    log_validation "Validating read operation for: $file_path"

    # Run validation checks
    if ! validate_workspace_confinement "$file_path"; then
        exit 2  # Blocking error
    fi

    if ! check_dangerous_patterns "$file_path"; then
        exit 2  # Blocking error
    fi

    validate_file_size "$file_path"  # Non-blocking warnings

    log_validation "Validation passed for: $file_path"
    echo "✅ Lightweight validation completed"
    exit 0
}

# Run main function
main "$@"
