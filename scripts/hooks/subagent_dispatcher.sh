#!/bin/bash

# Sub-Agent Dispatcher for Claude Code
# Purpose: Intelligently dispatch to appropriate sub-agents based on context
# Usage: subagent_dispatcher.sh <subagent_name> [file_path] [operation_type]

set -euo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly SUBAGENT_DIR="${PROJECT_ROOT}/.claude/agents"
readonly SECONDARY_SUBAGENT_DIR="${PROJECT_ROOT}/.claude/agents/secondary"
readonly AGENT_REGISTRY="${PROJECT_ROOT}/.claude/agents/registry.json"
readonly TOKEN_MONITOR_FILE="${PROJECT_ROOT}/.claude/token_usage.json"
readonly LOG_FILE="${PROJECT_ROOT}/.claude/subagent_dispatch.log"

# Logging function
log_dispatch() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SUBAGENT_DISPATCH: $1" >> "$LOG_FILE"
}

# Context budget monitoring
check_context_budget() {
    local operation_type="$1"
    local max_context_kb="${CONTEXT_BUDGET_KB:-50}"  # Default 50KB budget

    # Calculate current context usage (approximate)
    local current_usage=0
    if [[ -f "$AGENT_REGISTRY" ]]; then
        current_usage=$(wc -c < "$AGENT_REGISTRY" 2>/dev/null | awk '{print int($1/1024)}')
    fi

    # Allow higher budget for critical operations
    if [[ "$operation_type" == "security" ]]; then
        max_context_kb=$((max_context_kb * 2))
    fi

    if [[ $current_usage -gt $max_context_kb ]]; then
        log_dispatch "Context budget exceeded: ${current_usage}KB > ${max_context_kb}KB"
        return 1
    fi

    return 0
}

# Registry-based agent discovery (lightweight)
discover_all_agents() {
    if [[ ! -f "$AGENT_REGISTRY" ]]; then
        log_dispatch "ERROR: Agent registry not found at $AGENT_REGISTRY - falling back to file system scan"
        discover_all_agents_fallback
        return
    fi

    if ! command -v jq &> /dev/null; then
        log_dispatch "ERROR: jq not available - falling back to file system scan"
        discover_all_agents_fallback
        return
    fi

    # Extract agent names from registry (lightweight operation)
    jq -r '.primary_agents[].name | "primary:" + ., .secondary_agents[].name | "secondary:" + .' "$AGENT_REGISTRY" 2>/dev/null || {
        log_dispatch "ERROR: Failed to parse agent registry - falling back to file system scan"
        discover_all_agents_fallback
    }
}

