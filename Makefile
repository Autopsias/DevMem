# DevMem Project Makefile
# System maintenance and project management commands

# System maintenance targets
.PHONY: memory-status memory-validate memory-maintenance memory-dashboard memory-setup
.PHONY: system-health system-maintenance validate-system emergency-diagnostics
.PHONY: log-summary security-check
# Testing targets  
.PHONY: test test-agent-matching test-coverage lint-ci pre-commit-staged

# === MEMORY MAINTENANCE ===

# Show quick memory system status
memory-status:
	@./scripts/memory/memory_manager.sh status

# Validate memory system with optional fixes
memory-validate:
	@./scripts/memory/memory_manager.sh validate --fix --report

# Run full memory maintenance
memory-maintenance:
	@./scripts/memory/memory_manager.sh maintenance full

# Show memory system dashboard
memory-dashboard:
	@./scripts/memory/memory_manager.sh dashboard

# Setup periodic memory maintenance
memory-setup:
	@./scripts/memory/memory_manager.sh setup-periodic --enable

# Disable periodic memory maintenance
memory-stop:
	@./scripts/memory/memory_manager.sh setup-periodic --disable

# Show all available memory commands
memory-help:
	@echo "Memory Maintenance Commands:"
	@echo "  memory-status      - Show quick memory system status"
	@echo "  memory-validate    - Validate memory with fixes and report"  
	@echo "  memory-maintenance - Run full memory maintenance"
	@echo "  memory-dashboard   - Show interactive memory dashboard"
	@echo "  memory-setup       - Enable periodic memory maintenance"
	@echo "  memory-stop        - Disable periodic memory maintenance"
	@echo "  memory-help        - Show this help message"

# === SYSTEM HEALTH & MAINTENANCE ===

# System health check
system-health:
	@./scripts/system/simple_health_check.sh

# Full system maintenance
system-maintenance: memory-maintenance
	@echo "🔧 Running comprehensive system maintenance..."
	@./scripts/system/system_health.sh >/dev/null
	@echo "✅ System maintenance completed"

# Validate system integrity
validate-system:
	@echo "🔍 Validating system integrity..."
	@python scripts/validate_native_config.py
	@./scripts/system/system_health.sh --json >/dev/null && echo "✅ System validation passed" || echo "⚠️ System validation issues detected"

# Emergency diagnostics collection
emergency-diagnostics:
	@echo "🚨 Collecting emergency diagnostics..."
	@./scripts/emergency/collect_diagnostics.sh

# Log summary for troubleshooting
log-summary:
	@echo "📋 Recent log activity:"
	@echo "Security (last 5 entries):"
	@tail -n 5 .claude/security.log 2>/dev/null || echo "  No security log found"
	@echo "Quality (last 5 entries):"
	@tail -n 5 .claude/quality.log 2>/dev/null || echo "  No quality log found"
	@echo "Memory (last 3 entries):"
	@tail -n 3 .claude/memory_maintenance.log 2>/dev/null || echo "  No memory log found"

# Security check
security-check:
	@echo "🔒 Security status check:"
	@echo "Essential hooks status:"
	@ls -la scripts/hooks/essential_*.sh 2>/dev/null || echo "  ⚠️ Essential hooks not found"
	@echo "Recent security events:"
	@grep -c "BLOCKED\|DANGEROUS" .claude/security.log 2>/dev/null | sed 's/^/  /' || echo "  No security events logged"

# === TESTING & VALIDATION ===

# Run all tests
test:
	pytest tests/ -v

# Run agent matching tests specifically
test-agent-matching:
	pytest tests/test_agent_pattern_matching.py tests/test_agent_selection_edge_cases.py tests/test_agent_integration.py -v

# Run tests with coverage
test-coverage:
	pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# Code linting and formatting
lint-ci:
	ruff check . && black --check . && mypy .

# Pre-commit validation for staged changes
pre-commit-staged:
	pre-commit run --files $(shell git diff --cached --name-only)

# Benchmark agent selection performance
benchmark-agents:
	python scripts/benchmark_agent_selection.py

# === HELP & DOCUMENTATION ===

# Default target shows help
help:
	@echo "DevMem Project Commands:"
	@echo ""
	@echo "Testing & Validation:"
	@echo "  make test                 - Run all tests"
	@echo "  make test-agent-matching  - Run agent pattern matching tests"
	@echo "  make test-coverage        - Run tests with coverage analysis"
	@echo "  make lint-ci              - Code linting and formatting check"
	@echo "  make benchmark-agents     - Benchmark agent selection performance"
	@echo ""
	@echo "System Health & Maintenance:"
	@echo "  make system-health        - Comprehensive system health check"
	@echo "  make system-maintenance   - Full system maintenance (includes memory)"
	@echo "  make validate-system      - Validate system configuration"
	@echo "  make emergency-diagnostics - Collect emergency diagnostic information"
	@echo "  make log-summary          - Show recent log activity"
	@echo "  make security-check       - Check security status"
	@echo ""
	@echo "Memory Maintenance:"
	@echo "  make memory-help          - Show memory maintenance commands"
	@echo "  make memory-status        - Quick memory system status"
	@echo ""
	@echo "Maintenance Guide:"
	@echo "  cat docs/MAINTENANCE.md   - View complete maintenance procedures"
	@echo ""
	@echo "For detailed memory management:"
	@echo "  ./scripts/memory/memory_manager.sh --help"

.DEFAULT_GOAL := help