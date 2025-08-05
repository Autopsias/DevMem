"""Agent configuration schema for Claude Code settings.json format."""

from typing import Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class AgentType(Enum):
    """Agent type classification for configuration purposes."""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    META = "meta"

class PerformanceLevel(Enum):
    """Performance optimization levels."""
    MINIMAL = "minimal"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"
    ADAPTIVE = "adaptive"

@dataclass
class AgentPerformanceConfig:
    """Performance configuration for individual agents."""
    response_timeout: float = 30.0
    max_context_tokens: int = 8000
    parallel_execution_limit: int = 3
    cache_enabled: bool = True
    optimization_level: PerformanceLevel = PerformanceLevel.BALANCED

@dataclass
class AgentCoordinationConfig:
    """Coordination behavior configuration."""
    auto_delegation: bool = True
    natural_language_triggers: bool = True
    sequential_intelligence: bool = True
    context_preservation_rate: float = 0.95
    escalation_threshold: int = 3

@dataclass
class AgentConfig:
    """Individual agent configuration."""
    name: str
    type: AgentType
    enabled: bool = True
    performance: AgentPerformanceConfig = field(default_factory=AgentPerformanceConfig)
    coordination: AgentCoordinationConfig = field(default_factory=AgentCoordinationConfig)
    custom_settings: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentConfigurationSchema:
    """Complete agent ecosystem configuration schema."""
    version: str = "1.0"
    
    # Global agent system settings
    global_settings: Dict[str, Any] = field(default_factory=lambda: {
        "framework_enabled": True,
        "natural_delegation": True,
        "parallel_execution": True,
        "hot_reload": True
    })
    
    # Performance optimization settings
    performance: Dict[str, Any] = field(default_factory=lambda: {
        "token_optimization": True,
        "prompt_caching": True,
        "response_streaming": True,
        "resource_monitoring": True
    })
    
    # Agent configurations by name
    agents: Dict[str, AgentConfig] = field(default_factory=dict)
    
    # Logging and monitoring
    monitoring: Dict[str, Any] = field(default_factory=lambda: {
        "performance_tracking": True,
        "coordination_logging": False,
        "usage_analytics": True,
        "error_reporting": True
    })
    
    # Environment-specific overrides
    environment_overrides: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def create_default_config(cls) -> "AgentConfigurationSchema":
        """Create default configuration with all 34 agents."""
        config = cls()
        
        # Define primary agents (20)
        primary_agents = [
            "digdeep", "test-specialist", "code-quality-specialist",
            "infrastructure-engineer", "ci-specialist", "environment-analyst",
            "intelligent-enhancer", "meta-coordinator", "framework-coordinator",
            "git-commit-assistant", "agent-reviewer", "agent-creator",
            "lint-enforcer", "security-enforcer", "token-monitor",
            "user-feedback-coordinator", "architecture-validator", "health-monitor",
            "synthesis-coordinator", "analysis-gateway"
        ]
        
        # Define secondary agents (14 remaining for 34 total)
        secondary_agents = [
            "async-pattern-fixer", "type-system-expert", "mock-configuration-expert",
            "validation-tester", "linting-engineer", "docker-specialist",
            "performance-optimizer", "resource-optimizer", "environment-synchronizer",
            "security-auditor", "pattern-analyzer", "refactoring-coordinator",
            "dependency-resolver", "coverage-optimizer"
        ]
        
        # Add primary agents with enhanced settings
        for agent_name in primary_agents:
            config.agents[agent_name] = AgentConfig(
                name=agent_name,
                type=AgentType.PRIMARY,
                performance=AgentPerformanceConfig(
                    response_timeout=30.0,
                    max_context_tokens=10000,
                    parallel_execution_limit=5
                ),
                coordination=AgentCoordinationConfig(
                    auto_delegation=True,
                    sequential_intelligence=True
                )
            )
        
        # Add secondary agents with standard settings
        for agent_name in secondary_agents:
            config.agents[agent_name] = AgentConfig(
                name=agent_name,
                type=AgentType.SECONDARY,
                performance=AgentPerformanceConfig(
                    response_timeout=20.0,
                    max_context_tokens=6000,
                    parallel_execution_limit=2
                )
            )
        
        # Add meta-coordinator with special settings
        config.agents["meta-coordinator"].type = AgentType.META
        config.agents["meta-coordinator"].performance.parallel_execution_limit = 8
        config.agents["meta-coordinator"].performance.max_context_tokens = 15000
        
        return config

class ConfigurationValidator:
    """Validates agent configuration against schema."""
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []
        
        # Validate version
        if "version" not in config:
            errors.append("Configuration version is required")
        
        # Validate agents section
        if "agents" in config:
            agents_config = config["agents"]
            if not isinstance(agents_config, dict):
                errors.append("Agents configuration must be a dictionary")
            else:
                errors.extend(ConfigurationValidator._validate_agents(agents_config))
        
        # Validate performance settings
        if "performance" in config:
            perf_config = config["performance"]
            errors.extend(ConfigurationValidator._validate_performance(perf_config))
        
        return errors
    
    @staticmethod
    def _validate_agents(agents_config: Dict[str, Any]) -> List[str]:
        """Validate individual agent configurations."""
        errors = []
        
        for agent_name, agent_config in agents_config.items():
            if not isinstance(agent_config, dict):
                errors.append(f"Agent '{agent_name}' configuration must be a dictionary")
                continue
            
            # Validate required fields
            if "type" not in agent_config:
                errors.append(f"Agent '{agent_name}' missing required 'type' field")
            
            # Validate performance settings
            if "performance" in agent_config:
                perf = agent_config["performance"]
                if "response_timeout" in perf and perf["response_timeout"] <= 0:
                    errors.append(f"Agent '{agent_name}' response_timeout must be positive")
                
                if "max_context_tokens" in perf and perf["max_context_tokens"] <= 0:
                    errors.append(f"Agent '{agent_name}' max_context_tokens must be positive")
        
        return errors
    
    @staticmethod
    def _validate_performance(perf_config: Dict[str, Any]) -> List[str]:
        """Validate performance configuration."""
        errors = []
        
        if not isinstance(perf_config, dict):
            errors.append("Performance configuration must be a dictionary")
        
        return errors