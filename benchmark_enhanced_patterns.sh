#!/bin/bash

# Enhanced Pattern Recognition Benchmark Script
# 
# This script runs comprehensive benchmarks for the enhanced pattern recognition system
# and compares performance against targets and current baselines.
#
# Usage:
#   ./benchmark_enhanced_patterns.sh [quick|standard|comprehensive]
#   ./benchmark_enhanced_patterns.sh comparison
#   ./benchmark_enhanced_patterns.sh analyze results/

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="$SCRIPT_DIR/benchmark_results"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Performance targets
TARGET_ACCURACY=0.992     # 99.2%
TARGET_RESPONSE_TIME=0.7  # 0.7s
TARGET_CONTEXT_PRESERVATION=0.995  # 99.5%
TARGET_EDGE_CASE_HANDLING=0.95     # 95%

# Current baseline (for comparison)
CURRENT_ACCURACY=0.97     # 97%
CURRENT_RESPONSE_TIME=1.0 # 1.0s
CURRENT_CONTEXT_PRESERVATION=0.97  # 97%

function print_header() {
    echo -e "${BLUE}===============================================================================${NC}"
    echo -e "${BLUE}Enhanced Pattern Recognition System - Benchmark Suite${NC}"
    echo -e "${BLUE}===============================================================================${NC}"
    echo
}

function print_section() {
    echo -e "${YELLOW}--- $1 ---${NC}"
}

function print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

function print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

function print_error() {
    echo -e "${RED}❌ $1${NC}"
}

function print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

function setup_environment() {
    print_section "Environment Setup"
    
    # Create results directory
    mkdir -p "$RESULTS_DIR"
    
    # Check Python dependencies
    if ! python3 -c "import enhanced_pattern_recognition" 2>/dev/null; then
        print_error "Enhanced pattern recognition module not found"
        print_info "Make sure enhanced_pattern_recognition.py is in the current directory"
        exit 1
    fi
    
    print_success "Environment ready"
    echo
}

function run_quick_benchmark() {
    print_section "Quick Benchmark (1 iteration)"
    
    local output_file="$RESULTS_DIR/quick_benchmark_$TIMESTAMP.json"
    
    print_info "Running quick benchmark with 1 iteration..."
    python3 measure_agent_selection_performance.py \
        --mode benchmark \
        --iterations 1 \
        --output "$output_file" \
        --verbose
    
    print_success "Quick benchmark completed"
    print_info "Results saved to: $output_file"
    echo
}

function run_standard_benchmark() {
    print_section "Standard Benchmark (5 iterations)"
    
    local output_file="$RESULTS_DIR/standard_benchmark_$TIMESTAMP.json"
    
    print_info "Running standard benchmark with 5 iterations..."
    print_info "This may take a few minutes..."
    
    python3 measure_agent_selection_performance.py \
        --mode benchmark \
        --iterations 5 \
        --output "$output_file" \
        --verbose
    
    print_success "Standard benchmark completed"
    print_info "Results saved to: $output_file"
    echo
}

function run_comprehensive_benchmark() {
    print_section "Comprehensive Benchmark (20 iterations)"
    
    local output_file="$RESULTS_DIR/comprehensive_benchmark_$TIMESTAMP.json"
    
    print_info "Running comprehensive benchmark with 20 iterations..."
    print_info "This will take several minutes..."
    
    python3 measure_agent_selection_performance.py \
        --mode benchmark \
        --iterations 20 \
        --output "$output_file" \
        --verbose
    
    print_success "Comprehensive benchmark completed"
    print_info "Results saved to: $output_file"
    echo
}

function run_comparison_benchmark() {
    print_section "Comparison Analysis"
    
    local output_file="$RESULTS_DIR/comparison_benchmark_$TIMESTAMP.json"
    
    print_info "Running comparison benchmark..."
    print_info "This compares enhanced system against baseline targets"
    
    python3 measure_agent_selection_performance.py \
        --mode comparison \
        --iterations 10 \
        --output "$output_file" \
        --verbose
    
    print_success "Comparison benchmark completed"
    print_info "Results saved to: $output_file"
    echo
}

