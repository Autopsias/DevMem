"""Test default configurations and profiles effectiveness."""

import pytest
from typing import Dict, Any

from src.configuration.defaults import DefaultConfigurationProvider
from src.configuration.profiles import ConfigurationProfileManager, ConfigurationProfile
from src.configuration.schema import AgentConfigurationSchema, AgentType
from src.configuration.validation import ConfigurationValidator


class TestDefaultConfigurations:
    """Test default configuration effectiveness."""
    
    def test_default_configuration_creation(self):
        """Test that default configuration is created successfully."""
        config = DefaultConfigurationProvider.create_complete_default_configuration()
        
        assert isinstance(config, AgentConfigurationSchema)
        assert config.version == "1.0"
        assert len(config.agents) == 34  # Total number of agents
        
        # Verify all agents have required fields
        for agent_name, agent_config in config.agents.items():
            assert agent_config.name == agent_name
            assert isinstance(agent_config.type, AgentType)
            assert isinstance(agent_config.enabled, bool)
            assert agent_config.performance is not None
            assert agent_config.coordination is not None
    
    def test_default_global_settings(self):
        """Test default global settings are sensible."""
        settings = DefaultConfigurationProvider.get_default_global_settings()
        
        # Framework should be enabled by default
        assert settings["framework_enabled"] is True
        assert settings["natural_delegation"] is True
        assert settings["parallel_execution"] is True
        assert settings["hot_reload"] is True
    
    def test_default_performance_settings(self):
        """Test default performance settings are appropriate."""
        settings = DefaultConfigurationProvider.get_default_performance_settings()
        
        # Performance optimizations should be enabled
        assert settings["token_optimization"] is True
        assert settings["prompt_caching"] is True
        assert settings["response_streaming"] is True
        assert settings["resource_monitoring"] is True
    
    def test_default_monitoring_settings(self):
        """Test default monitoring settings balance visibility and performance."""
        settings = DefaultConfigurationProvider.get_default_monitoring_settings()
        
        # Essential monitoring enabled, verbose logging disabled
        assert settings["performance_tracking"] is True
        assert settings["coordination_logging"] is False  # Too verbose for default
        assert settings["usage_analytics"] is True
        assert settings["error_reporting"] is True
    
    def test_agent_type_defaults(self):
        """Test that different agent types have appropriate defaults."""
        primary_defaults = DefaultConfigurationProvider.get_primary_agent_defaults()
        secondary_defaults = DefaultConfigurationProvider.get_secondary_agent_defaults()
        meta_defaults = DefaultConfigurationProvider.get_meta_agent_defaults()
        
        # Primary agents should have more resources
        assert primary_defaults.performance.response_timeout > secondary_defaults.performance.response_timeout
        assert primary_defaults.performance.max_context_tokens > secondary_defaults.performance.max_context_tokens
        assert primary_defaults.performance.parallel_execution_limit > secondary_defaults.performance.parallel_execution_limit
        
        # Meta agents should have the most resources
        assert meta_defaults.performance.response_timeout > primary_defaults.performance.response_timeout
        assert meta_defaults.performance.max_context_tokens > primary_defaults.performance.max_context_tokens
        assert meta_defaults.performance.parallel_execution_limit > primary_defaults.performance.parallel_execution_limit
        
        # Coordination differences
        assert primary_defaults.coordination.auto_delegation is True
        assert secondary_defaults.coordination.auto_delegation is False  # Don't initiate delegation
        assert meta_defaults.coordination.escalation_threshold > primary_defaults.coordination.escalation_threshold
    
    def test_agent_specific_overrides(self):
        """Test that agent-specific overrides are applied correctly."""
        config = DefaultConfigurationProvider.create_complete_default_configuration()
        
        # Test specific agent overrides
        digdeep = config.agents["digdeep"]
        assert digdeep.performance.response_timeout == 45.0  # Override applied
        
        lint_enforcer = config.agents["lint-enforcer"]
        assert lint_enforcer.performance.response_timeout == 15.0  # Fast response
        assert lint_enforcer.performance.parallel_execution_limit == 1  # Sequential
        
        meta_coordinator = config.agents["meta-coordinator"]
        assert meta_coordinator.performance.max_context_tokens == 15000  # High context
        assert meta_coordinator.performance.parallel_execution_limit == 8  # High parallelism
    
    def test_configuration_validation(self):
        """Test that default configuration passes validation."""
        config = DefaultConfigurationProvider.create_complete_default_configuration()
        validator = ConfigurationValidator()
        
        # Convert to dict for validation
        config_dict = {
            "version": config.version,
            "global_settings": config.global_settings,
            "performance": config.performance,
            "monitoring": config.monitoring,
            "agents": {
                name: {
                    "enabled": agent.enabled,
                    "type": agent.type.value,
                    "performance": {
                        "response_timeout": agent.performance.response_timeout,
                        "max_context_tokens": agent.performance.max_context_tokens,
                        "parallel_execution_limit": agent.performance.parallel_execution_limit,
                        "cache_enabled": agent.performance.cache_enabled
                    },
                    "coordination": {
                        "auto_delegation": agent.coordination.auto_delegation,
                        "natural_language_triggers": agent.coordination.natural_language_triggers,
                        "sequential_intelligence": agent.coordination.sequential_intelligence,
                        "context_preservation_rate": agent.coordination.context_preservation_rate,
                        "escalation_threshold": agent.coordination.escalation_threshold
                    }
                }
                for name, agent in config.agents.items()
            }
        }
        
        issues = validator.validate_configuration(config_dict)
        
        # Should have no critical or error issues
        critical_errors = [i for i in issues if i.severity.value in ["critical", "error"]]
        assert len(critical_errors) == 0, f"Default configuration has errors: {critical_errors}"
    
    def test_environment_specific_defaults(self):
        """Test environment-specific default overrides."""
        env_defaults = DefaultConfigurationProvider.get_environment_specific_defaults()
        
        # Development environment
        dev_config = env_defaults["development"]
        assert dev_config["global_settings"]["hot_reload"] is True
        assert dev_config["monitoring"]["coordination_logging"] is True
        
        # Production environment
        prod_config = env_defaults["production"]
        assert prod_config["global_settings"]["hot_reload"] is False
        assert prod_config["monitoring"]["coordination_logging"] is False
        
        # Testing environment
        test_config = env_defaults["testing"]
        assert test_config["global_settings"]["parallel_execution"] is False
        assert test_config["monitoring"]["usage_analytics"] is False


