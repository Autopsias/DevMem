#!/bin/bash

# Universal Code Quality Enforcer
# Purpose: Automatic code quality enforcement for Python projects ONLY
# Usage: Called automatically by Claude Code edit hooks
# Fixed: Proper file filtering and syntax error resolution

set -euo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/code_quality_enforcement.log"
readonly AGENT_REGISTRY="${PROJECT_ROOT}/.claude/agent_registry.json"

# Logging function
log_quality() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] QUALITY_ENFORCER: $1" >> "$LOG_FILE"
}

# Extract file path from hook input following Anthropic guidelines
extract_file_path_from_hook_input() {
    # Method 1: Try JSON parsing if jq is available and HOOK_INPUT exists
    if [[ -n "${HOOK_INPUT:-}" ]] && command -v jq >/dev/null 2>&1; then
        local json_path
        json_path=$(echo "$HOOK_INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
        if [[ -n "$json_path" && "$json_path" != "null" ]]; then
            echo "$json_path"
            return 0
        fi
    fi
    
    # Method 2: Claude Code environment parameter
    if [[ -n "${CLAUDE_TOOL_PARAMETER_file_path:-}" ]]; then
        echo "${CLAUDE_TOOL_PARAMETER_file_path}"
        return 0
    fi
    
    # Method 3: Command line argument fallback
    if [[ -n "${1:-}" ]]; then
        echo "$1"
        return 0
    fi
    
    # Method 4: Try to extract from stdin if available
    if [[ -p /dev/stdin ]] && command -v jq >/dev/null 2>&1; then
        local stdin_path
        stdin_path=$(jq -r '.tool_input.file_path // empty' 2>/dev/null)
        if [[ -n "$stdin_path" && "$stdin_path" != "null" ]]; then
            echo "$stdin_path"
            return 0
        fi
    fi
    
    # Return empty if no path found
    echo ""
}

# Check if file is a Python file - EARLY EXIT PATTERN
is_python_file() {
    local file_path="${1:-}"
    [[ "$file_path" =~ \.py$ ]]
}

# EARLY EXIT: Check file type immediately and exit if not Python (Enhanced with JSON support)
early_exit_if_not_python() {
    # Use enhanced file path extraction following Anthropic guidelines
    local file_path
    file_path=$(extract_file_path_from_hook_input "$@")
    
    # Exit early if no file path provided
    if [[ -z "$file_path" ]]; then
        log_quality "No file path provided - skipping quality enforcement"
        exit 0
    fi
    
    # Exit early if not a Python file - THIS IS THE KEY FIX
    if ! is_python_file "$file_path"; then
        log_quality "Skipping non-Python file: $file_path (method: $(get_detection_method "$file_path"))"
        exit 0
    fi
    
    log_quality "Processing Python file: $file_path (method: $(get_detection_method "$file_path"))"
    # Store file path for use in other functions
    export PROCESSED_FILE_PATH="$file_path"
}

# Helper function to identify which method was used to detect the file path (for debugging)
get_detection_method() {
    local file_path="$1"
    
    if [[ -n "${HOOK_INPUT:-}" ]] && command -v jq >/dev/null 2>&1; then
        local json_path
        json_path=$(echo "$HOOK_INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
        if [[ "$json_path" == "$file_path" ]]; then
            echo "JSON_HOOK_INPUT"
            return
        fi
    fi
    
    if [[ "${CLAUDE_TOOL_PARAMETER_file_path:-}" == "$file_path" ]]; then
        echo "CLAUDE_PARAMETER"
        return
    fi
    
    echo "COMMAND_LINE_ARG"
}

# Check if file is a test file
is_test_file() {
    local file_path="${1:-}"
    [[ "$file_path" =~ test.*\.py$ ]] || [[ "$file_path" =~ .*_test\.py$ ]] || [[ "$file_path" =~ tests/.*\.py$ ]]
}

# Get file line count
get_line_count() {
    local file_path="$1"
    if [[ -f "$file_path" ]]; then
        wc -l < "$file_path" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

# Check file size limits
check_file_size_limits() {
    local file_path="$1"
    local line_count
    line_count=$(get_line_count "$file_path")
    
    if is_test_file "$file_path"; then
        # Test files can be up to 1000 lines
        if [[ "$line_count" -gt 1000 ]]; then
            echo "❌ File size violation: $file_path has $line_count lines (max 1000 for tests)"
            return 1
        fi
    else
        # Regular implementation files can be up to 750 lines
        if [[ "$line_count" -gt 750 ]]; then
            echo "❌ File size violation: $file_path has $line_count lines (max 750 for implementation)"
            return 1
        fi
    fi
    
    return 0
}

# Run basic linting checks (Enhanced with better error handling and timeout)
run_basic_linting() {
    local file_path="$1"
    local linting_passed=true
    local timeout_duration=30  # 30 second timeout for linting operations
    
    # Safety check for file existence
    if [[ ! -f "$file_path" ]]; then
        log_quality "WARNING: File does not exist for linting: $file_path"
        return 0  # Don't fail if file doesn't exist
    fi
    
    # Check for ruff if available (with timeout and error handling)
    if command -v ruff >/dev/null 2>&1; then
        if ! timeout "$timeout_duration" ruff check "$file_path" >/dev/null 2>&1; then
            local exit_code=$?
            if [[ $exit_code -eq 124 ]]; then
                echo "⚠️ Ruff check timed out for $file_path"
                log_quality "WARNING: Ruff timeout for $file_path"
            else
                echo "⚠️ Ruff linting issues detected in $file_path"
            fi
            linting_passed=false
        fi
    fi
    
    # Check for black formatting if available (with timeout and error handling)
    if command -v black >/dev/null 2>&1; then
        if ! timeout "$timeout_duration" black --check --quiet "$file_path" >/dev/null 2>&1; then
            local exit_code=$?
            if [[ $exit_code -eq 124 ]]; then
                echo "⚠️ Black check timed out for $file_path"
                log_quality "WARNING: Black timeout for $file_path"
            else
                echo "⚠️ Black formatting issues detected in $file_path"
            fi
            linting_passed=false
        fi
    fi
    
    # Check for isort if available (with timeout and error handling)
    if command -v isort >/dev/null 2>&1; then
        if ! timeout "$timeout_duration" isort --check-only --quiet "$file_path" >/dev/null 2>&1; then
            local exit_code=$?
            if [[ $exit_code -eq 124 ]]; then
                echo "⚠️ Isort check timed out for $file_path"
                log_quality "WARNING: Isort timeout for $file_path"
            else
                echo "⚠️ Import sorting issues detected in $file_path"
            fi
            linting_passed=false
        fi
    fi
    
    $linting_passed
}

# Check basic code quality (Enhanced with better pattern matching and error handling)
check_basic_quality() {
    local file_path="$1"
    local quality_passed=true
    
    # Safety check for file existence
    if [[ ! -f "$file_path" ]]; then
        log_quality "WARNING: File does not exist for quality check: $file_path"
        return 0  # Don't fail if file doesn't exist
    fi
    
    # Additional safety: check if file is readable
    if [[ ! -r "$file_path" ]]; then
        log_quality "WARNING: File is not readable for quality check: $file_path"
        return 0
    fi
        # Check for basic type hints (functions without type hints)
        if grep -q "^def " "$file_path" && ! grep -q "def.*:" "$file_path"; then
            echo "💡 Consider adding type hints to functions in $file_path"
            quality_passed=false
        fi
        
        # Check for variable naming (basic check for single-letter vars except in loops)
        if grep -q "\b[a-z]\s*=" "$file_path" && ! grep -q "for [a-z] in\|for [a-z]," "$file_path"; then
            echo "💡 Consider using descriptive variable names in $file_path"
            quality_passed=false
        fi
        
        # Check for function length (basic check for very long functions)
        if awk '/^def / {start=NR} /^def / && NR>start+50 {print "Long function detected"; exit 1}' "$file_path" >/dev/null 2>&1; then
            echo "💡 Consider breaking down long functions in $file_path"
            quality_passed=false
        fi
    
    $quality_passed
}

# Suggest agent coordination based on issues found
suggest_agent_coordination() {
    local file_path="$1"
    local issues_found="$2"
    
    echo "🤖 Agent Coordination Suggestions for $file_path:"
    
    if [[ "$issues_found" =~ "FILE_SIZE_VIOLATION" ]]; then
        echo "  💡 File size violations detected in $file_path"
        echo "  📋 Consider: 'I have file size limit violations that need refactoring'"
        echo "  🎯 This will activate: file-size-enforcer agent for systematic file splitting"
    fi
    
    if [[ "$issues_found" =~ "RUFF_ISSUES|BLACK_ISSUES|ISORT_ISSUES" ]]; then
        echo "  💡 Linting violations detected in $file_path"
        echo "  📋 Consider: 'I have linting errors that need systematic resolution'"
        echo "  🎯 This will activate: lint-enforcer agent for efficient tool execution"
    fi
    
    if [[ "$issues_found" =~ "TYPE_HINTS|VARIABLE_NAMING|FUNCTION_LENGTH" ]]; then
        echo "  💡 Code quality issues detected in $file_path"
        echo "  📋 Consider: 'I need comprehensive code quality analysis and improvement'"
        echo "  🎯 This will activate: code-quality-specialist agent for quality analysis"
    fi
    
    # Update agent registry if it exists - FIXED SYNTAX
    if [[ -f "$AGENT_REGISTRY" ]]; then
        # Fixed: Use printf instead of complex echo with nested quotes
        printf '%s: Quality issues detected in %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$file_path" >> "${AGENT_REGISTRY}.log"
    fi
}

# Main quality enforcement function (Enhanced with better error handling)
enforce_quality() {
    # Use the processed file path that was validated in early_exit_if_not_python
    local file_path="${PROCESSED_FILE_PATH:-$(extract_file_path_from_hook_input "$@")}"
    local issues_found=""
    
    # Additional safety check (should not be needed due to early exit, but defensive programming)
    if [[ -z "$file_path" ]]; then
        log_quality "ERROR: No file path available in enforce_quality function"
        return 0
    fi
    
    if ! is_python_file "$file_path"; then
        log_quality "ERROR: Non-Python file reached enforce_quality function: $file_path"
        return 0
    fi
    
    echo "🔍 Enforcing code quality for: $file_path"
    log_quality "QUALITY_CHECK_START: $file_path"
    
    # Check file size limits
    if ! check_file_size_limits "$file_path"; then
        issues_found="${issues_found}FILE_SIZE_VIOLATION "
    fi
    
    # Run basic linting checks
    if ! run_basic_linting "$file_path"; then
        issues_found="${issues_found}LINTING_ISSUES "
    fi
    
    # Check basic code quality
    if ! check_basic_quality "$file_path"; then
        issues_found="${issues_found}QUALITY_ISSUES "
    fi
    
    if [[ -n "$issues_found" ]]; then
        log_quality "ISSUES_FOUND: $file_path - $issues_found"
        suggest_agent_coordination "$file_path" "$issues_found"
        echo ""
        echo "✅ Quality enforcement completed with suggestions"
    else
        log_quality "QUALITY_PASSED: $file_path passed all quality checks"
        echo "✅ Code quality enforcement passed for $file_path"
    fi
    
    return 0
}

# Main function with EARLY EXIT
main() {
    # CRITICAL: Early exit for non-Python files BEFORE any other processing
    early_exit_if_not_python "$@"
    
    # If we reach here, we have a Python file to process
    enforce_quality "$@"
    
    # Keep log manageable
    if [[ -f "$LOG_FILE" && $(wc -l < "$LOG_FILE" 2>/dev/null || echo "0") -gt 200 ]]; then
        tail -n 100 "$LOG_FILE" > "${LOG_FILE}.tmp" 2>/dev/null && mv "${LOG_FILE}.tmp" "$LOG_FILE" 2>/dev/null || true
    fi
    
    exit 0
}

# Run main function
main "$@"