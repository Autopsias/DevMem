#!/usr/bin/env python3
"""Simple validation script for Claude Code agent framework health."""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any

def validate_agent_file(file_path: Path) -> List[str]:
    """Validate a single agent .md file."""
    errors = []
    
    try:
        content = file_path.read_text()
        
        # Check for YAML frontmatter
        if not content.startswith('---'):
            errors.append(f"Missing YAML frontmatter in {file_path}")
            return errors
            
        # Extract and validate YAML
        yaml_end = content.find('---', 3)
        if yaml_end == -1:
            errors.append(f"Invalid YAML frontmatter format in {file_path}")
            return errors
            
        try:
            frontmatter = yaml.safe_load(content[3:yaml_end])
        except yaml.YAMLError as e:
            errors.append(f"Invalid YAML in {file_path}: {e}")
            return errors
            
        # Validate required fields
        required_fields = ['name', 'description', 'tools']
        for field in required_fields:
            if field not in frontmatter:
                errors.append(f"Missing required field '{field}' in {file_path}")
                
        # Validate tools list
        if 'tools' in frontmatter:
            if not isinstance(frontmatter['tools'], list):
                errors.append(f"'tools' must be a list in {file_path}")
            elif len(frontmatter['tools']) > 10:
                errors.append(f"Too many tools (max 10) in {file_path}")
                
        # Check for "Use PROACTIVELY" in description
        if 'description' in frontmatter:
            if not isinstance(frontmatter['description'], str):
                errors.append(f"'description' must be a string in {file_path}")
            elif 'Use PROACTIVELY' not in frontmatter['description']:
                errors.append(f"Missing 'Use PROACTIVELY' in description of {file_path}")
                
    except Exception as e:
        errors.append(f"Error validating {file_path}: {e}")
        
    return errors

def validate_claude_md() -> List[str]:
    """Validate CLAUDE.md existence and format."""
    errors = []
    
    claude_md = Path('CLAUDE.md')
    if not claude_md.exists():
        errors.append("Missing CLAUDE.md file")
        return errors
        
    try:
        content = claude_md.read_text()
        if not content.strip():
            errors.append("CLAUDE.md is empty")
    except Exception as e:
        errors.append(f"Error reading CLAUDE.md: {e}")
        
    return errors

def main() -> int:
    """Run framework validation."""
    print("Validating Claude Code agent framework...")
    
    all_errors = []
    
    # Validate CLAUDE.md
    errors = validate_claude_md()
    if errors:
        all_errors.extend(errors)
        
    # Validate agent files
    agents_dir = Path('.claude/agents')
    if not agents_dir.exists():
        print("Error: Missing .claude/agents directory")
        return 1
        
    for file in agents_dir.glob('*.md'):
        errors = validate_agent_file(file)
        if errors:
            all_errors.extend(errors)
            
    # Report results
    if all_errors:
        print("\nValidation errors found:")
        for error in all_errors:
            print(f"- {error}")
        return 1
        
    print("\nValidation successful! Framework is healthy.")
    return 0

if __name__ == '__main__':
    sys.exit(main())