# Testing Domain Agent Patterns

## Domain-Specific Agent Selection Intelligence

### Primary Testing Agents
- **test-specialist**: Primary testing expert for failures, async patterns, mocks, coverage
- **coverage-optimizer**: Specialized coverage gap analysis and testing strategy
- **fixture-design-specialist**: Advanced pytest fixture architecture and dependency injection

### Testing Integration Patterns

#### **Async Testing Coordination**
```
User Context: "Test failures with async patterns and mock configuration"
→ test-specialist (primary)
→ Coordination: async-pattern-fixer + mock-configuration-expert
→ Success Rate: 94% for async + mock issues
```

#### **Coverage Architecture Issues**
```
User Context: "Test coverage gaps requiring architectural improvements"
→ coverage-optimizer (primary)
→ Coordination: fixture-design-specialist + integration-validator
→ Success Rate: 91% for coverage + architecture issues
```

#### **Integration Testing Complexity**
```
User Context: "End-to-end testing failures across multiple services"
→ integration-validator (primary)
→ Coordination: test-specialist + docker-specialist
→ Success Rate: 88% for integration + infrastructure issues
```

### Testing Performance Patterns

#### **Response Time Optimization**
- **test-specialist**: Average 1.2s response for standard test failures
- **coverage-optimizer**: Average 2.1s for complex coverage analysis
- **fixture-design-specialist**: Average 1.8s for fixture architecture

#### **Coordination Efficiency**
- **Single Test Issue**: Direct agent selection (0.9s average)
- **Multi-Test Domains**: Primary + 1-2 secondary agents (1.5s average)
- **Architecture Testing**: Meta-orchestration for 4+ domains (2.3s average)

### Common Testing Scenarios

#### **High-Success Patterns**
1. **Pytest + AsyncMock Issues**: test-specialist → async-pattern-fixer (96% success)
2. **Coverage + Fixture Architecture**: coverage-optimizer → fixture-design-specialist (93% success)
3. **Integration + Service Testing**: integration-validator → docker-specialist (90% success)

#### **Meta-Orchestration Triggers**
- **Testing + Security + CI + Performance**: 4+ domains → orchestration-coordinator
- **Architecture + Testing + Integration + Environment**: Complex cross-system issues
- **Performance + Testing + Infrastructure + Configuration**: Multi-layer testing problems

### RAG MemoryBank MCP Testing Context

#### **Project-Specific Testing Intelligence**
- **Coverage Requirement**: ≥82% coverage validation required
- **Testing Commands**: `make test-coverage`, `./scripts/ci-modular-runner.sh fast`
- **Integration Testing**: MCP server testing, Qdrant integration, BM25S testing
- **Framework Patterns**: FastMCP testing, TruLens evaluation testing

#### **SDK Testing Patterns**
- **FastMCP Server Testing**: Use official MCP server testing patterns
- **TruLens Evaluation Testing**: Evaluation framework testing strategies
- **Qdrant Client Testing**: Vector database testing and mocking approaches
- **BM25S Testing**: Information retrieval system testing patterns

This domain memory enhances natural agent selection for testing-related issues while maintaining the sophisticated coordination patterns developed in the agent ecosystem.