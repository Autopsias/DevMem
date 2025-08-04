---
description: Coordinate code quality analysis with security and architecture specialists
allowed-tools: [Read, Edit, MultiEdit, Bash, Grep, Glob]
argument-hint: "[file-path] [quality-scope]"
---

# Quality Analysis Coordination

Coordinate comprehensive code quality analysis with specialized secondary agents following Anthropic's natural delegation patterns.

## Usage
```
/quality-coordination [file-path] [quality-scope]
```

**Arguments:**
- `file-path`: Path to file or directory for quality analysis
- `quality-scope`: Optional scope (security, architecture, performance, types, style, all)

## Coordination Strategy

**Primary Analysis**: Start with code-quality-specialist for Semgrep scanning and quality analysis

**Secondary Agent Coordination** (based on quality findings):

### Security & Compliance Coordination
- **Deep Security Vulnerabilities** → security-auditor
- **Multi-Layer Security Issues** → security-auditor + configuration-validator

### Architecture & Pattern Coordination
- **Design Pattern Violations** → pattern-analyzer
- **Large-Scale Refactoring Needs** → refactoring-coordinator

### Performance & Optimization Coordination
- **Performance Anti-Patterns** → performance-optimizer
- **Resource Utilization Issues** → resource-optimizer

### Technical Quality Coordination
- **Complex Type System Issues** → type-system-expert
- **Async Pattern Problems** → async-pattern-fixer
- **Advanced Linting Issues** → linting-engineer

### Testing Quality Coordination
- **Test Quality Issues** → test-specialist
- **Mock Configuration Problems** → mock-configuration-expert

### Infrastructure Quality Coordination
- **Configuration Quality Issues** → configuration-validator
- **Dependency Quality Problems** → dependency-resolver

## Natural Language Coordination Pattern

The code-quality-specialist will provide systematic recommendations:

> "Code quality analysis with Semgrep scanning reveals [complex quality/security issue]. This comprehensive analysis would benefit from coordinating with `[secondary-agent]` for [specialized capability]. I recommend engaging them with this detailed context: [complete quality findings, security scan results, and specific areas requiring specialized attention]."

## Multi-Domain Coordination Examples

**Security + Architecture**: code-quality-specialist → security-auditor + pattern-analyzer + refactoring-coordinator
**Performance + Types**: code-quality-specialist → performance-optimizer + type-system-expert + async-pattern-fixer
**Testing + Configuration**: code-quality-specialist → test-specialist + mock-configuration-expert + configuration-validator

## Specialized Integration

Uses `mcp__semgrep__security_check` and `mcp__semgrep__semgrep_scan` for initial analysis, then coordinates with specialized secondary agents for comprehensive resolution.

Target analysis: $ARGUMENTS