class TestConfigurationProfiles:
    """Test configuration profiles effectiveness."""
    
    def test_all_profiles_creation(self):
        """Test that all profiles can be created without errors."""
        for profile in ConfigurationProfile:
            config = ConfigurationProfileManager.get_profile(profile)
            assert isinstance(config, AgentConfigurationSchema)
            assert len(config.agents) > 0
    
    def test_development_profile(self):
        """Test development profile characteristics."""
        config = ConfigurationProfileManager.get_profile(ConfigurationProfile.DEVELOPMENT)
        
        # Development should have enhanced debugging
        assert config.global_settings["hot_reload"] is True
        assert config.monitoring["coordination_logging"] is True
        
        # Longer timeouts for debugging
        avg_timeout = sum(agent.performance.response_timeout for agent in config.agents.values()) / len(config.agents)
        assert avg_timeout > 30.0  # Should be higher than base defaults
    
    def test_production_profile(self):
        """Test production profile characteristics."""
        config = ConfigurationProfileManager.get_profile(ConfigurationProfile.PRODUCTION)
        
        # Production should prioritize stability
        assert config.global_settings["hot_reload"] is False
        assert config.monitoring["coordination_logging"] is False
        
        # Optimizations enabled
        assert config.performance["token_optimization"] is True
        assert config.performance["prompt_caching"] is True
        
        # Faster response times
        avg_timeout = sum(agent.performance.response_timeout for agent in config.agents.values()) / len(config.agents)
        # Should be slightly lower than development
        dev_config = ConfigurationProfileManager.get_profile(ConfigurationProfile.DEVELOPMENT)
        dev_avg_timeout = sum(agent.performance.response_timeout for agent in dev_config.agents.values()) / len(dev_config.agents)
        assert avg_timeout < dev_avg_timeout
    
    def test_performance_profile(self):
        """Test high-performance profile characteristics."""
        config = ConfigurationProfileManager.get_profile(ConfigurationProfile.PERFORMANCE)
        
        # Aggressive performance settings
        assert config.performance["token_optimization"] is True
        assert config.monitoring["usage_analytics"] is False  # Reduced overhead
        
        # Higher parallelism
        avg_parallel_limit = sum(agent.performance.parallel_execution_limit for agent in config.agents.values()) / len(config.agents)
        
        # Compare with base configuration
        base_config = DefaultConfigurationProvider.create_complete_default_configuration()
        base_avg_parallel = sum(agent.performance.parallel_execution_limit for agent in base_config.agents.values()) / len(base_config.agents)
        
        assert avg_parallel_limit > base_avg_parallel
    
    def test_security_focused_profile(self):
        """Test security-focused profile characteristics."""
        config = ConfigurationProfileManager.get_profile(ConfigurationProfile.SECURITY_FOCUSED)
        
        # Security-oriented settings
        assert config.global_settings["parallel_execution"] is False  # Sequential for security
        assert config.monitoring["coordination_logging"] is True  # Audit logging
        
        # Security agents should be prioritized
        security_agents = ["security-enforcer", "code-quality-specialist", "security-auditor"]
        for agent_name in security_agents:
            if agent_name in config.agents:
                agent = config.agents[agent_name]
                assert agent.enabled is True
                # Should have enhanced resources
                assert agent.coordination.escalation_threshold <= 1
    
    def test_testing_profile(self):
        """Test testing profile characteristics."""
        config = ConfigurationProfileManager.get_profile(ConfigurationProfile.TESTING)
        
        # Predictable behavior
        assert config.global_settings["natural_delegation"] is False
        assert config.global_settings["parallel_execution"] is False
        assert config.performance["prompt_caching"] is False
        
        # All agents should have consistent settings
        timeouts = [agent.performance.response_timeout for agent in config.agents.values()]
        assert len(set(timeouts)) == 1  # All timeouts should be the same
        
        parallel_limits = [agent.performance.parallel_execution_limit for agent in config.agents.values()]
        assert all(limit == 1 for limit in parallel_limits)  # All sequential
    
    def test_minimal_profile(self):
        """Test minimal profile characteristics."""
        config = ConfigurationProfileManager.get_profile(ConfigurationProfile.MINIMAL)
        
        # Only essential agents enabled
        enabled_agents = [name for name, agent in config.agents.items() if agent.enabled]
        assert len(enabled_agents) < len(config.agents) / 2  # Less than half enabled
        
        # Essential agents should be included
        essential_agents = ["analysis-gateway", "digdeep", "test-specialist"]
        for agent_name in essential_agents:
            assert config.agents[agent_name].enabled is True
        
        # Minimal resource usage
        assert config.performance["prompt_caching"] is False
        assert config.monitoring["performance_tracking"] is False
    
    def test_ci_cd_profile(self):
        """Test CI/CD profile characteristics."""
        config = ConfigurationProfileManager.get_profile(ConfigurationProfile.CI_CD)
        
        # CI/CD optimizations
        assert config.performance["response_streaming"] is False  # Simpler logs
        assert config.monitoring["performance_tracking"] is False  # Reduced overhead
        
        # CI/CD relevant agents should be enabled
        ci_agents = ["ci-specialist", "test-specialist", "docker-specialist"]
        for agent_name in ci_agents:
            if agent_name in config.agents:
                assert config.agents[agent_name].enabled is True
    
    def test_profile_validation(self):
        """Test that all profiles pass validation."""
        validator = ConfigurationValidator()
        
        for profile in ConfigurationProfile:
            config = ConfigurationProfileManager.get_profile(profile)
            
            # Convert to validation format
            config_dict = {
                "version": config.version,
                "global_settings": config.global_settings,
                "performance": config.performance,
                "monitoring": config.monitoring,
                "agents": {
                    name: {
                        "enabled": agent.enabled,
                        "type": agent.type.value
                    }
                    for name, agent in config.agents.items()
                }
            }
            
            issues = validator.validate_configuration(config_dict)
            critical_errors = [i for i in issues if i.severity.value in ["critical", "error"]]
            
            assert len(critical_errors) == 0, f"Profile {profile.value} has errors: {critical_errors}"
    
    def test_custom_profile_creation(self):
        """Test custom profile creation based on existing profiles."""
        customizations = {
            "global_settings": {
                "hot_reload": True
            },
            "agents": {
                "test-specialist": {
                    "performance": {
                        "response_timeout": 60.0
                    }
                }
            }
        }
        
        custom_config = ConfigurationProfileManager.create_custom_profile(
            ConfigurationProfile.PRODUCTION,
            customizations
        )
        
        # Base production settings should be preserved
        assert custom_config.performance["token_optimization"] is True
        
        # Customizations should be applied
        assert custom_config.global_settings["hot_reload"] is True
        assert custom_config.agents["test-specialist"].performance.response_timeout == 60.0
    
    def test_profile_export_to_settings_json(self):
        """Test exporting profiles to Claude Code settings.json format."""
        profile_config = ConfigurationProfileManager.get_profile(ConfigurationProfile.DEVELOPMENT)
        settings_json = ConfigurationProfileManager.export_profile_as_settings_json(ConfigurationProfile.DEVELOPMENT)
        
        # Should have proper structure
        assert "agents" in settings_json
        assert "version" in settings_json["agents"]
        assert "global_settings" in settings_json["agents"]
        assert "performance" in settings_json["agents"]
        assert "monitoring" in settings_json["agents"]
        assert "agents" in settings_json["agents"]
        
        # Agent configurations should be properly formatted
        for agent_name, agent_config in settings_json["agents"]["agents"].items():
            assert "enabled" in agent_config
            assert "type" in agent_config
            assert "performance" in agent_config
            assert "coordination" in agent_config
    
    def test_profile_list_availability(self):
        """Test profile list functionality."""
        profiles = ConfigurationProfileManager.list_available_profiles()
        
        assert len(profiles) == len(ConfigurationProfile)
        
        for profile_info in profiles:
            assert "name" in profile_info
            assert "title" in profile_info
            assert "description" in profile_info
            
            # Verify profile actually exists
            profile = ConfigurationProfile(profile_info["name"])
            config = ConfigurationProfileManager.get_profile(profile)
            assert isinstance(config, AgentConfigurationSchema)


