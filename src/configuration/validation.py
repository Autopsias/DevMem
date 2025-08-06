"""Comprehensive configuration validation system."""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import re
import logging

logger = logging.getLogger(__name__)

class ValidationSeverity(Enum):
    """Validation error severity levels."""
    INFO = "info"
    WARNING = "warning"  
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class ValidationIssue:
    """Represents a configuration validation issue."""
    severity: ValidationSeverity
    message: str
    path: str
    value: Any = None
    suggestion: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "severity": self.severity.value,
            "message": self.message,
            "path": self.path,
            "value": self.value,
            "suggestion": self.suggestion
        }

class ConfigurationValidator:
    """Comprehensive configuration validation system."""
    
    def __init__(self):
        """Initialize configuration validator."""
        self._validators: Dict[str, Callable] = {
            "global_settings": self._validate_global_settings,
            "performance": self._validate_performance_settings,
            "monitoring": self._validate_monitoring_settings,
            "agents": self._validate_agents_configuration,
            "environment_overrides": self._validate_environment_overrides
        }
        
        # Known agent names for validation
        self._known_agents = {
            # Primary agents
            "digdeep", "test-specialist", "code-quality-specialist",
            "infrastructure-engineer", "ci-specialist", "environment-analyst", 
            "intelligent-enhancer", "meta-coordinator", "framework-coordinator",
            "git-commit-assistant", "agent-reviewer", "agent-creator",
            "lint-enforcer", "security-enforcer", "token-monitor",
            "user-feedback-coordinator", "architecture-validator", "health-monitor",
            "synthesis-coordinator", "analysis-gateway",
            
            # Secondary agents
            "async-pattern-fixer", "type-system-expert", "mock-configuration-expert",
            "validation-tester", "linting-engineer", "docker-specialist",
            "performance-optimizer", "resource-optimizer", "environment-synchronizer",
            "security-auditor", "pattern-analyzer", "refactoring-coordinator",
            "dependency-resolver", "coverage-optimizer"
        }
    
    def validate_configuration(self, config: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate complete configuration and return all issues."""
        issues = []
        
        # Validate configuration structure
        issues.extend(self._validate_structure(config))
        
        # Validate each section
        for section_name, validator in self._validators.items():
            if section_name in config:
                try:
                    section_issues = validator(config[section_name], f"/{section_name}")
                    issues.extend(section_issues)
                except Exception as e:
                    issues.append(ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        message=f"Failed to validate section '{section_name}': {e}",
                        path=f"/{section_name}"
                    ))
        
        # Cross-section validation
        issues.extend(self._validate_cross_section_consistency(config))
        
        return issues
    
    def _validate_structure(self, config: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate basic configuration structure."""
        issues = []
        
        # Check version
        if "version" not in config:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                message="Configuration version is missing",
                path="/version",
                suggestion="Add version field to track configuration schema"
            ))
        elif not isinstance(config["version"], str):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                message="Version must be a string",
                path="/version",
                value=config["version"]
            ))
        
        # Check for unknown top-level keys
        known_keys = {"version", "global_settings", "performance", "monitoring", 
                     "agents", "environment_overrides"}
        unknown_keys = set(config.keys()) - known_keys
        
        for key in unknown_keys:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                message=f"Unknown configuration section: {key}",
                path=f"/{key}",
                suggestion="Remove unknown sections or check documentation"
            ))
        
        return issues
    
    def _validate_global_settings(self, settings: Dict[str, Any], path: str) -> List[ValidationIssue]:
        """Validate global framework settings."""
        issues = []
        
        known_settings = {
            "framework_enabled", "natural_delegation", "parallel_execution", "hot_reload"
        }
        
        for key, value in settings.items():
            current_path = f"{path}/{key}"
            
            if key not in known_settings:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message=f"Unknown global setting: {key}",
                    path=current_path
                ))
                continue
            
            # All global settings should be boolean
            if not isinstance(value, bool):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message=f"Global setting '{key}' must be boolean",
                    path=current_path,
                    value=value,
                    suggestion=f"Use true or false instead of '{value}'"
                ))
        
        return issues
    
    def _validate_performance_settings(self, settings: Dict[str, Any], path: str) -> List[ValidationIssue]:
        """Validate performance configuration."""
        issues = []
        
        known_settings = {
            "token_optimization", "prompt_caching", "response_streaming", "resource_monitoring"
        }
        
        for key, value in settings.items():
            current_path = f"{path}/{key}"
            
            if key not in known_settings:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message=f"Unknown performance setting: {key}",
                    path=current_path
                ))
                continue
                
            # Performance settings should be boolean
            if not isinstance(value, bool):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message=f"Performance setting '{key}' must be boolean",
                    path=current_path,
                    value=value
                ))
        
        return issues
    
    def _validate_monitoring_settings(self, settings: Dict[str, Any], path: str) -> List[ValidationIssue]:
        """Validate monitoring configuration."""
        issues = []
        
        known_settings = {
            "performance_tracking", "coordination_logging", "usage_analytics", "error_reporting"
        }
        
        for key, value in settings.items():
            current_path = f"{path}/{key}"
            
            if key not in known_settings:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message=f"Unknown monitoring setting: {key}",
                    path=current_path
                ))
                continue
                
            # Monitoring settings should be boolean
            if not isinstance(value, bool):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message=f"Monitoring setting '{key}' must be boolean",
                    path=current_path,
                    value=value
                ))
        
        return issues
    
    def _validate_agents_configuration(self, agents_config: Dict[str, Any], path: str) -> List[ValidationIssue]:
        """Validate agents configuration."""
        issues = []
        
        if not isinstance(agents_config, dict):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.CRITICAL,
                message="Agents configuration must be a dictionary",
                path=path,
                value=type(agents_config).__name__
            ))
            return issues
        
        for agent_name, agent_config in agents_config.items():
            agent_path = f"{path}/{agent_name}"
            
            # Validate agent name
            if agent_name not in self._known_agents:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message=f"Unknown agent: {agent_name}",
                    path=agent_path,
                    suggestion=f"Known agents: {', '.join(sorted(self._known_agents))}"
                ))
            
            # Validate agent configuration
            if isinstance(agent_config, dict):
                issues.extend(self._validate_single_agent_config(agent_config, agent_path))
            else:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message=f"Agent configuration for '{agent_name}' must be a dictionary",
                    path=agent_path,
                    value=type(agent_config).__name__
                ))
        
        return issues
    
    def _validate_single_agent_config(self, config: Dict[str, Any], path: str) -> List[ValidationIssue]:
        """Validate single agent configuration."""
        issues = []
        
        # Validate enabled field
        if "enabled" in config:
            if not isinstance(config["enabled"], bool):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message="Agent 'enabled' field must be boolean",
                    path=f"{path}/enabled",
                    value=config["enabled"]
                ))
        
        # Validate type field
        if "type" in config:
            valid_types = {"primary", "secondary", "meta"}
            if config["type"] not in valid_types:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message=f"Invalid agent type: {config['type']}",
                    path=f"{path}/type",
                    value=config["type"],
                    suggestion=f"Use one of: {', '.join(valid_types)}"
                ))
        
        # Validate performance section
        if "performance" in config:
            issues.extend(self._validate_agent_performance(config["performance"], f"{path}/performance"))
        
        # Validate coordination section
        if "coordination" in config:
            issues.extend(self._validate_agent_coordination(config["coordination"], f"{path}/coordination"))
        
        return issues
    
    def _validate_agent_performance(self, performance: Dict[str, Any], path: str) -> List[ValidationIssue]:
        """Validate agent performance configuration."""
        issues = []
        
        # Validate response_timeout
        if "response_timeout" in performance:
            timeout = performance["response_timeout"]
            if not isinstance(timeout, (int, float)) or timeout <= 0:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message="response_timeout must be a positive number",
                    path=f"{path}/response_timeout",
                    value=timeout
                ))
            elif timeout > 300:  # 5 minutes
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message="response_timeout is very high (>5 minutes)",
                    path=f"{path}/response_timeout",
                    value=timeout,
                    suggestion="Consider reducing timeout for better responsiveness"
                ))
        
        # Validate max_context_tokens
        if "max_context_tokens" in performance:
            tokens = performance["max_context_tokens"]
            if not isinstance(tokens, int) or tokens <= 0:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message="max_context_tokens must be a positive integer",
                    path=f"{path}/max_context_tokens",
                    value=tokens
                ))
            elif tokens > 100000:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message="max_context_tokens is very high",
                    path=f"{path}/max_context_tokens",
                    value=tokens,
                    suggestion="High token limits may impact performance and cost"
                ))
        
        # Validate parallel_execution_limit
        if "parallel_execution_limit" in performance:
            limit = performance["parallel_execution_limit"]
            if not isinstance(limit, int) or limit <= 0:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message="parallel_execution_limit must be a positive integer",
                    path=f"{path}/parallel_execution_limit",
                    value=limit
                ))
            elif limit > 10:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message="parallel_execution_limit is very high",
                    path=f"{path}/parallel_execution_limit",
                    value=limit,
                    suggestion="High parallelism may cause resource contention"
                ))
        
        return issues
    
    def _validate_agent_coordination(self, coordination: Dict[str, Any], path: str) -> List[ValidationIssue]:
        """Validate agent coordination configuration."""
        issues = []
        
        boolean_fields = {"auto_delegation", "natural_language_triggers", "sequential_intelligence"}
        
        for field in boolean_fields:
            if field in coordination:
                if not isinstance(coordination[field], bool):
                    issues.append(ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        message=f"Coordination '{field}' must be boolean",
                        path=f"{path}/{field}",
                        value=coordination[field]
                    ))
        
        # Validate context_preservation_rate
        if "context_preservation_rate" in coordination:
            rate = coordination["context_preservation_rate"]
            if not isinstance(rate, (int, float)) or not (0.0 <= rate <= 1.0):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message="context_preservation_rate must be between 0.0 and 1.0",
                    path=f"{path}/context_preservation_rate",
                    value=rate
                ))
        
        # Validate escalation_threshold
        if "escalation_threshold" in coordination:
            threshold = coordination["escalation_threshold"]
            if not isinstance(threshold, int) or threshold <= 0:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message="escalation_threshold must be a positive integer",
                    path=f"{path}/escalation_threshold",
                    value=threshold
                ))
        
        return issues
    
    def _validate_environment_overrides(self, overrides: Dict[str, Any], path: str) -> List[ValidationIssue]:
        """Validate environment-specific overrides."""
        issues = []
        
        for env_name, env_config in overrides.items():
            env_path = f"{path}/{env_name}"
            
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', env_name):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message=f"Environment name '{env_name}' should contain only alphanumeric characters, hyphens, and underscores",
                    path=env_path
                ))
            
            # Recursively validate environment configuration
            if isinstance(env_config, dict):
                issues.extend(self.validate_configuration(env_config))
        
        return issues
    
    def _validate_cross_section_consistency(self, config: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate consistency across configuration sections."""
        issues = []
        
        global_settings = config.get("global_settings", {})
        agents_config = config.get("agents", {})
        
        # Check framework enabled vs agents enabled
        framework_enabled = global_settings.get("framework_enabled", True)
        if not framework_enabled:
            enabled_agents = [
                name for name, agent_config in agents_config.items() 
                if isinstance(agent_config, dict) and agent_config.get("enabled", True)
            ]
            
            if enabled_agents:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message="Framework is disabled but some agents are enabled",
                    path="/global_settings/framework_enabled",
                    value=False,
                    suggestion=f"Consider disabling agents: {', '.join(enabled_agents)}"
                ))
        
        # Check parallel execution vs agent limits
        parallel_enabled = global_settings.get("parallel_execution", True)
        if not parallel_enabled:
            agents_with_parallel = [
                name for name, agent_config in agents_config.items()
                if (isinstance(agent_config, dict) and 
                    agent_config.get("performance", {}).get("parallel_execution_limit", 1) > 1)
            ]
            
            if agents_with_parallel:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.INFO,
                    message="Parallel execution disabled but some agents have parallel limits > 1",
                    path="/global_settings/parallel_execution",
                    value=False,
                    suggestion=f"Agent parallel limits will be ignored for: {', '.join(agents_with_parallel)}"
                ))
        
        return issues
    
    def get_validation_summary(self, issues: List[ValidationIssue]) -> Dict[str, Any]:
        """Get summary of validation results."""
        by_severity = {}
        for severity in ValidationSeverity:
            by_severity[severity.value] = [
                issue for issue in issues if issue.severity == severity
            ]
        
        return {
            "total_issues": len(issues),
            "by_severity": {
                severity: len(issues_list) 
                for severity, issues_list in by_severity.items()
            },
            "has_errors": any(issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL] 
                            for issue in issues),
            "has_warnings": any(issue.severity == ValidationSeverity.WARNING for issue in issues)
        }