function analyze_results() {
    print_section "Results Analysis"
    
    local results_dir="$1"
    if [ -z "$results_dir" ]; then
        results_dir="$RESULTS_DIR"
    fi
    
    if [ ! -d "$results_dir" ]; then
        print_error "Results directory not found: $results_dir"
        exit 1
    fi
    
    print_info "Analyzing results from: $results_dir"
    
    # Find the most recent results file
    local latest_file
    latest_file=$(find "$results_dir" -name "*.json" -type f -exec ls -t {} + | head -n 1)
    
    if [ -z "$latest_file" ]; then
        print_error "No benchmark results found in $results_dir"
        exit 1
    fi
    
    print_info "Analyzing latest results: $(basename "$latest_file")"
    
    # Extract key metrics using Python
    python3 -c "
import json
import sys

with open('$latest_file', 'r') as f:
    data = json.load(f)

accuracy = data['accuracy_rate']
response_time = data['avg_response_time']
context_preservation = data['context_preservation_rate']
edge_case_handling = data['edge_case_handling']
total_tests = data['total_tests']

print(f'📊 PERFORMANCE SUMMARY:')
print(f'   Total Tests: {total_tests}')
print(f'   Accuracy Rate: {accuracy:.2%}')
print(f'   Avg Response Time: {response_time:.3f}s')
print(f'   Context Preservation: {context_preservation:.2%}')
print(f'   Edge Case Handling: {edge_case_handling:.2%}')
print()

# Target comparison
targets_met = 0
total_targets = 4

print('🎯 TARGET COMPARISON:')
if accuracy >= $TARGET_ACCURACY:
    print('   ✅ Accuracy: EXCEEDS TARGET')
    targets_met += 1
elif accuracy >= $CURRENT_ACCURACY:
    print('   🔶 Accuracy: MEETS CURRENT BASELINE')
else:
    print('   ❌ Accuracy: BELOW BASELINE')

if response_time <= $TARGET_RESPONSE_TIME:
    print('   ✅ Response Time: MEETS TARGET')
    targets_met += 1
elif response_time <= $CURRENT_RESPONSE_TIME:
    print('   🔶 Response Time: MEETS CURRENT BASELINE')
else:
    print('   ❌ Response Time: EXCEEDS ACCEPTABLE LIMIT')

if context_preservation >= $TARGET_CONTEXT_PRESERVATION:
    print('   ✅ Context Preservation: EXCEEDS TARGET')
    targets_met += 1
elif context_preservation >= $CURRENT_CONTEXT_PRESERVATION:
    print('   🔶 Context Preservation: MEETS CURRENT BASELINE')
else:
    print('   ❌ Context Preservation: BELOW BASELINE')

if edge_case_handling >= $TARGET_EDGE_CASE_HANDLING:
    print('   ✅ Edge Case Handling: MEETS TARGET')
    targets_met += 1
elif edge_case_handling >= 0.6:
    print('   🔶 Edge Case Handling: ACCEPTABLE')
else:
    print('   ❌ Edge Case Handling: NEEDS IMPROVEMENT')

print(f'\n📈 TARGETS MET: {targets_met}/{total_targets}')

if targets_met >= 3:
    print('🏆 OVERALL: EXCELLENT - Production Ready')
elif targets_met >= 2:
    print('👍 OVERALL: GOOD - Minor Improvements Recommended')
else:
    print('⚠️  OVERALL: NEEDS WORK - Significant Improvements Required')
"
    
    echo
    print_success "Analysis completed"
    echo
}

