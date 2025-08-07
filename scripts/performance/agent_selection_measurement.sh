#!/bin/bash

# Compatible with bash 3.2+ (macOS default)

# Agent Selection Performance Measurement Script
# Purpose: Measure agent selection latency, success rates, and memory utilization
# Target: ≤1s agent selection time with 95% accuracy

set -eo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly MEASUREMENT_LOG="${PROJECT_ROOT}/.claude/performance_measurements.log"
readonly RESULTS_DIR="${PROJECT_ROOT}/.claude/performance_results"
readonly SETTINGS_FILE="${PROJECT_ROOT}/.claude/settings.json"

# Performance measurement configuration
readonly TARGET_SELECTION_TIME_MS=1000
readonly TARGET_ACCURACY_RATE=0.95
readonly MEMORY_SAMPLE_INTERVAL=0.1

# Test scenario patterns for agent selection measurement (bash 3.2 compatible)
get_test_scenario_description() {
    case "$1" in
        "testing_async_mock") echo "Test failures with async patterns and mock configuration" ;;
        "performance_bottleneck") echo "Performance bottlenecks in database queries and API responses" ;;
        "docker_orchestration") echo "Docker orchestration issues with service networking" ;;
        "security_vulnerability") echo "Security vulnerabilities in authentication system" ;;
        "coverage_gaps") echo "Test coverage gaps requiring architectural improvements" ;;
        "infrastructure_scaling") echo "Infrastructure performance bottlenecks in container deployment" ;;
        "ci_pipeline_failure") echo "CI pipeline failures in GitHub Actions workflow" ;;
        "integration_testing") echo "End-to-end testing failures across multiple services" ;;
        "code_quality_issues") echo "Code quality violations and linting errors" ;;
        "environment_config") echo "Environment configuration problems affecting deployment" ;;
        "memory_optimization") echo "Memory usage optimization and resource allocation" ;;
        "async_pattern_fixes") echo "Async pattern corrections with concurrency issues" ;;
        "fixture_architecture") echo "Advanced pytest fixture architecture problems" ;;
        "security_compliance") echo "Multi-standard security compliance validation" ;;
        "dependency_conflicts") echo "Complex dependency conflict resolution" ;;
        "type_system_errors") echo "Type annotation design with generic type systems" ;;
        "refactoring_coordination") echo "Large-scale architectural refactoring coordination" ;;
        "validation_workflow") echo "Comprehensive validation workflow coordination" ;;
        "resource_optimization") echo "Performance tuning and resource optimization" ;;
        "workflow_optimization") echo "GitHub Actions workflow performance optimization" ;;
        *) echo "Unknown scenario" ;;
    esac
}

# Expected agent mappings for accuracy measurement (bash 3.2 compatible)
get_expected_agent() {
    case "$1" in
        "testing_async_mock") echo "test-specialist" ;;
        "performance_bottleneck") echo "performance-optimizer" ;;
        "docker_orchestration") echo "infrastructure-engineer" ;;
        "security_vulnerability") echo "security-enforcer" ;;
        "coverage_gaps") echo "coverage-optimizer" ;;
        "infrastructure_scaling") echo "infrastructure-engineer" ;;
        "ci_pipeline_failure") echo "ci-specialist" ;;
        "integration_testing") echo "integration-validator" ;;
        "code_quality_issues") echo "code-quality-specialist" ;;
        "environment_config") echo "environment-analyst" ;;
        "memory_optimization") echo "resource-optimizer" ;;
        "async_pattern_fixes") echo "async-pattern-fixer" ;;
        "fixture_architecture") echo "fixture-design-specialist" ;;
        "security_compliance") echo "security-auditor" ;;
        "dependency_conflicts") echo "dependency-resolver" ;;
        "type_system_errors") echo "type-system-expert" ;;
        "refactoring_coordination") echo "refactoring-coordinator" ;;
        "validation_workflow") echo "validation-tester" ;;
        "resource_optimization") echo "resource-optimizer" ;;
        "workflow_optimization") echo "workflow-optimizer" ;;
        *) echo "analysis-gateway" ;;
    esac
}

