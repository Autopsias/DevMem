#!/bin/bash

# Universal Code Quality Enforcer
# Purpose: Automatic code quality enforcement for Python projects
# Usage: Called automatically by Claude Code edit hooks

set -euo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/code_quality_enforcement.log"
readonly AGENT_REGISTRY="${PROJECT_ROOT}/.claude/agent_registry.json"

# Logging function
log_quality() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] QUALITY_ENFORCER: $1" >> "$LOG_FILE"
}

# Check if file is a Python file
is_python_file() {
    local file_path="${1:-}"
    [[ "$file_path" =~ \.py$ ]]
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
            log_quality "FILE_SIZE_VIOLATION: $file_path has $line_count lines (test file limit: 1000)"
            return 1
        fi
    else
        # Implementation files can be up to 750 lines
        if [[ "$line_count" -gt 750 ]]; then
            echo "❌ File size violation: $file_path has $line_count lines (max 750 for implementation)"
            log_quality "FILE_SIZE_VIOLATION: $file_path has $line_count lines (implementation limit: 750)"
            return 1
        fi
    fi
    
    return 0
}

# Run basic Python linting
run_basic_linting() {
    local file_path="$1"
    local has_issues=false
    
    # Check if ruff is available
    if command -v ruff &> /dev/null; then
        echo "🔍 Running ruff check on $file_path"
        if ! ruff check "$file_path" --quiet 2>/dev/null; then
            echo "⚠️ Ruff found linting issues in $file_path"
            log_quality "RUFF_ISSUES: $file_path has linting violations"
            has_issues=true
        fi
    fi
    
    # Check if black is available
    if command -v black &> /dev/null; then
        echo "🔍 Running black check on $file_path"
        if ! black --check --quiet "$file_path" 2>/dev/null; then
            echo "⚠️ Black found formatting issues in $file_path"
            log_quality "BLACK_ISSUES: $file_path has formatting violations"
            has_issues=true
        fi
    fi
    
    # Check if isort is available
    if command -v isort &> /dev/null; then
        echo "🔍 Running isort check on $file_path"
        if ! isort --check-only --quiet "$file_path" 2>/dev/null; then
            echo "⚠️ Isort found import sorting issues in $file_path"
            log_quality "ISORT_ISSUES: $file_path has import sorting violations"
            has_issues=true
        fi
    fi
    
    if [[ "$has_issues" == "true" ]]; then
        return 1
    fi
    
    return 0
}

# Check for common code quality issues
check_basic_quality() {
    local file_path="$1"
    local has_issues=false
    
    if [[ ! -f "$file_path" ]]; then
        return 0
    fi
    
    # Check for common anti-patterns
    if grep -q "data\s*=" "$file_path" || grep -q "result\s*=" "$file_path" || grep -q "temp\s*=" "$file_path"; then
        echo "⚠️ Found non-descriptive variable names in $file_path (data, result, temp)"
        log_quality "VARIABLE_NAMING: $file_path contains non-descriptive variable names"
        has_issues=true
    fi
    
    # Check for functions without type hints (basic check)
    if grep -q "def [^_].*(" "$file_path" && ! grep -q "def.*->.*:" "$file_path"; then
        echo "⚠️ Functions without type hints detected in $file_path"
        log_quality "TYPE_HINTS: $file_path may be missing type hints"
        has_issues=true
    fi
    
    # Check for overly long functions (basic check)
    local in_function=false
    local function_line_count=0
    local function_name=""
    
    while IFS= read -r line; do
        if [[ "$line" =~ ^[[:space:]]*def[[:space:]]+([^(]+) ]]; then
            if [[ "$in_function" == "true" && "$function_line_count" -gt 50 ]]; then
                echo "⚠️ Function '$function_name' is too long ($function_line_count lines, max 50) in $file_path"
                log_quality "FUNCTION_LENGTH: $function_name in $file_path has $function_line_count lines"
                has_issues=true
            fi
            in_function=true
            function_line_count=1
            function_name="${BASH_REMATCH[1]}"
        elif [[ "$in_function" == "true" ]]; then
            if [[ "$line" =~ ^[[:space:]]*def[[:space:]] ]] || [[ "$line" =~ ^[[:space:]]*class[[:space:]] ]] || [[ -z "${line// }" ]]; then
                if [[ "$function_line_count" -gt 50 ]]; then
                    echo "⚠️ Function '$function_name' is too long ($function_line_count lines, max 50) in $file_path"
                    log_quality "FUNCTION_LENGTH: $function_name in $file_path has $function_line_count lines"
                    has_issues=true
                fi
                in_function=false
            else
                ((function_line_count++))
            fi
        fi
    done < "$file_path"
    
    if [[ "$has_issues" == "true" ]]; then
        return 1
    fi
    
    return 0
}

# Suggest agent coordination based on issues found
suggest_agent_coordination() {
    local file_path="$1"
    local issues_found="$2"
    
    echo ""
    echo "🤖 Agent Coordination Suggestion:"
    
    if [[ "$issues_found" =~ "FILE_SIZE_VIOLATION" ]]; then
        echo "  💡 File size violations detected in $file_path"
        echo "  📋 Consider: 'I have oversized files that need systematic refactoring'"
        echo "  🎯 This will activate: file-size-enforcer agent for compliance enforcement"
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
    
    # Update agent registry if it exists
    if [[ -f "$AGENT_REGISTRY" ]]; then
        # Simple JSON update - in a real implementation, you'd use jq
        echo "$(date '+%Y-%m-%d %H:%M:%S'): Quality issues detected in $file_path" >> "${AGENT_REGISTRY}.log"
    fi
}

# Main quality enforcement function
enforce_quality() {
    local file_path="${CLAUDE_TOOL_PARAMETER_file_path:-${1:-}}"
    local issues_found=""
    
    if [[ -z "$file_path" ]]; then
        log_quality "No file path provided - skipping quality enforcement"
        return 0
    fi
    
    # Only process Python files
    if ! is_python_file "$file_path"; then
        log_quality "Skipping non-Python file: $file_path"
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

# Main function
main() {
    enforce_quality "$@"
    
    # Keep log manageable
    if [[ -f "$LOG_FILE" && $(wc -l < "$LOG_FILE" 2>/dev/null || echo "0") -gt 200 ]]; then
        tail -n 100 "$LOG_FILE" > "${LOG_FILE}.tmp" 2>/dev/null && mv "${LOG_FILE}.tmp" "$LOG_FILE" 2>/dev/null || true
    fi
    
    exit 0
}

# Run main function
main "$@"