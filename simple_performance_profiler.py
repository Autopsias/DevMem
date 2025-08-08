#!/usr/bin/env python3
"""
Simple Agent Selection Performance Profiler

Lightweight profiler for agent selection system using only standard library.
Analyzes response times, patterns, and identifies optimization opportunities.
"""

import time
import gc
import sys
import tracemalloc
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import json
import statistics
from pathlib import Path

# Import the agent selector to profile
try:
    from src.agent_selector import EnhancedAgentSelector, get_agent_selector
except ImportError:
    print("Warning: Could not import agent selector, using mock implementation")
    
    class MockResult:
        def __init__(self):
            self.agent_name = "test-specialist"
            self.confidence_score = 0.8
            self.matched_patterns = []
            self.processing_time_ms = 10.0
            self.context_keywords = []
            self.reasoning = "Mock selection"
    
    class MockAgentSelector:
        def __init__(self):
            self.agents = {}
            self.keyword_index = {}
            self.pattern_cache = {}
            self.selection_history = []
            
        def select_agent(self, query: str, context=None):
            time.sleep(0.005)  # Simulate processing time
            return MockResult()
            
        def get_selection_stats(self):
            return {
                'total_selections': 100,
                'agent_distribution': {'test-specialist': 30, 'infrastructure-engineer': 25},
                'average_confidence': 0.8,
                'average_processing_time_ms': 10.0
            }
    
    EnhancedAgentSelector = MockAgentSelector
    def get_agent_selector():
        return MockAgentSelector()

@dataclass
class PerformanceMetrics:
    """Performance metrics for a single operation"""
    execution_time_ms: float
    agent_selected: str
    confidence: float
    input_length: int
    query_type: str = "unknown"
    
@dataclass
class ProfileSummary:
    """Summary of profiling results"""
    total_operations: int
    avg_execution_time: float
    min_execution_time: float
    max_execution_time: float
    percentile_95_time: float
    percentile_99_time: float
    throughput_ops_per_sec: float
    agent_distribution: Dict[str, int]
    query_type_performance: Dict[str, Dict[str, float]]
    memory_analysis: Dict[str, Any]
    bottlenecks: List[str]
    optimization_opportunities: List[str]
    recommendations: List[str]

