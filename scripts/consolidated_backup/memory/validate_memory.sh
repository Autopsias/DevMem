#!/bin/bash

# Memory Validation Script
# Purpose: Comprehensive memory structure and content validation
# Usage: ./validate_memory.sh [--fix] [--report]

set -euo pipefail

# Configuration
readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly MEMORY_DIR="${PROJECT_ROOT}/.claude/memory"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/memory_validation.log"
readonly VALIDATION_REPORT="${PROJECT_ROOT}/.claude/memory_validation_report.md"

# Validation thresholds
readonly MAX_FILE_SIZE_BYTES=102400  # 100KB max per memory file
readonly MIN_FILE_SIZE_BYTES=100     # 100 bytes minimum
readonly MAX_TOTAL_MEMORY_MB=5       # 5MB total memory limit

# Logging function
log_validation() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] VALIDATION: $1" >> "$LOG_FILE"
}

# Report function
report() {
    echo "$1"
    echo "$1" >> "$VALIDATION_REPORT"
}

# Initialize validation report
init_report() {
    cat > "$VALIDATION_REPORT" << 'EOF'
# Memory Validation Report

Generated: $(date '+%Y-%m-%d %H:%M:%S')

## Summary

EOF
}

# Structure validation - check required files and directories exist
validate_memory_structure() {
    log_validation "Starting memory structure validation"
    local issues=0
    
    report "### Memory Structure Validation"
    
    # Check memory directory exists
    if [[ ! -d "$MEMORY_DIR" ]]; then
        report "L ERROR: Memory directory missing: $MEMORY_DIR"
        ((issues++))
        return $issues
    fi
    
    # Required files
    local required_files=(
        "agent-coordination-patterns.md"
    )
    
    # Check required memory files
    for required_file in "${required_files[@]}"; do
        local file_path="${MEMORY_DIR}/${required_file}"
        if [[ ! -f "$file_path" ]]; then
            report "L ERROR: Required memory file missing: $required_file"
            ((issues++))
        else
            report " Required file exists: $required_file"
        fi
    done
    
    # Check for recommended structure
    local recommended_dirs=(
        "domains"
    )
    
    for recommended_dir in "${recommended_dirs[@]}"; do
        local dir_path="${MEMORY_DIR}/${recommended_dir}"
        if [[ ! -d "$dir_path" ]]; then
            report "  WARNING: Recommended directory missing: $recommended_dir"
        else
            report " Recommended directory exists: $recommended_dir"
        fi
    done
    
    log_validation "Structure validation completed with $issues issues"
    return $issues
}

# Content validation - check file content quality and consistency
validate_memory_content() {
    log_validation "Starting memory content validation"
    local issues=0
    
    report "### Memory Content Validation"
    
    # Find all memory markdown files
    local memory_files=()
    while IFS= read -r -d '' file; do
        memory_files+=("$file")
    done < <(find "$MEMORY_DIR" -name "*.md" -type f -print0 2>/dev/null)
    
    report "Found ${#memory_files[@]} memory files to validate"
    
    for memory_file in "${memory_files[@]}"; do
        local filename=$(basename "$memory_file")
        local file_size=$(wc -c < "$memory_file" 2>/dev/null || echo "0")
        
        # File size validation
        if [[ $file_size -lt $MIN_FILE_SIZE_BYTES ]]; then
            report "L ERROR: File too small: $filename (${file_size} bytes < ${MIN_FILE_SIZE_BYTES})"
            ((issues++))
        elif [[ $file_size -gt $MAX_FILE_SIZE_BYTES ]]; then
            report "L ERROR: File too large: $filename (${file_size} bytes > ${MAX_FILE_SIZE_BYTES})"
            ((issues++))
        else
            report " File size OK: $filename (${file_size} bytes)"
        fi
        
        # Content structure validation
        if [[ -s "$memory_file" ]]; then
            # Check for basic markdown structure
            if ! grep -q "^#" "$memory_file" 2>/dev/null; then
                report "  WARNING: No markdown headers in: $filename"
            fi
            
            # Check for empty lines (basic formatting)
            local line_count=$(wc -l < "$memory_file" 2>/dev/null || echo "0")
            local non_empty_lines=$(grep -c "^[[:space:]]*[^[:space:]]" "$memory_file" 2>/dev/null || echo "0")
            
            if [[ $non_empty_lines -gt 0 && $line_count -gt 0 ]]; then
                local content_ratio=$((non_empty_lines * 100 / line_count))
                if [[ $content_ratio -lt 30 ]]; then
                    report "  WARNING: Low content density in: $filename (${content_ratio}%)"
                fi
            fi
        fi
        
        log_validation "Validated content: $filename"
    done
    
    log_validation "Content validation completed with $issues issues"
    return $issues
}

