---
description: Advanced multi-agent coordination following Anthropic's Claude Code best practices with natural agent selection
allowed-tools: [Read, Edit, MultiEdit, Bash, Grep, Glob]
argument-hint: "<complexity-level> [domain-context] - Specify coordination complexity and optional domain"
---

# Agent Coordination Command

Advanced multi-agent coordination following Anthropic's Claude Code best practices with natural agent selection and memory integration.

## Usage
```bash
/agent-coordinate <complexity-level> [domain-context]
```

## Complexity Levels

### **simple**
For single-domain issues requiring direct agent execution:
```bash
/agent-coordinate simple "linting violations in Python files"
/agent-coordinate simple "Docker container startup failure"
/agent-coordinate simple "pytest test failures"
```

### **multi**
For 2-3 domain issues requiring coordinated agent approach:
```bash
/agent-coordinate multi "test failures with security vulnerabilities"
/agent-coordinate multi "Docker performance issues affecting CI"
/agent-coordinate multi "code quality problems with architectural patterns"
```

### **strategic**
For 4+ domain complexity requiring meta-orchestration:
```bash
/agent-coordinate strategic "system architecture failure with testing, security, CI, and performance issues"
/agent-coordinate strategic "large-scale refactoring affecting multiple domains and systems"
/agent-coordinate strategic "infrastructure migration requiring comprehensive coordination"
```

## Memory-Enhanced Coordination

This command leverages the hierarchical memory architecture:

### **Agent Selection Intelligence**
- **@.claude/memory/agent-coordination-patterns.md** - Historical coordination patterns
- **@.claude/memory/domains/testing-patterns.md** - Testing domain expertise
- **@.claude/memory/domains/infrastructure-patterns.md** - Infrastructure domain intelligence
- **@.claude/memory/domains/security-patterns.md** - Security coordination patterns

### **Natural Claude Code Integration**
Following Anthropic's guidelines for natural agent delegation:

1. **Context Analysis**: Analyze domain complexity from user input
2. **Memory Lookup**: Reference historical coordination patterns
3. **Natural Selection**: Enable Claude Code's natural agent selection
4. **Coordination Enhancement**: Provide coordination context for optimal results

## Implementation

The command analyzes the complexity level and domain context to:

### **Simple Complexity**
- Enable direct Claude Code agent selection
- Provide enriched context for natural selection
- Reference domain-specific memory patterns
- Minimize coordination overhead

### **Multi Complexity**
- Identify primary agent based on domain analysis
- Suggest natural coordination patterns
- Reference successful historical coordination
- Enable parallel agent execution when beneficial

### **Strategic Complexity**
- Trigger meta-orchestration through natural language
- Reference complex coordination memory patterns
- Enable meta-coordinator for systematic coordination
- Provide comprehensive context for strategic planning

## Enhanced Agent Context

The command enriches agent selection context with:

### **RAG MemoryBank MCP Context**
- Project-specific patterns: FastMCP, TruLens, Qdrant, BM25S
- Quality requirements: ≥82% coverage, code standards
- Essential commands: `make docker-up`, `make test-coverage`
- Architecture patterns: Hybrid RAG pipeline, MCP server implementation

### **Performance Intelligence**
- Historical response times for similar coordination patterns
- Agent selection accuracy metrics and improvement tracking
- Coordination success rates for specific domain combinations
- Memory-driven optimization suggestions

### **Integration Patterns**
- Command-to-agent context propagation
- Memory system integration for learning capture
- Hook system coordination for performance enhancement
- Workflow orchestration for complex multi-step processes

## Example Workflows

### **Testing Architecture Enhancement**
```bash
/agent-coordinate multi "test coverage gaps with fixture design and integration issues"
```
→ **Natural Selection**: coverage-optimizer (primary) → fixture-design-specialist + integration-validator
→ **Memory Integration**: References testing domain patterns and successful coordination history
→ **Context Enrichment**: RAG MemoryBank testing standards and pytest patterns

### **Infrastructure Performance Optimization**
```bash
/agent-coordinate strategic "Docker orchestration performance affecting MCP server and Qdrant integration"
```
→ **Natural Selection**: infrastructure-engineer → docker-specialist + performance-optimizer + mcp-integration patterns
→ **Meta-Orchestration**: Complex infrastructure requiring strategic coordination
→ **Context Enrichment**: Project-specific MCP + Qdrant deployment patterns

### **Security Architecture Analysis**
```bash
/agent-coordinate multi "security vulnerabilities in code quality with architectural implications"
```
→ **Natural Selection**: code-quality-specialist → security-auditor + pattern-analyzer
→ **Memory Integration**: Security domain patterns and architectural coordination history
→ **Context Enrichment**: Security scanning patterns with Semgrep integration

This command seamlessly integrates with Claude Code's natural agent selection while providing sophisticated coordination intelligence through the memory system and domain expertise.