class TestConfigurationEffectiveness:
    """Test overall configuration effectiveness."""
    
    def test_performance_characteristics(self):
        """Test that different profiles have expected performance characteristics."""
        profiles = [
            ConfigurationProfile.DEVELOPMENT,
            ConfigurationProfile.PRODUCTION,
            ConfigurationProfile.PERFORMANCE,
            ConfigurationProfile.TESTING
        ]
        
        configs = {profile: ConfigurationProfileManager.get_profile(profile) for profile in profiles}
        
        # Performance profile should have highest parallelism
        performance_parallel = sum(
            agent.performance.parallel_execution_limit 
            for agent in configs[ConfigurationProfile.PERFORMANCE].agents.values()
        )
        
        for profile in [ConfigurationProfile.DEVELOPMENT, ConfigurationProfile.PRODUCTION]:
            profile_parallel = sum(
                agent.performance.parallel_execution_limit
                for agent in configs[profile].agents.values()
            )
            assert performance_parallel >= profile_parallel
        
        # Testing should have lowest parallelism (all agents with limit 1)
        testing_parallel = sum(
            agent.performance.parallel_execution_limit
            for agent in configs[ConfigurationProfile.TESTING].agents.values()
        )
        assert testing_parallel == len(configs[ConfigurationProfile.TESTING].agents)  # All should be 1
    
    def test_resource_usage_differences(self):
        """Test that profiles have appropriate resource usage patterns."""
        minimal_config = ConfigurationProfileManager.get_profile(ConfigurationProfile.MINIMAL)
        experimental_config = ConfigurationProfileManager.get_profile(ConfigurationProfile.EXPERIMENTAL)
        
        # Minimal should have fewer enabled agents
        minimal_enabled = sum(1 for agent in minimal_config.agents.values() if agent.enabled)
        experimental_enabled = sum(1 for agent in experimental_config.agents.values() if agent.enabled)
        
        assert minimal_enabled < experimental_enabled
        
        # Experimental should have higher context limits
        experimental_avg_context = sum(
            agent.performance.max_context_tokens 
            for agent in experimental_config.agents.values()
        ) / len(experimental_config.agents)
        
        minimal_avg_context = sum(
            agent.performance.max_context_tokens 
            for agent in minimal_config.agents.values() if agent.enabled
        ) / minimal_enabled
        
        assert experimental_avg_context > minimal_avg_context