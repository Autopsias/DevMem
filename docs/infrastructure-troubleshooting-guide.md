# Infrastructure Troubleshooting Guide

## Common Issues and Solutions

### 1. Memory System Issues

#### Test File Not Found Errors
**Problem**: Tests failing with "Test file not found" errors
**Solution**:
1. Check if test file was removed in Stories 1.2-1.5 infrastructure simplification
2. Update test references to use new simplified file structure
3. Remove outdated test references from test suites

#### Context Preservation Issues
**Problem**: Context not being preserved between agents (context preservation <97%)
**Solution**:
1. Verify simplified 2-file memory structure is being used
   - coordination-hub.md: Contains all coordination patterns
   - domain-intelligence.md: Contains all domain expertise
2. Check context enrichment patterns are properly implemented
3. Validate that file paths are correct in .claude/settings.json

### 2. Performance Issues

#### Agent Selection Performance
**Problem**: Agent selection taking longer than target (<1s)
**Solution**:
1. Verify cache hit ratios (target >95%)
2. Check memory system performance (target <25ms access time)
3. Validate coordination patterns are optimized
4. Monitor system resource usage

#### Coordination Performance
**Problem**: Coordination taking longer than expected
**Solution**:
1. Check for parallel execution efficiency
2. Verify sequential coordination patterns
3. Monitor resource allocation and usage
4. Validate meta-orchestration thresholds

### 3. Test Failures

#### CI Pipeline Tests
**Problem**: CI pipeline tests failing after infrastructure changes
**Solution**:
1. Remove outdated CI tests that reference removed Python infrastructure
2. Update test assertions to match new simplified architecture
3. Verify test files exist in correct locations
4. Update performance thresholds in tests

#### Coordination Pattern Tests
**Problem**: Coordination pattern tests failing
**Solution**:
1. Verify test uses correct file paths
2. Check agent coordination patterns
3. Validate performance metrics
4. Update test scenarios if needed

### 4. Recovery Procedures

#### Emergency System Recovery
If critical performance degradation is detected:
1. Measure current system performance
2. Compare against baseline metrics
3. If performance drop >10%, initiate rollback
4. Validate restoration success
5. Alert system administrators

#### Pattern-Specific Recovery
For coordination pattern failures:
1. Identify failing pattern
2. Load pattern validation suite
3. Test pattern in isolation
4. Restore pattern from backup if needed
5. Verify pattern restoration

## Health Check Commands

```bash
# Memory System Health Check
./scripts/system/system_health.sh

# Performance Validation
./scripts/performance/performance_summary.sh

# Coordination Testing
pytest tests/test_epic4_result_integration.py
pytest tests/test_s4_1_hierarchical_communication.py

# Pattern Validation
./scripts/system/simple_health_check.sh
```

## Performance Baseline Targets

- Memory Access: <25ms
- Cache Hit Ratio: >95%
- Context Preservation: >97%
- Agent Selection: <1s
- Coordination Success: >90%
- Parallel Execution: <2s for 3 agents

## Monitoring and Alerting

Monitor these key metrics:
- Memory lookup performance
- Agent selection accuracy
- System responsiveness
- Cache hit ratios
- Coordination success rates

Alert thresholds:
- Performance degradation >5%
- Success rate drop >5%
- Memory system errors