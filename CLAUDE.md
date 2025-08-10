# DevMem Claude Code Framework

A Python project using Claude Code's agent framework for intelligent task coordination.

## Essential Commands

### Development
- `pytest` - Run test suite
- `ruff check . && black --check .` - Code formatting and linting  
- `mypy .` - Type checking
- `pytest --cov=. --cov-report=term-missing` - Test coverage analysis

### Code Standards

- Maximum 750 lines per implementation file, 1000 for tests
- Maximum 50 lines per function
- Type hints required for all functions
- Docstrings for all public functions and classes
- Follow PEP 8 style guidelines

### Testing Requirements
- Pytest for testing
- Mock external dependencies in unit tests
- Integration tests for critical functionality
- Maintain minimum 80% test coverage

## Agent Framework

The project uses Claude Code's agent framework with specialized agents for different tasks:

### Core Agents
- code-quality-specialist: Code quality and standards enforcement
- test-specialist: Test failure analysis and coverage optimization

### Agent Activation
- Natural language problem description triggers appropriate agents
- Agents are proactively activated based on task context
- Use Task tool for complex multi-step operations

### Framework Guidelines
- Follow Anthropic's agent framework standards
- Use natural language delegation
- Keep agent implementations focused and minimal
- Validate framework health with `python validate.py`