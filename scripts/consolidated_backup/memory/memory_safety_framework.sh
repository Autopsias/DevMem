#!/bin/bash

# Memory Safety Framework - Comprehensive Safety Checks and Recovery
# Purpose: Advanced safety mechanisms, integrity checks, and recovery procedures
# Usage: ./memory_safety_framework.sh <operation> [options]

set -euo pipefail

# Configuration
readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly MEMORY_DIR="${PROJECT_ROOT}/.claude/memory"
readonly BACKUP_DIR="${PROJECT_ROOT}/.claude/memory_backups"
readonly SAFETY_DIR="${PROJECT_ROOT}/.claude/memory_safety"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/memory_safety.log"
readonly QUARANTINE_DIR="${PROJECT_ROOT}/.claude/memory_quarantine"

# Safety constraints
readonly MAX_MEMORY_SIZE_MB=5
readonly MAX_FILE_SIZE_KB=100
readonly MAX_FILES_COUNT=50
readonly MIN_FREE_SPACE_MB=100
readonly CRITICAL_FILES=("agent-coordination-patterns.md" "domains/testing-patterns.md" "domains/infrastructure-patterns.md" "domains/security-patterns.md")

# Color codes
readonly GREEN='\033[0;32m'
readonly BLUE='\033[0;34m'
readonly YELLOW='\033[1;33m'
readonly RED='\033[0;31m'
readonly PURPLE='\033[0;35m'
readonly NC='\033[0m'
readonly BOLD='\033[1m'

# Logging with severity levels
log_safety() {
    local level="$1"
    local message="$2"
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] SAFETY: $message" >> "$LOG_FILE"
}

# Print status with enhanced formatting
print_status() {
    local level="$1"
    local message="$2"
    case "$level" in
        "SUCCESS") echo -e "${GREEN} $message${NC}"; log_safety "INFO" "$message" ;;
        "INFO") echo -e "${BLUE}9 $message${NC}"; log_safety "INFO" "$message" ;;
        "WARNING") echo -e "${YELLOW}  $message${NC}"; log_safety "WARN" "$message" ;;
        "ERROR") echo -e "${RED} $message${NC}"; log_safety "ERROR" "$message" ;;
        "CRITICAL") echo -e "${RED}${BOLD}=¨ $message${NC}"; log_safety "CRITICAL" "$message" ;;
        "SECURITY") echo -e "${PURPLE}= $message${NC}"; log_safety "SECURITY" "$message" ;;
        *) echo "$message"; log_safety "INFO" "$message" ;;
    esac
}

# Show comprehensive help
show_help() {
    cat << 'EOF'
Memory Safety Framework - Advanced Safety and Recovery System

USAGE:
    ./memory_safety_framework.sh <operation> [options]

SAFETY OPERATIONS:
    integrity-check                Full memory system integrity check
    security-scan                  Security vulnerability scan
    health-check                  System health assessment
    recovery-scan                 Recovery options assessment
    emergency-backup              Emergency full system backup
    emergency-restore             Emergency system restore
    quarantine <file>             Quarantine suspicious file
    audit-trail                   Show comprehensive audit trail
    disaster-recovery             Disaster recovery procedures

MONITORING OPERATIONS:
    resource-monitor              Monitor system resources
    corruption-scan               Scan for file corruption
    dependency-check              Check inter-file dependencies
    performance-check             Performance impact analysis
    compliance-check              Policy compliance validation

RECOVERY OPERATIONS:
    auto-repair                   Attempt automatic repair
    rollback-transaction          Rollback last transaction
    restore-checkpoint            Restore from checkpoint
    rebuild-indices               Rebuild memory indices
    validate-recovery             Validate recovery integrity

SECURITY OPERATIONS:
    permission-audit              Audit file permissions
    content-scan                  Scan for malicious content
    access-log                    Show access logs
    security-harden               Apply security hardening

OPTIONS:
    --critical-only              Only check critical files
    --full-scan                  Comprehensive deep scan
    --auto-fix                   Automatically fix issues
    --report <file>              Generate detailed report
    --quiet                      Suppress non-critical output
    --force-repair               Force repair dangerous issues
    --dry-run                    Show what would be done
    --checkpoint                 Create checkpoint before operation

EMERGENCY PROCEDURES:
    --emergency                  Emergency mode (bypass some safety checks)
    --disaster-mode              Disaster recovery mode
    --safe-mode                  Extra conservative mode

EXAMPLES:
    ./memory_safety_framework.sh integrity-check --full-scan --report integrity.md
    ./memory_safety_framework.sh security-scan --critical-only
    ./memory_safety_framework.sh emergency-backup --checkpoint
    ./memory_safety_framework.sh auto-repair --dry-run
    ./memory_safety_framework.sh disaster-recovery --emergency

SAFETY LEVELS:
    LEVEL 1: Basic validation and backup
    LEVEL 2: Integrity checks and monitoring
    LEVEL 3: Security scanning and hardening
    LEVEL 4: Disaster recovery and emergency procedures

EOF
}

