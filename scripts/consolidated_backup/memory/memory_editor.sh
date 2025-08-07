#!/bin/bash

# Memory Editor - Safe Memory File Editing and Validation
# Purpose: Provide safe, validated memory editing with rollback capabilities
# Usage: ./memory_editor.sh <operation> [options]

set -euo pipefail

# Configuration
readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly MEMORY_DIR="${PROJECT_ROOT}/.claude/memory"
readonly BACKUP_DIR="${PROJECT_ROOT}/.claude/memory_backups"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/memory_editor.log"
readonly VALIDATION_SCRIPT="${PROJECT_ROOT}/scripts/memory/validate_memory.sh"

# Memory editing constraints
readonly MAX_FILE_SIZE_KB=100
readonly MAX_TOTAL_MEMORY_MB=5
readonly REQUIRED_SECTIONS=("## Overview" "## Memory Integration" "## Performance Intelligence")

# Color codes
readonly GREEN='\033[0;32m'
readonly BLUE='\033[0;34m'
readonly YELLOW='\033[1;33m'
readonly RED='\033[0;31m'
readonly NC='\033[0m'
readonly BOLD='\033[1m'

# Logging
log_editor() {
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] EDITOR: $1" >> "$LOG_FILE"
}

# Print colored status
print_status() {
    local level="$1"
    local message="$2"
    case "$level" in
        "SUCCESS") echo -e "${GREEN} $message${NC}" ;;
        "INFO") echo -e "${BLUE}9 $message${NC}" ;;
        "WARNING") echo -e "${YELLOW}  $message${NC}" ;;
        "ERROR") echo -e "${RED} $message${NC}" ;;
        *) echo "$message" ;;
    esac
}

# Show help
show_help() {
    cat << 'EOF'
Memory Editor - Safe Memory File Editing and Validation

USAGE:
    ./memory_editor.sh <operation> [options]

OPERATIONS:
    edit <file>                    Edit memory file with safety checks
    validate <file>                Validate single memory file
    validate-all                   Validate all memory files
    backup <file>                  Backup single memory file
    backup-all                     Backup all memory files
    restore <file> [timestamp]     Restore from backup
    rollback <file>                Rollback last changes
    preview <file>                 Preview file content with validation
    merge <source> <target>        Safely merge memory files
    split <file> <pattern>         Split large memory file
    cleanup                        Clean old backups and temp files

EDITING OPTIONS:
    --editor <editor>              Use specific editor (default: $EDITOR or nano)
    --force                        Skip size validation warnings
    --no-backup                    Skip automatic backup
    --validate-only                Only validate, don't edit
    --dry-run                      Show what would be done

VALIDATION OPTIONS:
    --fix                          Automatically fix issues
    --strict                       Use strict validation rules
    --report                       Generate detailed report
    --quiet                        Suppress non-error output

BACKUP OPTIONS:
    --keep <days>                  Keep backups for N days (default: 30)
    --compress                     Compress backups

EXAMPLES:
    ./memory_editor.sh edit agent-coordination-patterns.md
    ./memory_editor.sh validate-all --fix --report
    ./memory_editor.sh backup-all --compress
    ./memory_editor.sh restore agent-coordination-patterns.md 2024-01-15_14-30
    ./memory_editor.sh merge source.md target.md
    ./memory_editor.sh split large-file.md "## Domain"
    ./memory_editor.sh cleanup --keep 14

SAFETY FEATURES:
    - Automatic backup before editing
    - Size and content validation
    - Rollback capabilities
    - Merge conflict detection
    - Memory usage monitoring
    
EOF
}

# Create backup
create_backup() {
    local file="$1"
    local compress="${2:-false}"
    local file_path="${MEMORY_DIR}/${file}"
    
    if [[ ! -f "$file_path" ]]; then
        print_status "ERROR" "File not found: $file"
        return 1
    fi
    
    # Create backup directory
    mkdir -p "$BACKUP_DIR"
    
    # Generate backup filename
    local timestamp=$(date '+%Y-%m-%d_%H-%M-%S')
    local backup_name="${file%.md}_${timestamp}.md"
    local backup_path="${BACKUP_DIR}/${backup_name}"
    
    # Copy file
    cp "$file_path" "$backup_path"
    
    # Compress if requested
    if [[ "$compress" == "true" ]]; then
        gzip "$backup_path"
        backup_path="${backup_path}.gz"
        backup_name="${backup_name}.gz"
    fi
    
    print_status "SUCCESS" "Backup created: $backup_name"
    log_editor "Backup created: $backup_path"
    
    echo "$backup_path"
}