# Performance validation - check memory efficiency and size limits
validate_memory_performance() {
    log_validation "Starting memory performance validation"
    local issues=0
    
    report "### Memory Performance Validation"
    
    # Calculate total memory usage
    local total_size=0
    local file_count=0
    
    while IFS= read -r -d '' file; do
        local size=$(wc -c < "$file" 2>/dev/null || echo "0")
        total_size=$((total_size + size))
        ((file_count++))
    done < <(find "$MEMORY_DIR" -name "*.md" -type f -print0 2>/dev/null)
    
    local total_size_mb=$((total_size / 1024 / 1024))
    local avg_file_size=0
    if [[ $file_count -gt 0 ]]; then
        avg_file_size=$((total_size / file_count))
    fi
    
    report "Memory usage: ${file_count} files, ${total_size} bytes (${total_size_mb}MB), avg ${avg_file_size} bytes"
    
    # Check total size limit
    if [[ $total_size_mb -gt $MAX_TOTAL_MEMORY_MB ]]; then
        report "L ERROR: Total memory exceeds limit: ${total_size_mb}MB > ${MAX_TOTAL_MEMORY_MB}MB"
        ((issues++))
    else
        report " Total memory within limit: ${total_size_mb}MB d ${MAX_TOTAL_MEMORY_MB}MB"
    fi
    
    # Check for duplicate content patterns
    local duplicate_patterns=0
    if [[ $file_count -gt 1 ]]; then
        # Simple duplicate detection: look for files with identical sizes
        local size_counts=$(find "$MEMORY_DIR" -name "*.md" -type f -exec wc -c {} \; 2>/dev/null | \
                           awk '{print $1}' | sort | uniq -d | wc -l)
        if [[ $size_counts -gt 0 ]]; then
            report "  WARNING: Potential duplicate content detected ($size_counts size matches)"
            duplicate_patterns=$size_counts
        fi
    fi
    
    log_validation "Performance validation completed with $issues issues"
    return $issues
}

# Configuration validation - check settings.json integration
validate_memory_configuration() {
    log_validation "Starting memory configuration validation"
    local issues=0
    
    report "### Memory Configuration Validation"
    
    local config_file="${PROJECT_ROOT}/.claude/settings.json"
    
    if [[ ! -f "$config_file" ]]; then
        report "L ERROR: Configuration file missing: settings.json"
        ((issues++))
        return $issues
    fi
    
    # Validate JSON structure
    if ! python3 -c "import json; json.load(open('$config_file'))" 2>/dev/null; then
        report "L ERROR: Invalid JSON in settings.json"
        ((issues++))
        return $issues
    fi
    
    report " Configuration file exists and has valid JSON"
    
    # Check for memory-related configuration
    local memory_config_found=false
    if python3 -c "import json; config=json.load(open('$config_file')); exit(0 if 'memory_hierarchy' in config.get('agents', {}) else 1)" 2>/dev/null; then
        report " Memory hierarchy configuration found"
        memory_config_found=true
    else
        report "  WARNING: Memory hierarchy configuration not found"
    fi
    
    # Check for agent configuration
    if python3 -c "import json; config=json.load(open('$config_file')); exit(0 if 'coordination_patterns' in config.get('agents', {}) else 1)" 2>/dev/null; then
        report " Agent coordination patterns configuration found"
    else
        report "  WARNING: Agent coordination patterns configuration not found"
    fi
    
    log_validation "Configuration validation completed with $issues issues"
    return $issues
}

