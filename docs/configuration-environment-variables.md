# Environment Variable Configuration

This document describes how to configure the Claude Code Agent Framework using environment variables.

## Overview

The agent framework supports comprehensive configuration through environment variables, following Claude Code's hierarchical settings system. Environment variables have the highest precedence in the configuration hierarchy:

**Precedence Order:** Environment Variables > Local Settings > Project Settings > User Settings > Defaults

## Naming Convention

All agent framework environment variables use the prefix `CLAUDE_AGENT` followed by specific naming patterns:

- **Global Settings**: `CLAUDE_AGENT_<SETTING_NAME>`
- **Performance Settings**: `CLAUDE_AGENT_PERFORMANCE_<SETTING_NAME>`
- **Monitoring Settings**: `CLAUDE_AGENT_MONITORING_<SETTING_NAME>`
- **Agent-Specific**: `CLAUDE_AGENT__<AGENT_NAME>_<PROPERTY>`
- **Agent Performance**: `CLAUDE_AGENT__<AGENT_NAME>_PERFORMANCE_<PROPERTY>`
- **Agent Coordination**: `CLAUDE_AGENT__<AGENT_NAME>_COORDINATION_<PROPERTY>`

> **Note**: Agent names use double underscores (`__`) as separators and should be in UPPERCASE with underscores replacing hyphens.

## Global Framework Settings

### Framework Control
```bash
# Enable/disable the entire agent framework
CLAUDE_AGENT_FRAMEWORK_ENABLED=true

# Enable natural language delegation between agents
CLAUDE_AGENT_NATURAL_DELEGATION=true

# Enable parallel agent execution
CLAUDE_AGENT_PARALLEL_EXECUTION=true

# Enable hot reload of configuration changes
CLAUDE_AGENT_HOT_RELOAD=false
```

## Performance Settings

### System-wide Performance
```bash
# Enable token usage optimization
CLAUDE_AGENT_PERFORMANCE_TOKEN_OPTIMIZATION=true

# Enable prompt caching for better performance
CLAUDE_AGENT_PERFORMANCE_PROMPT_CACHING=true

# Enable response streaming
CLAUDE_AGENT_PERFORMANCE_RESPONSE_STREAMING=true

# Enable resource monitoring
CLAUDE_AGENT_PERFORMANCE_RESOURCE_MONITORING=false
```

## Monitoring Settings

### Analytics and Logging
```bash
# Enable performance tracking
CLAUDE_AGENT_MONITORING_PERFORMANCE_TRACKING=true

# Enable coordination logging (verbose)
CLAUDE_AGENT_MONITORING_COORDINATION_LOGGING=false

# Enable usage analytics
CLAUDE_AGENT_MONITORING_USAGE_ANALYTICS=true

# Enable error reporting
CLAUDE_AGENT_MONITORING_ERROR_REPORTING=true
```

## Agent-Specific Configuration

### Individual Agent Control
```bash
# Disable a specific agent
CLAUDE_AGENT__TEST_SPECIALIST_ENABLED=false

# Set agent type (primary, secondary, meta)
CLAUDE_AGENT__TEST_SPECIALIST_TYPE=primary
```

### Agent Performance Settings
```bash
# Set response timeout (seconds)
CLAUDE_AGENT__TEST_SPECIALIST_PERFORMANCE_RESPONSE_TIMEOUT=30.0

# Set maximum context tokens
CLAUDE_AGENT__TEST_SPECIALIST_PERFORMANCE_MAX_CONTEXT_TOKENS=8000

# Set parallel execution limit
CLAUDE_AGENT__TEST_SPECIALIST_PERFORMANCE_PARALLEL_EXECUTION_LIMIT=3

# Enable/disable caching for agent
CLAUDE_AGENT__TEST_SPECIALIST_PERFORMANCE_CACHE_ENABLED=true
```