class SimplePerformanceProfiler:
    """Lightweight profiler using only standard library"""
    
    def __init__(self):
        self.selector = get_agent_selector()
        self.metrics = []
        
    def create_diverse_queries(self) -> List[Tuple[str, str]]:
        """Create diverse test queries with different complexity levels"""
        return [
            # Simple queries
            ("test", "simple"),
            ("docker", "simple"),
            ("security", "simple"),
            ("help", "simple"),
            
            # Medium complexity
            ("Test failures with pytest async patterns", "medium"),
            ("Docker container orchestration issues", "medium"),
            ("Security vulnerability assessment needed", "medium"),
            ("Performance bottlenecks in production", "medium"),
            ("Code quality improvements required", "medium"),
            
            # High complexity
            ("Complex system-wide performance degradation affecting multiple services with security implications", "complex"),
            ("Multi-domain analysis required for infrastructure, testing, and security coordination", "complex"),
            ("Comprehensive architectural refactoring with performance implications and security concerns", "complex"),
            
            # Edge cases
            ("?", "edge"),
            ("", "edge"),
            ("A" * 500, "edge"),  # Very long query
            ("🚀 Docker 🐳 testing 🧪 security 🔒", "edge"),  # Emojis
            
            # Technical specifics
            ("Pytest async mock fixture configuration with coverage analysis", "technical"),
            ("Kubernetes service mesh networking with Istio configuration", "technical"),
            ("OAuth2 JWT token validation with RBAC authorization patterns", "technical"),
            
            # Real-world scenarios
            ("Production incident: API gateway returning 503 errors", "production"),
            ("CI/CD pipeline failing at test stage with timeout errors", "production"),
            ("Memory leak detected in containerized microservice", "production"),
            ("Security scan flagged vulnerabilities in dependencies", "production")
        ]
    
    def measure_single_operation(self, query: str, query_type: str) -> PerformanceMetrics:
        """Measure performance of single agent selection"""
        start_time = time.perf_counter()
        
        # Execute agent selection
        result = self.selector.select_agent(query)
        
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000  # Convert to ms
        
        return PerformanceMetrics(
            execution_time_ms=execution_time,
            agent_selected=result.agent_name,
            confidence=result.confidence_score,
            input_length=len(query),
            query_type=query_type
        )
    
    def memory_usage_analysis(self, queries: List[Tuple[str, str]], iterations: int = 5) -> Dict[str, Any]:
        """Analyze memory usage patterns"""
        tracemalloc.start()
        
        # Baseline measurement
        baseline = tracemalloc.take_snapshot()
        
        # Execute operations
        for _ in range(iterations):
            for query, query_type in queries:
                self.selector.select_agent(query)
        
        # Final measurement
        final = tracemalloc.take_snapshot()
        
        # Analyze differences
        top_stats = final.compare_to(baseline, 'lineno')[:10]
        
        total_memory_diff = sum(stat.size_diff for stat in top_stats)
        
        tracemalloc.stop()
        
        return {
            'total_memory_growth_bytes': total_memory_diff,
            'total_memory_growth_mb': total_memory_diff / 1024 / 1024,
            'top_memory_consumers': [
                {
                    'location': f"{stat.traceback.format()[0] if stat.traceback.format() else 'unknown'}",
                    'size_diff_bytes': stat.size_diff,
                    'count_diff': stat.count_diff
                }
                for stat in top_stats[:5]
            ]
        }
    
    def run_performance_analysis(self, iterations: int = 200) -> ProfileSummary:
        """Run comprehensive performance analysis"""
        print(f"Starting performance analysis with {iterations} iterations...")
        
        queries = self.create_diverse_queries()
        all_metrics = []
        
        # Warm up the system
        print("Warming up...")
        for query, query_type in queries[:5]:
            self.selector.select_agent(query)
        
        # Clear any cached data
        gc.collect()
        
        print("Collecting performance metrics...")
        start_time = time.time()
        
        # Collect metrics
        for i in range(iterations):
            for query, query_type in queries:
                metrics = self.measure_single_operation(query, query_type)
                all_metrics.append(metrics)
            
            if (i + 1) % 50 == 0:
                print(f"Completed {i + 1}/{iterations} iterations")
        
        total_runtime = time.time() - start_time
        
        print("Analyzing memory usage...")
        # Memory analysis
        memory_analysis = self.memory_usage_analysis(queries, iterations=10)
        
        print("Generating analysis report...")
        # Analyze results
        execution_times = [m.execution_time_ms for m in all_metrics]
        
        # Agent distribution
        agent_distribution = {}
        for metrics in all_metrics:
            agent_distribution[metrics.agent_selected] = agent_distribution.get(metrics.agent_selected, 0) + 1
        
        # Query type performance analysis
        query_type_performance = {}
        for query_type in set(m.query_type for m in all_metrics):
            type_metrics = [m for m in all_metrics if m.query_type == query_type]
            if type_metrics:
                type_times = [m.execution_time_ms for m in type_metrics]
                query_type_performance[query_type] = {
                    'count': len(type_metrics),
                    'avg_time': statistics.mean(type_times),
                    'min_time': min(type_times),
                    'max_time': max(type_times),
                    'median_time': statistics.median(type_times)
                }
        
        # Identify bottlenecks
        bottlenecks = self._identify_bottlenecks(all_metrics)
        
        # Identify optimization opportunities
        optimization_opportunities = self._identify_optimizations(all_metrics, query_type_performance)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(all_metrics, bottlenecks, optimization_opportunities)
        
        return ProfileSummary(
            total_operations=len(all_metrics),
            avg_execution_time=statistics.mean(execution_times),
            min_execution_time=min(execution_times),
            max_execution_time=max(execution_times),
            percentile_95_time=statistics.quantiles(execution_times, n=20)[18],  # 95th percentile
            percentile_99_time=statistics.quantiles(execution_times, n=100)[98], # 99th percentile
            throughput_ops_per_sec=len(all_metrics) / total_runtime,
            agent_distribution=agent_distribution,
            query_type_performance=query_type_performance,
            memory_analysis=memory_analysis,
            bottlenecks=bottlenecks,
            optimization_opportunities=optimization_opportunities,
            recommendations=recommendations
        )
    
    def _identify_bottlenecks(self, metrics: List[PerformanceMetrics]) -> List[str]:
        """Identify performance bottlenecks"""
        bottlenecks = []
        
        execution_times = [m.execution_time_ms for m in metrics]
        avg_time = statistics.mean(execution_times)
        p95_time = statistics.quantiles(execution_times, n=20)[18]
        
        # Time-based bottlenecks
        if avg_time > 25:  # > 25ms average
            bottlenecks.append(f"High average execution time: {avg_time:.2f}ms (target: <25ms)")
        
        if p95_time > 100:  # > 100ms at 95th percentile
            bottlenecks.append(f"High 95th percentile time: {p95_time:.2f}ms (target: <100ms)")
        
        # Variance bottlenecks
        time_variance = statistics.stdev(execution_times)
        if time_variance > 20:
            bottlenecks.append(f"High performance variance: {time_variance:.2f}ms (indicates inconsistent performance)")
        
        # Outlier analysis
        outliers = [t for t in execution_times if t > avg_time + 3 * time_variance]
        outlier_rate = len(outliers) / len(execution_times)
        if outlier_rate > 0.05:  # > 5% outliers
            bottlenecks.append(f"High outlier rate: {outlier_rate:.2%} operations significantly slower than average")
        
        # Query type specific bottlenecks
        query_types = set(m.query_type for m in metrics)
        for query_type in query_types:
            type_times = [m.execution_time_ms for m in metrics if m.query_type == query_type]
            if type_times:
                type_avg = statistics.mean(type_times)
                if type_avg > avg_time * 1.5:  # 50% slower than overall average
                    bottlenecks.append(f"Query type '{query_type}' is slow: {type_avg:.2f}ms avg (vs overall {avg_time:.2f}ms)")
        
        return bottlenecks
    
    def _identify_optimizations(self, metrics: List[PerformanceMetrics], 
                              query_performance: Dict[str, Dict[str, float]]) -> List[str]:
        """Identify optimization opportunities"""
        opportunities = []
        
        # Input length correlation analysis
        short_queries = [m for m in metrics if m.input_length < 20]
        long_queries = [m for m in metrics if m.input_length > 100]
        
        if short_queries and long_queries:
            short_avg = statistics.mean([m.execution_time_ms for m in short_queries])
            long_avg = statistics.mean([m.execution_time_ms for m in long_queries])
            
            if long_avg > short_avg * 2:  # Long queries significantly slower
                opportunities.append(f"Input length correlation: Long queries {long_avg:.2f}ms vs short {short_avg:.2f}ms - consider early pattern matching")
        
        # Agent selection pattern analysis
        agent_times = {}
        for agent in set(m.agent_selected for m in metrics):
            agent_metrics = [m for m in metrics if m.agent_selected == agent]
            if agent_metrics:
                agent_times[agent] = statistics.mean([m.execution_time_ms for m in agent_metrics])
        
        if agent_times:
            fastest_agent = min(agent_times, key=agent_times.get)
            slowest_agent = max(agent_times, key=agent_times.get)
            
            speed_ratio = agent_times[slowest_agent] / agent_times[fastest_agent]
            if speed_ratio > 2:
                opportunities.append(f"Agent selection variance: {slowest_agent} ({agent_times[slowest_agent]:.2f}ms) vs {fastest_agent} ({agent_times[fastest_agent]:.2f}ms) - investigate selection logic")
        
        # Pattern matching opportunities
        edge_case_performance = query_performance.get('edge', {})
        simple_performance = query_performance.get('simple', {})
        
        if edge_case_performance and simple_performance:
            edge_avg = edge_case_performance.get('avg_time', 0)
            simple_avg = simple_performance.get('avg_time', 0)
            
            if edge_avg > simple_avg * 3:  # Edge cases much slower
                opportunities.append(f"Edge case handling inefficient: {edge_avg:.2f}ms vs simple {simple_avg:.2f}ms - improve fallback logic")
        
        # Caching opportunities
        execution_times = [m.execution_time_ms for m in metrics]
        time_variance = statistics.stdev(execution_times)
        if time_variance < 5:  # Very consistent timing suggests little dynamic processing
            opportunities.append("Consistent execution times suggest caching opportunities for pattern matching results")
        
        return opportunities
    
    def _generate_recommendations(self, metrics: List[PerformanceMetrics],
                                bottlenecks: List[str], opportunities: List[str]) -> List[str]:
        """Generate actionable optimization recommendations"""
        recommendations = []
        
        avg_time = statistics.mean([m.execution_time_ms for m in metrics])
        
        # Performance targets
        if avg_time > 30:
            recommendations.append("PRIORITY HIGH: Optimize core pattern matching algorithm - avg time exceeds 30ms target")
        elif avg_time > 15:
            recommendations.append("PRIORITY MEDIUM: Fine-tune pattern matching - approaching performance limits")
        else:
            recommendations.append("PRIORITY LOW: Performance within acceptable range - monitor and maintain")
        
        # Specific optimizations based on bottlenecks
        if any("variance" in b.lower() for b in bottlenecks):
            recommendations.append("Implement performance consistency improvements: normalize execution paths")
        
        if any("outlier" in b.lower() for b in bottlenecks):
            recommendations.append("Add outlier detection and fast-path optimization for common patterns")
        
        # Memory optimization
        memory_mb = metrics[0].__dict__.get('memory_growth_mb', 0) if metrics else 0
        if memory_mb > 5:  # > 5MB growth
            recommendations.append("Implement memory optimization: reduce object creation and improve garbage collection")
        
        # Caching recommendations
        if len(set(m.agent_selected for m in metrics)) < 5:  # Low agent diversity
            recommendations.append("Consider result caching: agent selection patterns are predictable")
        
        # Algorithmic improvements
        if any("input length" in o.lower() for o in opportunities):
            recommendations.append("Implement early pattern matching: optimize for query length correlation")
        
        if any("agent selection variance" in o.lower() for o in opportunities):
            recommendations.append("Optimize agent selection pipeline: address performance differences between agents")
        
        return recommendations
    
    def print_detailed_report(self, summary: ProfileSummary):
        """Print comprehensive performance report"""
        print("\n" + "=" * 100)
        print("AGENT SELECTION SYSTEM - PERFORMANCE ANALYSIS REPORT")
        print("=" * 100)
        
        print(f"\n🚀 EXECUTION PERFORMANCE:")
        print(f"  Total Operations: {summary.total_operations:,}")
        print(f"  Average Time: {summary.avg_execution_time:.2f}ms (Target: <25ms)")
        print(f"  Minimum Time: {summary.min_execution_time:.2f}ms")
        print(f"  Maximum Time: {summary.max_execution_time:.2f}ms")
        print(f"  95th Percentile: {summary.percentile_95_time:.2f}ms (Target: <100ms)")
        print(f"  99th Percentile: {summary.percentile_99_time:.2f}ms")
        print(f"  Throughput: {summary.throughput_ops_per_sec:.1f} ops/second")
        
        print(f"\n📊 AGENT SELECTION DISTRIBUTION:")
        total_ops = sum(summary.agent_distribution.values())
        for agent, count in sorted(summary.agent_distribution.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_ops) * 100
            print(f"  {agent}: {count:,} ({percentage:.1f}%)")
        
        print(f"\n🔍 QUERY TYPE PERFORMANCE:")
        for query_type, metrics in summary.query_type_performance.items():
            print(f"  {query_type.upper()}:")
            print(f"    Count: {metrics['count']:,}")
            print(f"    Average: {metrics['avg_time']:.2f}ms")
            print(f"    Range: {metrics['min_time']:.2f}ms - {metrics['max_time']:.2f}ms")
            print(f"    Median: {metrics['median_time']:.2f}ms")
        
        print(f"\n💾 MEMORY ANALYSIS:")
        print(f"  Memory Growth: {summary.memory_analysis['total_memory_growth_mb']:.2f}MB")
        print(f"  Top Memory Consumers:")
        for consumer in summary.memory_analysis['top_memory_consumers'][:3]:
            print(f"    {consumer['location']}: {consumer['size_diff_bytes']} bytes")
        
        print(f"\n⚠️ PERFORMANCE BOTTLENECKS:")
        if summary.bottlenecks:
            for i, bottleneck in enumerate(summary.bottlenecks, 1):
                print(f"  {i}. {bottleneck}")
        else:
            print("  No significant bottlenecks detected")
        
        print(f"\n💡 OPTIMIZATION OPPORTUNITIES:")
        if summary.optimization_opportunities:
            for i, opportunity in enumerate(summary.optimization_opportunities, 1):
                print(f"  {i}. {opportunity}")
        else:
            print("  No major optimization opportunities identified")
        
        print(f"\n🎯 ACTIONABLE RECOMMENDATIONS:")
        for i, recommendation in enumerate(summary.recommendations, 1):
            print(f"  {i}. {recommendation}")
        
        # Performance scoring
        print(f"\n" + "=" * 100)
        print("PERFORMANCE ASSESSMENT:")
        
        score = 0
        max_score = 5
        
        # Execution time score
        if summary.avg_execution_time <= 15:
            print("  ✅ Execution Time: EXCELLENT (<15ms)")
            score += 1
        elif summary.avg_execution_time <= 25:
            print("  🟡 Execution Time: GOOD (15-25ms)")
            score += 0.5
        else:
            print("  ❌ Execution Time: NEEDS IMPROVEMENT (>25ms)")
        
        # 95th percentile score
        if summary.percentile_95_time <= 50:
            print("  ✅ Response Consistency: EXCELLENT (<50ms p95)")
            score += 1
        elif summary.percentile_95_time <= 100:
            print("  🟡 Response Consistency: GOOD (50-100ms p95)")
            score += 0.5
        else:
            print("  ❌ Response Consistency: NEEDS IMPROVEMENT (>100ms p95)")
        
        # Throughput score
        if summary.throughput_ops_per_sec >= 200:
            print("  ✅ Throughput: EXCELLENT (≥200 ops/sec)")
            score += 1
        elif summary.throughput_ops_per_sec >= 100:
            print("  🟡 Throughput: GOOD (100-200 ops/sec)")
            score += 0.5
        else:
            print("  ❌ Throughput: NEEDS IMPROVEMENT (<100 ops/sec)")
        
        # Memory efficiency score
        if summary.memory_analysis['total_memory_growth_mb'] <= 1:
            print("  ✅ Memory Efficiency: EXCELLENT (≤1MB growth)")
            score += 1
        elif summary.memory_analysis['total_memory_growth_mb'] <= 5:
            print("  🟡 Memory Efficiency: ACCEPTABLE (1-5MB growth)")
            score += 0.5
        else:
            print("  ❌ Memory Efficiency: NEEDS IMPROVEMENT (>5MB growth)")
        
        # Bottleneck score
        if len(summary.bottlenecks) == 0:
            print("  ✅ System Health: EXCELLENT (No bottlenecks)")
            score += 1
        elif len(summary.bottlenecks) <= 2:
            print("  🟡 System Health: GOOD (Minor bottlenecks)")
            score += 0.5
        else:
            print("  ❌ System Health: NEEDS ATTENTION (Multiple bottlenecks)")
        
        # Final assessment
        percentage = (score / max_score) * 100
        print(f"\n  OVERALL SCORE: {score:.1f}/{max_score} ({percentage:.1f}%)")
        
        if score >= 4.5:
            print("  🎉 SYSTEM STATUS: OPTIMAL - Excellent performance across all metrics")
        elif score >= 3.5:
            print("  👍 SYSTEM STATUS: GOOD - Strong performance with minor optimization opportunities")
        elif score >= 2.5:
            print("  ⚠️ SYSTEM STATUS: ACCEPTABLE - Some performance improvements needed")
        else:
            print("  🔧 SYSTEM STATUS: NEEDS OPTIMIZATION - Significant improvements required")
        
        print("=" * 100)
    
    def save_results(self, summary: ProfileSummary, filename: str = "performance_profile.json"):
        """Save profiling results to JSON file"""
        # Convert dataclass to dict for JSON serialization
        results_dict = {
            'total_operations': summary.total_operations,
            'avg_execution_time': summary.avg_execution_time,
            'min_execution_time': summary.min_execution_time,
            'max_execution_time': summary.max_execution_time,
            'percentile_95_time': summary.percentile_95_time,
            'percentile_99_time': summary.percentile_99_time,
            'throughput_ops_per_sec': summary.throughput_ops_per_sec,
            'agent_distribution': summary.agent_distribution,
            'query_type_performance': summary.query_type_performance,
            'memory_analysis': summary.memory_analysis,
            'bottlenecks': summary.bottlenecks,
            'optimization_opportunities': summary.optimization_opportunities,
            'recommendations': summary.recommendations,
            'timestamp': time.time(),
            'profiler_version': '1.0'
        }
        
        with open(filename, 'w') as f:
            json.dump(results_dict, f, indent=2)
        
        print(f"\nDetailed results saved to: {filename}")

def main():
    """Main execution"""
    profiler = SimplePerformanceProfiler()
    
    # Run performance analysis
    summary = profiler.run_performance_analysis(iterations=100)
    
    # Display results
    profiler.print_detailed_report(summary)
    
    # Save results
    profiler.save_results(summary)
    
    return summary

if __name__ == "__main__":
    main()
