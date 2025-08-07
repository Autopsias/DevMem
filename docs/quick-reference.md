# Quick Reference Guide

## Common Tasks

### Development

#### Run Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_epic4_result_integration.py

# Run with coverage
pytest --cov=. --cov-report=term-missing
```

#### Code Quality
```bash
# Check code style
ruff check .

# Format code
black .

# Run type checking
mypy .
```

#### System Health
```bash
# Quick health check
./scripts/system/simple_health_check.sh

# Full system check
./scripts/system/system_health.sh

# Performance validation
./scripts/performance/performance_summary.sh
```

### Infrastructure

#### Memory System
- coordination-hub.md: All coordination patterns
- domain-intelligence.md: Domain expertise
- Maximum file size: 750 lines
- Access time target: <25ms

#### Performance Targets
- Memory access: <25ms
- Cache hit ratio: >95%
- Context preservation: >97%
- Agent selection: <1s
- Coordination success: >90%

### Troubleshooting

#### Memory Issues
1. Check file integrity
2. Validate performance metrics
3. Review coordination patterns
4. Check system health

#### Performance Issues
1. Run health check
2. Check memory access time
3. Review cache hit ratio
4. Validate coordination success

#### Recovery Steps
1. Stop affected services
2. Load latest backup
3. Verify restoration
4. Run health checks

## Essential Files

### Configuration
- CLAUDE.md: Project configuration
- .claude/settings.json: Framework settings
- .claude/agents/: Agent definitions
- .claude/memory/: Memory system

### Documentation
- README.md: Project overview
- docs/architecture/: System design
- docs/infrastructure-*.md: Guides
- docs/rollback-*.md: Recovery procedures

## Common Issues

### Test Failures
1. Check test file exists
2. Verify file paths
3. Update test assertions
4. Run specific test file

### Performance Problems
1. Monitor metrics
2. Check file sizes
3. Review coordination
4. Validate patterns

### Configuration Issues
1. Verify file exists
2. Check file format
3. Validate settings
4. Run health check