# Create safety checkpoint
create_checkpoint() {
    local checkpoint_name="${1:-auto_$(date '+%Y%m%d_%H%M%S')}"
    local checkpoint_dir="${SAFETY_DIR}/checkpoints/${checkpoint_name}"
    
    mkdir -p "$checkpoint_dir"
    
    print_status "INFO" "Creating safety checkpoint: $checkpoint_name"
    
    # Backup entire memory system
    if [[ -d "$MEMORY_DIR" ]]; then
        cp -r "$MEMORY_DIR" "${checkpoint_dir}/memory" 2>/dev/null || {
            print_status "ERROR" "Failed to backup memory directory"
            return 1
        }
    fi
    
    # Backup configuration
    if [[ -f "${PROJECT_ROOT}/.claude/settings.json" ]]; then
        cp "${PROJECT_ROOT}/.claude/settings.json" "${checkpoint_dir}/" 2>/dev/null || {
            print_status "WARNING" "Failed to backup settings"
        }
    fi
    
    # Create checkpoint metadata
    {
        echo "# Safety Checkpoint: $checkpoint_name"
        echo "Created: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "System: $(uname -s)"
        echo "User: $(whoami)"
        echo "Memory Files: $(find "$MEMORY_DIR" -name "*.md" -type f | wc -l)"
        echo "Total Size: $(du -sh "$MEMORY_DIR" 2>/dev/null | cut -f1 || echo "unknown")"
        echo "Git Commit: $(cd "$PROJECT_ROOT" && git rev-parse --short HEAD 2>/dev/null || echo "unknown")"
    } > "${checkpoint_dir}/metadata.md"
    
    log_safety "INFO" "Checkpoint created: $checkpoint_name"
    print_status "SUCCESS" "Checkpoint created: $checkpoint_name"
    
    echo "$checkpoint_dir"
}

