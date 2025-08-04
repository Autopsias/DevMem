---
description: Comprehensive agent framework health monitoring with Anthropic compliance validation and ecosystem intelligence analysis
allowed-tools: [Read, Grep, Bash, Glob]
argument-hint: "[filter] - Optional filter: compliance, ecosystem, integration, duplication, gaps, or specific agent names"
---

# Review Agents Command

Perform **comprehensive framework health assessment** using the enhanced agent-reviewer capabilities for Anthropic compliance validation, ecosystem intelligence analysis, and integration health monitoring.

## Framework Analysis Scope
- **Primary agents** (16): @.claude/agents/
- **Secondary agents** (19): @.claude/agents/secondary/
- **Framework integration**: CLAUDE.md, hooks, slash commands, MCP patterns

## Comprehensive Analysis Framework

### 1. Anthropic Guidelines Compliance Engine
**YAML Frontmatter Validation**:
```bash
# Check "Use PROACTIVELY" pattern compliance
grep -r "Use PROACTIVELY" .claude/agents/ | wc -l
grep -r "description:" .claude/agents/ | grep -v "Use PROACTIVELY"
```

**Rich Trigger Phrase Analysis**:
```bash
# Validate trigger phrase richness
grep -r "Perfect when users" .claude/agents/ | wc -l
grep -r "when users need" .claude/agents/ | wc -l
```

**Tool Appropriateness Audit**:
```bash
# Analyze tool usage patterns
grep -r "tools:" .claude/agents/ | cut -d: -f2- | sort | uniq -c
```

### 2. Agent Ecosystem Intelligence Analysis
**Overlap Detection**:
```bash
# Performance domain overlap
grep -r "performance-optimizer\|resource-optimizer" .claude/agents/
# Quality domain overlap  
grep -r "code-quality-specialist\|lint-enforcer\|linting-engineer" .claude/agents/
# Infrastructure overlap
grep -r "infrastructure-engineer\|docker-specialist" .claude/agents/
```

**Coordination Pattern Analysis**:
```bash
# Track coordination patterns
grep -r 'Coordinate with `' .claude/agents/ | wc -l  # Explicit coordination
grep -r "natural delegation\|natural language" .claude/agents/ | wc -l  # Natural delegation
```

### 3. Integration Health Monitoring
**Memory System Integration**:
```bash
# Check @import patterns
grep -r "@.claude/" .claude/agents/ | wc -l
grep -r "@~/.claude/" .claude/agents/
```

**Hook System Coordination**:
```bash
# Validate hook integration
cat .claude/settings.json | jq '.hooks'
ls .claude/commands/*.md | wc -l
```

### 4. Framework Health Indicators
**🟢 OPTIMAL HEALTH**:
- Anthropic compliant (Use PROACTIVELY + rich triggers)
- No functional duplication
- Natural delegation patterns
- Proper integration patterns

**🟡 NEEDS ATTENTION**:
- Partial compliance issues
- Some coordination conflicts
- Minor integration problems
- Pattern modernization needed

**🔴 CRITICAL ISSUES**:
- Non-compliant with Anthropic guidelines
- Significant agent duplication
- Coordination conflicts
- Integration failures

### 5. Gap Analysis & Recommendations
**Workflow Coverage Assessment**:
- Identify uncovered user workflow areas
- Recommend new agent requirements or existing agent enhancements
- Track ecosystem evolution needs

**Duplication Consolidation**:
- Flag agents with >70% functional overlap
- Suggest merge/enhancement opportunities
- Preserve specialized expertise while reducing redundancy

## Usage Patterns & Examples

### Comprehensive Framework Analysis
```bash
/review-agents                    # Full framework health check
/review-agents compliance         # Anthropic guidelines compliance focus
/review-agents ecosystem         # Agent overlap and gap analysis
/review-agents integration       # CLAUDE.md, hooks, commands integration
/review-agents duplication       # Agent duplication detection
/review-agents gaps              # Workflow coverage gap analysis
```

### Targeted Agent Analysis
```bash
/review-agents primary           # Review 16 primary agents only
/review-agents secondary         # Review 19 secondary agents only
/review-agents test-specialist   # Specific agent deep analysis
/review-agents performance       # Performance domain agents
/review-agents quality           # Quality domain agents
```

### Integration-Specific Analysis
```bash
/review-agents hooks             # Hook system integration health
/review-agents memory            # CLAUDE.md memory integration
/review-agents mcp               # MCP pattern compliance
/review-agents commands          # Slash command compatibility
```

## Expected Framework Analysis Output

**Anthropic Compliance Report**:
- Compliance percentage across 33+ agents
- Non-compliant agents with specific improvement recommendations
- Tool usage optimization suggestions
- Natural delegation pattern adoption status

**Ecosystem Intelligence Report**:
- Agent overlap matrix with consolidation recommendations
- Coordination conflict identification and resolution strategies
- Workflow coverage gaps with enhancement suggestions
- Performance and effectiveness metrics

**Integration Health Report**:
- Memory system integration status
- Hook coordination effectiveness metrics
- Slash command compatibility assessment
- MCP pattern compliance and optimization recommendations

**Framework Optimization Recommendations**:
- Specific agent improvements with implementation guidance
- Ecosystem consolidation opportunities
- Integration enhancement strategies
- Performance optimization suggestions

This command leverages the enhanced **agent-reviewer** capabilities to provide comprehensive framework health monitoring following official Anthropic Claude Code standards.

## Filter Application
Filter: $ARGUMENTS

## Execution Context
The command automatically activates the enhanced **agent-reviewer** with comprehensive framework analysis capabilities, ensuring thorough evaluation of all 33+ agents across compliance, ecosystem intelligence, and integration health dimensions.