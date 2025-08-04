---
description: Generate new agents based on requirements following Claude Code standards
allowed-tools: [Read, Edit, Write, Grep]
argument-hint: "[specification] - Agent specification or requirements"
---

# Create Agent Command

Generate new Claude Code compliant agents based on provided specifications.

## Agent Creation Standards

### Template Requirements
- **YAML Frontmatter**: Must include name, description, and tools
- **Focused Instructions**: Maximum 50 lines of actionable content
- **Tool Access**: Minimal permissions required for the agent's purpose
- **Claude Code Compliance**: No Task tool usage, direct tool access only

### Agent Template Structure
```markdown
---
name: agent-name
description: Clear, specific purpose and invocation context
tools: [minimal required tools]
---

# Agent Name

You are a specialized agent for [specific purpose].

## Core Focus
- **Primary Function**: Clear definition of main responsibility
- **Secondary Functions**: Supporting capabilities

## Process
1. **Step 1**: Clear action with specific tools
2. **Step 2**: Follow-up actions
3. **Step 3**: Validation and results

Focus on [specific outcome or quality metric].
```

### Tool Categories
- **Analysis**: Read, Grep, Glob
- **Code Changes**: Edit, MultiEdit
- **System Operations**: Bash
- **Enhanced Knowledge**: mcp__Ref__, mcp__exa__, mcp__perplexity-ask__
- **Security**: mcp__semgrep__ tools

### Validation Checklist
- ✅ No Task tool in tools list
- ✅ Instructions under 50 lines
- ✅ Clear, actionable directives
- ✅ Appropriate tool permissions
- ✅ Specific focus area
- ✅ Claude Code standard compliance

## Usage
Provide agent specification as argument:

**Examples:**
- `/create-agent API testing specialist for FastAPI endpoints`
- `/create-agent Database migration agent for schema changes`
- `/create-agent Documentation generator for code comments`

Specification: $ARGUMENTS
EOF < /dev/null