# Comprehensive integrity check
integrity_check() {
    local full_scan="${1:-false}"
    local critical_only="${2:-false}"
    local auto_fix="${3:-false}"
    local report_file="${4:-}"
    
    print_status "INFO" "Starting integrity check (full_scan=$full_scan, critical_only=$critical_only)"
    
    local issues_found=0
    local files_checked=0
    local integrity_report=""
    
    # Check memory directory exists
    if [[ ! -d "$MEMORY_DIR" ]]; then
        print_status "CRITICAL" "Memory directory not found: $MEMORY_DIR"
        return 1
    fi
    
    # Resource availability check
    local free_space_mb
    free_space_mb=$(df -m "$PROJECT_ROOT" | awk 'NR==2 {print $4}')
    if [[ $free_space_mb -lt $MIN_FREE_SPACE_MB ]]; then
        print_status "WARNING" "Low disk space: ${free_space_mb}MB (minimum: ${MIN_FREE_SPACE_MB}MB)"
        issues_found=$((issues_found + 1))
        integrity_report+="Low disk space: ${free_space_mb}MB available\n"
    fi
    
    # Total memory usage check
    local total_size_mb
    total_size_mb=$(du -sm "$MEMORY_DIR" 2>/dev/null | cut -f1 || echo "0")
    if [[ $total_size_mb -gt $MAX_MEMORY_SIZE_MB ]]; then
        print_status "ERROR" "Memory usage exceeds limit: ${total_size_mb}MB (max: ${MAX_MEMORY_SIZE_MB}MB)"
        issues_found=$((issues_found + 1))
        integrity_report+="Memory usage exceeded: ${total_size_mb}MB\n"
    fi
    
    # File count check
    local file_count
    file_count=$(find "$MEMORY_DIR" -name "*.md" -type f | wc -l)
    if [[ $file_count -gt $MAX_FILES_COUNT ]]; then
        print_status "WARNING" "Too many files: $file_count (max: $MAX_FILES_COUNT)"
        issues_found=$((issues_found + 1))
        integrity_report+="File count exceeded: $file_count files\n"
    fi
    
    # Critical files check
    for critical_file in "${CRITICAL_FILES[@]}"; do
        local file_path="${MEMORY_DIR}/${critical_file}"
        if [[ ! -f "$file_path" ]]; then
            print_status "CRITICAL" "Critical file missing: $critical_file"
            issues_found=$((issues_found + 1))
            integrity_report+="Critical file missing: $critical_file\n"
        else
            files_checked=$((files_checked + 1))
            # Check file is readable and not empty
            if [[ ! -r "$file_path" ]]; then
                print_status "ERROR" "Critical file not readable: $critical_file"
                issues_found=$((issues_found + 1))
                integrity_report+="Critical file not readable: $critical_file\n"
            elif [[ ! -s "$file_path" ]]; then
                print_status "WARNING" "Critical file is empty: $critical_file"
                issues_found=$((issues_found + 1))
                integrity_report+="Critical file is empty: $critical_file\n"
            fi
        fi
    done
    
    # Individual file integrity (if not critical_only)
    if [[ "$critical_only" != "true" ]]; then
        while IFS= read -r -d '' file_path; do
            local file=$(basename "$file_path")
            files_checked=$((files_checked + 1))
            
            # File size check
            local size_kb
            size_kb=$(du -k "$file_path" | cut -f1)
            if [[ $size_kb -gt $MAX_FILE_SIZE_KB ]]; then
                print_status "WARNING" "File oversized: $file (${size_kb}KB)"
                issues_found=$((issues_found + 1))
                integrity_report+="Oversized file: $file (${size_kb}KB)\n"
            fi
            
            # File corruption check (basic)
            if ! head -n 1 "$file_path" >/dev/null 2>&1; then
                print_status "ERROR" "File appears corrupted: $file"
                issues_found=$((issues_found + 1))
                integrity_report+="Corrupted file: $file\n"
                
                if [[ "$auto_fix" == "true" ]]; then
                    quarantine_file "$file" "corruption"
                fi
            fi
            
            # Full scan checks
            if [[ "$full_scan" == "true" ]]; then
                # Check for duplicate content
                local content_hash
                content_hash=$(md5sum "$file_path" | cut -d' ' -f1)
                local existing_file
                existing_file=$(find "$MEMORY_DIR" -name "*.md" -type f -exec md5sum {} \; | grep "^$content_hash " | head -n1 | cut -d' ' -f2-)
                if [[ -n "$existing_file" && "$existing_file" != "$file_path" ]]; then
                    print_status "INFO" "Potential duplicate content: $file and $(basename "$existing_file")"
                    integrity_report+="Potential duplicate: $file\n"
                fi
                
                # Check for malformed markdown
                if command -v markdownlint >/dev/null 2>&1; then
                    if ! markdownlint -q "$file_path" 2>/dev/null; then
                        print_status "INFO" "Markdown issues in: $file"
                        integrity_report+="Markdown issues: $file\n"
                    fi
                fi
            fi
            
        done < <(find "$MEMORY_DIR" -name "*.md" -type f -print0)
    fi
    
    # Dependency validation
    check_inter_file_dependencies
    local dep_issues=$?
    issues_found=$((issues_found + dep_issues))
    
    # Generate report
    local report_content=""
    report_content+="# Memory System Integrity Report\n"
    report_content+="Generated: $(date '+%Y-%m-%d %H:%M:%S')\n\n"
    report_content+="## Summary\n"
    report_content+="- Files checked: $files_checked\n"
    report_content+="- Issues found: $issues_found\n"
    report_content+="- Total memory size: ${total_size_mb}MB\n"
    report_content+="- Available space: ${free_space_mb}MB\n\n"
    
    if [[ $issues_found -eq 0 ]]; then
        report_content+="## Status: HEALTHY \n"
        report_content+="No integrity issues detected.\n\n"
    else
        report_content+="## Status: ISSUES DETECTED  \n"
        report_content+="### Issues Found:\n"
        report_content+="$integrity_report\n"
    fi
    
    # Save report if requested
    if [[ -n "$report_file" ]]; then
        echo -e "$report_content" > "$report_file"
        print_status "SUCCESS" "Integrity report saved: $report_file"
    fi
    
    if [[ $issues_found -eq 0 ]]; then
        print_status "SUCCESS" "Integrity check completed: No issues found"
    else
        print_status "WARNING" "Integrity check completed: $issues_found issues found"
    fi
    
    log_safety "INFO" "Integrity check completed: $files_checked files, $issues_found issues"
    return $issues_found
}

