#!/bin/bash
# CI Modular Test Runner
# Optimized test execution with different modes

set -e

MODE="${1:-fast}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "=� CI Modular Runner - Mode: $MODE"
echo "Project: DevMem Agent Framework"
echo "Directory: $PROJECT_ROOT"
echo ""

case "$MODE" in
    fast)
        echo "� Fast Mode: Core tests only"
        pytest tests/test_agent_selection_validation.py tests/test_claude_code_agent_learning.py -v --tb=short
        ;;
    
    unit)
        echo ">� Unit Tests Mode"
        pytest tests/ -v --tb=short -m "unit or not integration"
        ;;
    
    integration)
        echo "= Integration Tests Mode" 
        pytest tests/ -v --tb=short -m integration
        ;;
    
    performance)
        echo "=� Performance Tests Mode"
        pytest tests/ -v --tb=short -m performance
        ;;
    
    coverage)
        echo "=� Coverage Analysis Mode"
        pytest tests/ --cov=. --cov-report=term-missing --cov-report=html --cov-fail-under=80
        ;;
    
    full)
        echo "<� Full Test Suite"
        pytest tests/ -v --tb=short
        ;;
    
    *)
        echo "L Unknown mode: $MODE"
        echo "Available modes: fast, unit, integration, performance, coverage, full"
        exit 1
        ;;
esac

echo ""
echo " Test execution completed"