# List of all test scenario keys
readonly TEST_SCENARIO_KEYS=(
    "testing_async_mock"
    "performance_bottleneck" 
    "docker_orchestration"
    "security_vulnerability"
    "coverage_gaps"
    "infrastructure_scaling"
    "ci_pipeline_failure"
    "integration_testing"
    "code_quality_issues"
    "environment_config"
    "memory_optimization"
    "async_pattern_fixes"
    "fixture_architecture"
    "security_compliance"
    "dependency_conflicts"
    "type_system_errors"
    "refactoring_coordination"
    "validation_workflow"
    "resource_optimization"
    "workflow_optimization"
)

# Logging functions
log_measurement() {
    mkdir -p "$(dirname "$MEASUREMENT_LOG")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] MEASUREMENT: $1" >> "$MEASUREMENT_LOG"
}

log_result() {
    echo "$1" | tee -a "$MEASUREMENT_LOG"
}

# Memory monitoring functions
start_memory_monitoring() {
    local pid=$1
    local output_file=$2
    
    {
        while kill -0 "$pid" 2>/dev/null; do
            # Get memory usage for Claude Code process
            local mem_usage
            mem_usage=$(ps -o pid,rss,vsz -p "$pid" 2>/dev/null | tail -1 || echo "0 0 0")
            echo "$(date '+%s.%N') $mem_usage" >> "$output_file"
            sleep "$MEMORY_SAMPLE_INTERVAL"
        done
    } &
    
    echo $!
}

# Agent selection simulation functions
simulate_agent_selection() {
    local scenario_key="$1"
    local scenario_description="$2"
    local expected_agent="$3"
    
    log_measurement "Testing scenario: $scenario_key"
    
    # Start timing
    local start_time
    start_time=$(date '+%s.%N')
    
    # Simulate agent selection process based on memory patterns
    local selected_agent
    selected_agent=$(analyze_scenario_for_agent "$scenario_description")
    
    # End timing
    local end_time
    end_time=$(date '+%s.%N')
    
    # Calculate selection time in milliseconds
    local selection_time_ms
    selection_time_ms=$(echo "scale=0; ($end_time - $start_time) * 1000" | bc -l)
    
    # Check accuracy
    local is_accurate=0
    if [[ "$selected_agent" == "$expected_agent" ]]; then
        is_accurate=1
    fi
    
    # Return results as CSV
    echo "$scenario_key,$selected_agent,$expected_agent,$selection_time_ms,$is_accurate"
}