# Fallback to file system discovery if registry unavailable
discover_all_agents_fallback() {
    local agents=()

    # Primary agents
    for agent_file in "${SUBAGENT_DIR}"/*.md; do
        if [[ -f "$agent_file" && ! "$agent_file" =~ /secondary/ ]]; then
            local agent_name=$(basename "$agent_file" .md)
            agents+=("primary:$agent_name")
        fi
    done

    # Secondary agents
    for agent_file in "${SECONDARY_SUBAGENT_DIR}"/*.md; do
        if [[ -f "$agent_file" ]]; then
            local agent_name=$(basename "$agent_file" .md)
            agents+=("secondary:$agent_name")
        fi
    done

    printf '%s\n' "${agents[@]}"
}

# Find agent file path (registry-assisted)
find_agent_path() {
    local agent_name="$1"

    # Try registry lookup first for faster resolution
    if [[ -f "$AGENT_REGISTRY" ]] && command -v jq &> /dev/null; then
        local registry_file=$(jq -r --arg name "$agent_name" '
            (.primary_agents[] | select(.name == $name) | .file),
            (.secondary_agents[] | select(.name == $name) | .file)
        ' "$AGENT_REGISTRY" 2>/dev/null | head -1)

        if [[ -n "$registry_file" && "$registry_file" != "null" ]]; then
            local full_path="${SUBAGENT_DIR}/${registry_file}"
            if [[ -f "$full_path" ]]; then
                echo "$full_path"
                return 0
            fi
        fi
    fi

    # Fallback to file system lookup
    local primary_path="${SUBAGENT_DIR}/${agent_name}.md"
    local secondary_path="${SECONDARY_SUBAGENT_DIR}/${agent_name}.md"

    if [[ -f "$primary_path" ]]; then
        echo "$primary_path"
        return 0
    elif [[ -f "$secondary_path" ]]; then
        echo "$secondary_path"
        return 0
    else
        return 1
    fi
}

# Extract agent type from path/metadata
get_agent_type() {
    local agent_path="$1"

    if [[ "$agent_path" =~ /secondary/ ]]; then
        echo "secondary"
    else
        echo "primary"
    fi
}

# Check if agent can spawn secondary agents (UltraThink capability)
can_spawn_secondary() {
    local agent_path="$1"

    # Only primary agents can spawn secondary agents
    if [[ "$(get_agent_type "$agent_path")" == "primary" ]]; then
        # Check if agent has UltraThink integration
        if grep -q "UltraThink" "$agent_path" 2>/dev/null; then
            return 0
        fi
    fi

    return 1
}

# Check token availability before dispatching
check_token_availability() {
    local operation_priority="$1"

    # Read current token usage if file exists
    if [[ -f "$TOKEN_MONITOR_FILE" ]]; then
        local usage_percent=$(jq -r '.usage_percentage // 0' "$TOKEN_MONITOR_FILE" 2>/dev/null || echo "0")

        # Apply circuit breaker logic
        if (( $(echo "$usage_percent >= 95" | bc -l) )); then
            echo "BLOCKED"
            return 1
        elif (( $(echo "$usage_percent >= 85" | bc -l) )); then
            [[ "$operation_priority" == "HIGH" ]] && echo "ALLOWED" || echo "BLOCKED"
        elif (( $(echo "$usage_percent >= 70" | bc -l) )); then
            [[ "$operation_priority" =~ ^(HIGH|MEDIUM)$ ]] && echo "ALLOWED" || echo "BLOCKED"
        else
            echo "ALLOWED"
        fi
    else
        # If no token monitoring file, assume available
        echo "ALLOWED"
    fi
}

# Determine operation priority based on context
determine_operation_priority() {
    local file_path="$1"
    local operation_type="$2"

    # High priority operations
    if [[ "$operation_type" == "security" ]]; then
        echo "HIGH"
        return
    fi

    if [[ -f "$file_path" ]]; then
        local file_size=$(wc -l < "$file_path" 2>/dev/null || echo "0")

        # File length violations are high priority
        if [[ "$file_path" =~ \.py$ && $file_size -gt 750 ]]; then
            echo "HIGH"
            return
        elif [[ "$file_path" =~ test_.*\.py$ && $file_size -gt 1000 ]]; then
            echo "HIGH"
            return
        elif [[ "$file_path" =~ __init__\.py$ && $file_size -gt 50 ]]; then
            echo "HIGH"
            return
        fi
    fi

    # Medium priority for code quality issues
    if [[ "$operation_type" =~ ^(quality|formatting)$ ]]; then
        echo "MEDIUM"
        return
    fi

    # Default to low priority
    echo "LOW"
}

# Execute sub-agent with Claude Code
execute_subagent() {
    local subagent_name="$1"
    local file_path="${2:-}"
    local operation_type="${3:-quality}"
    local parent_agent="${4:-}"  # For hierarchical spawning

    # Find agent path using discovery function
    local subagent_path
    if ! subagent_path=$(find_agent_path "$subagent_name"); then
        log_dispatch "ERROR: Sub-agent not found: $subagent_name - falling back to standard tools"
        execute_enhanced_fallback "$file_path" "$operation_type" "$subagent_name"
        return 0  # Return success for fallback mode
    fi

    local agent_type=$(get_agent_type "$subagent_path")
    log_dispatch "Found $agent_type agent: $subagent_name at $subagent_path"

    # Determine operation priority
    local priority=$(determine_operation_priority "$file_path" "$operation_type")
    log_dispatch "Operation priority: $priority for $file_path ($operation_type)"

    # Check context budget before loading agent
    if ! check_context_budget "$operation_type"; then
        log_dispatch "BLOCKED: Context budget exceeded, using enhanced fallback mode"
        execute_enhanced_fallback "$file_path" "$operation_type" "$subagent_name"
        return $?
    fi

    # Check token availability
    local token_status=$(check_token_availability "$priority")
    if [[ "$token_status" == "BLOCKED" ]]; then
        log_dispatch "BLOCKED: Token limit reached, falling back to standard tools"
        execute_standard_tools_fallback "$file_path" "$operation_type"
        return $?
    fi

    # Update token usage tracking
    update_token_usage_tracking "$subagent_name" "start"

    # Execute sub-agent via Claude Code Task tool
    log_dispatch "Executing sub-agent: $subagent_name for $file_path"

    # Create temporary prompt for sub-agent with hierarchical spawning support
    local temp_prompt="/tmp/subagent_prompt_$$"
    cat > "$temp_prompt" << EOF
Using the sub-agent instructions from $subagent_path, process the file: $file_path

Agent Context:
- Agent Type: $agent_type
- Agent Name: $subagent_name
- Parent Agent: ${parent_agent:-"None (direct invocation)"}
- Operation Type: $operation_type
- Priority Level: $priority
- Token Status: $token_status

Available Agent Ecosystem:
$(discover_all_agents | sed 's/^/- /')

Hierarchical Spawning Rules:
- Primary agents can spawn secondary agents for complex analysis using UltraThink triggers
- Secondary agents cannot spawn other agents (terminal nodes)
- Use Task tool with secondary agent name for complex issues requiring specialized analysis

Please follow the sub-agent's guidelines for:
1. User transparency - explain all changes clearly
2. Token efficiency - use batching and caching where possible
3. Quality enforcement - apply the specified standards
4. Error handling - provide clear feedback on any issues
5. Hierarchical coordination - spawn secondary agents for complex patterns when appropriate

Focus on the most critical issues first based on the priority level.
EOF

    # Execute sub-agent directly without Claude CLI recursion
    log_dispatch "Executing sub-agent via direct approach: $subagent_name"

    # Get agent description from registry (lightweight) or fallback to file
    local agent_description=""
    if [[ -f "$AGENT_REGISTRY" ]] && command -v jq &> /dev/null; then
        agent_description=$(jq -r --arg name "$subagent_name" '
            (.primary_agents[] | select(.name == $name) | .description),
            (.secondary_agents[] | select(.name == $name) | .description)
        ' "$AGENT_REGISTRY" 2>/dev/null | head -1)
    fi

    # Fallback to reading file header if registry lookup fails
    if [[ -z "$agent_description" || "$agent_description" == "null" ]]; then
        agent_description=$(head -10 "$subagent_path" 2>/dev/null | grep "^description:" | cut -d':' -f2- | sed 's/^ *//' || echo "Agent description unavailable")
    fi

    log_dispatch "Sub-agent metadata loaded for $subagent_name"

    # Create lightweight feedback for the user (no full file loading)
    echo "🤖 Sub-Agent Activated: $subagent_name ($agent_type)"
    echo "  📝 Target: $file_path"
    echo "  🔧 Operation: $operation_type"
    echo "  ⚡ Priority: $priority"
    echo ""
    echo "📋 Agent Purpose:"
    if [[ ${#agent_description} -gt 200 ]]; then
        echo "  ${agent_description:0:200}..."
    else
        echo "  $agent_description"
    fi
    echo ""
    echo "🎯 Recommendations from $subagent_name:"

    # Execute agent-specific analysis via enhanced fallback
    execute_enhanced_fallback "$file_path" "$operation_type" "$subagent_name"

    # Show additional agent-specific guidance
    if [[ "$subagent_name" == "ci-specialist" ]]; then
        echo ""
        echo "🔧 CI-Specialist Quick Actions:"
        echo "  • Check workflow syntax: yamllint .github/workflows/ci-modular.yml"
        echo "  • Test locally: ./scripts/ci-modular-runner.sh fast"
        echo "  • Trigger workflow: gh workflow run ci-modular.yml -f test_scope=fast"
        echo "  • View recent runs: gh run list --limit=5"
    fi

    log_dispatch "SUCCESS: Sub-agent $subagent_name completed successfully"
    update_token_usage_tracking "$subagent_name" "success"
    rm -f "$temp_prompt"
    return 0
}

# Enhanced fallback when Claude/sub-agents unavailable
execute_enhanced_fallback() {
    local file_path="$1"
    local operation_type="$2"
    local subagent_name="$3"

    log_dispatch "Enhanced fallback execution for $subagent_name: $file_path ($operation_type)"

    echo "🤖 Sub-Agent Fallback: $subagent_name (Enhanced Mode)"
    echo "  📝 Target: $file_path"
    echo "  🔧 Operation: $operation_type"
    echo "  ⚡ Mode: Enhanced tools fallback"
    echo ""

    # Agent-specific fallback logic
    case "$subagent_name" in
        "test-specialist")
            echo "🧪 Test Specialist Fallback: Running standard test analysis..."
            if [[ -d "tests" ]]; then
                echo "  📊 Test files found: $(find tests -name "*.py" | wc -l) files"
                if command -v pytest &> /dev/null; then
                    echo "  🔍 Running quick test validation..."
                    pytest tests/ --collect-only 2>/dev/null | grep "collected" || echo "  ⚠️ Test collection issues detected"
                fi
            fi
            echo "  💡 Recommended: Run 'make test-coverage' for full analysis"
            ;;
        "ci-specialist")
            echo "⚙️ CI Specialist Fallback: Running standard CI analysis..."
            if [[ -f ".github/workflows/ci-modular.yml" ]]; then
                echo "  ✅ Primary CI workflow found"
                if command -v yamllint &> /dev/null; then
                    yamllint .github/workflows/ci-modular.yml 2>/dev/null && echo "  ✅ Workflow syntax valid" || echo "  ❌ YAML syntax issues"
                fi
            fi
            echo "  💡 Recommended: Run './scripts/ci-modular-runner.sh fast' for local CI test"
            ;;
        "code-quality-specialist")
            echo "🔍 Code Quality Fallback: Running standard quality checks..."
            if command -v ruff &> /dev/null; then
                echo "  🔧 Running ruff check..."
                ruff check "$file_path" 2>&1 | head -5 || echo "  ✅ No ruff issues found"
            fi
            if command -v black &> /dev/null; then
                echo "  ⚫ Running black check..."
                black --check "$file_path" 2>&1 | head -3 || echo "  ✅ Code formatting correct"
            fi
            echo "  💡 Recommended: Run 'make lint-ci' for full quality check"
            ;;
        "security-enforcer")
            echo "🛡️ Security Fallback: Running basic security validation..."
            if [[ -f "$file_path" ]]; then
                echo "  🔍 Checking for common security patterns..."
                if grep -i "password\|secret\|token" "$file_path" | grep -v "test" | head -3; then
                    echo "  ⚠️ Potential secrets detected - review needed"
                else
                    echo "  ✅ No obvious secrets detected"
                fi
            fi
            echo "  💡 Recommended: Manual security review of sensitive operations"
            ;;
        "security-auditor")
            echo "🔍 Security Auditor Fallback: Deep vulnerability analysis and remediation..."
            if [[ -f "$file_path" ]]; then
                echo "  🛡️ Comprehensive security vulnerability scan:"

                # 1. Hardcoded secrets detection
                echo "  🔐 Analyzing hardcoded credentials..."
                secret_count=$(grep -i "password\s*=\|api_key\s*=\|secret\s*=\|token\s*=" "$file_path" | wc -l | tr -d ' \n\r\t')
                if [[ $secret_count -gt 0 ]]; then
                    echo "    ❌ Found $secret_count hardcoded credentials (HIGH SEVERITY)"
                    grep -n -i "password\s*=\|api_key\s*=\|secret\s*=\|token\s*=" "$file_path" | head -3
                else
                    echo "    ✅ No hardcoded credentials detected"
                fi

                # 2. SQL injection vulnerability analysis
                echo "  💉 Analyzing SQL injection vulnerabilities..."
                sql_injection_count=$(grep -c "f\".*SELECT\|f\".*INSERT\|f\".*UPDATE\|f\".*DELETE\|%.*SELECT\|%.*INSERT" "$file_path" 2>/dev/null | tr -d ' \n\r\t' || echo "0")
                if [[ $sql_injection_count -gt 0 ]]; then
                    echo "    ❌ Found $sql_injection_count potential SQL injection vulnerabilities (CRITICAL)"
                    grep -n "f\".*SELECT\|f\".*INSERT\|f\".*UPDATE\|f\".*DELETE\|%.*SELECT\|%.*INSERT" "$file_path" | head -3
                else
                    echo "    ✅ No SQL injection patterns detected"
                fi

                # 3. Command injection analysis
                echo "  ⚡ Analyzing command injection vulnerabilities..."
                cmd_injection_count=$(grep -c "subprocess.*shell=True\|os\.system\|os\.popen" "$file_path" 2>/dev/null | tr -d ' \n\r\t' || echo "0")
                if [[ $cmd_injection_count -gt 0 ]]; then
                    echo "    ❌ Found $cmd_injection_count potential command injection vulnerabilities (CRITICAL)"
                    grep -n "subprocess.*shell=True\|os\.system\|os\.popen" "$file_path" | head -3
                else
                    echo "    ✅ No command injection patterns detected"
                fi

                # 4. XSS vulnerability analysis
                echo "  🌐 Analyzing XSS vulnerabilities..."
                xss_count=$(grep -c "f\"<.*{.*}\|return.*<.*{" "$file_path" 2>/dev/null | tr -d ' \n\r\t' || echo "0")
                if [[ $xss_count -gt 0 ]]; then
                    echo "    ❌ Found $xss_count potential XSS vulnerabilities (HIGH SEVERITY)"
                    grep -n "f\"<.*{.*}\|return.*<.*{" "$file_path" | head -3
                else
                    echo "    ✅ No XSS patterns detected"
                fi

                # 5. Insecure cryptographic practices
                echo "  🔒 Analyzing cryptographic security..."
                weak_crypto_count=$(grep -c "hashlib\.md5\|hashlib\.sha1\|random\.randint\|random\.choice" "$file_path" 2>/dev/null | tr -d ' \n\r\t' || echo "0")
                if [[ $weak_crypto_count -gt 0 ]]; then
                    echo "    ⚠️ Found $weak_crypto_count weak cryptographic practices (MEDIUM SEVERITY)"
                    grep -n "hashlib\.md5\|hashlib\.sha1\|random\.randint\|random\.choice" "$file_path" | head -3
                else
                    echo "    ✅ No weak cryptographic patterns detected"
                fi

                # 6. Path traversal vulnerabilities
                echo "  📁 Analyzing path traversal vulnerabilities..."
                path_traversal_count=$(grep -c "open.*f\".*{" "$file_path" 2>/dev/null | tr -d ' \n\r\t' || echo "0")
                if [[ $path_traversal_count -gt 0 ]]; then
                    echo "    ❌ Found $path_traversal_count potential path traversal vulnerabilities (HIGH SEVERITY)"
                    grep -n "open.*f\".*{" "$file_path" | head -3
                else
                    echo "    ✅ No path traversal patterns detected"
                fi

                # 7. Insecure deserialization
                echo "  📦 Analyzing deserialization vulnerabilities..."
                deserial_count=$(grep -c "pickle\.loads\|yaml\.load\|json\.loads.*user" "$file_path" 2>/dev/null | tr -d ' \n\r\t' || echo "0")
                if [[ $deserial_count -gt 0 ]]; then
                    echo "    ❌ Found $deserial_count potential deserialization vulnerabilities (CRITICAL)"
                    grep -n "pickle\.loads\|yaml\.load\|json\.loads.*user" "$file_path" | head -3
                else
                    echo "    ✅ No insecure deserialization patterns detected"
                fi

                # 8. Information disclosure in error handling
                echo "  📝 Analyzing information disclosure risks..."
                info_disclosure_count=$(grep -c "print.*password\|print.*secret\|print.*Exception\|raise.*Expected:" "$file_path" 2>/dev/null | tr -d ' \n\r\t' || echo "0")
                if [[ $info_disclosure_count -gt 0 ]]; then
                    echo "    ⚠️ Found $info_disclosure_count potential information disclosure issues (MEDIUM SEVERITY)"
                    grep -n "print.*password\|print.*secret\|print.*Exception\|raise.*Expected:" "$file_path" | head -3
                else
                    echo "    ✅ No information disclosure patterns detected"
                fi

                # Overall security score calculation
                total_critical=$(( sql_injection_count + cmd_injection_count + deserial_count ))
                total_high=$(( secret_count + xss_count + path_traversal_count ))
                total_medium=$(( weak_crypto_count + info_disclosure_count ))
                total_issues=$(( total_critical + total_high + total_medium ))

                echo ""
                echo "  📊 Security Assessment Summary:"
                echo "    🔴 Critical issues: $total_critical (SQL injection, command injection, deserialization)"
                echo "    🟠 High severity: $total_high (secrets, XSS, path traversal)"
                echo "    🟡 Medium severity: $total_medium (weak crypto, info disclosure)"
                echo "    📈 Total security issues: $total_issues"

                if [[ $total_critical -gt 0 ]]; then
                    echo "    🚨 SECURITY ALERT: Critical vulnerabilities require immediate remediation"
                elif [[ $total_high -gt 0 ]]; then
                    echo "    ⚠️ High-priority security issues need attention"
                elif [[ $total_medium -gt 0 ]]; then
                    echo "    💡 Some security improvements recommended"
                else
                    echo "    ✅ No major security issues detected"
                fi
            fi

            echo "  🛡️ Security Auditor Recommendations:"
            echo "    • Use parameterized queries to prevent SQL injection"
            echo "    • Store secrets in environment variables or secure vaults"
            echo "    • Validate and sanitize all user inputs"
            echo "    • Use secure random generators for tokens (secrets module)"
            echo "    • Implement proper error handling without information disclosure"
            echo "    • Use strong cryptographic algorithms (SHA-256+, bcrypt)"
            echo "    • Validate file paths to prevent directory traversal"
            echo "    • Escape user content before rendering in HTML"
            echo "  💡 Next steps: Consider using bandit for automated security scanning"
            ;;
        "docker-specialist")
            echo "🐳 Docker Specialist Fallback: Running container orchestration analysis..."

            # Check Docker daemon status
            if command -v docker &> /dev/null; then
                echo "  🔍 Docker daemon status:"
                if docker info &> /dev/null; then
                    echo "    ✅ Docker daemon running"

                    # Container status check
                    echo "  📊 Container status:"
                    docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "    ⚠️ Could not retrieve container status"

                    # Network analysis
                    echo "  🌐 Network configuration:"
                    docker network ls --format "table {{.Name}}\t{{.Driver}}\t{{.Scope}}" 2>/dev/null || echo "    ⚠️ Could not retrieve network info"

                    # Resource usage
                    echo "  ⚡ Resource usage:"
                    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null | head -5 || echo "    ⚠️ Could not retrieve resource stats"

                    # Health check validation
                    if [[ -f "$file_path" && "$file_path" =~ docker-compose ]]; then
                        echo "  🏥 Docker Compose health checks:"
                        if grep -q "healthcheck:" "$file_path"; then
                            echo "    ✅ Health checks configured"
                            grep -A 5 "healthcheck:" "$file_path" | head -10
                        else
                            echo "    ⚠️ No health checks found in compose file"
                        fi
                    fi

                    # Service connectivity test
                    echo "  🔗 Service connectivity:"
                    local containers=$(docker ps --format "{{.Names}}" 2>/dev/null)
                    if [[ -n "$containers" ]]; then
                        echo "$containers" | while read -r container; do
                            if docker exec "$container" ping -c 1 google.com &> /dev/null; then
                                echo "    ✅ $container: Internet connectivity OK"
                            else
                                echo "    ⚠️ $container: Network connectivity issues"
                            fi
                        done
                    fi
                else
                    echo "    ❌ Docker daemon not accessible"
                fi
            else
                echo "  ❌ Docker not installed or not in PATH"
            fi

            echo "  💡 Recommended Docker troubleshooting:"
            echo "    • Check logs: docker logs <container_name>"
            echo "    • Inspect network: docker network inspect <network_name>"
            echo "    • Test connectivity: docker exec <container> ping <target>"
            echo "    • Resource monitoring: docker stats"
            echo "    • Compose validation: docker-compose config"
            ;;
        "resource-optimizer")
            echo "⚡ Resource Optimizer Fallback: Running performance and memory analysis..."
            if [[ -f "$file_path" ]]; then
                echo "  📊 File analysis: $(wc -l < "$file_path" 2>/dev/null || echo "0") lines"

                # Performance-specific analysis
                if [[ "$file_path" =~ \.py$ ]]; then
                    echo "  🐍 Python file analysis:"

                    # Check for async patterns
                    async_count=$(grep -c "async def\|await\|asyncio" "$file_path" 2>/dev/null || echo "0")
                    if [[ $async_count -gt 0 ]]; then
                        echo "    ⚡ Found $async_count async operations - potential concurrency optimization"
                    fi

                    # Check for loops and iterations
                    loop_count=$(grep -c "for \|while \|\.map(\|\.filter(" "$file_path" 2>/dev/null || echo "0")
                    if [[ $loop_count -gt 5 ]]; then
                        echo "    🔄 Found $loop_count loops/iterations - consider vectorization"
                    fi

                    # Check for database/API calls
                    db_calls=$(grep -c "\.execute(\|\.query(\|\.search(\|\.fetch(" "$file_path" 2>/dev/null || echo "0")
                    if [[ "$db_calls" -gt 0 ]]; then
                        echo "    🗄️ Found $db_calls database operations - consider connection pooling"
                    fi

                    # Check for memory-intensive operations
                    memory_ops=$(grep -c "\.load(\|\.read(\|\.process(\|pd\.DataFrame\|np\.array" "$file_path" 2>/dev/null || echo "0")
                    if [[ "$memory_ops" -gt 0 ]]; then
                        echo "    💾 Found $memory_ops memory operations - consider streaming/chunking"
                    fi
                fi

                # JSON performance data analysis
                if [[ "$file_path" =~ \.json$ && "$file_path" =~ performance|baseline ]]; then
                    echo "  📈 Performance baseline analysis:"
                    if command -v jq &> /dev/null; then
                        # Analyze performance metrics
                        high_variance=$(jq -r 'to_entries[] | select(.value.std_deviation > (.value.mean_value * 0.3)) | .key' "$file_path" 2>/dev/null || echo "")
                        if [[ -n "$high_variance" ]]; then
                            echo "    ⚠️ High variance tests: $high_variance"
                        fi

                        slow_tests=$(jq -r 'to_entries[] | select(.value.mean_value > 1.0) | .key' "$file_path" 2>/dev/null || echo "")
                        if [[ -n "$slow_tests" ]]; then
                            echo "    🐌 Slow operations (>1s): $slow_tests"
                        fi
                    fi
                fi
            fi

            echo "  💡 Resource Optimization Recommendations:"
            echo "    • Profile with cProfile or py-spy for CPU bottlenecks"
            echo "    • Use memory_profiler for memory usage analysis"
            echo "    • Consider async/await for I/O-bound operations"
            echo "    • Implement connection pooling for database operations"
            echo "    • Use streaming for large data processing"
            echo "    • Monitor resource usage with system tools"
            ;;
        "coverage-optimizer")
            echo "📊 Coverage Optimizer Fallback: Running standard coverage analysis without external dependencies..."
            if [[ -f "coverage.lcov" ]]; then
                echo "  ✅ Coverage report found: coverage.lcov"
                # Extract coverage percentage if available
                if command -v lcov &> /dev/null; then
                    lcov --summary coverage.lcov 2>/dev/null | grep "lines" | head -1 || echo "  📊 Coverage data available"
                fi
            fi
            if [[ -d "tests" ]]; then
                echo "  📁 Test directory found: $(find tests -name "*.py" | wc -l) test files"
                if [[ -f "$file_path" ]]; then
                    # Quick analysis without external tools to avoid hanging
                    test_files=$(find tests -name "*$(basename "$file_path" .py)*" | wc -l)
                    echo "  🎯 Related test files: $test_files"
                fi
            fi
            echo "  💡 Coverage Optimization Recommendations:"
            echo "    • Run 'make test-coverage' for comprehensive coverage analysis"
            echo "    • Add edge case tests for conditional branches"
            echo "    • Implement integration tests for cross-module functionality"
            echo "    • Use pytest-cov for detailed coverage reporting"
            echo "    • Consider property-based testing with hypothesis"
            ;;
        *)
            echo "🤖 Generic Fallback: Basic analysis for $subagent_name..."
            if [[ -f "$file_path" ]]; then
                echo "  📄 File exists: $(wc -l < "$file_path" 2>/dev/null || echo "0") lines"
                echo "  🔍 File type: $(file "$file_path" 2>/dev/null | cut -d: -f2 || echo "unknown")"
            fi
            echo "  💡 Recommended: Manual review required for specific analysis"
            ;;
    esac

    echo ""
    echo "🔄 Fallback Mode: Limited functionality - consider upgrading Claude CLI integration"
    return 0
}