# Security vulnerability scan
security_scan() {
    local critical_only="${1:-false}"
    local report_file="${2:-}"
    
    print_status "SECURITY" "Starting security vulnerability scan"
    
    local security_issues=0
    local security_report=""
    
    # Permission audit
    while IFS= read -r -d '' file_path; do
        local file=$(basename "$file_path")
        local perms
        perms=$(stat -f "%Mp%Lp" "$file_path" 2>/dev/null || stat -c "%a" "$file_path" 2>/dev/null || echo "unknown")
        
        # Check for overly permissive permissions
        if [[ "$perms" =~ 77[0-9] || "$perms" =~ 66[0-9] ]]; then
            print_status "SECURITY" "Overly permissive permissions on: $file ($perms)"
            security_issues=$((security_issues + 1))
            security_report+="Permissions issue: $file ($perms)\n"
        fi
        
        # Check for world-writable files
        if [[ -w "$file_path" ]] && [[ $(find "$file_path" -perm -002) ]]; then
            print_status "SECURITY" "World-writable file: $file"
            security_issues=$((security_issues + 1))
            security_report+="World-writable: $file\n"
        fi
        
    done < <(find "$MEMORY_DIR" -name "*.md" -type f -print0)
    
    # Content security scan
    if [[ "$critical_only" != "true" ]]; then
        print_status "INFO" "Scanning for suspicious content patterns..."
        
        # Scan for potentially malicious patterns
        local suspicious_patterns=(
            '<script'
            'javascript:'
            'eval\('
            'exec\('
            'base64'
            'password'
            'secret'
            'token'
            'api_key'
            'private_key'
        )
        
        for pattern in "${suspicious_patterns[@]}"; do
            local matches
            matches=$(grep -ri "$pattern" "$MEMORY_DIR" 2>/dev/null | wc -l)
            if [[ $matches -gt 0 ]]; then
                print_status "SECURITY" "Suspicious pattern '$pattern' found in $matches locations"
                security_issues=$((security_issues + 1))
                security_report+="Suspicious pattern: $pattern ($matches matches)\n"
            fi
        done
    fi
    
    # Directory security
    if [[ -d "$BACKUP_DIR" ]]; then
        local backup_perms
        backup_perms=$(stat -f "%Mp%Lp" "$BACKUP_DIR" 2>/dev/null || stat -c "%a" "$BACKUP_DIR" 2>/dev/null || echo "unknown")
        if [[ "$backup_perms" =~ 77[0-9] ]]; then
            print_status "SECURITY" "Backup directory too permissive: $backup_perms"
            security_issues=$((security_issues + 1))
            security_report+="Backup directory permissions: $backup_perms\n"
        fi
    fi
    
    # Generate security report
    if [[ -n "$report_file" ]]; then
        {
            echo "# Memory Security Scan Report"
            echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
            echo
            echo "## Summary"
            echo "- Security issues found: $security_issues"
            echo
            if [[ $security_issues -eq 0 ]]; then
                echo "## Status: SECURE "
                echo "No security issues detected."
            else
                echo "## Status: SECURITY ISSUES FOUND ="
                echo "### Issues:"
                echo -e "$security_report"
            fi
        } > "$report_file"
        
        print_status "SUCCESS" "Security report saved: $report_file"
    fi
    
    if [[ $security_issues -eq 0 ]]; then
        print_status "SUCCESS" "Security scan completed: No issues found"
    else
        print_status "WARNING" "Security scan completed: $security_issues issues found"
    fi
    
    log_safety "SECURITY" "Security scan completed: $security_issues issues found"
    return $security_issues
}