# Fix function - attempt to fix common issues
fix_memory_issues() {
    log_validation "Starting memory issue fixing"
    
    report "### Memory Issue Fixing"
    
    # Create missing directories
    if [[ ! -d "${MEMORY_DIR}/domains" ]]; then
        mkdir -p "${MEMORY_DIR}/domains"
        report " Created missing domains directory"
    fi
    
    # Create missing required files with basic structure
    if [[ ! -f "${MEMORY_DIR}/agent-coordination-patterns.md" ]]; then
        cat > "${MEMORY_DIR}/agent-coordination-patterns.md" << 'EOF'
# Agent Coordination Patterns

## Overview
This file contains agent coordination patterns for the Claude Code framework.

## Primary Agents
- Analysis and coordination patterns will be automatically populated

## Memory Integration
- Patterns are automatically learned and stored
- Configuration is maintained through settings.json
EOF
        report " Created missing agent-coordination-patterns.md"
    fi
    
    # Remove empty files
    local removed_files=0
    while IFS= read -r -d '' file; do
        if [[ ! -s "$file" ]]; then
            rm -f "$file"
            report " Removed empty file: $(basename "$file")"
            ((removed_files++))
        fi
    done < <(find "$MEMORY_DIR" -name "*.md" -type f -print0 2>/dev/null)
    
    if [[ $removed_files -gt 0 ]]; then
        report "Removed $removed_files empty files"
    fi
    
    log_validation "Memory issue fixing completed"
}

# Generate summary report
generate_summary() {
    local total_issues=$1
    
    report ""
    report "## Validation Summary"
    report ""
    
    if [[ $total_issues -eq 0 ]]; then
        report " **Memory validation PASSED** - No issues found"
        log_validation "Memory validation PASSED"
    else
        report "L **Memory validation FAILED** - $total_issues issues found"
        log_validation "Memory validation FAILED with $total_issues issues"
    fi
    
    report ""
    report "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
    
    echo
    echo "Validation report saved to: $VALIDATION_REPORT"
    echo "Full log available at: $LOG_FILE"
}

# Main validation function
run_validation() {
    local fix_issues="${1:-false}"
    local show_report="${2:-false}"
    
    log_validation "Starting memory validation (fix=$fix_issues, report=$show_report)"
    
    # Initialize report
    init_report
    
    local total_issues=0
    
    # Run all validations
    validate_memory_structure || total_issues=$((total_issues + $?))
    validate_memory_content || total_issues=$((total_issues + $?))
    validate_memory_performance || total_issues=$((total_issues + $?))
    validate_memory_configuration || total_issues=$((total_issues + $?))
    
    # Fix issues if requested
    if [[ "$fix_issues" == "true" ]]; then
        fix_memory_issues
        # Re-run critical validations after fixing
        report ""
        report "### Re-validation After Fixes"
        validate_memory_structure || true
    fi
    
    # Generate summary
    generate_summary $total_issues
    
    # Show report if requested
    if [[ "$show_report" == "true" ]] || [[ $total_issues -gt 0 ]]; then
        echo
        cat "$VALIDATION_REPORT"
    fi
    
    return $total_issues
}

# Command line argument processing
main() {
    local fix_issues=false
    local show_report=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --fix)
                fix_issues=true
                shift
                ;;
            --report)
                show_report=true
                shift
                ;;
            -h|--help)
                echo "Usage: $0 [--fix] [--report]"
                echo "  --fix    Attempt to fix common memory issues"
                echo "  --report Show detailed validation report"
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    run_validation "$fix_issues" "$show_report"
}

# Execute main function
main "$@"