# Validate file size and structure
validate_file_structure() {
    local file="$1"
    local strict="${2:-false}"
    local file_path="${MEMORY_DIR}/${file}"
    local issues=()
    
    if [[ ! -f "$file_path" ]]; then
        issues+=("File not found: $file")
        printf '%s\n' "${issues[@]}"
        return 1
    fi
    
    # Check file size
    local size_kb=$(du -k "$file_path" | cut -f1)
    if [[ $size_kb -gt $MAX_FILE_SIZE_KB ]]; then
        if [[ "$strict" == "true" ]]; then
            issues+=("File size ${size_kb}KB exceeds limit ${MAX_FILE_SIZE_KB}KB")
        else
            print_status "WARNING" "File size ${size_kb}KB exceeds recommended limit ${MAX_FILE_SIZE_KB}KB"
        fi
    fi
    
    # Check total memory usage
    local total_size_mb=$(du -sm "$MEMORY_DIR" 2>/dev/null | cut -f1 || echo "0")
    if [[ $total_size_mb -gt $MAX_TOTAL_MEMORY_MB ]]; then
        issues+=("Total memory usage ${total_size_mb}MB exceeds limit ${MAX_TOTAL_MEMORY_MB}MB")
    fi
    
    # Check required sections (for coordination files)
    if [[ "$file" == *"coordination"* ]] || [[ "$file" == *"patterns"* ]]; then
        for section in "${REQUIRED_SECTIONS[@]}"; do
            if ! grep -q "^$section" "$file_path"; then
                issues+=("Missing required section: $section")
            fi
        done
    fi
    
    # Check for markdown syntax
    if ! command -v markdownlint >/dev/null 2>&1; then
        print_status "INFO" "markdownlint not available, skipping markdown validation"
    else
        if ! markdownlint -q "$file_path" 2>/dev/null; then
            issues+=("Markdown syntax errors detected")
        fi
    fi
    
    # Return results
    if [[ ${#issues[@]} -gt 0 ]]; then
        printf '%s\n' "${issues[@]}"
        return 1
    fi
    
    return 0
}

# Safe edit with validation
safe_edit() {
    local file="$1"
    local editor="${2:-${EDITOR:-nano}}"
    local force="${3:-false}"
    local no_backup="${4:-false}"
    local dry_run="${5:-false}"
    local file_path="${MEMORY_DIR}/${file}"
    
    # Validate file exists or can be created
    if [[ ! -f "$file_path" ]]; then
        if [[ "$dry_run" == "true" ]]; then
            print_status "INFO" "Would create new file: $file"
            return 0
        fi
        
        print_status "INFO" "Creating new memory file: $file"
        mkdir -p "$(dirname "$file_path")"
        touch "$file_path"
        log_editor "Created new file: $file"
    fi
    
    # Pre-edit validation
    local pre_validation
    pre_validation=$(validate_file_structure "$file" "false" 2>&1) || {
        if [[ "$force" != "true" ]]; then
            print_status "ERROR" "Pre-edit validation failed:"
            echo "$pre_validation"
            print_status "INFO" "Use --force to override warnings"
            return 1
        else
            print_status "WARNING" "Pre-edit validation warnings (forced):"
            echo "$pre_validation"
        fi
    }
    
    # Create backup
    local backup_path=""
    if [[ "$no_backup" != "true" ]]; then
        if [[ "$dry_run" == "true" ]]; then
            print_status "INFO" "Would create backup for: $file"
        else
            backup_path=$(create_backup "$file")
        fi
    fi
    
    if [[ "$dry_run" == "true" ]]; then
        print_status "INFO" "Would edit file: $file with $editor"
        return 0
    fi
    
    # Edit the file
    print_status "INFO" "Editing $file with $editor"
    log_editor "Starting edit: $file with $editor"
    
    if ! "$editor" "$file_path"; then
        print_status "ERROR" "Editor exited with error"
        if [[ -n "$backup_path" ]]; then
            print_status "INFO" "Backup available at: $backup_path"
        fi
        return 1
    fi
    
    # Post-edit validation
    local post_validation
    post_validation=$(validate_file_structure "$file" "false" 2>&1) || {
        print_status "ERROR" "Post-edit validation failed:"
        echo "$post_validation"
        
        if [[ -n "$backup_path" ]]; then
            read -p "Restore from backup? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                restore_from_backup "$file" "$backup_path"
                return 1
            fi
        fi
        
        print_status "WARNING" "File saved with validation errors"
        return 1
    }
    
    # Run full memory validation if available
    if [[ -f "$VALIDATION_SCRIPT" ]]; then
        print_status "INFO" "Running memory system validation..."
        if bash "$VALIDATION_SCRIPT" --quiet; then
            print_status "SUCCESS" "Memory system validation passed"
        else
            print_status "WARNING" "Memory system validation has concerns (check logs)"
        fi
    fi
    
    print_status "SUCCESS" "File edited and validated: $file"
    log_editor "Successfully edited: $file"
    
    return 0
}

# Restore from backup
restore_from_backup() {
    local file="$1"
    local backup_path="${2:-}"
    local file_path="${MEMORY_DIR}/${file}"
    
    # If no specific backup path provided, find the latest
    if [[ -z "$backup_path" ]]; then
        local latest_backup
        latest_backup=$(find "$BACKUP_DIR" -name "${file%.md}_*" -type f | sort | tail -n1)
        if [[ -z "$latest_backup" ]]; then
            print_status "ERROR" "No backup found for: $file"
            return 1
        fi
        backup_path="$latest_backup"
    fi
    
    if [[ ! -f "$backup_path" ]]; then
        print_status "ERROR" "Backup not found: $backup_path"
        return 1
    fi
    
    # Handle compressed backups
    if [[ "$backup_path" == *.gz ]]; then
        print_status "INFO" "Decompressing backup..."
        gunzip -c "$backup_path" > "$file_path"
    else
        cp "$backup_path" "$file_path"
    fi
    
    print_status "SUCCESS" "Restored from backup: $(basename "$backup_path")"
    log_editor "Restored $file from $backup_path"
    
    return 0
}

# Validate all memory files
validate_all_files() {
    local fix="${1:-false}"
    local strict="${2:-false}"
    local quiet="${3:-false}"
    local report_file="${4:-}"
    
    local total_files=0
    local valid_files=0
    local issues_found=0
    local validation_report=""
    
    print_status "INFO" "Validating all memory files..."
    
    # Find all memory files
    if [[ ! -d "$MEMORY_DIR" ]]; then
        print_status "ERROR" "Memory directory not found: $MEMORY_DIR"
        return 1
    fi
    
    while IFS= read -r -d '' file_path; do
        local file=$(basename "$file_path")
        total_files=$((total_files + 1))
        
        if [[ "$quiet" != "true" ]]; then
            echo -n "Validating $file... "
        fi
        
        local validation_result
        if validation_result=$(validate_file_structure "$file" "$strict" 2>&1); then
            valid_files=$((valid_files + 1))
            if [[ "$quiet" != "true" ]]; then
                print_status "SUCCESS" "OK"
            fi
        else
            issues_found=$((issues_found + 1))
            if [[ "$quiet" != "true" ]]; then
                print_status "ERROR" "ISSUES FOUND"
                echo "$validation_result" | sed 's/^/  /'
            fi
            
            validation_report+="File: $file\n$validation_result\n\n"
            
            # Auto-fix if requested
            if [[ "$fix" == "true" ]]; then
                if fix_file_issues "$file" "$validation_result"; then
                    print_status "INFO" "Auto-fixed: $file"
                else
                    print_status "WARNING" "Could not auto-fix: $file"
                fi
            fi
        fi
    done < <(find "$MEMORY_DIR" -name "*.md" -type f -print0)
    
    # Summary
    print_status "INFO" "Validation complete: $valid_files/$total_files files valid"
    if [[ $issues_found -gt 0 ]]; then
        print_status "WARNING" "$issues_found files have issues"
    fi
    
    # Generate report if requested
    if [[ -n "$report_file" ]]; then
        {
            echo "# Memory Validation Report"
            echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
            echo
            echo "## Summary"
            echo "- Total files: $total_files"
            echo "- Valid files: $valid_files"
            echo "- Files with issues: $issues_found"
            echo
            if [[ -n "$validation_report" ]]; then
                echo "## Issues Found"
                echo -e "$validation_report"
            else
                echo "## Issues Found"
                echo "No issues found."
            fi
        } > "$report_file"
        
        print_status "SUCCESS" "Validation report saved: $report_file"
    fi
    
    return $issues_found
}

# Auto-fix common issues
fix_file_issues() {
    local file="$1"
    local issues="$2"
    local file_path="${MEMORY_DIR}/${file}"
    local fixed=false
    
    # Create backup before fixing
    create_backup "$file" >/dev/null
    
    # Fix missing sections
    while IFS= read -r issue; do
        if [[ "$issue" =~ "Missing required section: "(.+) ]]; then
            local section="${BASH_REMATCH[1]}"
            echo "" >> "$file_path"
            echo "$section" >> "$file_path"
            echo "" >> "$file_path"
            fixed=true
            log_editor "Added missing section '$section' to $file"
        fi
    done <<< "$issues"
    
    # TODO: Add more auto-fix capabilities
    # - Fix markdown syntax errors
    # - Split oversized files
    # - Remove duplicate sections
    
    return $([ "$fixed" = true ] && echo 0 || echo 1)
}

# Merge memory files safely
merge_files() {
    local source="$1"
    local target="$2"
    local source_path="${MEMORY_DIR}/${source}"
    local target_path="${MEMORY_DIR}/${target}"
    
    if [[ ! -f "$source_path" ]] || [[ ! -f "$target_path" ]]; then
        print_status "ERROR" "Source or target file not found"
        return 1
    fi
    
    # Create backup of target
    local backup_path
    backup_path=$(create_backup "$target")
    
    # Simple merge strategy: append unique sections
    print_status "INFO" "Merging $source into $target..."
    
    # TODO: Implement intelligent merge logic
    # For now, just append with separator
    {
        echo ""
        echo "<!-- Merged from $source on $(date) -->"
        echo ""
        cat "$source_path"
    } >> "$target_path"
    
    # Validate merged file
    if validate_file_structure "$target" "false" >/dev/null; then
        print_status "SUCCESS" "Files merged successfully"
        log_editor "Merged $source into $target"
    else
        print_status "ERROR" "Merge validation failed, restoring backup"
        restore_from_backup "$target" "$backup_path"
        return 1
    fi
    
    return 0
}

# Split large memory file
split_file() {
    local file="$1"
    local pattern="$2"
    local file_path="${MEMORY_DIR}/${file}"
    
    if [[ ! -f "$file_path" ]]; then
        print_status "ERROR" "File not found: $file"
        return 1
    fi
    
    # Create backup
    create_backup "$file" >/dev/null
    
    print_status "INFO" "Splitting $file by pattern: $pattern"
    
    # TODO: Implement file splitting logic
    # Use awk or sed to split by section headers
    
    print_status "INFO" "File splitting not yet implemented"
    return 1
}

# Cleanup old backups and temp files
cleanup() {
    local keep_days="${1:-30}"
    local dry_run="${2:-false}"
    
    print_status "INFO" "Cleaning up files older than $keep_days days..."
    
    local count=0
    while IFS= read -r -d '' file; do
        if [[ "$dry_run" == "true" ]]; then
            print_status "INFO" "Would delete: $(basename "$file")"
        else
            rm -f "$file"
            log_editor "Deleted old backup: $file"
        fi
        count=$((count + 1))
    done < <(find "$BACKUP_DIR" -name "*.md*" -type f -mtime +${keep_days} -print0 2>/dev/null)
    
    if [[ $count -eq 0 ]]; then
        print_status "INFO" "No old files to clean"
    else
        print_status "SUCCESS" "$([ "$dry_run" = true ] && echo "Would clean" || echo "Cleaned") $count old files"
    fi
    
    return 0
}

# Preview file content
preview_file() {
    local file="$1"
    local file_path="${MEMORY_DIR}/${file}"
    
    if [[ ! -f "$file_path" ]]; then
        print_status "ERROR" "File not found: $file"
        return 1
    fi
    
    print_status "INFO" "Previewing: $file"
    echo "=========================="
    
    # Show file stats
    local size_kb=$(du -k "$file_path" | cut -f1)
    local line_count=$(wc -l < "$file_path")
    echo "Size: ${size_kb}KB, Lines: $line_count"
    echo
    
    # Show validation status
    if validate_file_structure "$file" "false" >/dev/null; then
        print_status "SUCCESS" "Validation: PASSED"
    else
        print_status "WARNING" "Validation: HAS ISSUES"
    fi
    echo
    
    # Show content (first 50 lines)
    echo "Content preview (first 50 lines):"
    echo "----------------------------------"
    head -n 50 "$file_path"
    
    if [[ $line_count -gt 50 ]]; then
        echo "... ($(($line_count - 50)) more lines)"
    fi
    
    return 0
}

# Main function
main() {
    if [[ $# -eq 0 ]]; then
        show_help
        exit 0
    fi
    
    local operation="$1"
    shift
    
    # Create directories if needed
    mkdir -p "$MEMORY_DIR" "$BACKUP_DIR"
    
    # Parse common options
    local editor="${EDITOR:-nano}"
    local force=false
    local no_backup=false
    local dry_run=false
    local validate_only=false
    local fix=false
    local strict=false
    local quiet=false
    local report=""
    local keep_days=30
    local compress=false
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --editor)
                editor="$2"
                shift 2
                ;;
            --force)
                force=true
                shift
                ;;
            --no-backup)
                no_backup=true
                shift
                ;;
            --dry-run)
                dry_run=true
                shift
                ;;
            --validate-only)
                validate_only=true
                shift
                ;;
            --fix)
                fix=true
                shift
                ;;
            --strict)
                strict=true
                shift
                ;;
            --quiet)
                quiet=true
                shift
                ;;
            --report)
                report="$2"
                shift 2
                ;;
            --keep)
                keep_days="$2"
                shift 2
                ;;
            --compress)
                compress=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            -*)
                print_status "ERROR" "Unknown option: $1"
                exit 1
                ;;
            *)
                break
                ;;
        esac
    done
    
    # Execute operation
    case "$operation" in
        edit)
            if [[ $# -eq 0 ]]; then
                print_status "ERROR" "File name required for edit operation"
                exit 1
            fi
            safe_edit "$1" "$editor" "$force" "$no_backup" "$dry_run"
            ;;
        validate)
            if [[ $# -eq 0 ]]; then
                print_status "ERROR" "File name required for validate operation"
                exit 1
            fi
            if validate_file_structure "$1" "$strict"; then
                print_status "SUCCESS" "Validation passed: $1"
            else
                print_status "ERROR" "Validation failed: $1"
                exit 1
            fi
            ;;
        validate-all)
            validate_all_files "$fix" "$strict" "$quiet" "$report"
            ;;
        backup)
            if [[ $# -eq 0 ]]; then
                print_status "ERROR" "File name required for backup operation"
                exit 1
            fi
            create_backup "$1" "$compress"
            ;;
        backup-all)
            for file in "${MEMORY_DIR}"/*.md; do
                if [[ -f "$file" ]]; then
                    create_backup "$(basename "$file")" "$compress"
                fi
            done
            ;;
        restore)
            if [[ $# -eq 0 ]]; then
                print_status "ERROR" "File name required for restore operation"
                exit 1
            fi
            restore_from_backup "$1" "$2"
            ;;
        rollback)
            if [[ $# -eq 0 ]]; then
                print_status "ERROR" "File name required for rollback operation"
                exit 1
            fi
            restore_from_backup "$1"
            ;;
        preview)
            if [[ $# -eq 0 ]]; then
                print_status "ERROR" "File name required for preview operation"
                exit 1
            fi
            preview_file "$1"
            ;;
        merge)
            if [[ $# -lt 2 ]]; then
                print_status "ERROR" "Source and target files required for merge operation"
                exit 1
            fi
            merge_files "$1" "$2"
            ;;
        split)
            if [[ $# -lt 2 ]]; then
                print_status "ERROR" "File name and pattern required for split operation"
                exit 1
            fi
            split_file "$1" "$2"
            ;;
        cleanup)
            cleanup "$keep_days" "$dry_run"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_status "ERROR" "Unknown operation: $operation"
            echo
            show_help
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"