### Agent Coordination Settings
```bash
# Enable auto-delegation
CLAUDE_AGENT__TEST_SPECIALIST_COORDINATION_AUTO_DELEGATION=true

# Enable natural language triggers
CLAUDE_AGENT__TEST_SPECIALIST_COORDINATION_NATURAL_LANGUAGE_TRIGGERS=true

# Enable sequential intelligence
CLAUDE_AGENT__TEST_SPECIALIST_COORDINATION_SEQUENTIAL_INTELLIGENCE=true

# Set context preservation rate (0.0 to 1.0)
CLAUDE_AGENT__TEST_SPECIALIST_COORDINATION_CONTEXT_PRESERVATION_RATE=0.95

# Set escalation threshold
CLAUDE_AGENT__TEST_SPECIALIST_COORDINATION_ESCALATION_THRESHOLD=3
```

## Supported Agents

### Primary Agents (20)
- `DIGDEEP` - Five Whys root cause analysis
- `TEST_SPECIALIST` - Testing expertise and failure analysis  
- `CODE_QUALITY_SPECIALIST` - Security scanning and quality analysis
- `INFRASTRUCTURE_ENGINEER` - Docker orchestration and infrastructure
- `CI_SPECIALIST` - GitHub Actions and CI/CD pipeline analysis
- `ENVIRONMENT_ANALYST` - System environment and dependency analysis
- `INTELLIGENT_ENHANCER` - AI-powered code improvements
- `META_COORDINATOR` - Complex multi-domain orchestration
- `FRAMEWORK_COORDINATOR` - Framework architecture analysis
- `GIT_COMMIT_ASSISTANT` - Git workflow automation
- `AGENT_REVIEWER` - Agent health monitoring
- `AGENT_CREATOR` - New agent generation
- `LINT_ENFORCER` - Code formatting and linting
- `SECURITY_ENFORCER` - Fast security pattern detection
- `TOKEN_MONITOR` - Token usage monitoring
- `USER_FEEDBACK_COORDINATOR` - Real-time feedback coordination
- `ARCHITECTURE_VALIDATOR` - Architectural compliance validation
- `HEALTH_MONITOR` - Architectural health monitoring
- `SYNTHESIS_COORDINATOR` - Multi-agent result integration
- `ANALYSIS_GATEWAY` - First-line technical problem analysis

### Secondary Agents (14)
- `ASYNC_PATTERN_FIXER` - Async/await pattern corrections
- `TYPE_SYSTEM_EXPERT` - Type annotation design
- `MOCK_CONFIGURATION_EXPERT` - Advanced mock setup
- `VALIDATION_TESTER` - Comprehensive validation workflow
- `LINTING_ENGINEER` - Systematic code compliance
- `DOCKER_SPECIALIST` - Container orchestration
- `PERFORMANCE_OPTIMIZER` - System-wide performance analysis
- `RESOURCE_OPTIMIZER` - Resource allocation optimization
- `ENVIRONMENT_SYNCHRONIZER` - Cross-environment coordination
- `SECURITY_AUDITOR` - Comprehensive security vulnerability analysis
- `PATTERN_ANALYZER` - Architectural pattern analysis
- `REFACTORING_COORDINATOR` - Large-scale architectural refactoring
- `DEPENDENCY_RESOLVER` - Complex dependency resolution
- `COVERAGE_OPTIMIZER` - Strategic coverage analysis

## Value Types

Environment variables are automatically parsed to appropriate types:

- **Boolean**: `true`, `false`, `yes`, `no`, `1`, `0`, `on`, `off`
- **Integer**: Numeric values without decimals
- **Float**: Numeric values with decimals
- **String**: All other values
- **JSON**: Values starting with `{` or `[` are parsed as JSON

### Examples
```bash
# Boolean values
CLAUDE_AGENT_FRAMEWORK_ENABLED=true
CLAUDE_AGENT_HOT_RELOAD=false
CLAUDE_AGENT_MONITORING_COORDINATION_LOGGING=yes

# Numeric values
CLAUDE_AGENT__DIGDEEP_PERFORMANCE_RESPONSE_TIMEOUT=45.5
CLAUDE_AGENT__META_COORDINATOR_PERFORMANCE_MAX_CONTEXT_TOKENS=15000

# String values
CLAUDE_AGENT__TEST_SPECIALIST_TYPE=primary
```

