# Quick Agent Selection Performance Report
Generated: 2025-08-07 22:15:11

## Summary Results
- **Total Tests**:       16 scenarios
- **Accuracy**: 0% (0/      16 correct)
- **Average Selection Time**: infms
- **Min Selection Time**: 999999ms
- **Max Selection Time**: test-specialistms

## Performance Targets
- **Time Target**: ≤1000ms ✅ PASSED
- **Accuracy Target**: ≥95% ❌ FAILED

## Detailed Results
| Scenario | Expected | Selected | Time (ms) | Status |
|----------|----------|----------|-----------|--------|
| scenario | expected_agent | selected_agent | time_ms | ❌ |
| testing_async_mock | test-specialist | async-pattern-fixer | 3 | ❌ |
| performance_bottleneck | performance-optimizer | analysis-gateway | 3 | ❌ |
| docker_orchestration | infrastructure-engineer | infrastructure-engineer | 4 | ✅ |
| security_vulnerability | security-enforcer | analysis-gateway | 3 | ❌ |
| coverage_gaps | coverage-optimizer | analysis-gateway | 3 | ❌ |
| infrastructure_scaling | infrastructure-engineer | infrastructure-engineer | 3 | ✅ |
| ci_pipeline_failure | ci-specialist | ci-specialist | 3 | ✅ |
| integration_testing | integration-validator | test-specialist | 3 | ❌ |
| code_quality_issues | code-quality-specialist | code-quality-specialist | 4 | ✅ |
| environment_config | environment-analyst | analysis-gateway | 3 | ❌ |
| memory_optimization | resource-optimizer | performance-optimizer | 3 | ❌ |
| async_pattern_fixes | async-pattern-fixer | analysis-gateway | 3 | ❌ |
| fixture_architecture | fixture-design-specialist | analysis-gateway | 4 | ❌ |
| security_compliance | security-auditor | analysis-gateway | 4 | ❌ |
| dependency_conflicts | dependency-resolver | dependency-resolver | 3 | ✅ |

## Performance Analysis
- **≤500ms**: 0 selections (0%)
- **501-1000ms**: 0 selections (0%)
- **>1000ms**: 16 selections (100%)

## Memory System Status
⚠️ **NEEDS ACCURACY TUNING**: Fast selection but accuracy below target
