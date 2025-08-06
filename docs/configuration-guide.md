# Claude Code Agent Framework Configuration Guide

This guide covers the complete configuration system for the Claude Code Agent Framework, including default configurations, profiles, and customization options.

## Overview

The Claude Code Agent Framework uses a hierarchical configuration system that integrates seamlessly with Claude Code's native settings system. Configuration can be managed through:

- **Settings Files**: `.claude/settings.json` (hierarchical)
- **Environment Variables**: `CLAUDE_AGENT_*` prefixed variables
- **Configuration Profiles**: Pre-built configurations for common use cases
- **Dynamic Adjustments**: Automatic optimization based on usage patterns

## Configuration Hierarchy

Settings are applied in the following precedence order (highest to lowest):

1. **Environment Variables** - Runtime overrides
2. **Local Settings** - `.claude/settings.local.json` (git-ignored)
3. **Project Settings** - `.claude/settings.json` (committed)
4. **User Settings** - `~/.claude/settings.json` (personal)
5. **Profile Defaults** - Selected configuration profile
6. **System Defaults** - Built-in sensible defaults

## Quick Start

### 1. Using Configuration Profiles

The easiest way to configure the framework is using pre-built profiles:

```python
from src.configuration import ConfigurationProfileManager, ConfigurationProfile

# Get development configuration
config = ConfigurationProfileManager.get_profile(ConfigurationProfile.DEVELOPMENT)

# Export to Claude Code settings format
settings = ConfigurationProfileManager.export_profile_as_settings_json(
    ConfigurationProfile.PRODUCTION
)

# Save to project settings
import json
with open('.claude/settings.json', 'w') as f:
    json.dump(settings, f, indent=2)
```

### 2. Environment Variable Configuration

Set environment variables for quick configuration changes:

```bash
# Enable framework with enhanced debugging
export CLAUDE_AGENT_FRAMEWORK_ENABLED=true
export CLAUDE_AGENT_MONITORING_COORDINATION_LOGGING=true
export CLAUDE_AGENT_HOT_RELOAD=true

# Disable a specific agent
export CLAUDE_AGENT__PERFORMANCE_OPTIMIZER_ENABLED=false

# Adjust timeout for slow agent
export CLAUDE_AGENT__TEST_SPECIALIST_PERFORMANCE_RESPONSE_TIMEOUT=45.0
```

### 3. Settings File Configuration

Add agent configuration to your `.claude/settings.json`:

```json
{
  "agents": {
    "version": "1.0",
    "global_settings": {
      "framework_enabled": true,
      "natural_delegation": true,
      "parallel_execution": true,
      "hot_reload": true
    },
    "performance": {
      "token_optimization": true,
      "prompt_caching": true,
      "response_streaming": true,
      "resource_monitoring": true
    },
    "agents": {
      "test-specialist": {
        "enabled": true,
        "performance": {
          "response_timeout": 30.0,
          "max_context_tokens": 10000
        }
      }
    }
  }
}
```

## Available Profiles

### Development Profile
**Use Case**: Local development with debugging capabilities

**Characteristics**:
- Hot reload enabled
- Verbose coordination logging
- Extended timeouts for debugging
- All optimizations enabled for testing

**When to Use**: 
- Local development environment
- Debugging agent coordination issues
- Testing new agent configurations

```bash
# Apply development profile via environment
export CLAUDE_AGENT_PROFILE=development
```

### Production Profile  
**Use Case**: Stable production deployment

**Characteristics**:
- Hot reload disabled for stability
- Optimized performance settings
- Reduced logging to minimize overhead
- Faster response timeouts

**When to Use**:
- Production deployments
- Live user-facing applications
- Performance-critical environments

### Performance Profile
**Use Case**: Maximum performance optimization

**Characteristics**:
- Aggressive parallelism settings
- Minimal logging overhead
- Optimized cache usage
- Fastest possible response times

**When to Use**:
- High-throughput scenarios
- Performance benchmarking
- Resource-abundant environments

### Security-Focused Profile
**Use Case**: Enhanced security monitoring

**Characteristics**:
- Sequential execution for security validation
- Priority for security-related agents
- Enhanced audit logging
- Stricter escalation thresholds

**When to Use**:
- Security-sensitive applications
- Compliance requirements
- Code review workflows

### Testing Profile
**Use Case**: Predictable test environments

**Characteristics**:
- Disabled caching for consistency
- Sequential execution for predictability
- Fixed timeouts across all agents
- Minimal randomness in behavior

**When to Use**:
- Automated testing
- CI/CD pipelines
- Integration tests

### Minimal Profile
**Use Case**: Resource-constrained environments

**Characteristics**:
- Only essential agents enabled
- Reduced memory usage
- Lower context token limits
- Minimal monitoring overhead

