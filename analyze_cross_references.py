#!/usr/bin/env python3
"""
Cross-Reference Analysis Tool
Detailed analysis of memory file cross-references to identify validation issues.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

def analyze_cross_references(project_root: Path) -> Dict[str, any]:
    """Analyze all cross-references in memory files."""
    memory_root = project_root / ".claude" / "memory"
    
    memory_files = [
        memory_root / "agent-coordination-core.md",
        memory_root / "agent-coordination-patterns.md", 
        memory_root / "domains" / "project-specific-patterns.md",
        memory_root / "domains" / "testing-patterns.md",
        memory_root / "domains" / "infrastructure-patterns.md",
        memory_root / "domains" / "security-patterns.md"
    ]
    
    all_references = []
    reference_analysis = {}
    
    for file_path in memory_files:
        if not file_path.exists():
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all @references
            reference_lines = []
            for line_num, line in enumerate(content.split('\n'), 1):
                if '@' in line:
                    # Extract references more carefully
                    refs = re.findall(r'@([^\s\]]+)', line)
                    for ref in refs:
                        reference_lines.append({
                            'line_num': line_num,
                            'line_text': line.strip(),
                            'reference': ref,
                            'original_line': line
                        })
            
            reference_analysis[str(file_path.relative_to(project_root))] = {
                'total_references': len(reference_lines),
                'references': reference_lines
            }
            
            all_references.extend(reference_lines)
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    return {
        'all_references': all_references,
        'by_file': reference_analysis,
        'project_root': project_root
    }

def validate_reference_path(ref_path: str, project_root: Path) -> Tuple[bool, str]:
    """Validate a reference path and return status with reason."""
    
    # Handle different reference types
    if ref_path.startswith('.claude/memory/'):
        full_path = project_root / ref_path
        if full_path.exists():
            return True, "Valid memory file reference"
        else:
            return False, f"Memory file not found: {full_path}"
    
    elif ref_path.startswith('~/.claude/'):
        return True, "User-level configuration (assumed valid)"
    
    elif ref_path == 'CLAUDE.md':
        full_path = project_root / 'CLAUDE.md'
        if full_path.exists():
            return True, "Valid project configuration"
        else:
            return False, "CLAUDE.md not found"
    
    elif ref_path.startswith('docs/'):
        full_path = project_root / ref_path
        if full_path.exists():
            return True, "Valid documentation reference"
        else:
            return False, f"Documentation file not found: {full_path}"
    
    elif ref_path.endswith('.md'):
        # Try various locations for markdown files
        possible_paths = [
            project_root / ref_path,
            project_root / 'docs' / ref_path,
            project_root / '.claude' / 'memory' / ref_path
        ]
        
        for path in possible_paths:
            if path.exists():
                return True, f"Found at: {path}"
        
        return False, f"Markdown file not found in any expected location"
    
    else:
        return False, f"Unknown reference format: {ref_path}"

def main():
    """Analyze cross-references and generate detailed report."""
    project_root = Path(__file__).parent
    
    print("Cross-Reference Validation Analysis")
    print("=" * 50)
    
    analysis = analyze_cross_references(project_root)
    
    total_refs = len(analysis['all_references'])
    valid_refs = 0
    invalid_refs = []
    
    print(f"Total references found: {total_refs}")
    print()
    
    # Validate each reference
    for ref_data in analysis['all_references']:
        ref_path = ref_data['reference']
        is_valid, reason = validate_reference_path(ref_path, project_root)
        
        if is_valid:
            valid_refs += 1
        else:
            invalid_refs.append({
                'reference': ref_path,
                'reason': reason,
                'line_text': ref_data['line_text'],
                'line_num': ref_data['line_num']
            })
    
    validation_rate = (valid_refs / total_refs) * 100 if total_refs > 0 else 0
    
    print(f"Valid references: {valid_refs}")
    print(f"Invalid references: {len(invalid_refs)}")
    print(f"Validation rate: {validation_rate:.1f}%")
    print()
    
    # Show references by file
    print("References by File:")
    print("-" * 30)
    for file_path, file_data in analysis['by_file'].items():
        print(f"{file_path}: {file_data['total_references']} references")
        
        # Show some example references
        for ref_data in file_data['references'][:3]:  # Show first 3
            ref_path = ref_data['reference']
            is_valid, reason = validate_reference_path(ref_path, project_root)
            status = "✓" if is_valid else "✗"
            print(f"  {status} @{ref_path} - {reason}")
        
        if len(file_data['references']) > 3:
            print(f"  ... and {len(file_data['references']) - 3} more")
        print()
    
    # Show all invalid references
    if invalid_refs:
        print("Invalid References Details:")
        print("-" * 40)
        for invalid in invalid_refs:
            print(f"✗ @{invalid['reference']}")
            print(f"  Reason: {invalid['reason']}")
            print(f"  Context: {invalid['line_text'][:80]}...")
            print()
    
    # Recommendations
    print("Recommendations:")
    print("-" * 20)
    
    missing_files = set()
    for invalid in invalid_refs:
        if "not found" in invalid['reason']:
            # Extract the missing file path
            if invalid['reference'].startswith('.claude/memory/'):
                missing_files.add(invalid['reference'])
            elif invalid['reference'].startswith('docs/'):
                missing_files.add(invalid['reference'])
    
    if missing_files:
        print("Create missing files:")
        for missing in sorted(missing_files):
            print(f"  - {missing}")
        print()
    
    print("Fix reference format issues:")
    reference_formats = set()
    for invalid in invalid_refs:
        if "Unknown reference format" in invalid['reason']:
            reference_formats.add(invalid['reference'])
    
    for ref in sorted(reference_formats):
        print(f"  - Review reference: @{ref}")
    
    print(f"\nCurrent validation rate: {validation_rate:.1f}%")
    print(f"Target validation rate: 100.0%")
    print(f"Improvement needed: {100.0 - validation_rate:.1f} percentage points")

if __name__ == "__main__":
    main()