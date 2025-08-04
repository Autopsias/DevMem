---
description: Analyze and fix pre-commit hook failures, linting violations, and code quality issues
allowed-tools: [Read, Edit, MultiEdit, Bash, Grep, Glob, mcp__semgrep__security_check, mcp__semgrep__semgrep_scan]
argument-hint: "[hook scope] - Specific hooks or 'all' for comprehensive analysis"
---

# Pre-Commit Fix

Analyze and fix pre-commit hook failures, linting violations, and code quality issues for: ${ARGUMENTS:-all hooks}

This command addresses code quality and security issues, naturally engaging specialized quality assurance expertise.

## Code Quality Analysis Focus

**Linting Violations & Code Formatting:**
- Ruff, black, isort, and other formatting issues
- Code style compliance and consistency
- Import organization and unused imports
- Line length and whitespace issues

**Type Annotation Problems:**
- Missing type hints and mypy violations
- Generic type usage and complex type annotations
- Type compatibility across Python versions
- Type stub files and interface definitions

**Security Vulnerabilities:**
- Security pattern detection with Semgrep
- Secret detection and credential exposure
- SQL injection and XSS vulnerability patterns
- Dependency vulnerability analysis

**Code Quality Standards:**
- Complexity metrics and code organization
- Function and file length limits (50 lines/750 lines)
- Variable naming and descriptive patterns
- Architecture and design pattern compliance

**SDK Pattern Compliance:**
- FastMCP, TruLens, and Qdrant usage patterns
- MCP server integration best practices
- RAG pipeline implementation standards
- Test coverage requirements (≥82%)

**Pre-commit Configuration:**
- Hook configuration optimization
- Performance improvements and caching
- Cross-platform compatibility fixes
- Integration with CI/CD workflows

**Expected Deliverables:**
- Specific fixes with exact line numbers
- Code quality improvements and pattern compliance
- Security vulnerability remediation
- Pre-commit configuration optimizations
