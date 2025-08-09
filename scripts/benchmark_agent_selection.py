#!/usr/bin/env python3
"""Benchmark script for agent selection performance validation."""

import time
import statistics
from typing import List, Dict
from dataclasses import dataclass
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent_selector import EnhancedAgentSelector
from tests.test_agent_pattern_matching import CurrentPatternMatcher, TestQuery


@dataclass
class BenchmarkResult:
    """Result of benchmarking agent selection."""
    name: str
    accuracy: float
    avg_processing_time_ms: float
    median_processing_time_ms: float
    p95_processing_time_ms: float
    avg_confidence: float
    total_queries: int
    correct_selections: int


class AgentSelectionBenchmark:
    """Comprehensive benchmark for agent selection systems."""
    
    def __init__(self):
        self.test_queries = self._create_comprehensive_test_set()
        self.current_matcher = CurrentPatternMatcher()
        self.enhanced_selector = EnhancedAgentSelector()
    
    def _create_comprehensive_test_set(self) -> List[TestQuery]:
        """Create comprehensive test set for benchmarking."""
        return [
            # Test-specialist queries
            TestQuery("pytest test failing with async mock configuration", "test-specialist", (0.7, 1.0)),
            TestQuery("unit tests not passing coverage requirements", "test-specialist", (0.6, 0.9)),
            TestQuery("integration test fixtures need improvement", "test-specialist", (0.6, 0.9)),
            TestQuery("async test patterns causing race conditions", "test-specialist", (0.7, 1.0)),
            TestQuery("mock configuration breaking test assertions", "test-specialist", (0.7, 1.0)),
            
            # Infrastructure-engineer queries  
            TestQuery("docker orchestration issues with container networking", "infrastructure-engineer", (0.7, 1.0)),
            TestQuery("kubernetes cluster service mesh problems", "infrastructure-engineer", (0.7, 1.0)),
            TestQuery("container scaling and resource allocation", "infrastructure-engineer", (0.7, 1.0)),
            TestQuery("deployment pipeline automation failing", "infrastructure-engineer", (0.6, 0.9)),
            TestQuery("service discovery and load balancing issues", "infrastructure-engineer", (0.6, 0.9)),
            
            # Security-enforcer queries
            TestQuery("security vulnerability scan reveals credential leaks", "security-enforcer", (0.8, 1.0)),
            TestQuery("authentication flow security audit needed", "security-enforcer", (0.7, 1.0)),
            TestQuery("compliance validation for data encryption", "security-enforcer", (0.7, 1.0)),
            TestQuery("OAuth2 token security hardening required", "security-enforcer", (0.7, 1.0)),
            TestQuery("RBAC policy enforcement and validation", "security-enforcer", (0.6, 0.9)),
            
            # Performance-optimizer queries
            TestQuery("performance bottleneck in latency optimization", "performance-optimizer", (0.7, 1.0)),
            TestQuery("memory usage optimization and profiling", "performance-optimizer", (0.7, 1.0)),
            TestQuery("CPU utilization analysis and tuning", "performance-optimizer", (0.7, 1.0)),
            TestQuery("database query performance improvements", "performance-optimizer", (0.6, 0.9)),
            TestQuery("throughput optimization for high load", "performance-optimizer", (0.6, 0.9)),
            
            # Intelligent-enhancer queries
            TestQuery("refactor code with better variable naming", "intelligent-enhancer", (0.6, 1.0)),
            TestQuery("function splitting and architecture improvement", "intelligent-enhancer", (0.7, 1.0)),
            TestQuery("type annotation system enhancement needed", "intelligent-enhancer", (0.6, 0.9)),
            TestQuery("code quality improvements and refactoring", "intelligent-enhancer", (0.6, 0.9)),
            TestQuery("architectural pattern modernization", "intelligent-enhancer", (0.5, 0.8)),
            
            # Code-quality-specialist queries
            TestQuery("lint errors and formatting issues", "code-quality-specialist", (0.6, 0.9)),
            TestQuery("style guide enforcement and validation", "code-quality-specialist", (0.6, 0.9)),
            TestQuery("code standard compliance checking", "code-quality-specialist", (0.5, 0.8)),
            
            # CI-specialist queries
            TestQuery("GitHub Actions workflow optimization", "ci-specialist", (0.6, 0.9)),
            TestQuery("CI pipeline automation and configuration", "ci-specialist", (0.7, 1.0)),
            TestQuery("build automation and deployment pipeline", "ci-specialist", (0.6, 0.9)),
            
            # Edge cases and ambiguous queries
            TestQuery("something is broken with the tests", "test-specialist", (0.4, 0.7)),
            TestQuery("performance and security issues", "performance-optimizer", (0.4, 0.7)),
            TestQuery("help with docker and testing", "infrastructure-engineer", (0.3, 0.6)),
            TestQuery("need to improve code quality", "intelligent-enhancer", (0.4, 0.7)),
            TestQuery("fix the CI pipeline", "ci-specialist", (0.5, 0.8)),
            
            # Natural language variations
            TestQuery("tests are failing", "test-specialist", (0.5, 0.8)),
            TestQuery("container won't start", "infrastructure-engineer", (0.4, 0.7)),
            TestQuery("app is not secure", "security-enforcer", (0.4, 0.7)),
            TestQuery("system is slow", "performance-optimizer", (0.4, 0.7)),
            TestQuery("code needs cleanup", "intelligent-enhancer", (0.4, 0.7)),
        ]
    
    def benchmark_matcher(self, matcher, name: str) -> BenchmarkResult:
        """Benchmark a specific matcher implementation."""
        correct_selections = 0
        processing_times = []
        confidence_scores = []
        
        for test_query in self.test_queries:
            # Time the selection
            start_time = time.perf_counter()
            
            if hasattr(matcher, 'select_agent'):
                result = matcher.select_agent(test_query.query)
            else:
                result = matcher.match_agent(test_query.query)
            
            processing_time = (time.perf_counter() - start_time) * 1000
            processing_times.append(processing_time)
            
            # Check accuracy
            if result.agent_name == test_query.expected_agent:
                correct_selections += 1
            
            # Collect confidence scores
            confidence_scores.append(result.confidence_score)
        
        total_queries = len(self.test_queries)
        accuracy = correct_selections / total_queries
        avg_processing_time = statistics.mean(processing_times)
        median_processing_time = statistics.median(processing_times)
        p95_processing_time = sorted(processing_times)[int(0.95 * len(processing_times))]
        avg_confidence = statistics.mean(confidence_scores)
        
        return BenchmarkResult(
            name=name,
            accuracy=accuracy,
            avg_processing_time_ms=avg_processing_time,
            median_processing_time_ms=median_processing_time,
            p95_processing_time_ms=p95_processing_time,
            avg_confidence=avg_confidence,
            total_queries=total_queries,
            correct_selections=correct_selections
        )
    
    def run_load_test(self, matcher, num_queries: int = 1000) -> Dict[str, float]:
        """Run load test with repeated queries."""
        queries = [tq.query for tq in self.test_queries] * (num_queries // len(self.test_queries) + 1)
        queries = queries[:num_queries]
        
        start_time = time.perf_counter()
        results = []
        
        for query in queries:
            if hasattr(matcher, 'select_agent'):
                result = matcher.select_agent(query)
            else:
                result = matcher.match_agent(query)
            results.append(result)
        
        total_time = (time.perf_counter() - start_time) * 1000
        
        return {
            'total_time_ms': total_time,
            'avg_time_per_query_ms': total_time / num_queries,
            'queries_per_second': num_queries / (total_time / 1000),
            'total_queries': num_queries
        }
    
    def run_comprehensive_benchmark(self) -> Dict[str, BenchmarkResult]:
        """Run comprehensive benchmark comparing all implementations."""
        print("Running comprehensive agent selection benchmark...\n")
        
        results = {}
        
        # Benchmark current matcher
        print("Benchmarking current pattern matcher...")
        current_result = self.benchmark_matcher(self.current_matcher, "Current Matcher")
        results['current'] = current_result
        
        # Benchmark enhanced selector
        print("Benchmarking enhanced agent selector...")
        enhanced_result = self.benchmark_matcher(self.enhanced_selector, "Enhanced Selector")
        results['enhanced'] = enhanced_result
        
        return results
    
    def print_benchmark_results(self, results: Dict[str, BenchmarkResult]):
        """Print formatted benchmark results."""
        print("\n" + "="*80)
        print("AGENT SELECTION BENCHMARK RESULTS")
        print("="*80)
        
        for name, result in results.items():
            print(f"\n{result.name}:")
            print(f"  Accuracy:          {result.accuracy:.2%} ({result.correct_selections}/{result.total_queries})")
            print(f"  Avg Confidence:    {result.avg_confidence:.3f}")
            print(f"  Avg Time:          {result.avg_processing_time_ms:.2f}ms")
            print(f"  Median Time:       {result.median_processing_time_ms:.2f}ms")
            print(f"  P95 Time:          {result.p95_processing_time_ms:.2f}ms")
        
        # Print comparison if we have both results
        if 'current' in results and 'enhanced' in results:
            current = results['current']
            enhanced = results['enhanced']
            
            accuracy_improvement = (enhanced.accuracy - current.accuracy) / current.accuracy * 100
            time_change = (enhanced.avg_processing_time_ms - current.avg_processing_time_ms) / current.avg_processing_time_ms * 100
            confidence_improvement = (enhanced.avg_confidence - current.avg_confidence) / current.avg_confidence * 100
            
            print("\nIMPROVEMENT ANALYSIS:")
            print(f"  Accuracy:          {accuracy_improvement:+.1f}%")
            print(f"  Confidence:        {confidence_improvement:+.1f}%")
            print(f"  Processing Time:   {time_change:+.1f}%")
            
            # Determine overall result
            if accuracy_improvement > 15 and confidence_improvement > 10:
                print("  Overall Result:    🎉 SIGNIFICANT IMPROVEMENT")
            elif accuracy_improvement > 5 and confidence_improvement > 5:
                print("  Overall Result:    ✅ IMPROVEMENT")
            elif accuracy_improvement > 0:
                print("  Overall Result:    📈 MINOR IMPROVEMENT")
            else:
                print("  Overall Result:    ⚠️  NO SIGNIFICANT IMPROVEMENT")
    
    def run_load_test_comparison(self):
        """Run and compare load test performance."""
        print("\nRunning load test comparison...")
        
        current_load = self.run_load_test(self.current_matcher, 1000)
        enhanced_load = self.run_load_test(self.enhanced_selector, 1000)
        
        print("\nLOAD TEST RESULTS (1000 queries):")
        print("Current Matcher:")
        print(f"  Total Time:        {current_load['total_time_ms']:.1f}ms")
        print(f"  Avg per Query:     {current_load['avg_time_per_query_ms']:.2f}ms")
        print(f"  Queries/Second:    {current_load['queries_per_second']:.1f}")
        
        print("\nEnhanced Selector:")
        print(f"  Total Time:        {enhanced_load['total_time_ms']:.1f}ms")
        print(f"  Avg per Query:     {enhanced_load['avg_time_per_query_ms']:.2f}ms")
        print(f"  Queries/Second:    {enhanced_load['queries_per_second']:.1f}")
        
        throughput_improvement = (enhanced_load['queries_per_second'] - current_load['queries_per_second']) / current_load['queries_per_second'] * 100
        print(f"\nThroughput Change:   {throughput_improvement:+.1f}%")


def main():
    """Main benchmark execution."""
    benchmark = AgentSelectionBenchmark()
    
    # Run comprehensive benchmark
    results = benchmark.run_comprehensive_benchmark()
    benchmark.print_benchmark_results(results)
    
    # Run load test comparison
    benchmark.run_load_test_comparison()
    
    print("\n" + "="*80)
    print("BENCHMARK COMPLETE")
    print("="*80)
    
    # Return exit code based on results
    if 'enhanced' in results:
        enhanced = results['enhanced']
        if enhanced.accuracy >= 0.80 and enhanced.avg_processing_time_ms < 3.0:
            print("✅ Enhanced agent selector meets performance requirements")
            return 0
        else:
            print("❌ Enhanced agent selector does not meet performance requirements")
            return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
