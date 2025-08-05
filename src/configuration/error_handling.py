"""Configuration error handling and recovery system."""

import json
import time
import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from .validation import ValidationIssue, ValidationSeverity
from .schema import AgentConfigurationSchema

logger = logging.getLogger(__name__)

class RecoveryStrategy(Enum):
    """Configuration recovery strategies."""
    IGNORE = "ignore"
    DEFAULT_VALUE = "default_value"
    BACKUP_RESTORE = "backup_restore"
    USER_PROMPT = "user_prompt"
    AUTO_FIX = "auto_fix"

@dataclass
class RecoveryAction:
    """Recovery action for configuration issues."""
    issue_path: str
    strategy: RecoveryStrategy
    action_data: Dict[str, Any]
    applied_at: float
    success: bool
    error_message: Optional[str] = None

class ConfigurationErrorHandler:
    """Handles configuration errors and provides recovery mechanisms."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize configuration error handler."""
        self.project_root = project_root or Path.cwd()
        self._recovery_log: List[RecoveryAction] = []
        self._recovery_callbacks: List[Callable[[RecoveryAction], None]] = []
        
        # Recovery strategy mapping by error type
        self._recovery_strategies = {
            ValidationSeverity.CRITICAL: RecoveryStrategy.BACKUP_RESTORE,
            ValidationSeverity.ERROR: RecoveryStrategy.AUTO_FIX,
            ValidationSeverity.WARNING: RecoveryStrategy.DEFAULT_VALUE,
            ValidationSeverity.INFO: RecoveryStrategy.IGNORE
        }
        
        # Backup configuration paths
        self._backup_dir = self.project_root / ".claude" / "config_backups"
        self._backup_dir.mkdir(parents=True, exist_ok=True)
    
    def handle_validation_issues(self, issues: List[ValidationIssue], 
                                current_config: Dict[str, Any]) -> Dict[str, Any]:
        """Handle validation issues and return recovered configuration."""
        if not issues:
            return current_config
        
        logger.info(f"Handling {len(issues)} configuration validation issues")
        
        # Create backup before any recovery attempts
        backup_path = self._create_backup(current_config)
        logger.info(f"Created configuration backup: {backup_path}")
        
        recovered_config = current_config.copy()
        
        # Process issues by severity (most critical first)
        sorted_issues = sorted(issues, key=lambda x: x.severity.value, reverse=True)
        
        for issue in sorted_issues:
            recovery_action = self._handle_single_issue(issue, recovered_config)
            self._recovery_log.append(recovery_action)
            
            # Notify callbacks
            for callback in self._recovery_callbacks:
                try:
                    callback(recovery_action)
                except Exception as e:
                    logger.error(f"Error in recovery callback: {e}")
        
        # Validate recovered configuration
        from .validation import ConfigurationValidator
        validator = ConfigurationValidator()
        remaining_issues = validator.validate_configuration(recovered_config)
        
        critical_issues = [i for i in remaining_issues if i.severity == ValidationSeverity.CRITICAL]
        if critical_issues:
            logger.error(f"Failed to resolve {len(critical_issues)} critical issues, restoring backup")
            return self._restore_from_backup(backup_path)
        
        logger.info(f"Successfully recovered configuration with {len(remaining_issues)} remaining issues")
        return recovered_config
    
    def _handle_single_issue(self, issue: ValidationIssue, config: Dict[str, Any]) -> RecoveryAction:
        """Handle a single validation issue."""
        strategy = self._recovery_strategies.get(issue.severity, RecoveryStrategy.IGNORE)
        
        recovery_action = RecoveryAction(
            issue_path=issue.path,
            strategy=strategy,
            action_data={},
            applied_at=time.time(),
            success=False
        )
        
        try:
            if strategy == RecoveryStrategy.IGNORE:
                recovery_action.success = True
                recovery_action.action_data = {"action": "ignored"}
                
            elif strategy == RecoveryStrategy.DEFAULT_VALUE:
                recovery_action.success = self._apply_default_value(issue, config, recovery_action)
                
            elif strategy == RecoveryStrategy.AUTO_FIX:
                recovery_action.success = self._apply_auto_fix(issue, config, recovery_action)
                
            elif strategy == RecoveryStrategy.BACKUP_RESTORE:
                recovery_action.success = self._prepare_backup_restore(issue, recovery_action)
                
            else:
                recovery_action.error_message = f"Unknown recovery strategy: {strategy}"
                
        except Exception as e:
            recovery_action.error_message = str(e)
            logger.error(f"Error applying recovery strategy {strategy} for {issue.path}: {e}")
        
        return recovery_action
    
    def _apply_default_value(self, issue: ValidationIssue, config: Dict[str, Any], 
                           action: RecoveryAction) -> bool:
        """Apply default value for configuration issue."""
        path_parts = issue.path.strip('/').split('/')
        
        # Default values for common configuration paths
        default_values = {
            "version": "1.0",
            "global_settings/framework_enabled": True,
            "global_settings/natural_delegation": True,
            "global_settings/parallel_execution": True,
            "global_settings/hot_reload": True,
            "performance/token_optimization": True,
            "performance/prompt_caching": True,
            "performance/response_streaming": True,
            "performance/resource_monitoring": True,
            "monitoring/performance_tracking": True,
            "monitoring/coordination_logging": False,
            "monitoring/usage_analytics": True,
            "monitoring/error_reporting": True
        }
        
        path_key = '/'.join(path_parts)
        if path_key in default_values:
            self._set_nested_value(config, path_parts, default_values[path_key])
            action.action_data = {
                "action": "set_default_value",
                "path": path_key,
                "value": default_values[path_key]
            }
            return True
        
        # Handle agent-specific defaults
        if len(path_parts) >= 2 and path_parts[0] == "agents":
            agent_name = path_parts[1]
            
            # Ensure agent exists
            if "agents" not in config:
                config["agents"] = {}
            if agent_name not in config["agents"]:
                config["agents"][agent_name] = {}
            
            # Apply agent-specific defaults
            if len(path_parts) == 3 and path_parts[2] == "enabled":
                config["agents"][agent_name]["enabled"] = True
                action.action_data = {"action": "enabled_agent", "agent": agent_name}
                return True
            elif len(path_parts) == 3 and path_parts[2] == "type":
                # Default to primary for known primary agents, secondary otherwise
                primary_agents = {
                    "digdeep", "test-specialist", "code-quality-specialist",
                    "infrastructure-engineer", "ci-specialist", "environment-analyst",
                    "intelligent-enhancer", "meta-coordinator", "framework-coordinator",
                    "git-commit-assistant", "agent-reviewer", "agent-creator",
                    "lint-enforcer", "security-enforcer", "token-monitor",
                    "user-feedback-coordinator", "architecture-validator", "health-monitor",
                    "synthesis-coordinator", "analysis-gateway"
                }
                agent_type = "primary" if agent_name in primary_agents else "secondary"
                config["agents"][agent_name]["type"] = agent_type
                action.action_data = {"action": "set_agent_type", "agent": agent_name, "type": agent_type}
                return True
        
        action.error_message = f"No default value available for path: {issue.path}"
        return False
    
    def _apply_auto_fix(self, issue: ValidationIssue, config: Dict[str, Any], 
                       action: RecoveryAction) -> bool:
        """Apply automatic fix for configuration issue."""
        # Auto-fix strategies based on issue message patterns
        if "must be boolean" in issue.message:
            return self._fix_boolean_value(issue, config, action)
        elif "must be a positive number" in issue.message or "must be a positive integer" in issue.message:
            return self._fix_numeric_value(issue, config, action)
        elif "must be between 0.0 and 1.0" in issue.message:
            return self._fix_range_value(issue, config, action, 0.0, 1.0)
        elif "Unknown" in issue.message:
            return self._fix_unknown_setting(issue, config, action)
        
        action.error_message = f"No auto-fix available for: {issue.message}"
        return False
    
    def _fix_boolean_value(self, issue: ValidationIssue, config: Dict[str, Any], 
                          action: RecoveryAction) -> bool:
        """Fix boolean value issues."""
        path_parts = issue.path.strip('/').split('/')
        current_value = self._get_nested_value(config, path_parts)
        
        if current_value is None:
            return False
        
        # Convert common boolean representations
        if isinstance(current_value, str):
            lower_val = current_value.lower()
            if lower_val in ("true", "yes", "1", "on"):
                fixed_value = True
            elif lower_val in ("false", "no", "0", "off"):
                fixed_value = False
            else:
                action.error_message = f"Cannot convert '{current_value}' to boolean"
                return False
        elif isinstance(current_value, (int, float)):
            fixed_value = bool(current_value)
        else:
            action.error_message = f"Cannot convert {type(current_value)} to boolean"
            return False
        
        self._set_nested_value(config, path_parts, fixed_value)
        action.action_data = {
            "action": "convert_to_boolean",
            "original_value": current_value,
            "fixed_value": fixed_value
        }
        return True
    
    def _fix_numeric_value(self, issue: ValidationIssue, config: Dict[str, Any], 
                          action: RecoveryAction) -> bool:
        """Fix numeric value issues."""
        path_parts = issue.path.strip('/').split('/')
        current_value = self._get_nested_value(config, path_parts)
        
        if current_value is None:
            return False
        
        try:
            # Try to convert to appropriate numeric type
            if "integer" in issue.message:
                if isinstance(current_value, str):
                    fixed_value = int(float(current_value))  # Handle "30.0" -> 30
                else:
                    fixed_value = int(current_value)
            else:
                fixed_value = float(current_value)
            
            # Ensure positive
            if fixed_value <= 0:
                # Use reasonable defaults based on path
                if "timeout" in issue.path.lower():
                    fixed_value = 30.0
                elif "token" in issue.path.lower():
                    fixed_value = 8000
                elif "limit" in issue.path.lower():
                    fixed_value = 3
                else:
                    fixed_value = 1
            
            self._set_nested_value(config, path_parts, fixed_value)
            action.action_data = {
                "action": "convert_to_numeric",
                "original_value": current_value,
                "fixed_value": fixed_value
            }
            return True
            
        except (ValueError, TypeError) as e:
            action.error_message = f"Cannot convert '{current_value}' to number: {e}"
            return False
    
    def _fix_range_value(self, issue: ValidationIssue, config: Dict[str, Any], 
                        action: RecoveryAction, min_val: float, max_val: float) -> bool:
        """Fix value that must be within a specific range."""
        path_parts = issue.path.strip('/').split('/')
        current_value = self._get_nested_value(config, path_parts)
        
        if current_value is None:
            return False
        
        try:
            numeric_value = float(current_value)
            fixed_value = max(min_val, min(numeric_value, max_val))
            
            self._set_nested_value(config, path_parts, fixed_value)
            action.action_data = {
                "action": "clamp_to_range",
                "original_value": current_value,
                "fixed_value": fixed_value,
                "range": f"{min_val}-{max_val}"
            }
            return True
            
        except (ValueError, TypeError) as e:
            action.error_message = f"Cannot convert '{current_value}' to number for range fixing: {e}"
            return False
    
    def _fix_unknown_setting(self, issue: ValidationIssue, config: Dict[str, Any], 
                           action: RecoveryAction) -> bool:
        """Fix unknown setting issues by removing them."""
        path_parts = issue.path.strip('/').split('/')
        
        if len(path_parts) >= 1:
            # Remove the unknown setting
            parent_parts = path_parts[:-1]
            setting_name = path_parts[-1]
            
            if parent_parts:
                parent = self._get_nested_value(config, parent_parts)
                if isinstance(parent, dict) and setting_name in parent:
                    del parent[setting_name]
            else:
                # Top-level setting
                if setting_name in config:
                    del config[setting_name]
            
            action.action_data = {
                "action": "remove_unknown_setting",
                "removed_setting": setting_name,
                "path": issue.path
            }
            return True
        
        return False
    
    def _prepare_backup_restore(self, issue: ValidationIssue, action: RecoveryAction) -> bool:
        """Prepare for backup restore (critical issues)."""
        action.action_data = {
            "action": "prepare_backup_restore",
            "issue": issue.message,
            "requires_backup_restore": True
        }
        return True
    
    def _create_backup(self, config: Dict[str, Any]) -> Path:
        """Create backup of current configuration."""
        timestamp = int(time.time())
        backup_filename = f"config_backup_{timestamp}.json"
        backup_path = self._backup_dir / backup_filename
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        # Keep only last 10 backups
        self._cleanup_old_backups()
        
        return backup_path
    
    def _cleanup_old_backups(self) -> None:
        """Clean up old backup files, keeping only the most recent 10."""
        backup_files = list(self._backup_dir.glob("config_backup_*.json"))
        backup_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        
        # Remove backups beyond the 10 most recent
        for old_backup in backup_files[10:]:
            try:
                old_backup.unlink()
                logger.debug(f"Removed old backup: {old_backup}")
            except Exception as e:
                logger.warning(f"Failed to remove old backup {old_backup}: {e}")
    
    def _restore_from_backup(self, backup_path: Path) -> Dict[str, Any]:
        """Restore configuration from backup file."""
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                restored_config = json.load(f)
            
            logger.info(f"Restored configuration from backup: {backup_path}")
            return restored_config
            
        except Exception as e:
            logger.error(f"Failed to restore from backup {backup_path}: {e}")
            # Return default configuration as last resort
            return AgentConfigurationSchema.create_default_config().__dict__
    
    def _get_nested_value(self, data: Dict[str, Any], path_parts: List[str]) -> Any:
        """Get nested value from dictionary using path parts."""
        current = data
        for part in path_parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current
    
    def _set_nested_value(self, data: Dict[str, Any], path_parts: List[str], value: Any) -> None:
        """Set nested value in dictionary using path parts."""
        current = data
        for part in path_parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        current[path_parts[-1]] = value
    
    def register_recovery_callback(self, callback: Callable[[RecoveryAction], None]) -> None:
        """Register callback for recovery actions."""
        self._recovery_callbacks.append(callback)
    
    def get_recovery_log(self) -> List[RecoveryAction]:
        """Get log of all recovery actions."""
        return self._recovery_log.copy()
    
    def get_recovery_statistics(self) -> Dict[str, Any]:
        """Get statistics about recovery actions."""
        if not self._recovery_log:
            return {"total_recoveries": 0}
        
        by_strategy = {}
        by_success = {"successful": 0, "failed": 0}
        
        for action in self._recovery_log:
            strategy_name = action.strategy.value
            by_strategy[strategy_name] = by_strategy.get(strategy_name, 0) + 1
            
            if action.success:
                by_success["successful"] += 1
            else:
                by_success["failed"] += 1
        
        return {
            "total_recoveries": len(self._recovery_log),
            "by_strategy": by_strategy,
            "by_success": by_success,
            "success_rate": by_success["successful"] / len(self._recovery_log),
            "last_recovery": max(self._recovery_log, key=lambda a: a.applied_at).applied_at if self._recovery_log else None
        }