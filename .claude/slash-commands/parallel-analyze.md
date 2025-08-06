---
name: parallel-analyze
description: Run comprehensive 4-agent system analysis (security, performance, testing, infrastructure) via direct coordination
---

# Parallel System Analysis

This command spawns 4 agents simultaneously to analyze a system comprehensively via analysis-gateway direct coordination:

**Usage:** `/parallel-analyze "system or component name"`

**Agents spawned in parallel via direct Task() calls:**
- security-enforcer: Security vulnerability analysis
- performance-optimizer: Performance bottleneck identification  
- test-specialist: Test coverage and quality assessment
- infrastructure-engineer: Infrastructure and deployment analysis

**Example:** `/parallel-analyze "authentication system"`

## Implementation

This command will execute the following direct parallel coordination:

```
analysis-gateway: "Comprehensive 4-domain analysis of [system] spanning security, performance, testing, and infrastructure domains. I'll coordinate analysis using 4 tasks in parallel: security vulnerability assessment, performance optimization analysis, testing strategy evaluation, and infrastructure review."
```

The analysis-gateway will handle the direct parallel execution with Task() calls for optimal efficiency.