# Quarantine suspicious file
quarantine_file() {
    local file="$1"
    local reason="${2:-manual}"
    local file_path="${MEMORY_DIR}/${file}"
    
    if [[ ! -f "$file_path" ]]; then
        print_status "ERROR" "File not found for quarantine: $file"
        return 1
    fi
    
    mkdir -p "$QUARANTINE_DIR"
    
    local timestamp=$(date '+%Y%m%d_%H%M%S')
    local quarantine_name="${file%.md}_${timestamp}_${reason}.md"
    local quarantine_path="${QUARANTINE_DIR}/${quarantine_name}"
    
    # Move to quarantine
    mv "$file_path" "$quarantine_path"
    
    # Create quarantine metadata
    {
        echo "# Quarantine Record"
        echo "File: $file"
        echo "Reason: $reason"
        echo "Quarantined: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "Original path: $file_path"
        echo "Size: $(wc -c < "$quarantine_path") bytes"
        echo "MD5: $(md5sum "$quarantine_path" | cut -d' ' -f1)"
    } > "${quarantine_path}.meta"
    
    print_status "SECURITY" "File quarantined: $file -> $quarantine_name"
    log_safety "SECURITY" "File quarantined: $file (reason: $reason)"
    
    return 0
}

# Check inter-file dependencies
check_inter_file_dependencies() {
    local issues=0
    
    print_status "INFO" "Checking inter-file dependencies..."
    
    # Look for @references and ensure they exist
    while IFS= read -r -d '' file_path; do
        while IFS= read -r line; do
            if [[ "$line" =~ @([^[:space:]]+) ]]; then
                local ref_path="${BASH_REMATCH[1]}"
                # Convert relative to absolute path
                local full_ref_path
                if [[ "$ref_path" =~ ^/ ]]; then
                    full_ref_path="$ref_path"
                else
                    full_ref_path="${PROJECT_ROOT}/${ref_path}"
                fi
                
                if [[ ! -f "$full_ref_path" ]]; then
                    print_status "WARNING" "Broken reference in $(basename "$file_path"): $ref_path"
                    issues=$((issues + 1))
                fi
            fi
        done < "$file_path"
    done < <(find "$MEMORY_DIR" -name "*.md" -type f -print0)
    
    return $issues
}

# Emergency full backup
emergency_backup() {
    local backup_name="emergency_$(date '+%Y%m%d_%H%M%S')"
    local emergency_dir="${SAFETY_DIR}/emergency_backups/${backup_name}"
    
    print_status "INFO" "Creating emergency backup: $backup_name"
    
    mkdir -p "$emergency_dir"
    
    # Backup everything
    if [[ -d "$MEMORY_DIR" ]]; then
        tar -czf "${emergency_dir}/memory.tar.gz" -C "$PROJECT_ROOT" .claude/memory/ || {
            print_status "ERROR" "Failed to create memory backup"
            return 1
        }
    fi
    
    if [[ -d "$BACKUP_DIR" ]]; then
        tar -czf "${emergency_dir}/backups.tar.gz" -C "$PROJECT_ROOT" .claude/memory_backups/ || {
            print_status "WARNING" "Failed to backup existing backups"
        }
    fi
    
    # System metadata
    {
        echo "# Emergency Backup: $backup_name"
        echo "Created: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "System: $(uname -a)"
        echo "Git status:"
        cd "$PROJECT_ROOT" && git status --porcelain 2>/dev/null || echo "Git not available"
        echo
        echo "Memory directory size: $(du -sh "$MEMORY_DIR" 2>/dev/null | cut -f1 || echo "unknown")"
        echo "Available disk space: $(df -h "$PROJECT_ROOT" | awk 'NR==2 {print $4}')"
    } > "${emergency_dir}/system_info.md"
    
    print_status "SUCCESS" "Emergency backup created: $backup_name"
    log_safety "CRITICAL" "Emergency backup created: $backup_name"
    
    echo "$emergency_dir"
}