## Configuration Validation

The system validates environment variables and will log warnings for:
- Unknown environment variable names
- Invalid value types
- Conflicting settings (e.g., disabled framework but enabled agents)

## Usage Examples

### Development Environment
```bash
# Optimize for development speed
export CLAUDE_AGENT_PERFORMANCE_PROMPT_CACHING=true
export CLAUDE_AGENT_MONITORING_COORDINATION_LOGGING=true
export CLAUDE_AGENT_HOT_RELOAD=true
```

### Production Environment
```bash
# Optimize for production performance
export CLAUDE_AGENT_PERFORMANCE_TOKEN_OPTIMIZATION=true
export CLAUDE_AGENT_PERFORMANCE_RESPONSE_STREAMING=true
export CLAUDE_AGENT_MONITORING_PERFORMANCE_TRACKING=true
export CLAUDE_AGENT_HOT_RELOAD=false
```

### Debugging Specific Agent
```bash
# Enable verbose logging for test specialist
export CLAUDE_AGENT__TEST_SPECIALIST_COORDINATION_ESCALATION_THRESHOLD=1
export CLAUDE_AGENT__TEST_SPECIALIST_PERFORMANCE_RESPONSE_TIMEOUT=60.0
export CLAUDE_AGENT_MONITORING_COORDINATION_LOGGING=true
```

### Disable Heavy Agents
```bash
# Disable resource-intensive agents in constrained environments
export CLAUDE_AGENT__META_COORDINATOR_ENABLED=false
export CLAUDE_AGENT__PERFORMANCE_OPTIMIZER_ENABLED=false
export CLAUDE_AGENT_PERFORMANCE_RESOURCE_MONITORING=false
```

## Integration with Claude Code

Environment variables work seamlessly with Claude Code's settings.json hierarchy:

1. **Default Configuration**: Built-in sensible defaults
2. **User Settings**: `~/.claude/settings.json`
3. **Project Settings**: `.claude/settings.json`
4. **Local Settings**: `.claude/settings.local.json`
5. **Environment Variables**: Highest precedence

### Settings.json Integration
You can also use Claude Code's "env" setting in settings.json to inject environment variables:

```json
{
  "env": {
    "CLAUDE_AGENT_FRAMEWORK_ENABLED": "true",
    "CLAUDE_AGENT_PERFORMANCE_TOKEN_OPTIMIZATION": "true"
  },
  "agents": {
    "global_settings": {
      "framework_enabled": true
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **Agent not responding to environment variable changes**
   - Ensure variable name follows exact naming convention
   - Check agent name is correctly converted (hyphens to underscores, uppercase)
   - Verify hot reload is enabled: `CLAUDE_AGENT_HOT_RELOAD=true`

2. **Configuration not taking effect**
   - Check precedence order - environment variables override settings files
   - Validate variable names using the patterns above
   - Review logs for configuration validation warnings

3. **Performance issues**
   - Disable monitoring in production: `CLAUDE_AGENT_MONITORING_COORDINATION_LOGGING=false`
   - Enable caching: `CLAUDE_AGENT_PERFORMANCE_PROMPT_CACHING=true`
   - Optimize token usage: `CLAUDE_AGENT_PERFORMANCE_TOKEN_OPTIMIZATION=true`

### Debugging Commands
```bash
# Check all agent-related environment variables
env | grep CLAUDE_AGENT

# Validate configuration (if validation tool available)
python -m src.configuration.environment_handler validate
```

## Best Practices

1. **Use descriptive names**: Follow the established naming convention exactly
2. **Document custom settings**: Keep track of production environment variables
3. **Test configuration changes**: Use development environment first
4. **Monitor performance impact**: Enable monitoring when testing new settings
5. **Use settings files for persistent config**: Environment variables for deployment-specific overrides

## Security Considerations

- Never set sensitive values directly in environment variables in production
- Use secure secret management systems for sensitive configuration
- Regularly audit environment variable configurations
- Be cautious with coordination logging in production (may contain sensitive context)

For more information about Claude Code's settings system, see the [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code/settings).