# DevMem

A Python project with Claude Code Framework

## Essential Commands

### Development
- `pytest` - Run test suite
- `ruff check . && black --check .` - Code formatting and linting  
- `mypy .` - Type checking
- `pytest --cov=. --cov-report=term-missing` - Test coverage analysis

### Claude Code Framework
- Natural language problem description triggers appropriate agents automatically
- 35+ specialized agents for development, testing, security, and infrastructure
- `/digdeep [problem]` - Deep problem analysis using Five Whys methodology
- `/testfix [scope]` - Analyze and fix test failures
- `/commit` - Intelligent git commits with quality validation

### Quality Gates
- Minimum 80% test coverage required
- All type checking must pass before merge
- Code formatting enforced via pre-commit hooks
- Security scanning integrated into CI pipeline

## Code Standards

### File Organization
- Maximum 750 lines per implementation file
- Maximum 1000 lines per test file  
- Maximum 50 lines per function
- Use descriptive variable names (avoid `data`, `result`, `temp`)

### Python Requirements
- Type hints required for all functions
- Docstrings for all public functions and classes
- Use `pathlib` instead of `os.path` for file operations
- Follow PEP 8 style guidelines

### Testing Requirements
- Pytest for all testing (unless project uses different framework)
- Mock external dependencies in unit tests
- Integration tests for API endpoints and database operations
- Performance tests for critical path functions

## Agent Framework Integration

The Claude Code Framework provides intelligent agent coordination following Anthropic standards:

- **Natural Language Triggering**: Describe problems naturally instead of calling agents explicitly
- **Automatic Agent Selection**: Framework selects appropriate specialists based on problem description
- **Sequential Intelligence**: Multi-step problems trigger coordinated agent workflows
- **Memory Patterns**: @import references for consistent coordination patterns

### Framework Memory Patterns
@.claude/memory/agent-coordination-patterns.md
@.claude/memory/domains/testing-patterns.md
@.claude/memory/domains/infrastructure-patterns.md
@.claude/memory/domains/security-patterns.md

## Project-Specific Guidelines

@docs/contributing.md
@docs/architecture.md