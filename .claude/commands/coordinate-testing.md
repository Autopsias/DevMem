---
description: Coordinate multiple testing agents for comprehensive analysis
allowed-tools: [Read, Edit, MultiEdit, Bash, Grep, Glob]
argument-hint: "[test-file-path] [analysis-scope]"
---

# Coordinate Testing Analysis

Coordinate comprehensive testing analysis using multiple specialized agents following Anthropic's natural delegation patterns.

## Usage
```
/coordinate-testing [test-file-path] [analysis-scope]
```

**Arguments:**
- `test-file-path`: Path to test file or directory to analyze
- `analysis-scope`: Optional scope (async, mocks, coverage, fixtures, all)

## Coordination Strategy

**Primary Analysis**: Start with test-specialist for comprehensive testing analysis

**Secondary Agent Coordination** (based on findings):

1. **Async Testing Issues**: If async patterns detected → Coordinate with async-pattern-fixer
2. **Mock Configuration Problems**: If mock issues found → Engage mock-configuration-expert
3. **Coverage Strategy Needs**: If coverage gaps identified → Coordinate with coverage-optimizer
4. **Fixture Design Issues**: If fixture problems detected → Engage fixture-design-specialist
5. **CI/CD Test Failures**: If environment issues found → Coordinate with ci-specialist

## Natural Language Coordination

The test-specialist will use natural language to recommend coordination:

> "Testing analysis reveals [specific complex issue]. This would benefit from coordinating with `[secondary-agent]` for [specialized capability]. I recommend engaging them with this context: [detailed test findings and specific focus areas]."

## Multi-Domain Coordination Examples

**Complex Async Testing**: test-specialist → async-pattern-fixer + mock-configuration-expert
**Coverage Architecture**: test-specialist → coverage-optimizer + fixture-design-specialist
**CI Integration Testing**: test-specialist → ci-specialist + integration-validator

Target analysis: $ARGUMENTS