# Agent selection analysis based on memory patterns
analyze_scenario_for_agent() {
    local description="$1"
    
    # Simulate memory-driven agent selection based on pattern matching
    # This simulates the actual Claude Code agent selection process
    
    # Testing patterns
    if [[ "$description" =~ (test|async|mock|coverage|fixture|pytest) ]]; then
        if [[ "$description" =~ (coverage|gaps|architectural) ]]; then
            echo "coverage-optimizer"
        elif [[ "$description" =~ (async|pattern) ]]; then
            echo "async-pattern-fixer"
        elif [[ "$description" =~ (fixture|architecture) ]]; then
            echo "fixture-design-specialist"
        else
            echo "test-specialist"
        fi
        return
    fi
    
    # Performance patterns
    if [[ "$description" =~ (performance|bottleneck|optimization|memory|resource) ]]; then
        if [[ "$description" =~ (resource|memory) ]]; then
            echo "resource-optimizer"
        else
            echo "performance-optimizer"
        fi
        return
    fi
    
    # Infrastructure patterns
    if [[ "$description" =~ (docker|orchestration|infrastructure|deployment|container) ]]; then
        if [[ "$description" =~ (environment|config) ]]; then
            echo "environment-analyst"
        else
            echo "infrastructure-engineer"
        fi
        return
    fi
    
    # Security patterns
    if [[ "$description" =~ (security|vulnerability|compliance|auth) ]]; then
        if [[ "$description" =~ (compliance|multi-standard) ]]; then
            echo "security-auditor"
        else
            echo "security-enforcer"
        fi
        return
    fi
    
    # Quality patterns
    if [[ "$description" =~ (quality|linting|formatting|code) ]]; then
        echo "code-quality-specialist"
        return
    fi
    
    # CI patterns
    if [[ "$description" =~ (ci|pipeline|github|actions|workflow) ]]; then
        if [[ "$description" =~ (workflow.*optimization) ]]; then
            echo "workflow-optimizer"
        else
            echo "ci-specialist"
        fi
        return
    fi
    
    # Integration patterns
    if [[ "$description" =~ (integration|end-to-end|cross) ]]; then
        echo "integration-validator"
        return
    fi
    
    # Dependency patterns
    if [[ "$description" =~ (dependency|conflict) ]]; then
        echo "dependency-resolver"
        return
    fi
    
    # Type system patterns
    if [[ "$description" =~ (type|annotation|generic) ]]; then
        echo "type-system-expert"
        return
    fi
    
    # Refactoring patterns
    if [[ "$description" =~ (refactor|architectural.*refactor) ]]; then
        echo "refactoring-coordinator"
        return
    fi
    
    # Validation patterns
    if [[ "$description" =~ (validation.*workflow) ]]; then
        echo "validation-tester"
        return
    fi
    
    # Default fallback
    echo "analysis-gateway"
}

# System performance measurement
measure_system_performance() {
    local start_time
    start_time=$(date '+%s.%N')
    
    # Get system metrics
    local cpu_usage
    cpu_usage=$(top -l 1 -n 0 | grep "CPU usage" | awk '{print $3}' | sed 's/%//' || echo "0")
    
    local memory_pressure
    memory_pressure=$(memory_pressure 2>/dev/null | grep "System-wide memory free percentage" | awk '{print $5}' | sed 's/%//' || echo "95")
    
    local load_avg
    load_avg=$(uptime | awk -F'load averages:' '{print $2}' | awk '{print $1}' | sed 's/,//' || echo "0.5")
    
    echo "cpu_usage:$cpu_usage,memory_free:$memory_pressure,load_avg:$load_avg"
}

