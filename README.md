# DevMem - Claude Code Framework Project

## Overview
DevMem is a Python project built with the Claude Code Framework, providing intelligent agent coordination and memory-driven development workflows.

## Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/your-username/DevMem.git
cd DevMem

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage
1. Add the project configuration to CLAUDE.md
2. Create .claude/settings.json for framework settings
3. Use natural language to trigger appropriate agents
4. Run validation commands to verify changes

### Key Commands
```bash
# Run tests
pytest

# Check code quality
ruff check . && black --check .

# Run type checking
mypy .

# Check test coverage
pytest --cov=. --cov-report=term-missing
```

## Documentation Structure

### User Guides
- [Getting Started](docs/getting-started.md)
- [Quick Reference](docs/quick-reference.md)
- [Infrastructure Troubleshooting](docs/infrastructure-troubleshooting-guide.md)

### Technical Documentation
- [Infrastructure Architecture](docs/architecture/simplified-memory-architecture.md)
- [Memory System](docs/architecture/streamlined-memory-update-procedures.md)
- [Maintenance Procedures](docs/infrastructure-maintenance-procedures.md)
- [Rollback Procedures](docs/rollback-recovery-procedures.md)

## Project Standards

### Code Quality
- Maximum 750 lines per implementation file
- Maximum 1000 lines per test file
- Maximum 50 lines per function
- PEP 8 style guidelines enforced

### Testing
- Minimum 80% test coverage required
- Type checking must pass before merge
- Code formatting enforced via pre-commit hooks
- Security scanning integrated into CI pipeline

## Architecture

### Claude Code Framework
- Natural language problem description triggers appropriate agents
- 35+ specialized agents for development, testing, security, and infrastructure
- Simplified 2-file memory architecture for optimal performance
- Security and quality gates enforced throughout

### Memory System
- coordination-hub.md: All coordination patterns
- domain-intelligence.md: Domain expertise
- Sub-25ms access time for optimal performance
- 95%+ cache hit ratio for frequent patterns

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes following project standards
4. Run quality checks
5. Submit a pull request

## License
MIT License (see LICENSE file)