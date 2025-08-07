#!/bin/bash

# Simple health check script for validating essential infrastructure functionality

echo "=== DevMem Infrastructure Health Check ==="
echo "Checking critical system components..."

# Check memory files
MEMORY_DIR=".claude/memory"
echo -n "Memory System: "
if [ -f "${MEMORY_DIR}/coordination-hub.md" ] && [ -f "${MEMORY_DIR}/domain-intelligence.md" ]; then
    echo "✅ OK (2-file structure verified)"
else
    echo "❌ ERROR (Missing core memory files)"
    exit 1
fi

# Check agent files
AGENTS_DIR=".claude/agents"
echo -n "Agent System: "
if [ -d "$AGENTS_DIR" ]; then
    AGENT_COUNT=$(ls -1 ${AGENTS_DIR}/*.md 2>/dev/null | wc -l)
    if [ $AGENT_COUNT -ge 20 ]; then
        echo "✅ OK ($AGENT_COUNT agents found)"
    else
        echo "⚠️  WARNING (Only $AGENT_COUNT agents found, expected 20+)"
    fi
else
    echo "❌ ERROR (Agents directory not found)"
    exit 1
fi

# Check config file
CONFIG_FILE=".claude/settings.json"
echo -n "Configuration: "
if [ -f "$CONFIG_FILE" ]; then
    echo "✅ OK"
else
    echo "❌ ERROR (settings.json not found)"
    exit 1
fi

# Run essential tests
echo -n "Essential Tests: "
if pytest tests/test_epic4_result_integration.py -v --tb=short &> test_output.log; then
    echo "✅ OK"
else
    echo "❌ ERROR (test failures)"
    echo "Test failures:"
    cat test_output.log
    rm test_output.log
    exit 1
fi

# Cleanup
rm -f test_output.log

echo "=== Health Check Complete ==="