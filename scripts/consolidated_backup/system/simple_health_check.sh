#\!/bin/bash

# Simplified System Health Check Script
# Purpose: Quick health check for simplified Claude Code Framework

set -euo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'

echo
echo "=== System Health Check ==="
echo "Generated: $(date)"
echo

# Check essential files
score=100
issues=0

echo "Essential Files Check:"

# Check settings.json
if [[ -f "$PROJECT_ROOT/.claude/settings.json" ]]; then
    if python -c "import json; json.load(open('$PROJECT_ROOT/.claude/settings.json'))" 2>/dev/null; then
        echo -e "  ${GREEN}✅ settings.json: Valid${NC}"
    else
        echo -e "  ${RED}❌ settings.json: Invalid JSON${NC}"
        ((issues++))
        ((score -= 30))
    fi
else
    echo -e "  ${RED}❌ settings.json: Missing${NC}"
    ((issues++))
    ((score -= 50))
fi

# Check essential hooks
if [[ -x "$PROJECT_ROOT/scripts/hooks/essential_security.sh" ]]; then
    echo -e "  ${GREEN}✅ Security hook: Present and executable${NC}"
else
    echo -e "  ${RED}❌ Security hook: Missing or not executable${NC}"
    ((issues++))
    ((score -= 25))
fi

if [[ -x "$PROJECT_ROOT/scripts/hooks/essential_quality.sh" ]]; then
    echo -e "  ${GREEN}✅ Quality hook: Present and executable${NC}"
else
    echo -e "  ${RED}❌ Quality hook: Missing or not executable${NC}"
    ((issues++))
    ((score -= 25))
fi

# Check memory directory
if [[ -d "$PROJECT_ROOT/.claude/memory" ]]; then
    file_count=$(find "$PROJECT_ROOT/.claude/memory" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    usage=$(du -sm "$PROJECT_ROOT/.claude/memory" 2>/dev/null | cut -f1 || echo "0")
    echo -e "  ${GREEN}✅ Memory directory: $file_count files, ${usage}MB${NC}"
    
    if [[ $file_count -gt 12 ]]; then
        echo -e "  ${YELLOW}⚠️  Many memory files ($file_count), consider cleanup${NC}"
        ((score -= 10))
    fi
    
    if [[ $usage -gt 3 ]]; then
        echo -e "  ${YELLOW}⚠️  High memory usage (${usage}MB)${NC}"
        ((score -= 15))
    fi
else
    echo -e "  ${RED}❌ Memory directory: Missing${NC}"
    ((issues++))
    ((score -= 20))
fi

echo
echo "=== Overall Health Summary ==="

if [[ $score -ge 90 ]]; then
    echo -e "${GREEN}✅ System Health: EXCELLENT ($score/100)${NC}"
elif [[ $score -ge 75 ]]; then
    echo -e "${YELLOW}🟡 System Health: GOOD ($score/100)${NC}"
elif [[ $score -ge 60 ]]; then
    echo -e "${YELLOW}🟠 System Health: WARNING ($score/100)${NC}"
else
    echo -e "${RED}🔴 System Health: CRITICAL ($score/100)${NC}"
fi

echo "Total Issues: $issues"

if [[ $issues -gt 0 ]]; then
    echo
    echo "Recommended Actions:"
    echo "  • Run: make memory-maintenance"
    echo "  • Check: make log-summary"
    echo "  • Validate: python scripts/validate_native_config.py"
fi

echo

# Exit with appropriate code
if [[ $score -lt 60 ]]; then
    exit 2  # Critical
elif [[ $score -lt 70 ]]; then
    exit 1  # Warning
else
    exit 0  # OK
fi
EOF < /dev/null