**When to Use**:
- Resource-limited environments
- Edge computing scenarios
- Cost-sensitive deployments

### CI/CD Profile
**Use Case**: Continuous integration pipelines

**Characteristics**:
- CI/CD relevant agents prioritized
- Reduced monitoring overhead
- Optimized for build processes
- Simple log output format

**When to Use**:
- GitHub Actions workflows
- Build and deployment pipelines
- Automated quality checks

### Experimental Profile
**Use Case**: Testing new features and capabilities

**Characteristics**:
- Enhanced parallelism
- Higher resource limits
- Experimental features enabled
- Comprehensive monitoring

**When to Use**:
- Testing new agent capabilities
- Research and development
- Feature experimentation

## Configuration Sections

### Global Settings

Controls framework-wide behavior:

```json
{
  "global_settings": {
    "framework_enabled": true,        // Enable/disable entire framework
    "natural_delegation": true,       // Allow natural language agent delegation
    "parallel_execution": true,       // Enable parallel agent execution
    "hot_reload": true               // Enable configuration hot-reload
  }
}
```

### Performance Settings

System-wide performance optimizations:

```json
{
  "performance": {
    "token_optimization": true,       // Optimize token usage
    "prompt_caching": true,          // Enable prompt caching
    "response_streaming": true,      // Stream responses
    "resource_monitoring": true      // Monitor resource usage
  }
}
```

### Monitoring Settings

Observability and logging configuration:

```json
{
  "monitoring": {
    "performance_tracking": true,     // Track performance metrics
    "coordination_logging": false,   // Log coordination details (verbose)
    "usage_analytics": true,         // Collect usage analytics
    "error_reporting": true          // Enable error reporting
  }
}
```

### Agent Configuration

Individual agent settings:

```json
{
  "agents": {
    "agent-name": {
      "enabled": true,
      "type": "primary",              // primary, secondary, meta
      "performance": {
        "response_timeout": 30.0,     // Timeout in seconds
        "max_context_tokens": 8000,   // Maximum context size
        "parallel_execution_limit": 3, // Max parallel tasks
        "cache_enabled": true         // Enable caching for this agent
      },
      "coordination": {
        "auto_delegation": true,      // Can delegate to other agents
        "natural_language_triggers": true,  // Respond to natural language
        "sequential_intelligence": true,    // Use sequential coordination
        "context_preservation_rate": 0.95,  // Context retention rate (0-1)
        "escalation_threshold": 3     // Failures before escalation
      }
    }
  }
}
```

## Agent Types and Defaults

### Primary Agents (20 total)

High-level coordination and analysis agents with enhanced resources:

- **Default Timeout**: 30 seconds
- **Default Context**: 10,000 tokens
- **Default Parallelism**: 5 tasks
- **Auto-delegation**: Enabled

**Examples**: `digdeep`, `test-specialist`, `code-quality-specialist`, `infrastructure-engineer`

### Secondary Agents (14 total)

Specialized task agents with focused capabilities:

- **Default Timeout**: 20 seconds
- **Default Context**: 6,000 tokens  
- **Default Parallelism**: 2 tasks
- **Auto-delegation**: Disabled

**Examples**: `async-pattern-fixer`, `docker-specialist`, `security-auditor`

### Meta Agents (1 total)

Strategic coordination agents with maximum resources:

- **Default Timeout**: 60 seconds
- **Default Context**: 15,000 tokens
- **Default Parallelism**: 8 tasks
- **Enhanced Features**: All enabled

**Examples**: `meta-coordinator`

## Advanced Configuration

### Dynamic Adaptation

The framework automatically adjusts configuration based on usage patterns:

```json
{
  "adaptive_configuration": {
    "enabled": true,
    "learning_rate": 0.1,
    "adaptation_interval": 300,      // 5 minutes
    "rules": [
      {
        "condition": "high_failure_rate",
        "adjustment": "reduce_parallel_limit"
      }
    ]
  }
}
```

### Custom Profiles

Create custom profiles based on existing ones:

```python
from src.configuration import ConfigurationProfileManager, ConfigurationProfile

# Create custom profile
custom_config = ConfigurationProfileManager.create_custom_profile(
    base_profile=ConfigurationProfile.PRODUCTION,
    customizations={
        "global_settings": {
            "hot_reload": True  # Enable hot reload in production variant
        },
        "agents": {
            "test-specialist": {
                "performance": {
                    "response_timeout": 45.0
                }
            }
        }
    }
)
```

### Environment-Specific Overrides

Configure different settings per environment:

```json
{
  "environment_overrides": {
    "development": {
      "monitoring": {
        "coordination_logging": true
      }
    },
    "staging": {
      "performance": {
        "token_optimization": false
      }
    },
    "production": {
      "global_settings": {
        "hot_reload": false
      }
    }
  }
}
```