# Legacy fallback (kept for compatibility)
execute_standard_tools_fallback() {
    local file_path="$1"
    local operation_type="$2"

    execute_enhanced_fallback "$file_path" "$operation_type" "generic"
}

# Update token usage tracking
update_token_usage_tracking() {
    local subagent_name="$1"
    local status="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # Create or update token usage file
    local temp_file="/tmp/token_update_$$"

    if [[ -f "$TOKEN_MONITOR_FILE" ]]; then
        cp "$TOKEN_MONITOR_FILE" "$temp_file"
    else
        echo '{"usage_percentage": 0, "operations": []}' > "$temp_file"
    fi

    # Add operation record
    jq --arg agent "$subagent_name" --arg status "$status" --arg time "$timestamp" \
       '.operations += [{agent: $agent, status: $status, timestamp: $time}] |
        .operations = (.operations | sort_by(.timestamp) | .[-50:])' \
       "$temp_file" > "$TOKEN_MONITOR_FILE"

    rm -f "$temp_file"
}

# Secondary agent spawning function (called by primary agents)
spawn_secondary_agent() {
    local secondary_agent_name="$1"
    local file_path="$2"
    local operation_type="$3"
    local parent_agent="$4"

    log_dispatch "Secondary agent spawn requested: $secondary_agent_name by $parent_agent"

    # Validate parent agent can spawn secondary agents
    local parent_path
    if ! parent_path=$(find_agent_path "$parent_agent"); then
        log_dispatch "ERROR: Parent agent not found: $parent_agent"
        return 1
    fi

    if ! can_spawn_secondary "$parent_path"; then
        log_dispatch "ERROR: Parent agent $parent_agent cannot spawn secondary agents"
        return 1
    fi

    # Execute secondary agent with parent context
    execute_subagent "$secondary_agent_name" "$file_path" "$operation_type" "$parent_agent"
}

