"""Environment variable handler for Claude Code agent configuration."""

import os
import re
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class EnvironmentVariableHandler:
    """Handles environment variable configuration for agent ecosystem."""
    
    # Environment variable naming conventions
    PREFIX = "CLAUDE_AGENT"
    SEPARATORS = {
        "SECTION": "_",
        "AGENT": "__",
        "PROPERTY": "_"
    }
    
    # Valid environment variable patterns
    PATTERNS = {
        # Global settings: CLAUDE_AGENT_FRAMEWORK_ENABLED=true
        "GLOBAL": re.compile(rf"^{PREFIX}_(FRAMEWORK_ENABLED|NATURAL_DELEGATION|PARALLEL_EXECUTION|HOT_RELOAD)$"),
        
        # Performance settings: CLAUDE_AGENT_PERFORMANCE_TOKEN_OPTIMIZATION=true
        "PERFORMANCE": re.compile(rf"^{PREFIX}_PERFORMANCE_(TOKEN_OPTIMIZATION|PROMPT_CACHING|RESPONSE_STREAMING|RESOURCE_MONITORING)$"),
        
        # Monitoring settings: CLAUDE_AGENT_MONITORING_PERFORMANCE_TRACKING=false
        "MONITORING": re.compile(rf"^{PREFIX}_MONITORING_(PERFORMANCE_TRACKING|COORDINATION_LOGGING|USAGE_ANALYTICS|ERROR_REPORTING)$"),
        
        # Agent-specific settings: CLAUDE_AGENT__TEST_SPECIALIST_ENABLED=false
        "AGENT_GLOBAL": re.compile(rf"^{PREFIX}__([A-Z_]+)_(ENABLED|TYPE)$"),
        
        # Agent performance: CLAUDE_AGENT__TEST_SPECIALIST_PERFORMANCE_TIMEOUT=30.0
        "AGENT_PERFORMANCE": re.compile(rf"^{PREFIX}__([A-Z_]+)_PERFORMANCE_(RESPONSE_TIMEOUT|MAX_CONTEXT_TOKENS|PARALLEL_EXECUTION_LIMIT|CACHE_ENABLED)$"),
        
        # Agent coordination: CLAUDE_AGENT__TEST_SPECIALIST_COORDINATION_AUTO_DELEGATION=true
        "AGENT_COORDINATION": re.compile(rf"^{PREFIX}__([A-Z_]+)_COORDINATION_(AUTO_DELEGATION|NATURAL_LANGUAGE_TRIGGERS|SEQUENTIAL_INTELLIGENCE|CONTEXT_PRESERVATION_RATE|ESCALATION_THRESHOLD)$")
    }
    
    def __init__(self):
        """Initialize environment variable handler."""
        self._env_cache: Optional[Dict[str, Any]] = None
        self._last_scan_env_vars: Optional[Dict[str, str]] = None
    
    def get_environment_config(self) -> Dict[str, Any]:
        """Get configuration overrides from environment variables."""
        current_env = {k: v for k, v in os.environ.items() if k.startswith(self.PREFIX)}
        
        # Check if environment has changed
        if self._last_scan_env_vars != current_env:
            logger.debug("Environment variables changed, rescanning...")
            self._env_cache = self._parse_environment_variables()
            self._last_scan_env_vars = current_env.copy()
        
        return self._env_cache or {}
    
    def _parse_environment_variables(self) -> Dict[str, Any]:
        """Parse all relevant environment variables into configuration structure."""
        config = {
            "global_settings": {},
            "performance": {},
            "monitoring": {},
            "agents": {}
        }
        
        for env_var, env_value in os.environ.items():
            if not env_var.startswith(self.PREFIX):
                continue
            
            try:
                parsed_value = self._parse_env_value(env_value)
                self._apply_env_var_to_config(config, env_var, parsed_value)
            except Exception as e:
                logger.warning(f"Failed to parse environment variable {env_var}={env_value}: {e}")
        
        # Remove empty sections
        config = {k: v for k, v in config.items() if v}
        
        if config:
            logger.info(f"Loaded configuration from {len([k for k in os.environ.keys() if k.startswith(self.PREFIX)])} environment variables")
        
        return config
    
    def _apply_env_var_to_config(self, config: Dict[str, Any], env_var: str, value: Any) -> None:
        """Apply single environment variable to configuration structure."""
        # Check against each pattern
        for pattern_name, pattern in self.PATTERNS.items():
            match = pattern.match(env_var)
            if match:
                self._handle_pattern_match(config, pattern_name, match, value)
                return
        
        logger.debug(f"Environment variable {env_var} doesn't match any known pattern")
    
    def _handle_pattern_match(self, config: Dict[str, Any], pattern_name: str, match: re.Match, value: Any) -> None:
        """Handle matched environment variable pattern."""
        if pattern_name == "GLOBAL":
            # CLAUDE_AGENT_FRAMEWORK_ENABLED -> global_settings.framework_enabled
            key = match.group(1).lower()
            config["global_settings"][key] = value
            
        elif pattern_name == "PERFORMANCE":
            # CLAUDE_AGENT_PERFORMANCE_TOKEN_OPTIMIZATION -> performance.token_optimization
            key = match.group(1).lower()
            config["performance"][key] = value
            
        elif pattern_name == "MONITORING":
            # CLAUDE_AGENT_MONITORING_PERFORMANCE_TRACKING -> monitoring.performance_tracking
            key = match.group(1).lower()
            config["monitoring"][key] = value
            
        elif pattern_name == "AGENT_GLOBAL":
            # CLAUDE_AGENT__TEST_SPECIALIST_ENABLED -> agents.test-specialist.enabled
            agent_name = self._normalize_agent_name(match.group(1))
            property_name = match.group(2).lower()
            
            if agent_name not in config["agents"]:
                config["agents"][agent_name] = {}
            
            config["agents"][agent_name][property_name] = value
            
        elif pattern_name == "AGENT_PERFORMANCE":
            # CLAUDE_AGENT__TEST_SPECIALIST_PERFORMANCE_TIMEOUT -> agents.test-specialist.performance.response_timeout
            agent_name = self._normalize_agent_name(match.group(1))
            property_name = match.group(2).lower()
            
            if agent_name not in config["agents"]:
                config["agents"][agent_name] = {}
            if "performance" not in config["agents"][agent_name]:
                config["agents"][agent_name]["performance"] = {}
            
            config["agents"][agent_name]["performance"][property_name] = value
            
        elif pattern_name == "AGENT_COORDINATION":
            # CLAUDE_AGENT__TEST_SPECIALIST_COORDINATION_AUTO_DELEGATION -> agents.test-specialist.coordination.auto_delegation
            agent_name = self._normalize_agent_name(match.group(1))
            property_name = match.group(2).lower()
            
            if agent_name not in config["agents"]:
                config["agents"][agent_name] = {}
            if "coordination" not in config["agents"][agent_name]:
                config["agents"][agent_name]["coordination"] = {}
            
            config["agents"][agent_name]["coordination"][property_name] = value
    
    def _normalize_agent_name(self, env_agent_name: str) -> str:
        """Normalize environment variable agent name to standard format."""
        # Convert TEST_SPECIALIST to test-specialist
        return env_agent_name.lower().replace("_", "-")
    
    def _parse_env_value(self, env_value: str) -> Any:
        """Parse environment variable value to appropriate Python type."""
        # Handle boolean values
        lower_value = env_value.lower()
        if lower_value in ("true", "yes", "1", "on"):
            return True
        elif lower_value in ("false", "no", "0", "off"):
            return False
        
        # Handle numeric values
        try:
            # Try integer first
            if '.' not in env_value:
                return int(env_value)
            else:
                return float(env_value)
        except ValueError:
            pass
        
        # Handle JSON values (for complex structures)
        if env_value.startswith('{') or env_value.startswith('['):
            try:
                import json
                return json.loads(env_value)
            except json.JSONDecodeError:
                pass
        
        # Return as string
        return env_value
    
    def get_documentation(self) -> Dict[str, Any]:
        """Get documentation for all supported environment variables."""
        return {
            "prefix": self.PREFIX,
            "global_settings": {
                f"{self.PREFIX}_FRAMEWORK_ENABLED": {
                    "description": "Enable/disable the entire agent framework",
                    "type": "boolean",
                    "default": True,
                    "example": "CLAUDE_AGENT_FRAMEWORK_ENABLED=false"
                },
                f"{self.PREFIX}_NATURAL_DELEGATION": {
                    "description": "Enable natural language delegation between agents",
                    "type": "boolean", 
                    "default": True,
                    "example": "CLAUDE_AGENT_NATURAL_DELEGATION=true"
                },
                f"{self.PREFIX}_PARALLEL_EXECUTION": {
                    "description": "Enable parallel agent execution",
                    "type": "boolean",
                    "default": True,
                    "example": "CLAUDE_AGENT_PARALLEL_EXECUTION=true"
                },
                f"{self.PREFIX}_HOT_RELOAD": {
                    "description": "Enable hot reload of configuration changes",
                    "type": "boolean",
                    "default": True,
                    "example": "CLAUDE_AGENT_HOT_RELOAD=false"
                }
            },
            "performance_settings": {
                f"{self.PREFIX}_PERFORMANCE_TOKEN_OPTIMIZATION": {
                    "description": "Enable token usage optimization",
                    "type": "boolean",
                    "default": True,
                    "example": "CLAUDE_AGENT_PERFORMANCE_TOKEN_OPTIMIZATION=true"
                },
                f"{self.PREFIX}_PERFORMANCE_PROMPT_CACHING": {
                    "description": "Enable prompt caching for better performance",
                    "type": "boolean",
                    "default": True,
                    "example": "CLAUDE_AGENT_PERFORMANCE_PROMPT_CACHING=false"
                }
            },
            "agent_specific": {
                f"{self.PREFIX}__AGENT_NAME_ENABLED": {
                    "description": "Enable/disable specific agent (replace AGENT_NAME with actual agent name in uppercase with underscores)",
                    "type": "boolean",
                    "example": "CLAUDE_AGENT__TEST_SPECIALIST_ENABLED=false"
                },
                f"{self.PREFIX}__AGENT_NAME_PERFORMANCE_RESPONSE_TIMEOUT": {
                    "description": "Set response timeout for specific agent in seconds",
                    "type": "float",
                    "example": "CLAUDE_AGENT__TEST_SPECIALIST_PERFORMANCE_RESPONSE_TIMEOUT=45.0"
                }
            },
            "agent_names": [
                "DIGDEEP", "TEST_SPECIALIST", "CODE_QUALITY_SPECIALIST",
                "INFRASTRUCTURE_ENGINEER", "CI_SPECIALIST", "ENVIRONMENT_ANALYST",
                "INTELLIGENT_ENHANCER", "META_COORDINATOR", "FRAMEWORK_COORDINATOR",
                "GIT_COMMIT_ASSISTANT", "AGENT_REVIEWER", "AGENT_CREATOR",
                "LINT_ENFORCER", "SECURITY_ENFORCER", "TOKEN_MONITOR",
                "USER_FEEDBACK_COORDINATOR", "ARCHITECTURE_VALIDATOR", "HEALTH_MONITOR",
                "SYNTHESIS_COORDINATOR", "ANALYSIS_GATEWAY", "ASYNC_PATTERN_FIXER",
                "TYPE_SYSTEM_EXPERT", "MOCK_CONFIGURATION_EXPERT", "VALIDATION_TESTER",
                "LINTING_ENGINEER", "DOCKER_SPECIALIST", "PERFORMANCE_OPTIMIZER",
                "RESOURCE_OPTIMIZER", "ENVIRONMENT_SYNCHRONIZER", "SECURITY_AUDITOR",
                "PATTERN_ANALYZER", "REFACTORING_COORDINATOR", "DEPENDENCY_RESOLVER",
                "COVERAGE_OPTIMIZER"
            ]
        }
    
    def validate_environment_variables(self) -> List[str]:
        """Validate all agent-related environment variables."""
        warnings = []
        
        for env_var in os.environ:
            if not env_var.startswith(self.PREFIX):
                continue
            
            # Check if it matches any valid pattern
            is_valid = any(pattern.match(env_var) for pattern in self.PATTERNS.values())
            
            if not is_valid:
                warnings.append(f"Unknown environment variable: {env_var}")
        
        return warnings