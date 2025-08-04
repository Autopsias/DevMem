---
description: Documentation for Claude Code slash commands and deep problem analysis workflows
allowed-tools: [Read]
argument-hint: "Documentation only - no arguments required"
---

# Claude Code Slash Commands - Deep Problem Analysis

## Overview

This directory contains custom Claude Code slash commands for advanced problem analysis and solution implementation.

## Available Commands

### `/digdeep` - Deep Problem Analysis

**Purpose**: Comprehensive problem analysis using UltraThink methodology with parallel coordinated sub-agents.

**Usage**:
```
/digdeep [problem description]
```

**Examples**:
```
/digdeep The CI pipeline is failing with Docker timeout issues
/digdeep Tests are failing with async/await errors after recent changes
/digdeep My development environment won't start and shows port conflicts
/digdeep Coverage is dropping and some integration tests are flaky
```

## How It Works

### 1. Natural Language Interaction
After you invoke `/digdeep`, all interactions will be in natural language. The system will:
- Ask clarifying questions about your problem
- Request additional context and symptoms
- Gather information about recent changes
- Understand your environment and setup

### 2. UltraThink Analysis Methodology
The system applies systematic analysis:
- **Problem Classification**: Categorizes the issue type
- **Scope Assessment**: Determines analysis depth needed
- **Evidence Gathering**: Collects relevant data and patterns
- **Root Cause Identification**: Maps symptoms to underlying causes

### 3. Parallel Sub-Agent Coordination
Six specialized agents work simultaneously:
- **Environment & System Analyst**: Dependencies, configuration, resources
- **Code Quality & Pattern Analyst**: Standards, lint, security, performance
- **Infrastructure & Service Analyst**: Docker, CI/CD, networking, scaling
- **Test & Mock Pattern Analyst**: Test failures, async patterns, fixtures
- **Git & Change Impact Analyst**: Recent changes, merge conflicts, dependencies
- **Log & Error Correlation Analyst**: Error patterns, timing, event correlation

### 4. Comprehensive Output
You receive:
- **Executive Summary**: Problem overview and recommended solution
- **Root Cause Analysis**: Primary causes with supporting evidence
- **Solution Scenarios**: 3-5 ranked options with success probabilities
- **Implementation Plan**: Step-by-step execution guide
- **Todo List**: Actionable tasks created with TodoWrite tool
- **Validation Plan**: Success criteria and verification steps
- **Risk Assessment**: Potential issues and mitigation strategies

## Expected Workflow

```
1. User: /digdeep CI tests are timing out randomly
2. System: I'll analyze your CI timeout issues. Can you tell me:
   - When did these timeouts start occurring?
   - Which specific tests are timing out?
   - Have there been recent changes to CI configuration?
   - What error messages are you seeing?

3. User: [Provides context in natural language]

4. System: [Launches 6 parallel analysis agents]
   - Agent 1: Checking system resources and CI runner constraints...
   - Agent 2: Analyzing test patterns and execution time trends...
   - Agent 3: Examining Docker configurations and service health...
   - Agent 4: Reviewing test isolation and async patterns...
   - Agent 5: Analyzing recent commits for performance impacts...
   - Agent 6: Correlating timeout patterns with system logs...

5. System: [Provides comprehensive analysis and implementation plan]
   - Root cause: Resource contention during parallel test execution
   - Primary solution: Optimize CI runner configuration (85% success probability)
   - Alternative solutions: Test execution batching, resource scaling
   - Todo list with 12 specific implementation tasks
   - Validation checklist for confirming resolution
```

## Integration with Project Infrastructure

The `/digdeep` command leverages your existing project patterns:
- **Uses Task tool**: For coordinating parallel sub-agent analysis
- **Follows CLAUDE.md standards**: Respects your development guidelines
- **Integrates with existing scripts**: References ci-modular-runner, docker-orchestrator, etc.
- **TodoWrite integration**: Creates structured, prioritized task lists
- **Quality compliance**: Aligns with lint-ci and testing standards

## Tips for Best Results

1. **Be specific**: Include error messages, log excerpts, or specific symptoms
2. **Provide context**: Mention recent changes, environment details, or timing
3. **Share attempts**: Tell the system what you've already tried
4. **Ask follow-ups**: Engage in the natural language conversation for deeper analysis
5. **Use the todos**: The generated TodoWrite tasks provide a clear action plan

## File Structure

```
.claude/commands/
├── README.md          # This documentation
└── digdeep.md         # Main deep analysis command
```

## Command Status

✅ **digdeep.md** - Implemented and ready for use
📋 **README.md** - Documentation complete
🧪 **Testing** - Ready for user validation

The `/digdeep` command is now available for use in Claude Code. Simply type `/digdeep [your problem description]` to begin comprehensive problem analysis.