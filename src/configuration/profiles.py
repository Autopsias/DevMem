"""Out-of-the-box configuration profiles for different use cases."""

from typing import Dict, Any, List
from dataclasses import asdict
from enum import Enum

from .defaults import DefaultConfigurationProvider
from .schema import AgentConfigurationSchema

class ConfigurationProfile(Enum):
    """Available configuration profiles."""
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    PERFORMANCE = "performance"
    SECURITY_FOCUSED = "security_focused"
    TESTING = "testing"
    MINIMAL = "minimal"
    EXPERIMENTAL = "experimental"
    CI_CD = "ci_cd"

class ConfigurationProfileManager:
    """Manages predefined configuration profiles for different use cases."""
    
    @classmethod
    def get_profile(cls, profile: ConfigurationProfile) -> AgentConfigurationSchema:
        """Get configuration for specified profile."""
        method_name = f"_get_{profile.value}_profile"
        
        if hasattr(cls, method_name):
            return getattr(cls, method_name)()
        else:
            raise ValueError(f"Unknown configuration profile: {profile.value}")
    
    @classmethod
    def list_available_profiles(cls) -> List[Dict[str, str]]:
        """List all available configuration profiles with descriptions."""
        return [
            {
                "name": "development",
                "title": "Development",
                "description": "Optimized for local development with enhanced debugging and hot reload"
            },
            {
                "name": "production",
                "title": "Production",
                "description": "Optimized for production use with stability and performance focus"
            },
            {
                "name": "performance",
                "title": "High Performance",
                "description": "Maximum performance configuration with aggressive optimizations"
            },
            {
                "name": "security_focused",
                "title": "Security Focused",
                "description": "Enhanced security monitoring and validation with security-first agents"
            },
            {
                "name": "testing",
                "title": "Testing",
                "description": "Configured for test environments with predictable behavior"
            },
            {
                "name": "minimal",
                "title": "Minimal",
                "description": "Lightweight configuration with only essential agents enabled"
            },
            {
                "name": "experimental",
                "title": "Experimental",
                "description": "Experimental features enabled for testing new capabilities"
            },
            {
                "name": "ci_cd",
                "title": "CI/CD",
                "description": "Optimized for continuous integration and deployment pipelines"
            }
        ]
    
    @classmethod
    def _get_development_profile(cls) -> AgentConfigurationSchema:
        """Development profile with debugging features enabled."""
        config = DefaultConfigurationProvider.create_complete_default_configuration()
        
        # Development-specific overrides
        config.global_settings.update({
            "hot_reload": True,
            "framework_enabled": True,
            "natural_delegation": True,
            "parallel_execution": True
        })
        
        config.performance.update({
            "token_optimization": False,  # Less aggressive for debugging
            "prompt_caching": True,
            "response_streaming": True,
            "resource_monitoring": True
        })
        
        config.monitoring.update({
            "performance_tracking": True,
            "coordination_logging": True,  # Verbose logging for development
            "usage_analytics": True,
            "error_reporting": True
        })
        
        # Enhanced timeouts for debugging
        for agent_name, agent_config in config.agents.items():
            agent_config.performance.response_timeout *= 1.5  # 50% longer timeouts
        
        return config
    
    @classmethod
    def _get_production_profile(cls) -> AgentConfigurationSchema:
        """Production profile optimized for stability and performance."""
        config = DefaultConfigurationProvider.create_complete_default_configuration()
        
        # Production-specific overrides
        config.global_settings.update({
            "hot_reload": False,  # Disabled for stability
            "framework_enabled": True,
            "natural_delegation": True,
            "parallel_execution": True
        })
        
        config.performance.update({
            "token_optimization": True,
            "prompt_caching": True,
            "response_streaming": True,
            "resource_monitoring": True
        })
        
        config.monitoring.update({
            "performance_tracking": True,
            "coordination_logging": False,  # Reduced logging in production
            "usage_analytics": True,
            "error_reporting": True
        })
        
        # Slightly reduced timeouts for responsiveness
        for agent_name, agent_config in config.agents.items():
            agent_config.performance.response_timeout *= 0.9  # 10% faster timeouts
            agent_config.coordination.escalation_threshold = max(1, agent_config.coordination.escalation_threshold - 1)
        
        return config
    
    @classmethod
    def _get_performance_profile(cls) -> AgentConfigurationSchema:
        """High-performance profile with aggressive optimizations."""
        config = DefaultConfigurationProvider.create_complete_default_configuration()
        
        # Performance-focused overrides
        config.global_settings.update({
            "hot_reload": False,
            "framework_enabled": True,
            "natural_delegation": True,
            "parallel_execution": True
        })
        
        config.performance.update({
            "token_optimization": True,
            "prompt_caching": True,
            "response_streaming": True,
            "resource_monitoring": True
        })
        
        config.monitoring.update({
            "performance_tracking": True,
            "coordination_logging": False,
            "usage_analytics": False,  # Reduced overhead
            "error_reporting": True
        })
        
        # Aggressive performance settings
        for agent_name, agent_config in config.agents.items():
            agent_config.performance.response_timeout *= 0.7  # 30% faster timeouts
            agent_config.performance.cache_enabled = True
            agent_config.performance.parallel_execution_limit = min(8, agent_config.performance.parallel_execution_limit * 2)
            agent_config.coordination.escalation_threshold = 1  # Quick escalation
        
        return config
    
    @classmethod
    def _get_security_focused_profile(cls) -> AgentConfigurationSchema:
        """Security-focused profile with enhanced security monitoring."""
        config = DefaultConfigurationProvider.create_complete_default_configuration()
        
        # Security-focused overrides
        config.global_settings.update({
            "hot_reload": False,  # Disabled for security
            "framework_enabled": True,
            "natural_delegation": True,
            "parallel_execution": False  # Sequential for security validation
        })
        
        config.monitoring.update({
            "performance_tracking": True,
            "coordination_logging": True,  # Enhanced logging for security audit
            "usage_analytics": True,
            "error_reporting": True
        })
        
        # Prioritize security agents
        security_agents = [
            "security-enforcer", "code-quality-specialist", "security-auditor",
            "architecture-validator", "pattern-analyzer"
        ]
        
        for agent_name, agent_config in config.agents.items():
            if agent_name in security_agents:
                # Enhanced settings for security agents
                agent_config.performance.response_timeout *= 1.5
                agent_config.performance.max_context_tokens = min(15000, agent_config.performance.max_context_tokens * 1.5)
                agent_config.coordination.escalation_threshold = 1
            else:
                # Reduced priority for non-security agents
                agent_config.performance.parallel_execution_limit = 1
        
        return config
    
    @classmethod
    def _get_testing_profile(cls) -> AgentConfigurationSchema:
        """Testing profile with predictable behavior."""
        config = DefaultConfigurationProvider.create_complete_default_configuration()
        
        # Testing-specific overrides
        config.global_settings.update({
            "hot_reload": False,
            "framework_enabled": True,
            "natural_delegation": False,  # Predictable behavior
            "parallel_execution": False  # Sequential for test stability
        })
        
        config.performance.update({
            "token_optimization": False,
            "prompt_caching": False,  # Consistent behavior
            "response_streaming": False,
            "resource_monitoring": False
        })
        
        config.monitoring.update({
            "performance_tracking": False,
            "coordination_logging": False,
            "usage_analytics": False,
            "error_reporting": True
        })
        
        # Consistent test settings
        for agent_name, agent_config in config.agents.items():
            agent_config.performance.response_timeout = 30.0  # Fixed timeout
            agent_config.performance.parallel_execution_limit = 1
            agent_config.performance.cache_enabled = False
            agent_config.coordination.auto_delegation = False
        
        return config
    
    @classmethod
    def _get_minimal_profile(cls) -> AgentConfigurationSchema:
        """Minimal profile with only essential agents enabled."""
        config = DefaultConfigurationProvider.create_complete_default_configuration()
        
        # Minimal resource usage
        config.performance.update({
            "token_optimization": True,
            "prompt_caching": False,  # Reduced memory usage
            "response_streaming": False,
            "resource_monitoring": False
        })
        
        config.monitoring.update({
            "performance_tracking": False,
            "coordination_logging": False,
            "usage_analytics": False,
            "error_reporting": True
        })
        
        # Essential agents only
        essential_agents = {
            "analysis-gateway", "digdeep", "test-specialist", 
            "code-quality-specialist", "git-commit-assistant",
            "lint-enforcer", "security-enforcer"
        }
        
        for agent_name, agent_config in config.agents.items():
            if agent_name not in essential_agents:
                agent_config.enabled = False
            else:
                # Minimal settings for enabled agents
                agent_config.performance.response_timeout = 20.0
                agent_config.performance.max_context_tokens = 5000
                agent_config.performance.parallel_execution_limit = 1
        
        return config
    
    @classmethod
    def _get_experimental_profile(cls) -> AgentConfigurationSchema:
        """Experimental profile with experimental features enabled."""
        config = DefaultConfigurationProvider.create_complete_default_configuration()
        
        # Experimental settings
        config.global_settings.update({
            "hot_reload": True,
            "framework_enabled": True,
            "natural_delegation": True,
            "parallel_execution": True
        })
        
        config.performance.update({
            "token_optimization": True,
            "prompt_caching": True,
            "response_streaming": True,
            "resource_monitoring": True
        })
        
        config.monitoring.update({
            "performance_tracking": True,
            "coordination_logging": True,
            "usage_analytics": True,
            "error_reporting": True
        })
        
        # Experimental agent settings
        for agent_name, agent_config in config.agents.items():
            # Higher parallelism for experimental features
            agent_config.performance.parallel_execution_limit = min(10, agent_config.performance.parallel_execution_limit * 3)
            agent_config.performance.max_context_tokens = min(20000, agent_config.performance.max_context_tokens * 2)
            agent_config.coordination.context_preservation_rate = 0.99
        
        return config
    
    @classmethod
    def _get_ci_cd_profile(cls) -> AgentConfigurationSchema:
        """CI/CD profile optimized for build and deployment pipelines."""
        config = DefaultConfigurationProvider.create_complete_default_configuration()
        
        # CI/CD-specific overrides
        config.global_settings.update({
            "hot_reload": False,
            "framework_enabled": True,
            "natural_delegation": True,
            "parallel_execution": True
        })
        
        config.performance.update({
            "token_optimization": True,
            "prompt_caching": True,
            "response_streaming": False,  # Simpler output for logs
            "resource_monitoring": False  # Reduce overhead
        })
        
        config.monitoring.update({
            "performance_tracking": False,
            "coordination_logging": False,
            "usage_analytics": False,
            "error_reporting": True
        })
        
        # CI/CD relevant agents prioritized
        ci_cd_agents = {
            "ci-specialist", "test-specialist", "code-quality-specialist",
            "infrastructure-engineer", "docker-specialist", "security-enforcer",
            "lint-enforcer", "git-commit-assistant"
        }
        
        for agent_name, agent_config in config.agents.items():
            if agent_name in ci_cd_agents:
                # Enhanced for CI/CD agents
                agent_config.performance.response_timeout *= 1.2
                agent_config.performance.parallel_execution_limit = min(5, agent_config.performance.parallel_execution_limit * 2)
            else:
                # Minimal resources for non-CI agents
                agent_config.enabled = False
        
        return config
    
    @classmethod
    def create_custom_profile(cls, base_profile: ConfigurationProfile, 
                            customizations: Dict[str, Any]) -> AgentConfigurationSchema:
        """Create custom profile based on existing profile with customizations."""
        config = cls.get_profile(base_profile)
        
        # Apply customizations
        if "global_settings" in customizations:
            config.global_settings.update(customizations["global_settings"])
        
        if "performance" in customizations:
            config.performance.update(customizations["performance"])
        
        if "monitoring" in customizations:
            config.monitoring.update(customizations["monitoring"])
        
        if "agents" in customizations:
            agent_customizations = customizations["agents"]
            for agent_name, agent_custom in agent_customizations.items():
                if agent_name in config.agents:
                    agent_config = config.agents[agent_name]
                    
                    if "enabled" in agent_custom:
                        agent_config.enabled = agent_custom["enabled"]
                    
                    if "performance" in agent_custom:
                        for key, value in agent_custom["performance"].items():
                            setattr(agent_config.performance, key, value)
                    
                    if "coordination" in agent_custom:
                        for key, value in agent_custom["coordination"].items():
                            setattr(agent_config.coordination, key, value)
        
        return config
    
    @classmethod
    def export_profile_as_settings_json(cls, profile: ConfigurationProfile) -> Dict[str, Any]:
        """Export profile as Claude Code settings.json format."""
        config = cls.get_profile(profile)
        
        # Convert to settings.json structure
        settings_json = {
            "agents": {
                "version": config.version,
                "global_settings": config.global_settings,
                "performance": config.performance,
                "monitoring": config.monitoring,
                "agents": {}
            }
        }
        
        # Convert agent configurations
        for agent_name, agent_config in config.agents.items():
            settings_json["agents"]["agents"][agent_name] = {
                "enabled": agent_config.enabled,
                "type": agent_config.type.value,
                "performance": asdict(agent_config.performance),
                "coordination": asdict(agent_config.coordination),
                "custom_settings": agent_config.custom_settings
            }
        
        return settings_json