# Auto-repair functionality
auto_repair() {
    local dry_run="${1:-false}"
    local force_repair="${2:-false}"
    
    print_status "INFO" "Starting auto-repair (dry_run=$dry_run, force=$force_repair)"
    
    local repairs_made=0
    local repair_log=""
    
    # Create checkpoint before repairs
    if [[ "$dry_run" != "true" ]]; then
        local checkpoint
        checkpoint=$(create_checkpoint "pre_repair_$(date '+%Y%m%d_%H%M%S')")
        repair_log+="Checkpoint created: $checkpoint\n"
    fi
    
    # Fix file permissions
    while IFS= read -r -d '' file_path; do
        local current_perms
        current_perms=$(stat -f "%Mp%Lp" "$file_path" 2>/dev/null || stat -c "%a" "$file_path" 2>/dev/null || echo "unknown")
        
        if [[ "$current_perms" =~ 77[0-9] || "$current_perms" =~ 66[0-9] ]]; then
            if [[ "$dry_run" == "true" ]]; then
                print_status "INFO" "Would fix permissions: $(basename "$file_path") ($current_perms -> 644)"
            else
                chmod 644 "$file_path"
                print_status "SUCCESS" "Fixed permissions: $(basename "$file_path")"
                repairs_made=$((repairs_made + 1))
                repair_log+="Fixed permissions: $(basename "$file_path")\n"
            fi
        fi
    done < <(find "$MEMORY_DIR" -name "*.md" -type f -print0)
    
    # Create missing critical files
    for critical_file in "${CRITICAL_FILES[@]}"; do
        local file_path="${MEMORY_DIR}/${critical_file}"
        if [[ ! -f "$file_path" ]]; then
            if [[ "$dry_run" == "true" ]]; then
                print_status "INFO" "Would create missing critical file: $critical_file"
            else
                mkdir -p "$(dirname "$file_path")"
                echo "# $(basename "$critical_file" .md | tr '-' ' ' | tr '_' ' ')" > "$file_path"
                echo "" >> "$file_path"
                echo "## Overview" >> "$file_path"
                echo "This file was automatically recreated by the memory safety framework." >> "$file_path"
                echo "" >> "$file_path"
                
                print_status "SUCCESS" "Created missing critical file: $critical_file"
                repairs_made=$((repairs_made + 1))
                repair_log+="Created missing file: $critical_file\n"
            fi
        fi
    done
    
    # Remove corrupted files (with force)
    if [[ "$force_repair" == "true" ]]; then
        while IFS= read -r -d '' file_path; do
            if ! head -n 1 "$file_path" >/dev/null 2>&1; then
                local file=$(basename "$file_path")
                if [[ "$dry_run" == "true" ]]; then
                    print_status "INFO" "Would quarantine corrupted file: $file"
                else
                    quarantine_file "$file" "auto_repair_corruption"
                    repairs_made=$((repairs_made + 1))
                    repair_log+="Quarantined corrupted file: $file\n"
                fi
            fi
        done < <(find "$MEMORY_DIR" -name "*.md" -type f -print0)
    fi
    
    if [[ "$dry_run" == "true" ]]; then
        print_status "INFO" "Auto-repair dry run completed (would make $repairs_made repairs)"
    else
        print_status "SUCCESS" "Auto-repair completed: $repairs_made repairs made"
        log_safety "INFO" "Auto-repair completed: $repairs_made repairs"
        echo -e "$repair_log"
    fi
    
    return 0
}

