# Primary Agent Spawning Protocol (S4.1 Implementation)

## Overview
Structured Task() delegation template with coordination context for Epic 4's hierarchical communication architecture.

## Coordination ID System

### ID Generation Pattern
```
COORD-{PRIMARY_AGENT}-{YYYY-MM-DD}-{HH-MM}-{DOMAIN_HASH}
```

**Examples:**
- `COORD-test-specialist-2025-08-05-14-30-A7B9C`
- `COORD-meta-coordinator-2025-08-05-14-30-F3D2E`

### ID Components
- **PREFIX**: Always "COORD-"
- **PRIMARY_AGENT**: Name of coordinating primary agent
- **TIMESTAMP**: ISO date and time
- **DOMAIN_HASH**: 5-char hash of problem domain context

## Structured Task() Delegation Template

### Template Structure
```python
Task(
    subagent_type="{secondary_agent_name}",
    description="{coordination_context_description}",
    prompt="""## Coordination Context
- **Coordination ID**: {coordination_id}
- **Primary Agent**: {primary_agent_name}
- **Problem Domain**: {domain_description}
- **Complexity Level**: {High/Medium/Low}
- **Integration Requirements**: {cross_domain_dependencies}

## Analysis Request
{detailed_analysis_request}

## Response Requirements
Please provide your response using the Secondary Agent Response Protocol:

### Executive Summary
[Brief overview of findings and recommendations]

### Domain Analysis Results
[Detailed domain-specific analysis with severity/complexity ratings]

### Cross-Domain Integration Notes
- **Dependencies**: [What other domains must be addressed first]
- **Conflicts**: [Potential conflicts with other domain recommendations]
- **Synergies**: [Opportunities for complementary domain solutions]

### Implementation Guidance
- **Priority Level**: [Critical/High/Medium/Low]
- **Dependencies**: [Sequential requirements]
- **Testing Requirements**: [Domain-specific validation needs]
- **Risk Assessment**: [Potential implementation risks]

### Coordination Metadata
- **Coordination ID**: {coordination_id}
- **Domain Completion**: [Estimated complexity and time]
- **Integration Priority**: [How this domain ranks in overall solution]
"""
)
```

## Coordination Metadata Standards

### Required Metadata Fields
- **coordination_id**: Unique identifier for tracking
- **primary_agent**: Originating agent name  
- **problem_context**: Brief problem description
- **complexity_assessment**: High/Medium/Low
- **expected_domains**: List of anticipated analysis domains
- **integration_requirements**: Cross-domain dependencies

### Enhanced Task() Examples

#### Example 1: Testing Domain Coordination
```python
coordination_id = "COORD-test-specialist-2025-08-05-14-30-A7B9C"

Task(
    subagent_type="async-pattern-fixer",
    description="Async testing pattern analysis with coordination context",
    prompt=f"""## Coordination Context
- **Coordination ID**: {coordination_id}
- **Primary Agent**: test-specialist
- **Problem Domain**: Async testing patterns and concurrency issues
- **Complexity Level**: High
- **Integration Requirements**: Must coordinate with mock-configuration and coverage analysis

## Analysis Request
Analyze async/await testing patterns in the test suite, focusing on:
1. AsyncMock configuration issues causing test failures
2. @pytest.mark.asyncio decorator problems
3. Async context manager testing patterns
4. Concurrency-related test isolation issues

## Response Requirements
[Full Secondary Agent Response Protocol structure]

### Coordination Metadata
- **Coordination ID**: {coordination_id}
- **Domain Completion**: High complexity, ~15-20 minutes
- **Integration Priority**: Critical for overall testing solution
"""
)
```

#### Example 2: Infrastructure Domain Coordination
```python
coordination_id = "COORD-infrastructure-engineer-2025-08-05-14-30-F3D2E"

Task(
    subagent_type="docker-specialist",
    description="Container orchestration analysis with coordination context",
    prompt=f"""## Coordination Context
- **Coordination ID**: {coordination_id}
- **Primary Agent**: infrastructure-engineer
- **Problem Domain**: Docker container orchestration and networking
- **Complexity Level**: Medium
- **Integration Requirements**: Must align with performance and environment analysis

## Analysis Request
Analyze Docker container orchestration issues:
1. Service networking configuration problems
2. Container health check failures
3. Resource allocation and scaling patterns
4. Inter-service communication bottlenecks

## Response Requirements
[Full Secondary Agent Response Protocol structure]

### Coordination Metadata
- **Coordination ID**: {coordination_id}
- **Domain Completion**: Medium complexity, ~10-15 minutes
- **Integration Priority**: High for infrastructure stability
"""
)
```

## Context Preservation Patterns

### Context Flow Architecture
```
Primary Agent Analysis
    ↓ (Enhanced context)
Structured Task() Delegation
    ↓ (Coordination metadata)
Secondary Agent Analysis
    ↓ (Integration intelligence)
Primary Agent Result Synthesis
    ↓ (Unified solution)
User Response
```

### Context Enrichment Guidelines
1. **Problem Context**: Include sufficient background for independent analysis
2. **Integration Context**: Specify cross-domain dependencies and conflicts
3. **Solution Context**: Define expected integration patterns and priorities
4. **Validation Context**: Specify testing and validation requirements

## Communication Flow Logging

### Log Structure
```json
{
  "coordination_id": "COORD-test-specialist-2025-08-05-14-30-A7B9C",
  "timestamp": "2025-08-05T14:30:00Z",
  "primary_agent": "test-specialist",
  "action": "spawn_secondary",
  "secondary_agent": "async-pattern-fixer",
  "context": {
    "problem_domain": "async_testing_patterns",
    "complexity": "High",
    "expected_dependencies": ["mock-configuration", "coverage-analysis"]
  },
  "status": "initiated"
}
```

### Logging Events
- **spawn_secondary**: Primary agent spawns secondary agent
- **secondary_complete**: Secondary agent completes analysis
- **integration_start**: Primary agent begins result integration
- **coordination_complete**: Full coordination cycle complete
- **conflict_detected**: Cross-domain conflicts identified

## Implementation Guidelines

### For Primary Agents
1. **Generate Coordination ID** using standard pattern
2. **Assess Complexity** and determine secondary agent needs
3. **Use Structured Template** for all Task() delegations
4. **Log Coordination Events** for debugging and optimization
5. **Process Integration Intelligence** from secondary agent responses

### For Enhanced Task() Execution
1. **Include Coordination Context** in all delegations
2. **Specify Integration Requirements** clearly
3. **Request Standardized Response Format** 
4. **Enable Cross-Domain Intelligence** through metadata
5. **Support Result Synthesis** through structured responses

## Performance Optimization

### Parallel Coordination Efficiency
- **Batch Coordination IDs**: Generate unique IDs for parallel spawning
- **Context Reuse**: Share common context across related spawns
- **Integration Preparation**: Pre-specify integration patterns
- **Response Standardization**: Ensure consistent secondary agent outputs

### Resource Management
- **Coordination Tracking**: Monitor active coordination sessions
- **Context Size Optimization**: Balance detail with performance
- **Integration Efficiency**: Streamline result synthesis patterns
- **Memory Management**: Efficient coordination metadata handling

This protocol enables structured, traceable, and efficient primary-to-secondary agent coordination following Epic 4's communication architecture requirements.