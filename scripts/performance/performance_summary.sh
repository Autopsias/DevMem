#!/bin/bash

# Performance Measurement Summary Script
# Purpose: Display comprehensive performance measurement results
# Usage: ./scripts/performance/performance_summary.sh

set -eo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly RESULTS_DIR="${PROJECT_ROOT}/.claude/performance_results"

# Display performance summary
main() {
    echo ""
    echo "=============================================================="
    echo "📈 CLAUDE CODE AGENT SELECTION PERFORMANCE SUMMARY"
    echo "=============================================================="
    echo ""
    
    # Check if measurements have been run
    if [[ ! -d "$RESULTS_DIR" ]]; then
        echo "⚠️ No performance measurements found."
        echo "Run: ./scripts/performance/enhanced_agent_measurement.sh"
        echo ""
        return 1
    fi
    
    echo "🎯 TARGET PERFORMANCE CRITERIA:"
    echo "   ⏱️ Selection Time: ≤ 1000ms"
    echo "   🎯 Accuracy Rate: ≥ 95%"
    echo ""
    
    # Display latest enhanced results if available
    if [[ -f "$RESULTS_DIR/enhanced_results.csv" ]]; then
        echo "🚀 LATEST ENHANCED MEASUREMENT RESULTS:"
        
        local total_tests=$(tail -n +2 "$RESULTS_DIR/enhanced_results.csv" | wc -l | tr -d ' ')
        local correct_count=$(awk -F',' 'NR>1 && $5 == "correct" {count++} END {print count+0}' "$RESULTS_DIR/enhanced_results.csv")
        local avg_time=$(awk -F',' 'NR>1 {sum+=$4; count++} END {print (count > 0) ? int(sum/count) : 0}' "$RESULTS_DIR/enhanced_results.csv")
        local accuracy=0
        [[ $total_tests -gt 0 ]] && accuracy=$(( correct_count * 100 / total_tests ))
        
        echo "   📋 Total Test Scenarios: $total_tests"
        echo "   🎯 Selection Accuracy: $accuracy% ($correct_count/$total_tests correct)"
        echo "   ⏱️ Average Selection Time: ${avg_time}ms"
        echo ""
        
        # Performance target status
        echo "📊 PERFORMANCE TARGET STATUS:"
        if [[ $avg_time -le 1000 ]]; then
            echo "   ✅ Speed Target: PASSED (${avg_time}ms ≤ 1000ms)"
        else
            echo "   ❌ Speed Target: FAILED (${avg_time}ms > 1000ms)"
        fi
        
        if [[ $accuracy -ge 95 ]]; then
            echo "   ✅ Accuracy Target: PASSED (${accuracy}% ≥ 95%)"
        else
            echo "   ❌ Accuracy Target: FAILED (${accuracy}% < 95%)"
        fi
        echo ""
        
        # Overall assessment
        echo "🏆 OVERALL SYSTEM STATUS:"
        if [[ $avg_time -le 1000 ]] && [[ $accuracy -ge 95 ]]; then
            echo "   ✅ OPTIMAL: All performance targets met"
            echo "   ✨ System ready for production deployment"
        elif [[ $avg_time -le 1000 ]]; then
            echo "   ⚠️ FAST BUT NEEDS ACCURACY TUNING"
            echo "   🎯 Speed excellent, accuracy needs $(( 95 - accuracy ))% improvement"
        elif [[ $accuracy -ge 95 ]]; then
            echo "   ⚠️ ACCURATE BUT NEEDS SPEED OPTIMIZATION"
            echo "   ⏱️ Accuracy excellent, speed needs $(( avg_time - 1000 ))ms improvement"
        else
            echo "   🚨 COMPREHENSIVE OPTIMIZATION REQUIRED"
            echo "   ⏱️ Speed needs $(( avg_time - 1000 ))ms improvement"
            echo "   🎯 Accuracy needs $(( 95 - accuracy ))% improvement"
        fi
        echo ""
        
        # Domain performance breakdown
        echo "📉 DOMAIN-SPECIFIC PERFORMANCE:"
        echo "   Testing Domain: $(grep -E "(test|async|mock|coverage|fixture|integration|validation)" "$RESULTS_DIR/enhanced_results.csv" | awk -F',' '$5 == "correct" {count++} END {print count+0}') / $(grep -E "(test|async|mock|coverage|fixture|integration|validation)" "$RESULTS_DIR/enhanced_results.csv" | wc -l | tr -d ' ') correct"
        echo "   Performance Domain: $(grep -E "(performance|optimization|memory|resource)" "$RESULTS_DIR/enhanced_results.csv" | awk -F',' '$5 == "correct" {count++} END {print count+0}') / $(grep -E "(performance|optimization|memory|resource)" "$RESULTS_DIR/enhanced_results.csv" | wc -l | tr -d ' ') correct"
        echo "   Infrastructure Domain: $(grep -E "(docker|infrastructure|environment|deployment|container)" "$RESULTS_DIR/enhanced_results.csv" | awk -F',' '$5 == "correct" {count++} END {print count+0}') / $(grep -E "(docker|infrastructure|environment|deployment|container)" "$RESULTS_DIR/enhanced_results.csv" | wc -l | tr -d ' ') correct"
        echo "   Security Domain: $(grep -E "(security|vulnerability|compliance)" "$RESULTS_DIR/enhanced_results.csv" | awk -F',' '$5 == "correct" {count++} END {print count+0}') / $(grep -E "(security|vulnerability|compliance)" "$RESULTS_DIR/enhanced_results.csv" | wc -l | tr -d ' ') correct"
        echo ""
    fi
    
    echo "📁 AVAILABLE REPORTS:"
    
    # List available reports
    if [[ -f "$RESULTS_DIR/comprehensive_measurement_report.md" ]]; then
        echo "   📈 Comprehensive Analysis: $RESULTS_DIR/comprehensive_measurement_report.md"
    fi
    
    if [[ -f "$RESULTS_DIR/enhanced_performance_report.md" ]]; then
        echo "   📉 Enhanced Report: $RESULTS_DIR/enhanced_performance_report.md"
    fi
    
    if [[ -f "$RESULTS_DIR/quick_performance_report.md" ]]; then
        echo "   ⚡ Quick Report: $RESULTS_DIR/quick_performance_report.md"
    fi
    
    echo ""
    echo "📀 RAW DATA FILES:"
    
    # List raw data files
    if [[ -f "$RESULTS_DIR/enhanced_results.csv" ]]; then
        echo "   📊 Enhanced Results: $RESULTS_DIR/enhanced_results.csv"
    fi
    
    if [[ -f "$RESULTS_DIR/quick_results.csv" ]]; then
        echo "   ⚡ Quick Results: $RESULTS_DIR/quick_results.csv"
    fi
    
    if [[ -f "$RESULTS_DIR/memory_usage.log" ]]; then
        echo "   💾 Memory Usage: $RESULTS_DIR/memory_usage.log"
    fi
    
    if [[ -f "$RESULTS_DIR/system_performance.log" ]]; then
        echo "   📆 System Performance: $RESULTS_DIR/system_performance.log"
    fi
    
    echo ""
    echo "🔧 MEASUREMENT COMMANDS:"
    echo "   Run Enhanced Test: ./scripts/performance/enhanced_agent_measurement.sh"
    echo "   Run Quick Test: ./scripts/performance/quick_agent_measurement.sh"
    echo "   View This Summary: ./scripts/performance/performance_summary.sh"
    echo ""
    
    # Memory system status
    echo "💾 MEMORY SYSTEM STATUS:"
    if [[ -f "${PROJECT_ROOT}/.claude/settings.json" ]]; then
        local memory_enabled=$(grep -o '"memory_integration_enabled": true' "${PROJECT_ROOT}/.claude/settings.json" >/dev/null && echo "true" || echo "false")
        echo "   Memory Integration: $(if [[ "$memory_enabled" == "true" ]]; then echo "✅ Enabled"; else echo "❌ Disabled"; fi)"
    fi
    
    if [[ -d "${PROJECT_ROOT}/.claude/memory" ]]; then
        local memory_files=$(find "${PROJECT_ROOT}/.claude/memory" -name "*.md" | wc -l | tr -d ' ')
        echo "   Memory Pattern Files: $memory_files files"
    fi
    
    echo ""
    echo "=============================================================="
    echo ""
}

main "$@"