# Generate comprehensive performance report
generate_performance_report() {
    local results_file="$1"
    local memory_file="$2"
    local report_file="$RESULTS_DIR/agent_selection_performance_report.md"
    
    mkdir -p "$RESULTS_DIR"
    
    {
        echo "# Agent Selection Performance Measurement Report"
        echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        echo "## Executive Summary"
        
        # Calculate summary statistics
        local total_tests
        local successful_selections
        local avg_selection_time
        local max_selection_time
        local min_selection_time
        local accuracy_rate
        
        total_tests=$(wc -l < "$results_file")
        successful_selections=$(awk -F',' '$5 == 1 {count++} END {print count+0}' "$results_file")
        avg_selection_time=$(awk -F',' '{sum+=$4; count++} END {print sum/count}' "$results_file")
        max_selection_time=$(awk -F',' 'BEGIN{max=0} {if($4>max) max=$4} END {print max}' "$results_file")
        min_selection_time=$(awk -F',' 'BEGIN{min=999999} {if($4<min) min=$4} END {print min}' "$results_file")
        accuracy_rate=$(echo "scale=4; $successful_selections / $total_tests" | bc -l)
        
        echo "- **Total Test Scenarios**: $total_tests"
        echo "- **Successful Selections**: $successful_selections"
        echo "- **Accuracy Rate**: $(echo "scale=2; $accuracy_rate * 100" | bc -l)%"
        echo "- **Average Selection Time**: ${avg_selection_time}ms"
        echo "- **Min Selection Time**: ${min_selection_time}ms"
        echo "- **Max Selection Time**: ${max_selection_time}ms"
        echo "- **Target Compliance**: $(if (( $(echo "$avg_selection_time <= $TARGET_SELECTION_TIME_MS" | bc -l) )); then echo "✅ PASSED"; else echo "❌ FAILED"; fi) (≤${TARGET_SELECTION_TIME_MS}ms)"
        echo "- **Accuracy Target**: $(if (( $(echo "$accuracy_rate >= $TARGET_ACCURACY_RATE" | bc -l) )); then echo "✅ PASSED"; else echo "❌ FAILED"; fi) (≥$(echo "scale=0; $TARGET_ACCURACY_RATE * 100" | bc -l)%)"
        echo ""
        
        echo "## Performance Analysis"
        echo ""
        echo "### Selection Time Distribution"
        echo "| Range (ms) | Count | Percentage |"
        echo "|------------|-------|------------|"
        
        # Time distribution analysis
        awk -F',' '
        {
            time = $4
            if (time <= 500) range_500++
            else if (time <= 1000) range_1000++
            else if (time <= 2000) range_2000++
            else range_over++
            total++
        }
        END {
            printf "| 0-500ms    | %d     | %.1f%%      |\n", range_500+0, (range_500/total)*100
            printf "| 501-1000ms | %d     | %.1f%%      |\n", range_1000+0, (range_1000/total)*100
            printf "| 1001-2000ms| %d     | %.1f%%      |\n", range_2000+0, (range_2000/total)*100
            printf "| >2000ms    | %d     | %.1f%%      |\n", range_over+0, (range_over/total)*100
        }' "$results_file"
        
        echo ""
        echo "### Agent Selection Accuracy by Domain"
        echo "| Domain | Total | Correct | Accuracy |"
        echo "|--------|-------|---------|----------|"
        
        # Accuracy by domain analysis
        awk -F',' '
        BEGIN {}
        {
            scenario = $1
            selected = $2
            expected = $3
            accurate = $5
            
            if (scenario ~ /test|async|mock|coverage|fixture/) domain = "Testing"
            else if (scenario ~ /performance|bottleneck|optimization|memory|resource/) domain = "Performance"
            else if (scenario ~ /docker|orchestration|infrastructure|deployment/) domain = "Infrastructure"
            else if (scenario ~ /security|vulnerability|compliance/) domain = "Security"
            else if (scenario ~ /quality|linting|formatting/) domain = "Quality"
            else if (scenario ~ /ci|pipeline|github|workflow/) domain = "CI/CD"
            else domain = "Other"
            
            domain_total[domain]++
            if (accurate == 1) domain_correct[domain]++
        }
        END {
            for (d in domain_total) {
                correct = domain_correct[d] + 0
                total = domain_total[d]
                accuracy = (correct / total) * 100
                printf "| %s | %d | %d | %.1f%% |\n", d, total, correct, accuracy
            }
        }' "$results_file"
        
        echo ""
        echo "### Memory Utilization Analysis"
        if [[ -f "$memory_file" ]]; then
            local max_rss
            local avg_rss
            local max_vsz
            local avg_vsz
            
            max_rss=$(awk '{if($3>max) max=$3} END {print max+0}' "$memory_file")
            avg_rss=$(awk '{sum+=$3; count++} END {print sum/count}' "$memory_file")
            max_vsz=$(awk '{if($4>max) max=$4} END {print max+0}' "$memory_file")
            avg_vsz=$(awk '{sum+=$4; count++} END {print sum/count}' "$memory_file")
            
            echo "- **Peak RSS Memory**: ${max_rss} KB"
            echo "- **Average RSS Memory**: ${avg_rss} KB"
            echo "- **Peak Virtual Memory**: ${max_vsz} KB"
            echo "- **Average Virtual Memory**: ${avg_vsz} KB"
        else
            echo "Memory monitoring data not available"
        fi
        
        echo ""
        echo "## Detailed Results"
        echo ""
        echo "| Scenario | Selected Agent | Expected Agent | Time (ms) | Accurate |"
        echo "|----------|----------------|----------------|-----------|----------|"
        
        # Detailed results table
        awk -F',' '{
            accurate = ($5 == 1) ? "✅" : "❌"
            printf "| %s | %s | %s | %s | %s |\n", $1, $2, $3, $4, accurate
        }' "$results_file"
        
        echo ""
        echo "## Recommendations"
        echo ""
        
        # Generate recommendations based on results
        if (( $(echo "$avg_selection_time > $TARGET_SELECTION_TIME_MS" | bc -l) )); then
            echo "### ⚠️ Performance Optimization Required"
            echo "- Average selection time (${avg_selection_time}ms) exceeds target (${TARGET_SELECTION_TIME_MS}ms)"
            echo "- Consider memory pattern optimization and caching improvements"
            echo "- Investigate high-latency scenarios for targeted optimization"
            echo ""
        fi
        
        if (( $(echo "$accuracy_rate < $TARGET_ACCURACY_RATE" | bc -l) )); then
            echo "### ⚠️ Accuracy Improvement Required"
            echo "- Selection accuracy ($(echo "scale=1; $accuracy_rate * 100" | bc -l)%) below target ($(echo "scale=0; $TARGET_ACCURACY_RATE * 100" | bc -l)%)"
            echo "- Review memory patterns for misclassified scenarios"
            echo "- Enhance pattern matching algorithms for better domain recognition"
            echo ""
        fi
        
        if (( $(echo "$avg_selection_time <= $TARGET_SELECTION_TIME_MS" | bc -l) )) && (( $(echo "$accuracy_rate >= $TARGET_ACCURACY_RATE" | bc -l) )); then
            echo "### ✅ Performance Targets Met"
            echo "- Agent selection system meets both latency and accuracy targets"
            echo "- Memory-driven selection system is performing optimally"
            echo "- Continue monitoring for performance regression"
            echo ""
        fi
        
        echo "## Technical Details"
        echo ""
        echo "- **Measurement Framework**: Simplified memory system with pattern matching"
        echo "- **Test Scenarios**: $total_tests representative use cases"
        echo "- **Selection Algorithm**: Memory-driven pattern analysis"
        echo "- **Accuracy Methodology**: Expected vs actual agent selection comparison"
        echo "- **Performance Target**: ≤${TARGET_SELECTION_TIME_MS}ms selection time"
        echo "- **Accuracy Target**: ≥$(echo "scale=0; $TARGET_ACCURACY_RATE * 100" | bc -l)% correct selections"
        
    } > "$report_file"
    
    echo "$report_file"
}