## Configuration Validation

The framework validates configuration automatically:

```python
from src.configuration import ConfigurationValidator

validator = ConfigurationValidator()
issues = validator.validate_configuration(config_dict)

for issue in issues:
    print(f"{issue.severity.value}: {issue.message} at {issue.path}")
```

### Common Validation Issues

1. **Invalid timeout values**: Must be positive numbers
2. **Token limits out of range**: Should be between 1,000-50,000
3. **Unknown agent names**: Check spelling and agent availability
4. **Conflicting settings**: Framework disabled but agents enabled

## Monitoring and Observability

### Configuration Health

Monitor configuration effectiveness:

```python
from src.configuration import ConfigurationMonitor

monitor = ConfigurationMonitor()
health_summary = monitor.get_health_summary()

print(f"Overall status: {health_summary['overall_status']}")
for metric_name, metric_data in health_summary['latest_metrics'].items():
    print(f"{metric_name}: {metric_data['value']} ({metric_data['status']})")
```

### Performance Metrics

Track key performance indicators:

- **Average Response Time**: Agent response latency
- **Success Rate**: Percentage of successful agent executions
- **Token Usage**: Context token consumption patterns  
- **Parallel Utilization**: Efficiency of parallel execution
- **Cache Hit Rate**: Effectiveness of caching

### Adaptive Adjustments

View automatic configuration adjustments:

```python
from src.configuration import AdaptiveConfigurationManager

adaptive_manager = AdaptiveConfigurationManager()
adjustments = adaptive_manager.get_adjustments_history()

for adjustment in adjustments[-5:]:  # Last 5 adjustments
    print(f"Rule: {adjustment['rule_name']}")
    print(f"Affected agents: {adjustment['affected_agents']}")
    print(f"Adjustments: {adjustment['adjustments']}")
```

## Troubleshooting

### Common Issues

1. **Agents not responding**
   - Check `framework_enabled` setting
   - Verify agent is enabled individually
   - Check timeout settings aren't too low

2. **Performance issues**
   - Enable `token_optimization` 
   - Reduce `coordination_logging`
   - Adjust `parallel_execution_limit`

3. **Configuration not taking effect**
   - Check configuration hierarchy precedence
   - Verify hot reload is enabled
   - Check for validation errors

4. **High resource usage**
   - Use `minimal` profile
   - Disable `resource_monitoring`
   - Reduce `max_context_tokens`

### Debug Mode

Enable comprehensive debugging:

```bash
export CLAUDE_AGENT_MONITORING_COORDINATION_LOGGING=true
export CLAUDE_AGENT_MONITORING_PERFORMANCE_TRACKING=true
export CLAUDE_AGENT_HOT_RELOAD=true
```

### Configuration Recovery

The framework automatically recovers from configuration errors:

- **Invalid values**: Replaced with sensible defaults
- **Missing settings**: Auto-populated with defaults
- **Critical errors**: Configuration restored from backup

## Best Practices

### Development
- Use `development` profile for local work
- Enable coordination logging for debugging
- Use longer timeouts when debugging

### Testing  
- Use `testing` profile for consistent behavior
- Disable caching and randomness
- Use sequential execution for predictability

### Production
- Use `production` profile as starting point
- Disable hot reload for stability
- Monitor performance metrics
- Use environment variables for deployment-specific overrides

### Performance Optimization
- Start with `performance` profile
- Monitor token usage and adjust limits
- Use adaptive configuration for automatic tuning
- Profile different agent combinations

### Security
- Use `security_focused` profile for sensitive code
- Enable audit logging
- Use sequential execution for security validation
- Regularly review agent permissions

## Integration Examples

### GitHub Actions

```yaml
# .github/workflows/test.yml
env:
  CLAUDE_AGENT_PROFILE: ci_cd
  CLAUDE_AGENT_MONITORING_PERFORMANCE_TRACKING: false
  CLAUDE_AGENT__CI_SPECIALIST_ENABLED: true
```

### Docker Compose

```yaml
# docker-compose.yml
services:
  app:
    environment:
      - CLAUDE_AGENT_PROFILE=production
      - CLAUDE_AGENT_HOT_RELOAD=false
      - CLAUDE_AGENT_PERFORMANCE_TOKEN_OPTIMIZATION=true
```

### Development Script

```bash
#!/bin/bash
# dev-setup.sh

export CLAUDE_AGENT_PROFILE=development
export CLAUDE_AGENT_MONITORING_COORDINATION_LOGGING=true
export CLAUDE_AGENT_HOT_RELOAD=true

echo "Development environment configured"
```

For complete environment variable documentation, see [Environment Variables Guide](./configuration-environment-variables.md).

For advanced usage patterns and API documentation, see the source code in `src/configuration/`.