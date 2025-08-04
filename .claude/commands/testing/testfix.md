---
description: Analyze and fix test failures, async/await patterns, mock configurations, and coverage issues
allowed-tools: [Read, Edit, MultiEdit, Bash, Grep, Glob, Task]
argument-hint: "[test scope] - Specific tests or 'all' for comprehensive analysis"
---

# Test Fix

I have test failures and need help fixing them for: ${ARGUMENTS:-all tests}

This naturally triggers Claude Code's native agent selection for test-related problems. The system will automatically engage the test-specialist agent and coordinate with secondary agents as needed.

**Test Analysis Focus:**

**Test Failure Diagnosis:**
- Pytest failures, assertion errors, and import issues
- Root cause identification for failing tests
- Test isolation issues and dependency conflicts
- Parametrized test failures and fixture problems

**Async/Await Testing Patterns:**
- Correct async test patterns using `@pytest.mark.asyncio`
- Fix AsyncMock vs Mock usage in async tests
- Resolve 'object Mock can't be used in await expression' errors
- Debug async context manager and generator testing

**Mock Configuration:**
- Configure Mock and AsyncMock with proper return values
- Set up complex mock behaviors and side effects
- Fix mock isolation and state persistence issues
- Debug mock call verification and argument matching

**Coverage Optimization:**
- Identify uncovered code paths and missing test cases
- Analyze coverage reports for quality gaps
- Design tests for edge cases and error conditions
- Optimize test suite structure for better coverage

**Expected Deliverables:**
- Specific fixes with exact line numbers
- Proper async/mock patterns implementation
- Test isolation and reliability improvements
- Coverage gap resolution with new test cases
- Recommendations for other agents if needed (ci-specialist, async-pattern-fixer)