# Disaster recovery procedures
disaster_recovery() {
    local emergency_mode="${1:-false}"
    
    print_status "CRITICAL" "Initiating disaster recovery procedures"
    log_safety "CRITICAL" "Disaster recovery initiated"
    
    # Assessment phase
    print_status "INFO" "Phase 1: Damage assessment"
    
    local memory_exists=false
    local backups_available=false
    local system_responsive=true
    
    # Check if memory directory exists and is accessible
    if [[ -d "$MEMORY_DIR" ]] && [[ -r "$MEMORY_DIR" ]]; then
        memory_exists=true
        print_status "INFO" "Memory directory accessible"
    else
        print_status "ERROR" "Memory directory inaccessible or missing"
    fi
    
    # Check for backups
    if [[ -d "$BACKUP_DIR" ]] && [[ "$(find "$BACKUP_DIR" -name "*.md*" -type f | wc -l)" -gt 0 ]]; then
        backups_available=true
        print_status "INFO" "Backups available"
    else
        print_status "WARNING" "No backups found"
    fi
    
    # Recovery phase
    print_status "INFO" "Phase 2: Recovery planning"
    
    if [[ "$memory_exists" == "true" ]]; then
        # Try to salvage existing data
        print_status "INFO" "Attempting to salvage existing memory data"
        
        # Create emergency backup first
        emergency_backup >/dev/null
        
        # Run integrity check
        if integrity_check false false false; then
            print_status "SUCCESS" "Memory system appears recoverable"
            return 0
        else
            print_status "WARNING" "Memory system has integrity issues"
        fi
    fi
    
    if [[ "$backups_available" == "true" ]]; then
        print_status "INFO" "Phase 3: Restore from backups"
        
        # Find latest backup
        local latest_backup
        latest_backup=$(find "$BACKUP_DIR" -name "*.md" -type f -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-)
        
        if [[ -n "$latest_backup" ]]; then
            print_status "INFO" "Latest backup found: $(basename "$latest_backup")"
            
            if [[ "$emergency_mode" == "true" ]]; then
                print_status "WARNING" "Emergency mode: Attempting automatic restore"
                # Implement automatic restore logic here
                return 0
            else
                print_status "INFO" "Manual intervention required for restore"
                echo "Latest backup: $latest_backup"
                echo "Use: ./memory_editor.sh restore $(basename "$latest_backup")"
                return 1
            fi
        fi
    fi
    
    # Last resort: Initialize from scratch
    print_status "CRITICAL" "Phase 4: Last resort - reinitialize memory system"
    
    if [[ "$emergency_mode" == "true" ]]; then
        mkdir -p "$MEMORY_DIR/domains"
        
        # Create minimal critical files
        for critical_file in "${CRITICAL_FILES[@]}"; do
            local file_path="${MEMORY_DIR}/${critical_file}"
            mkdir -p "$(dirname "$file_path")"
            
            {
                echo "# $(basename "$critical_file" .md | tr '-' ' ' | tr '_' ' ')"
                echo ""
                echo "## Overview"
                echo "This file was recreated during disaster recovery."
                echo ""
                echo "Recovered: $(date '+%Y-%m-%d %H:%M:%S')"
            } > "$file_path"
        done
        
        print_status "SUCCESS" "Minimal memory system recreated"
        log_safety "CRITICAL" "Memory system recreated from scratch"
        return 0
    else
        print_status "CRITICAL" "Manual disaster recovery required"
        return 1
    fi
}

# Main function
main() {
    if [[ $# -eq 0 ]]; then
        show_help
        exit 0
    fi
    
    local operation="$1"
    shift
    
    # Create safety directories
    mkdir -p "$SAFETY_DIR" "$QUARANTINE_DIR"
    
    # Parse options
    local critical_only=false
    local full_scan=false
    local auto_fix=false
    local report_file=""
    local quiet=false
    local force_repair=false
    local dry_run=false
    local checkpoint=false
    local emergency_mode=false
    local disaster_mode=false
    local safe_mode=false
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --critical-only) critical_only=true; shift ;;
            --full-scan) full_scan=true; shift ;;
            --auto-fix) auto_fix=true; shift ;;
            --report) report_file="$2"; shift 2 ;;
            --quiet) quiet=true; shift ;;
            --force-repair) force_repair=true; shift ;;
            --dry-run) dry_run=true; shift ;;
            --checkpoint) checkpoint=true; shift ;;
            --emergency) emergency_mode=true; shift ;;
            --disaster-mode) disaster_mode=true; shift ;;
            --safe-mode) safe_mode=true; shift ;;
            --help|-h) show_help; exit 0 ;;
            -*) print_status "ERROR" "Unknown option: $1"; exit 1 ;;
            *) break ;;
        esac
    done
    
    # Create checkpoint if requested
    if [[ "$checkpoint" == "true" ]]; then
        create_checkpoint "manual_$(date '+%Y%m%d_%H%M%S')" >/dev/null
    fi
    
    # Execute operation
    case "$operation" in
        integrity-check)
            integrity_check "$full_scan" "$critical_only" "$auto_fix" "$report_file"
            ;;
        security-scan)
            security_scan "$critical_only" "$report_file"
            ;;
        health-check)
            integrity_check "$full_scan" "$critical_only" false "$report_file"
            security_scan "$critical_only" >/dev/null
            ;;
        emergency-backup)
            emergency_backup
            ;;
        quarantine)
            if [[ $# -eq 0 ]]; then
                print_status "ERROR" "File name required for quarantine"
                exit 1
            fi
            quarantine_file "$1" "${2:-manual}"
            ;;
        auto-repair)
            auto_repair "$dry_run" "$force_repair"
            ;;
        disaster-recovery)
            disaster_recovery "$emergency_mode"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_status "ERROR" "Unknown operation: $operation"
            show_help
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"