# Main execution
main() {
    local subagent_name="${1:-}"
    local file_path="${2:-}"
    local operation_type="${3:-quality}"

    # Note: Task hook invocation is handled in the hook invocation section below
    # Removed early exit to allow proper agent detection

    # Handle dry-run for testing
    if [[ "$file_path" == "--dry-run" || "$operation_type" == "--dry-run" ]]; then
        local subagent_path
        if subagent_path=$(find_agent_path "$subagent_name"); then
            local agent_type=$(get_agent_type "$subagent_path")
            echo "✅ Agent found: $subagent_name ($agent_type) at $subagent_path"
            return 0
        else
            echo "❌ Agent not found: $subagent_name"
            return 1
        fi
    fi

    # Handle hook invocation without arguments (PostToolUse:Task hook)
    if [[ -z "$subagent_name" ]]; then
        # Check if this is a hook invocation (common in Claude Code)
        if [[ -n "${CLAUDE_TOOL_NAME:-}" ]] || [[ -n "${TOOL_NAME:-}" ]] || [[ "$0" =~ hook ]]; then
            # Hook context - extract agent from environment or task parameters
            local task_description="${CLAUDE_TOOL_PARAMETER_description:-}"
            local task_prompt="${CLAUDE_TOOL_PARAMETER_prompt:-}"
            local detected_agent=""

            # Try to extract agent name from task parameters
            if [[ -n "$task_description" ]]; then
                log_dispatch "Analyzing task description for agent patterns: '$task_description'"
                # Check for SLASH COMMAND patterns first (highest priority)
                if [[ "$task_description" =~ /testing:cifix|cifix ]]; then
                    detected_agent="ci-specialist"
                elif [[ "$task_description" =~ /testing:testfix|testfix ]]; then
                    detected_agent="test-specialist"
                elif [[ "$task_description" =~ /testing:precommitfix|precommitfix ]]; then
                    detected_agent="code-quality-specialist"
                elif [[ "$task_description" =~ /digdeep|digdeep ]]; then
                    detected_agent="digdeep"
                elif [[ "$task_description" =~ /coordinate-testing|coordinate.*testing ]]; then
                    detected_agent="test-specialist"
                elif [[ "$task_description" =~ /coordinate-framework|coordinate.*framework ]]; then
                    detected_agent="framework-coordinator"
                elif [[ "$task_description" =~ /quality-coordination|quality.*coordination ]]; then
                    detected_agent="code-quality-specialist"
                elif [[ "$task_description" =~ /find-agent|find.*agent ]]; then
                    detected_agent="agent-reviewer"
                elif [[ "$task_description" =~ /review-agents|review.*agents ]]; then
                    detected_agent="agent-reviewer"
                elif [[ "$task_description" =~ /create-agent|create.*agent ]]; then
                    detected_agent="agent-creator"
                elif [[ "$task_description" =~ /deep-analysis|deep.*analysis ]]; then
                    detected_agent="digdeep"
                elif [[ "$task_description" =~ /commit ]]; then
                    detected_agent="git-commit-assistant"

                # Check for PRIMARY agent patterns (natural language - case insensitive)
                # Order matters: specific patterns first, then general ones
                elif echo "$task_description" | grep -qi -E "test.*fail|fix.*test|test.*broken|test.*coverage|async.*test|mock.*config|pytest|unittest|tests.*failing|one.*failure.*test|failure.*local.*test"; then
                    detected_agent="test-specialist"
                elif echo "$task_description" | grep -qi -E "fix.*ci|github.*actions|pipeline.*fail|deployment.*problem|workflow.*trouble|ci.*pipeline"; then
                    detected_agent="ci-specialist"
                elif echo "$task_description" | grep -qi -E "digdeep|why.*broken|what.*wrong|analyze.*issue|investigate.*problem|root.*cause|system.*failure|debug|troubleshoot"; then
                    detected_agent="digdeep"
                elif echo "$task_description" | grep -qi -E "code.*quality|security.*check|code.*review|security.*scan|check.*vulnerabilities|linting.*error|security.*analysis"; then
                    detected_agent="code-quality-specialist"
                elif echo "$task_description" | grep -qi -E "infrastructure|docker|container|deployment.*architecture|service.*networking"; then
                    detected_agent="infrastructure-engineer"
                elif echo "$task_description" | grep -qi -E "agent.*review|agent.*health|review.*agents"; then
                    detected_agent="agent-reviewer"

                # Check for SECONDARY agent patterns (case-insensitive)
                elif echo "$task_description" | grep -qi -E "async.*pattern|async.*fix|concurrency.*bug|asyncio.*issue|async.*optimization"; then
                    detected_agent="async-pattern-fixer"
                elif echo "$task_description" | grep -qi -E "docker.*help|container.*start|docker.*compose|container.*networking|docker.*performance|containerization"; then
                    detected_agent="docker-specialist"
                elif echo "$task_description" | grep -qi -E "security.*audit|vulnerability.*analysis|threat.*modeling|security.*assessment|compliance.*validation"; then
                    detected_agent="security-auditor"
                elif echo "$task_description" | grep -qi -E "optimize.*performance|speed.*up.*code|performance.*bottleneck|slow.*performance|scalability.*issue"; then
                    detected_agent="performance-optimizer"
                elif echo "$task_description" | grep -qi -E "improve.*coverage|coverage.*gap|test.*coverage.*analysis|coverage.*optimization|missing.*test"; then
                    detected_agent="coverage-optimizer"
                elif echo "$task_description" | grep -qi -E "type.*hint|type.*annotation|type.*checking|mypy.*error|generic.*type"; then
                    detected_agent="type-system-expert"
                elif echo "$task_description" | grep -qi -E "mock.*configuration|test.*mocking|mock.*setup|mock.*behavior|testing.*mock"; then
                    detected_agent="mock-configuration-expert"
                elif echo "$task_description" | grep -qi -E "validation.*testing|qa.*validation|quality.*assurance|validation.*workflow|test.*validation"; then
                    detected_agent="validation-tester"
                elif echo "$task_description" | grep -qi -E "fix.*linting.*error|systematic.*code.*style|cross.*module.*style|architectural.*compliance|code.*formatting"; then
                    detected_agent="linting-engineer"
                elif echo "$task_description" | grep -qi -E "optimize.*resource.*usage|memory.*optimization|cpu.*efficiency|resource.*allocation.*problem|system.*resource.*tuning"; then
                    detected_agent="resource-optimizer"
                elif echo "$task_description" | grep -qi -E "environment.*problem|deployment.*sync|ci.*environment.*issue|local.*vs.*production|environment.*alignment"; then
                    detected_agent="environment-synchronizer"
                elif echo "$task_description" | grep -qi -E "analyze.*design.*pattern|architectural.*consistency.*problem|sdk.*compliance.*violation|pattern.*validation.*issue|design.*pattern.*migration"; then
                    detected_agent="pattern-analyzer"
                elif echo "$task_description" | grep -qi -E "refactor.*code|restructure.*project|architectural.*refactoring|code.*organization|module.*restructuring"; then
                    detected_agent="refactoring-coordinator"
                elif echo "$task_description" | grep -qi -E "dependency.*conflict|import.*error|package.*version.*problem|dependency.*hell|circular.*dependenc"; then
                    detected_agent="dependency-resolver"
                elif echo "$task_description" | grep -qi -E "fixture.*problem|test.*fixture|pytest.*setup|test.*configuration|fixture.*design"; then
                    detected_agent="fixture-design-specialist"
                elif echo "$task_description" | grep -qi -E "integration.*test|end.*to.*end.*testing|system.*integration|workflow.*validation|cross.*system.*testing"; then
                    detected_agent="integration-validator"
                elif echo "$task_description" | grep -qi -E "config.*problem|environment.*sync|configuration.*validation|config.*drift|configuration.*management"; then
                    detected_agent="configuration-validator"
                elif echo "$task_description" | grep -qi -E "optimize.*workflow|github.*actions.*optimization|workflow.*performance|ci.*optimization|pipeline.*optimization"; then
                    detected_agent="workflow-optimizer"
                elif echo "$task_description" | grep -qi -E "file.*too.*large|split.*large.*file|file.*size.*limit|file.*length.*violation|refactor.*oversized.*file"; then
                    detected_agent="file-size-enforcer"
                fi
            fi

            # If no agent detected from description, check task prompt
            if [[ -z "$detected_agent" && -n "$task_prompt" ]]; then
                log_dispatch "Analyzing task prompt for agent patterns: '$task_prompt'"
                # Check for SLASH COMMAND patterns in task prompt
                if [[ "$task_prompt" =~ /testing:cifix|cifix ]]; then
                    detected_agent="ci-specialist"
                elif [[ "$task_prompt" =~ /testing:testfix|testfix ]]; then
                    detected_agent="test-specialist"
                elif [[ "$task_prompt" =~ /testing:precommitfix|precommitfix ]]; then
                    detected_agent="code-quality-specialist"
                elif [[ "$task_prompt" =~ /digdeep|digdeep ]]; then
                    detected_agent="digdeep"
                elif [[ "$task_prompt" =~ /coordinate-testing|coordinate.*testing ]]; then
                    detected_agent="test-specialist"
                elif [[ "$task_prompt" =~ /coordinate-framework|coordinate.*framework ]]; then
                    detected_agent="framework-coordinator"
                elif [[ "$task_prompt" =~ /quality-coordination|quality.*coordination ]]; then
                    detected_agent="code-quality-specialist"
                elif [[ "$task_prompt" =~ /find-agent|find.*agent ]]; then
                    detected_agent="agent-reviewer"
                elif [[ "$task_prompt" =~ /review-agents|review.*agents ]]; then
                    detected_agent="agent-reviewer"
                elif [[ "$task_prompt" =~ /create-agent|create.*agent ]]; then
                    detected_agent="agent-creator"
                elif [[ "$task_prompt" =~ /deep-analysis|deep.*analysis ]]; then
                    detected_agent="digdeep"
                elif [[ "$task_prompt" =~ /commit ]]; then
                    detected_agent="git-commit-assistant"

                # Check for PRIMARY agent patterns in task prompt (natural language - case insensitive)
                # Order matters: specific patterns first, then general ones
                elif echo "$task_prompt" | grep -qi -E "test.*fail|fix.*test|test.*broken|test.*coverage|async.*test|mock.*config|pytest|unittest|tests.*failing|one.*failure.*test|failure.*local.*test"; then
                    detected_agent="test-specialist"
                elif echo "$task_prompt" | grep -qi -E "fix.*ci|github.*actions|pipeline.*fail|deployment.*problem|workflow.*trouble|ci.*pipeline"; then
                    detected_agent="ci-specialist"
                elif echo "$task_prompt" | grep -qi -E "digdeep|why.*broken|what.*wrong|analyze.*issue|investigate.*problem|root.*cause|system.*failure|debug|troubleshoot"; then
                    detected_agent="digdeep"
                elif echo "$task_prompt" | grep -qi -E "code.*quality|security.*check|code.*review|security.*scan|check.*vulnerabilities|linting.*error|security.*analysis"; then
                    detected_agent="code-quality-specialist"
                elif echo "$task_prompt" | grep -qi -E "infrastructure|docker|container|deployment.*architecture|service.*networking"; then
                    detected_agent="infrastructure-engineer"
                elif echo "$task_prompt" | grep -qi -E "agent.*review|agent.*health|review.*agents"; then
                    detected_agent="agent-reviewer"
                fi

                if [[ -n "$detected_agent" ]]; then
                    log_dispatch "Hook invocation detected agent: $detected_agent from task prompt"
                fi
            fi

            if [[ -n "$detected_agent" ]]; then
                log_dispatch "Hook invocation detected agent: $detected_agent from task parameters"
                subagent_name="$detected_agent"
                file_path="${file_path:-hook_context}"
                operation_type="${operation_type:-hook_operation}"
            else
                # No agent detected - graceful exit for hook context
                log_dispatch "Hook invocation without detectable agent pattern - graceful exit"
                log_dispatch "Task description: '$task_description'"
                log_dispatch "Task prompt: '$task_prompt'"
                log_dispatch "Environment variables: CLAUDE_TOOL_NAME=${CLAUDE_TOOL_NAME:-none}"
                echo "🤖 Agent system monitoring: Task completed without agent specialization needed"
                echo "  📝 Task description: ${task_description:0:100}${task_description:100:+...}"
                echo "  📝 Task prompt: ${task_prompt:0:100}${task_prompt:100:+...}"
                exit 0
            fi
        else
            # Direct CLI usage - show help and exit with error
            echo "Usage: $0 <subagent_name> [file_path] [operation_type]"
            echo ""
            echo "Available Sub-Agents:"
            echo ""
            echo "PRIMARY AGENTS:"
            discover_all_agents | grep "^primary:" | sed 's/primary:/  - /' | sort
            echo ""
            echo "SECONDARY AGENTS:"
            discover_all_agents | grep "^secondary:" | sed 's/secondary:/  - /' | sort
            echo ""
            echo "Usage Examples:"
            echo "  $0 code-quality-specialist /path/to/file.py quality"
            echo "  $0 digdeep /path/to/problem.md analysis"
            echo "  $0 test-specialist /path/to/test.py testing"
            echo ""
            echo "Hook Integration: Automatically triggered by Claude Code Task operations"
            exit 1
        fi
    fi

    # Ensure log directory exists
    mkdir -p "$(dirname "$LOG_FILE")"
    touch "$LOG_FILE"

    # Ensure token monitor file directory exists
    mkdir -p "$(dirname "$TOKEN_MONITOR_FILE")"

    log_dispatch "Starting sub-agent dispatch: $subagent_name for $file_path ($operation_type)"

    # Execute the sub-agent
    log_dispatch "Attempting to execute sub-agent: $subagent_name"
    if execute_subagent "$subagent_name" "$file_path" "$operation_type"; then
        log_dispatch "Sub-agent dispatch completed successfully - exit 0"
        exit 0
    else
        # Handle failure based on context and operation type
        local exit_code=0  # Default to success for fallback mode

        # Determine if this should be a blocking failure
        if [[ -n "${SUBAGENT_QUALITY_CONTEXT:-}" ]]; then
            # Called by quality enforcer - check if this should block
            if [[ "$operation_type" == "security" && "$subagent_name" == "security-enforcer" ]]; then
                log_dispatch "Security validation failed in quality enforcer context - blocking with exit 1"
                exit_code=1  # Block security violations in quality context
            else
                log_dispatch "Non-security agent failed in quality enforcer context - non-blocking"
                exit_code=0  # Non-blocking for other quality checks
            fi
        elif [[ -n "${CLAUDE_TOOL_NAME:-}" && "$CLAUDE_TOOL_NAME" == "Task" ]]; then
            log_dispatch "Sub-agent dispatch failed in Task hook context - using fallback mode with exit 0"
            exit_code=0  # Never block Task tool operations
        else
            log_dispatch "Sub-agent dispatch failed in direct context - using exit 1"
            exit_code=1  # Return error for direct CLI usage
        fi

        log_dispatch "Sub-agent dispatch failed - Context: Hook=${CLAUDE_TOOL_NAME:-none}, Quality=${SUBAGENT_QUALITY_CONTEXT:-none}, Agent=$subagent_name, ExitCode=$exit_code"

        # Add stderr output for non-zero exit codes to clarify PostToolUse warnings
        if [[ $exit_code -eq 1 ]]; then
            echo "Sub-agent dispatch failed: Agent=$subagent_name, Context=Hook:${CLAUDE_TOOL_NAME:-none}/Quality:${SUBAGENT_QUALITY_CONTEXT:-none}, Operation=$operation_type" >&2
        fi

        exit $exit_code
    fi
}

# Run main function
main "$@"
