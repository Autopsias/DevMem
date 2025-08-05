"""Default configurations for Claude Code agent ecosystem."""

from typing import Dict, Any

from .schema import (
    AgentConfigurationSchema, 
    AgentConfig, 
    AgentType,
    AgentPerformanceConfig,
    AgentCoordinationConfig,
    PerformanceLevel
)

class DefaultConfigurationProvider:
    """Provides sensible default configurations for all agent types."""
    
    @staticmethod
    def get_default_global_settings() -> Dict[str, Any]:
        """Get default global framework settings."""
        return {
            "framework_enabled": True,
            "natural_delegation": True,
            "parallel_execution": True,
            "hot_reload": True
        }
    
    @staticmethod
    def get_default_performance_settings() -> Dict[str, Any]:
        """Get default performance settings."""
        return {
            "token_optimization": True,
            "prompt_caching": True,
            "response_streaming": True,
            "resource_monitoring": True
        }
    
    @staticmethod
    def get_default_monitoring_settings() -> Dict[str, Any]:
        """Get default monitoring settings."""
        return {
            "performance_tracking": True,
            "coordination_logging": False,  # Disabled by default to reduce verbosity
            "usage_analytics": True,
            "error_reporting": True
        }
    
    @staticmethod
    def get_primary_agent_defaults() -> AgentConfig:
        """Get default configuration for primary agents."""
        return AgentConfig(
            name="",  # Will be set per agent
            type=AgentType.PRIMARY,
            enabled=True,
            performance=AgentPerformanceConfig(
                response_timeout=30.0,
                max_context_tokens=10000,
                parallel_execution_limit=5,
                cache_enabled=True,
                optimization_level=PerformanceLevel.BALANCED
            ),
            coordination=AgentCoordinationConfig(
                auto_delegation=True,
                natural_language_triggers=True,
                sequential_intelligence=True,
                context_preservation_rate=0.95,
                escalation_threshold=3
            )
        )
    
    @staticmethod
    def get_secondary_agent_defaults() -> AgentConfig:
        """Get default configuration for secondary agents."""
        return AgentConfig(
            name="",  # Will be set per agent
            type=AgentType.SECONDARY,
            enabled=True,
            performance=AgentPerformanceConfig(
                response_timeout=20.0,
                max_context_tokens=6000,
                parallel_execution_limit=2,
                cache_enabled=True,
                optimization_level=PerformanceLevel.BALANCED
            ),
            coordination=AgentCoordinationConfig(
                auto_delegation=False,  # Secondary agents don't initiate delegation
                natural_language_triggers=True,
                sequential_intelligence=False,  # Simpler coordination
                context_preservation_rate=0.90,
                escalation_threshold=2
            )
        )
    
    @staticmethod
    def get_meta_agent_defaults() -> AgentConfig:
        """Get default configuration for meta agents (like meta-coordinator)."""
        return AgentConfig(
            name="",
            type=AgentType.META,
            enabled=True,
            performance=AgentPerformanceConfig(
                response_timeout=60.0,  # Longer timeout for complex coordination
                max_context_tokens=15000,  # Higher context for comprehensive analysis
                parallel_execution_limit=8,  # Can handle more parallel tasks
                cache_enabled=True,
                optimization_level=PerformanceLevel.AGGRESSIVE
            ),
            coordination=AgentCoordinationConfig(
                auto_delegation=True,
                natural_language_triggers=True,
                sequential_intelligence=True,
                context_preservation_rate=0.98,  # Higher context preservation
                escalation_threshold=5  # Higher threshold before escalation
            )
        )
    
    @staticmethod
    def get_agent_specific_overrides() -> Dict[str, Dict[str, Any]]:
        """Get agent-specific configuration overrides."""
        return {
            # High-performance agents
            "digdeep": {
                "performance": {
                    "response_timeout": 45.0,  # Complex analysis takes longer
                    "max_context_tokens": 12000,
                    "parallel_execution_limit": 3  # Deep analysis shouldn't be too parallel
                }
            },
            
            "meta-coordinator": {
                "performance": {
                    "response_timeout": 60.0,
                    "max_context_tokens": 15000,
                    "parallel_execution_limit": 8
                },
                "coordination": {
                    "escalation_threshold": 5
                }
            },
            
            # Testing and quality agents (need more resources)
            "test-specialist": {
                "performance": {
                    "response_timeout": 40.0,
                    "max_context_tokens": 11000
                }
            },
            
            "code-quality-specialist": {
                "performance": {
                    "response_timeout": 35.0,
                    "max_context_tokens": 9000
                }
            },
            
            # Infrastructure agents (can be resource-intensive)
            "infrastructure-engineer": {
                "performance": {
                    "response_timeout": 50.0,
                    "max_context_tokens": 12000
                }
            },
            
            "docker-specialist": {
                "performance": {
                    "response_timeout": 35.0,
                    "max_context_tokens": 8000
                }
            },
            
            # Fast response agents
            "lint-enforcer": {
                "performance": {
                    "response_timeout": 15.0,
                    "max_context_tokens": 4000,
                    "parallel_execution_limit": 1,  # Linting should be sequential
                    "optimization_level": "aggressive"
                }
            },
            
            "security-enforcer": {
                "performance": {
                    "response_timeout": 20.0,
                    "max_context_tokens": 6000,
                    "optimization_level": "aggressive"  # Security checks should be fast
                }
            },
            
            # Resource monitoring agents
            "token-monitor": {
                "performance": {
                    "response_timeout": 10.0,
                    "max_context_tokens": 3000,
                    "parallel_execution_limit": 1,
                    "optimization_level": "minimal"  # Monitoring should be lightweight
                }
            },
            
            "health-monitor": {
                "performance": {
                    "response_timeout": 15.0,
                    "max_context_tokens": 4000,
                    "parallel_execution_limit": 1,
                    "optimization_level": "minimal"
                }
            },
            
            # Coordination and communication agents
            "synthesis-coordinator": {
                "performance": {
                    "response_timeout": 45.0,
                    "max_context_tokens": 13000,  # Needs to synthesize multiple agent outputs
                    "parallel_execution_limit": 1  # Synthesis is inherently sequential
                },
                "coordination": {
                    "context_preservation_rate": 0.98
                }
            },
            
            "user-feedback-coordinator": {
                "performance": {
                    "response_timeout": 25.0,
                    "max_context_tokens": 7000,
                    "optimization_level": "balanced"
                }
            },
            
            # Development and enhancement agents
            "intelligent-enhancer": {
                "performance": {
                    "response_timeout": 40.0,
                    "max_context_tokens": 10000
                }
            },
            
            "refactoring-coordinator": {
                "performance": {
                    "response_timeout": 50.0,
                    "max_context_tokens": 12000
                }
            },
            
            # Analysis and validation agents
            "pattern-analyzer": {
                "performance": {
                    "response_timeout": 30.0,
                    "max_context_tokens": 9000
                }
            },
            
            "architecture-validator": {
                "performance": {
                    "response_timeout": 35.0,
                    "max_context_tokens": 10000
                }
            },
            
            # Environment and system agents
            "environment-analyst": {
                "performance": {
                    "response_timeout": 30.0,
                    "max_context_tokens": 8000
                }
            },
            
            "environment-synchronizer": {
                "performance": {
                    "response_timeout": 40.0,
                    "max_context_tokens": 9000
                }
            },
            
            # Git and version control
            "git-commit-assistant": {
                "performance": {
                    "response_timeout": 20.0,
                    "max_context_tokens": 5000,
                    "parallel_execution_limit": 1  # Git operations should be sequential
                }
            },
            
            # CI/CD agents
            "ci-specialist": {
                "performance": {
                    "response_timeout": 45.0,
                    "max_context_tokens": 11000
                }
            },
            
            # Agent management
            "agent-reviewer": {
                "performance": {
                    "response_timeout": 30.0,
                    "max_context_tokens": 8000
                }
            },
            
            "agent-creator": {
                "performance": {
                    "response_timeout": 35.0,
                    "max_context_tokens": 9000
                }
            }
        }
    
    @classmethod
    def create_complete_default_configuration(cls) -> AgentConfigurationSchema:
        """Create complete default configuration with all agents."""
        config = AgentConfigurationSchema(
            version="1.0",
            global_settings=cls.get_default_global_settings(),
            performance=cls.get_default_performance_settings(),
            monitoring=cls.get_default_monitoring_settings(),
            agents={},
            environment_overrides={}
        )
        
        # Define all agents with their types
        agent_definitions = {
            # Primary agents (20)
            "digdeep": AgentType.PRIMARY,
            "test-specialist": AgentType.PRIMARY,
            "code-quality-specialist": AgentType.PRIMARY,
            "infrastructure-engineer": AgentType.PRIMARY,
            "ci-specialist": AgentType.PRIMARY,
            "environment-analyst": AgentType.PRIMARY,
            "intelligent-enhancer": AgentType.PRIMARY,
            "meta-coordinator": AgentType.META,  # Special case
            "framework-coordinator": AgentType.PRIMARY,
            "git-commit-assistant": AgentType.PRIMARY,
            "agent-reviewer": AgentType.PRIMARY,
            "agent-creator": AgentType.PRIMARY,
            "lint-enforcer": AgentType.PRIMARY,
            "security-enforcer": AgentType.PRIMARY,
            "token-monitor": AgentType.PRIMARY,
            "user-feedback-coordinator": AgentType.PRIMARY,
            "architecture-validator": AgentType.PRIMARY,
            "health-monitor": AgentType.PRIMARY,
            "synthesis-coordinator": AgentType.PRIMARY,
            "analysis-gateway": AgentType.PRIMARY,
            
            # Secondary agents (14)
            "async-pattern-fixer": AgentType.SECONDARY,
            "type-system-expert": AgentType.SECONDARY,
            "mock-configuration-expert": AgentType.SECONDARY,
            "validation-tester": AgentType.SECONDARY,
            "linting-engineer": AgentType.SECONDARY,
            "docker-specialist": AgentType.SECONDARY,
            "performance-optimizer": AgentType.SECONDARY,
            "resource-optimizer": AgentType.SECONDARY,
            "environment-synchronizer": AgentType.SECONDARY,
            "security-auditor": AgentType.SECONDARY,
            "pattern-analyzer": AgentType.SECONDARY,
            "refactoring-coordinator": AgentType.SECONDARY,
            "dependency-resolver": AgentType.SECONDARY,
            "coverage-optimizer": AgentType.SECONDARY
        }
        
        # Create agent configurations
        for agent_name, agent_type in agent_definitions.items():
            if agent_type == AgentType.PRIMARY:
                base_config = cls.get_primary_agent_defaults()
            elif agent_type == AgentType.META:
                base_config = cls.get_meta_agent_defaults()
            else:
                base_config = cls.get_secondary_agent_defaults()
            
            base_config.name = agent_name
            base_config.type = agent_type
            
            config.agents[agent_name] = base_config
        
        # Apply agent-specific overrides
        overrides = cls.get_agent_specific_overrides()
        for agent_name, agent_overrides in overrides.items():
            if agent_name in config.agents:
                agent_config = config.agents[agent_name]
                
                # Apply performance overrides
                if "performance" in agent_overrides:
                    perf_overrides = agent_overrides["performance"]
                    for key, value in perf_overrides.items():
                        if key == "optimization_level" and isinstance(value, str):
                            # Handle string enum values
                            try:
                                agent_config.performance.optimization_level = PerformanceLevel(value)
                            except ValueError:
                                pass  # Keep default
                        else:
                            setattr(agent_config.performance, key, value)
                
                # Apply coordination overrides
                if "coordination" in agent_overrides:
                    coord_overrides = agent_overrides["coordination"]
                    for key, value in coord_overrides.items():
                        setattr(agent_config.coordination, key, value)
        
        return config
    
    @staticmethod
    def get_environment_specific_defaults() -> Dict[str, Dict[str, Any]]:
        """Get environment-specific default overrides."""
        return {
            "development": {
                "global_settings": {
                    "hot_reload": True
                },
                "performance": {
                    "token_optimization": False,  # Less aggressive optimization for debugging
                    "prompt_caching": True
                },
                "monitoring": {
                    "coordination_logging": True,  # Enable verbose logging in dev
                    "performance_tracking": True
                }
            },
            
            "testing": {
                "global_settings": {
                    "parallel_execution": False  # Sequential execution for predictable tests
                },
                "performance": {
                    "response_streaming": False,  # Disable streaming for test stability
                    "resource_monitoring": False
                },
                "monitoring": {
                    "coordination_logging": False,
                    "usage_analytics": False
                }
            },
            
            "production": {
                "global_settings": {
                    "hot_reload": False  # Disabled in production for stability
                },
                "performance": {
                    "token_optimization": True,
                    "prompt_caching": True,
                    "response_streaming": True,
                    "resource_monitoring": True
                },
                "monitoring": {
                    "coordination_logging": False,  # Reduced logging in production
                    "performance_tracking": True,
                    "usage_analytics": True,
                    "error_reporting": True
                }
            },
            
            "ci": {
                "global_settings": {
                    "parallel_execution": True,
                    "hot_reload": False
                },
                "performance": {
                    "token_optimization": True,
                    "response_streaming": False,  # Simpler output for CI
                    "resource_monitoring": False
                },
                "monitoring": {
                    "coordination_logging": False,
                    "performance_tracking": False,  # Reduce overhead in CI
                    "usage_analytics": False,
                    "error_reporting": True
                }
            }
        }