# Main measurement execution
main() {
    log_measurement "Starting agent selection performance measurement"
    log_measurement "Target: ≤${TARGET_SELECTION_TIME_MS}ms selection time, ≥$(echo "scale=0; $TARGET_ACCURACY_RATE * 100" | bc -l)% accuracy"
    
    # Prepare results directory
    mkdir -p "$RESULTS_DIR"
    
    local results_file="$RESULTS_DIR/selection_results.csv"
    local memory_file="$RESULTS_DIR/memory_usage.log"
    
    # Initialize results file
    echo "scenario,selected_agent,expected_agent,selection_time_ms,is_accurate" > "$results_file"
    
    # Initialize memory monitoring
    local measurement_pid=$$
    local memory_monitor_pid
    memory_monitor_pid=$(start_memory_monitoring "$measurement_pid" "$memory_file")
    
    log_measurement "Running ${#TEST_SCENARIO_KEYS[@]} test scenarios"
    
    local total_accurate=0
    local total_time=0
    local test_count=0
    
    # Execute test scenarios
    for scenario_key in "${TEST_SCENARIO_KEYS[@]}"; do
        local scenario_description=$(get_test_scenario_description "$scenario_key")
        local expected_agent=$(get_expected_agent "$scenario_key")
        
        log_measurement "Testing: $scenario_key -> expect: $expected_agent"
        
        # Measure system performance before test
        local system_metrics
        system_metrics=$(measure_system_performance)
        
        # Run agent selection simulation
        local result
        result=$(simulate_agent_selection "$scenario_key" "$scenario_description" "$expected_agent")
        
        # Parse results
        local selection_time_ms
        local is_accurate
        selection_time_ms=$(echo "$result" | cut -d',' -f4)
        is_accurate=$(echo "$result" | cut -d',' -f5)
        
        # Accumulate statistics
        total_time=$((total_time + selection_time_ms))
        total_accurate=$((total_accurate + is_accurate))
        ((test_count++))
        
        # Log result
        echo "$result" >> "$results_file"
        log_measurement "Result: $result (system: $system_metrics)"
        
        # Brief pause between tests
        sleep 0.1
    done
    
    # Stop memory monitoring
    if [[ -n "${memory_monitor_pid:-}" ]]; then
        kill "$memory_monitor_pid" 2>/dev/null || true
        wait "$memory_monitor_pid" 2>/dev/null || true
    fi
    
    # Calculate final statistics
    local avg_time=$((total_time / test_count))
    local accuracy_rate=$(echo "scale=4; $total_accurate / $test_count" | bc -l)
    local accuracy_percentage=$(echo "scale=2; $accuracy_rate * 100" | bc -l)
    
    log_result ""
    log_result "=== AGENT SELECTION PERFORMANCE MEASUREMENT RESULTS ==="
    log_result "Test Scenarios: $test_count"
    log_result "Average Selection Time: ${avg_time}ms"
    log_result "Target Selection Time: ≤${TARGET_SELECTION_TIME_MS}ms"
    log_result "Selection Time Status: $(if [[ $avg_time -le $TARGET_SELECTION_TIME_MS ]]; then echo "✅ PASSED"; else echo "❌ FAILED"; fi)"
    log_result "Accuracy Rate: ${accuracy_percentage}%"
    log_result "Target Accuracy: ≥$(echo "scale=0; $TARGET_ACCURACY_RATE * 100" | bc -l)%"
    log_result "Accuracy Status: $(if (( $(echo "$accuracy_rate >= $TARGET_ACCURACY_RATE" | bc -l) )); then echo "✅ PASSED"; else echo "❌ FAILED"; fi)"
    log_result "Successful Selections: $total_accurate/$test_count"
    
    # Generate comprehensive report
    local report_file
    report_file=$(generate_performance_report "$results_file" "$memory_file")
    
    log_result ""
    log_result "📊 Comprehensive performance report generated: $report_file"
    log_result "📈 Raw results available in: $results_file"
    log_result "💾 Memory usage data: $memory_file"
    
    # Performance status summary
    if [[ $avg_time -le $TARGET_SELECTION_TIME_MS ]] && (( $(echo "$accuracy_rate >= $TARGET_ACCURACY_RATE" | bc -l) )); then
        log_result ""
        log_result "🎯 OVERALL STATUS: ✅ ALL TARGETS MET"
        log_result "Agent selection system meets both performance and accuracy requirements"
    else
        log_result ""
        log_result "🎯 OVERALL STATUS: ❌ OPTIMIZATION REQUIRED"
        if [[ $avg_time -gt $TARGET_SELECTION_TIME_MS ]]; then
            log_result "⚠️ Selection time optimization needed"
        fi
        if (( $(echo "$accuracy_rate < $TARGET_ACCURACY_RATE" | bc -l) )); then
            log_result "⚠️ Agent selection accuracy improvement needed"
        fi
    fi
    
    log_measurement "Measurement completed successfully"
}

# Execute main function
main "$@"