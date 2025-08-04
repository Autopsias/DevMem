---
description: Discover agents by capability for coordination planning
allowed-tools: [Read, Glob, Grep]
argument-hint: "[capability] [domain]"
---

# Agent Discovery by Capability

Discover agents matching specific capabilities for coordination planning following Anthropic's sub-agent discovery patterns.

## Usage
```
/find-agent [capability] [domain]
```

**Arguments:**
- `capability`: Required capability (async, security, performance, testing, architecture, etc.)
- `domain`: Optional domain filter (development, infrastructure, architecture, testing, integration)

## Agent Discovery Process

1. **Search Agent Descriptions**: Scan agent metadata for capability matches
2. **Domain Classification**: Group agents by specialization domain
3. **Coordination Recommendations**: Suggest coordination patterns based on capabilities

## Agent Capability Matrix

### Development Quality Domain
- **async-pattern-fixer**: async, concurrency, performance, deadlock-prevention
- **type-system-expert**: type-annotations, generics, type-safety, protocol-design
- **mock-configuration-expert**: mocking, testing, behavior-configuration, coordination
- **validation-tester**: qa, validation, workflows, testing-strategy
- **linting-engineer**: code-style, formatting, compliance, standards

### Infrastructure & Performance Domain
- **docker-specialist**: containers, orchestration, networking, troubleshooting
- **performance-optimizer**: performance, bottlenecks, scalability, optimization
- **resource-optimizer**: resource-allocation, efficiency, memory, cpu
- **environment-synchronizer**: environment-coordination, deployment, synchronization

### Architecture & Security Domain
- **security-auditor**: security, vulnerabilities, compliance, threat-modeling
- **pattern-analyzer**: architecture, design-patterns, consistency, validation
- **refactoring-coordinator**: refactoring, architecture, cross-module, coordination
- **dependency-resolver**: dependencies, conflicts, compatibility, resolution

### Testing & Integration Domain
- **coverage-optimizer**: coverage, testing-strategy, gap-analysis, optimization
- **fixture-design-specialist**: fixtures, dependency-injection, testing-architecture
- **integration-validator**: cross-system, validation, end-to-end, workflows
- **configuration-validator**: configuration, multi-environment, synchronization
- **workflow-optimizer**: ci-cd, github-actions, workflows, optimization

## Coordination Planning

Based on capability search results, the command provides:

1. **Matching Agents**: List of agents with required capabilities
2. **Coordination Patterns**: Suggested primary agent → secondary agent coordination
3. **Context Requirements**: Information needed for effective agent coordination

## Natural Language Integration

Results are formatted for easy integration with Anthropic's natural delegation patterns:

> "For [capability] requirements in [domain], consider coordinating with `[agent-name]` which specializes in [specific capabilities]. This agent can be engaged with context about [relevant technical details]."

Search target: $ARGUMENTS