function generate_performance_report() {
    print_section "Generating Performance Report"
    
    local report_file="$RESULTS_DIR/performance_summary_$TIMESTAMP.md"
    
    cat > "$report_file" << EOF
# Enhanced Pattern Recognition System - Performance Report

**Generated:** $(date)
**Test Suite:** Enhanced Agent Selection Benchmarks

## Performance Targets

| Metric | Target | Current Baseline | Status |
|--------|--------|------------------|--------|
| Accuracy Rate | 99.2% | 97% | - |
| Response Time | ≤0.7s | ≤1.0s | - |
| Context Preservation | 99.5% | 97% | - |
| Edge Case Handling | 95% | Manual | - |

## Test Results

*Results will be populated after running benchmarks*

## Recommendations

*Recommendations will be generated based on benchmark results*

## Implementation Status

- [x] Enhanced Pattern Recognition System implemented
- [x] Multi-tier pattern matching (Explicit, Context-Aware, Fallback)
- [x] Context enrichment pipeline
- [x] Validation framework
- [x] Adaptive learning system
- [x] Comprehensive benchmark suite

## Next Steps

1. Run comprehensive benchmarks
2. Analyze performance gaps
3. Implement targeted improvements
4. Validate production readiness
EOF

    print_success "Performance report template created: $report_file"
    echo
}

function show_usage() {
    echo "Usage: $0 [command] [options]"
    echo
    echo "Commands:"
    echo "  quick         Run quick benchmark (1 iteration)"
    echo "  standard      Run standard benchmark (5 iterations) [default]"
    echo "  comprehensive Run comprehensive benchmark (20 iterations)"
    echo "  comparison    Run comparison against baseline"
    echo "  analyze [dir] Analyze results from directory"
    echo "  report        Generate performance report template"
    echo "  help          Show this help message"
    echo
    echo "Examples:"
    echo "  $0                    # Run standard benchmark"
    echo "  $0 comprehensive      # Run comprehensive benchmark"
    echo "  $0 analyze results/   # Analyze results from specific directory"
    echo
}

function run_performance_validation() {
    print_section "Performance Validation"
    
    print_info "Running validation checks..."
    
    # Check if system meets minimum requirements
    local validation_output
    validation_output=$(python3 -c "
from enhanced_pattern_recognition import EnhancedPatternRecognitionSystem
import time

# Quick validation test
system = EnhancedPatternRecognitionSystem()

test_cases = [
    'Test failures with async patterns and mock configuration',
    'Docker orchestration problems with service networking',
    'Security vulnerability assessment with compliance validation',
    'Coordinating analysis using 3 tasks in parallel: security, performance, testing'
]

total_time = 0
correct_selections = 0

for test in test_cases:
    start = time.time()
    agent, confidence, details = system.select_agent(test)
    end = time.time()
    
    response_time = end - start
    total_time += response_time
    
    # Basic validation
    if confidence > 0.5 and response_time < 2.0:
        correct_selections += 1

avg_time = total_time / len(test_cases)
accuracy = correct_selections / len(test_cases)

print(f'Quick validation results:')
print(f'Average response time: {avg_time:.3f}s')
print(f'Basic accuracy: {accuracy:.2%}')
print(f'System status: {"READY" if avg_time < 1.5 and accuracy > 0.7 else "NEEDS WORK"}')
" 2>&1)
    
    echo "$validation_output"
    
    if echo "$validation_output" | grep -q "READY"; then
        print_success "System validation passed - ready for benchmarking"
    else
        print_warning "System validation indicates potential issues"
    fi
    
    echo
}

function main() {
    print_header
    
    local command="${1:-standard}"
    shift || true
    
    case "$command" in
        "quick")
            setup_environment
            run_performance_validation
            run_quick_benchmark
            analyze_results
            ;;
        "standard")
            setup_environment
            run_performance_validation
            run_standard_benchmark
            analyze_results
            ;;
        "comprehensive")
            setup_environment
            run_performance_validation
            run_comprehensive_benchmark
            analyze_results
            ;;
        "comparison")
            setup_environment
            run_performance_validation
            run_comparison_benchmark
            analyze_results
            ;;
        "analyze")
            analyze_results "$1"
            ;;
        "report")
            generate_performance_report
            ;;
        "help")
            show_usage
            ;;
        *)
            print_error "Unknown command: $command"
            echo
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
