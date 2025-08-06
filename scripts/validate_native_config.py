#!/usr/bin/env python3
"""
Native Configuration Validation Script
Purpose: Validate .claude/settings.json follows Claude Code native patterns
Usage: python scripts/validate_native_config.py
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List

def validate_env_section(env_config: Dict[str, str]) -> List[str]:
    """Validate environment variables section."""
    errors = []
    
    # Required environment variables
    required_env_vars = [
        "PYTHONPATH",
        "CLAUDE_AGENT_FRAMEWORK_ENABLED", 
        "CLAUDE_AGENT_PERFORMANCE_TARGET_MS",
        "TEST_COVERAGE_MINIMUM"
    ]
    
    for var in required_env_vars:
        if var not in env_config:
            errors.append(f"Missing required environment variable: {var}")
    
    # Validate boolean values
    boolean_vars = [
        "CLAUDE_AGENT_FRAMEWORK_ENABLED",
        "CLAUDE_AGENT_NATURAL_DELEGATION", 
        "CLAUDE_AGENT_PARALLEL_EXECUTION",
        "QUALITY_GATES_ENABLED",
        "SECURITY_SCANNING_ENABLED"
    ]
    
    for var in boolean_vars:
        if var in env_config and env_config[var] not in ["true", "false"]:
            errors.append(f"Environment variable {var} must be 'true' or 'false'")
    
    # Validate numeric values
    numeric_vars = [
        ("CLAUDE_AGENT_PERFORMANCE_TARGET_MS", 500, 10000),
        ("CLAUDE_AGENT_MAX_CONTEXT_TOKENS", 1000, 200000),
        ("TEST_COVERAGE_MINIMUM", 0, 100)
    ]
    
    for var, min_val, max_val in numeric_vars:
        if var in env_config:
            try:
                value = int(env_config[var])
                if not (min_val <= value <= max_val):
                    errors.append(f"{var} must be between {min_val} and {max_val}")
            except ValueError:
                errors.append(f"{var} must be a valid integer")
    
    return errors

def validate_permissions_section(permissions_config: Dict[str, Any]) -> List[str]:
    """Validate permissions section."""
    errors = []
    
    required_keys = ["allow", "deny", "defaultMode"]
    for key in required_keys:
        if key not in permissions_config:
            errors.append(f"Missing required permissions key: {key}")
    
    # Validate defaultMode
    valid_modes = ["acceptEdits", "requirePermission", "bypassPermissions"]
    if "defaultMode" in permissions_config:
        if permissions_config["defaultMode"] not in valid_modes:
            errors.append(f"defaultMode must be one of: {valid_modes}")
    
    # Validate allow/deny are arrays
    for key in ["allow", "deny"]:
        if key in permissions_config and not isinstance(permissions_config[key], list):
            errors.append(f"permissions.{key} must be an array")
    
    return errors

def validate_hooks_section(hooks_config: Dict[str, Any]) -> List[str]:
    """Validate hooks section."""
    errors = []
    
    valid_hook_types = ["PreToolUse", "PostToolUse", "SessionStart", "Stop"]
    
    for hook_type, hooks in hooks_config.items():
        if hook_type not in valid_hook_types:
            errors.append(f"Invalid hook type: {hook_type}")
            continue
            
        if not isinstance(hooks, list):
            errors.append(f"Hook {hook_type} must be an array")
            continue
            
        for i, hook in enumerate(hooks):
            if not isinstance(hook, dict):
                errors.append(f"Hook {hook_type}[{i}] must be an object")
                continue
                
            if "matcher" not in hook:
                errors.append(f"Hook {hook_type}[{i}] missing 'matcher'")
                
            if "hooks" not in hook:
                errors.append(f"Hook {hook_type}[{i}] missing 'hooks' array")
                continue
                
            for j, sub_hook in enumerate(hook["hooks"]):
                if "type" not in sub_hook:
                    errors.append(f"Hook {hook_type}[{i}].hooks[{j}] missing 'type'")
                if "command" not in sub_hook:
                    errors.append(f"Hook {hook_type}[{i}].hooks[{j}] missing 'command'")
                
                # Validate timeout if present
                if "timeout" in sub_hook:
                    try:
                        timeout = int(sub_hook["timeout"])
                        if not (1 <= timeout <= 300):
                            errors.append(f"Hook timeout must be between 1 and 300 seconds")
                    except (ValueError, TypeError):
                        errors.append(f"Hook timeout must be a valid integer")
    
    return errors

def validate_agents_section(agents_config: Dict[str, Any]) -> List[str]:
    """Validate agents section."""
    errors = []
    
    required_keys = ["version", "framework_config", "performance_targets"]
    for key in required_keys:
        if key not in agents_config:
            errors.append(f"Missing required agents key: {key}")
    
    # Validate version
    if "version" in agents_config:
        try:
            version = agents_config["version"]
            if not isinstance(version, str) or not version:
                errors.append("agents.version must be a non-empty string")
        except (ValueError, TypeError):
            errors.append("agents.version must be a valid version string")
    
    # Validate framework_config boolean flags
    if "framework_config" in agents_config:
        framework_config = agents_config["framework_config"]
        boolean_flags = [
            "natural_delegation_enabled",
            "parallel_execution_enabled", 
            "sequential_intelligence_enabled",
            "memory_integration_enabled"
        ]
        
        for flag in boolean_flags:
            if flag in framework_config and not isinstance(framework_config[flag], bool):
                errors.append(f"agents.framework_config.{flag} must be a boolean")
    
    # Validate performance_targets
    if "performance_targets" in agents_config:
        performance_targets = agents_config["performance_targets"]
        numeric_targets = [
            ("agent_selection_time_ms", 100, 60000),
            ("coordination_latency_ms", 50, 10000),
            ("context_preservation_rate", 0.0, 1.0),
            ("sequential_accuracy_rate", 0.0, 1.0)
        ]
        
        for target, min_val, max_val in numeric_targets:
            if target in performance_targets:
                try:
                    value = float(performance_targets[target])
                    if not (min_val <= value <= max_val):
                        errors.append(f"agents.performance_targets.{target} must be between {min_val} and {max_val}")
                except (ValueError, TypeError):
                    errors.append(f"agents.performance_targets.{target} must be a valid number")
    
    return errors

def validate_configuration(config_path: Path) -> bool:
    """Validate the complete configuration file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error reading config: {e}")
        return False
    
    # Define validators mapping
    section_validators = {
        "env": validate_env_section,
        "permissions": validate_permissions_section, 
        "hooks": validate_hooks_section,
        "agents": validate_agents_section
    }
    
    all_errors = []
    
    # Validate each section dynamically
    for section_name, validator in section_validators.items():
        if section_name in config:
            all_errors.extend(validator(config[section_name]))
    
    # Report results
    if all_errors:
        print("❌ Configuration validation failed:")
        for error in all_errors:
            print(f"  • {error}")
        return False
    else:
        _print_validation_success(config)
        return True

def _print_validation_success(config: Dict[str, Any]) -> None:
    """Print successful validation details."""
    print("✅ Configuration validation passed!")
    print(f"  • Environment variables: {len(config.get('env', {}))}")
    print(f"  • Permission rules: {len(config.get('permissions', {}).get('allow', []))} allowed")
    print(f"  • Hook configurations: {len(config.get('hooks', {}))}")
    print(f"  • Agent framework version: {config.get('agents', {}).get('version', 'N/A')}")

def main():
    """Main validation function."""
    project_root = Path(__file__).parent.parent
    config_path = project_root / ".claude" / "settings.json"
    
    print("🔍 Validating Claude Code native configuration...")
    print(f"📁 Config file: {config_path}")
    print()
    
    success = validate_configuration(config_path)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()