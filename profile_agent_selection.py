#!/usr/bin/env python3
"""
Agent Selection Performance Profiler

Comprehensive profiling of agent selection system performance including:
- Response times and resource usage
- Memory usage patterns
- Critical path analysis
- Performance bottleneck identification
- Optimization opportunities
"""

import time
import psutil
import gc
import tracemalloc
import cProfile
import pstats
import io
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import json
import statistics
import sys
from pathlib import Path

# Import the agent selector to profile
try:
    from src.agent_selector import EnhancedAgentSelector, get_agent_selector
except ImportError:
    print("Warning: Could not import agent selector, using mock implementation")
    
    class MockAgentSelector:
        def __init__(self):
            self.agents = {}
            self.keyword_index = {}
            self.pattern_cache = {}
            self.selection_history = []
            
        def select_agent(self, query: str, context=None):
            time.sleep(0.01)  # Simulate processing time
            from dataclasses import dataclass
            
            @dataclass
            class MockResult:
                agent_name: str = "test-specialist"
                confidence_score: float = 0.8
                matched_patterns: List[str] = None
                processing_time_ms: float = 10.0
                context_keywords: List[str] = None
                reasoning: str = "Mock selection"
                
                def __post_init__(self):
                    if self.matched_patterns is None:
                        self.matched_patterns = []
                    if self.context_keywords is None:
                        self.context_keywords = []
                        
            return MockResult()
            
        def get_selection_stats(self):
            return {
                'total_selections': 0,
                'agent_distribution': {},
                'average_confidence': 0.8,
                'average_processing_time_ms': 10.0
            }
    
    EnhancedAgentSelector = MockAgentSelector
    def get_agent_selector():
        return MockAgentSelector()

@dataclass
class PerformanceMetrics:
    """Performance metrics for a single operation"""
    execution_time: float
    memory_usage: float
    cpu_usage: float
    agent_selected: str
    confidence: float
    input_length: int
    
@dataclass  
class ProfileResult:
    """Complete profiling results"""
    total_operations: int
    avg_execution_time: float
    min_execution_time: float
    max_execution_time: float
    percentile_95_time: float
    avg_memory_usage: float
    peak_memory_usage: float
    avg_cpu_usage: float
    throughput_ops_per_sec: float
    agent_distribution: Dict[str, int]
    input_size_analysis: Dict[str, float]
    critical_path_analysis: Dict[str, Any]
    bottleneck_analysis: Dict[str, Any]
    recommendations: List[str]

class AgentSelectionProfiler:
    """Comprehensive profiler for agent selection system"""
    
    def __init__(self):
        self.selector = get_agent_selector()
        self.metrics = []
        self.profile_data = None
        
    def create_test_queries(self) -> List[Tuple[str, str]]:
        """Create diverse test queries for profiling"""
        return [
            ("Simple testing issue", "simple"),
            ("Docker container orchestration problems with Kubernetes scaling and networking issues", "medium"),
            ("Complex system-wide performance degradation affecting multiple services with security implications requiring comprehensive analysis across testing, infrastructure, and security domains with parallel coordination", "complex"),
            ("test", "minimal"),
            ("Security vulnerability assessment with compliance validation and penetration testing requirements for enterprise infrastructure including container orchestration and CI/CD pipeline security", "enterprise"),
            ("Need help", "vague"),
            ("Pytest async mock fixture configuration coverage", "technical"),
            ("Urgent production incident requiring immediate infrastructure analysis", "urgent"),
            ("Code quality refactoring with type annotations and variable naming", "quality"),
            ("Multi-domain analysis spanning testing, security, performance, and infrastructure", "multi_domain")
        ]
    
    def measure_single_operation(self, query: str) -> PerformanceMetrics:
        """Measure performance of a single agent selection operation"""
        # Start monitoring
        process = psutil.Process()
        start_cpu = process.cpu_percent()
        start_memory = process.memory_info().rss / 1024 / 1024  # MB
        start_time = time.perf_counter()
        
        # Execute agent selection
        result = self.selector.select_agent(query)
        
        # End monitoring
        end_time = time.perf_counter()
        end_memory = process.memory_info().rss / 1024 / 1024  # MB
        end_cpu = process.cpu_percent()
        
        return PerformanceMetrics(
            execution_time=(end_time - start_time) * 1000,  # Convert to ms
            memory_usage=end_memory - start_memory,
            cpu_usage=max(end_cpu - start_cpu, 0),
            agent_selected=result.agent_name,
            confidence=result.confidence_score,
            input_length=len(query)
        )
    
    def profile_with_cprofile(self, queries: List[str], iterations: int = 10) -> Dict[str, Any]:
        """Profile using cProfile for detailed function-level analysis"""
        profiler = cProfile.Profile()
        
        # Run profiling
        profiler.enable()
        
        for _ in range(iterations):
            for query, _ in queries:
                self.selector.select_agent(query)
        
        profiler.disable()
        
        # Analyze results
        stream = io.StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.sort_stats('cumulative')
        stats.print_stats(20)  # Top 20 functions
        
        profile_output = stream.getvalue()
        
        # Extract key metrics
        stats.sort_stats('tottime')
        top_time_functions = []
        for func_name, (cc, nc, tt, ct, callers) in list(stats.stats.items())[:10]:
            top_time_functions.append({
                'function': str(func_name),
                'total_time': tt,
                'cumulative_time': ct,
                'calls': cc
            })
        
        return {
            'profile_output': profile_output,
            'top_time_functions': top_time_functions,
            'total_calls': stats.total_calls
        }
    
    def memory_profile(self, queries: List[str], iterations: int = 5) -> Dict[str, Any]:
        """Profile memory usage patterns"""
        tracemalloc.start()
        
        memory_snapshots = []
        
        for i in range(iterations):
            # Take snapshot before
            snapshot_before = tracemalloc.take_snapshot()
            
            # Execute operations
            for query, _ in queries:
                self.selector.select_agent(query)
            
            # Take snapshot after
            snapshot_after = tracemalloc.take_snapshot()
            
            # Analyze difference
            stats = snapshot_after.compare_to(snapshot_before, 'lineno')
            
            total_size_diff = sum(stat.size_diff for stat in stats)
            memory_snapshots.append({
                'iteration': i,
                'size_diff_mb': total_size_diff / 1024 / 1024,
                'top_differences': [
                    {
                        'filename': stat.traceback.filename,
                        'lineno': stat.traceback.lineno,
                        'size_diff': stat.size_diff,
                        'count_diff': stat.count_diff
                    }
                    for stat in stats[:5]
                ]
            })
            
            # Force garbage collection
            gc.collect()
        
        tracemalloc.stop()
        
        return {
            'snapshots': memory_snapshots,
            'avg_memory_growth': statistics.mean([s['size_diff_mb'] for s in memory_snapshots]),
            'peak_memory_growth': max([s['size_diff_mb'] for s in memory_snapshots])
        }
    
    def run_comprehensive_profile(self, iterations: int = 100) -> ProfileResult:
        """Run comprehensive performance profiling"""
        print(f"Running comprehensive profile with {iterations} iterations...")
        
        queries = self.create_test_queries()
        all_metrics = []
        
        # Warm up
        print("Warming up...")
        for query, _ in queries[:3]:
            self.selector.select_agent(query)
        
        print("Collecting performance metrics...")
        start_time = time.time()
        
        # Collect metrics
        for i in range(iterations):
            for query, query_type in queries:
                metrics = self.measure_single_operation(query)
                metrics.query_type = query_type  # Add query type for analysis
                all_metrics.append(metrics)
            
            if (i + 1) % 20 == 0:
                print(f"Completed {i + 1}/{iterations} iterations")
        
        total_time = time.time() - start_time
        
        print("Running detailed profiling...")
        # Detailed profiling
        cprofile_results = self.profile_with_cprofile(queries, iterations=5)
        memory_results = self.memory_profile(queries, iterations=5)
        
        print("Analyzing results...")
        # Analyze results
        execution_times = [m.execution_time for m in all_metrics]
        memory_usages = [m.memory_usage for m in all_metrics]
        cpu_usages = [m.cpu_usage for m in all_metrics]
        
        agent_distribution = {}
        input_size_buckets = {'small': [], 'medium': [], 'large': []}
        
        for metrics in all_metrics:
            # Agent distribution
            agent_distribution[metrics.agent_selected] = agent_distribution.get(metrics.agent_selected, 0) + 1
            
            # Input size analysis
            if metrics.input_length < 50:
                input_size_buckets['small'].append(metrics.execution_time)
            elif metrics.input_length < 150:
                input_size_buckets['medium'].append(metrics.execution_time)
            else:
                input_size_buckets['large'].append(metrics.execution_time)
        
        # Critical path analysis
        critical_path_analysis = {
            'cprofile_insights': cprofile_results,
            'memory_insights': memory_results,
            'slowest_operations': sorted(all_metrics, key=lambda x: x.execution_time, reverse=True)[:10]
        }
        
        # Bottleneck analysis
        bottleneck_analysis = self._analyze_bottlenecks(all_metrics, cprofile_results)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(all_metrics, bottleneck_analysis)
        
        return ProfileResult(
            total_operations=len(all_metrics),
            avg_execution_time=statistics.mean(execution_times),
            min_execution_time=min(execution_times),
            max_execution_time=max(execution_times),
            percentile_95_time=statistics.quantiles(execution_times, n=20)[18],  # 95th percentile
            avg_memory_usage=statistics.mean(memory_usages),
            peak_memory_usage=max(memory_usages),
            avg_cpu_usage=statistics.mean(cpu_usages),
            throughput_ops_per_sec=len(all_metrics) / total_time,
            agent_distribution=agent_distribution,
            input_size_analysis={
                'small_avg': statistics.mean(input_size_buckets['small']) if input_size_buckets['small'] else 0,
                'medium_avg': statistics.mean(input_size_buckets['medium']) if input_size_buckets['medium'] else 0,
                'large_avg': statistics.mean(input_size_buckets['large']) if input_size_buckets['large'] else 0
            },
            critical_path_analysis=critical_path_analysis,
            bottleneck_analysis=bottleneck_analysis,
            recommendations=recommendations
        )
    
    def _analyze_bottlenecks(self, metrics: List[PerformanceMetrics], 
                           cprofile_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance bottlenecks"""
        # Time-based bottlenecks
        slow_operations = [m for m in metrics if m.execution_time > 50]  # > 50ms
        slow_operation_rate = len(slow_operations) / len(metrics)
        
        # Memory-based bottlenecks  
        high_memory_ops = [m for m in metrics if m.memory_usage > 5]  # > 5MB
        memory_pressure_rate = len(high_memory_ops) / len(metrics)
        
        # CPU-based bottlenecks
        high_cpu_ops = [m for m in metrics if m.cpu_usage > 10]  # > 10%
        cpu_pressure_rate = len(high_cpu_ops) / len(metrics)
        
        # Function-level bottlenecks from cProfile
        function_bottlenecks = cprofile_results['top_time_functions'][:5]
        
        return {
            'slow_operation_rate': slow_operation_rate,
            'memory_pressure_rate': memory_pressure_rate,
            'cpu_pressure_rate': cpu_pressure_rate,
            'function_bottlenecks': function_bottlenecks,
            'performance_variance': statistics.stdev([m.execution_time for m in metrics]),
            'outlier_count': len([m for m in metrics if m.execution_time > 100])  # > 100ms outliers
        }
    
    def _generate_recommendations(self, metrics: List[PerformanceMetrics],
                                bottleneck_analysis: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        avg_time = statistics.mean([m.execution_time for m in metrics])
        p95_time = statistics.quantiles([m.execution_time for m in metrics], n=20)[18]
        
        # Performance recommendations
        if avg_time > 30:  # > 30ms average
            recommendations.append(f"Average execution time ({avg_time:.1f}ms) exceeds target (30ms). Consider pattern matching optimization.")
        
        if p95_time > 100:  # > 100ms at 95th percentile
            recommendations.append(f"95th percentile response time ({p95_time:.1f}ms) is high. Investigate outlier cases.")
        
        # Memory recommendations
        avg_memory = statistics.mean([m.memory_usage for m in metrics])
        if avg_memory > 2:  # > 2MB average
            recommendations.append(f"Average memory usage ({avg_memory:.1f}MB) is high. Consider caching optimization.")
        
        # Bottleneck recommendations
        if bottleneck_analysis['slow_operation_rate'] > 0.1:
            recommendations.append(f"High slow operation rate ({bottleneck_analysis['slow_operation_rate']:.1%}). Focus on algorithm optimization.")
        
        if bottleneck_analysis['performance_variance'] > 20:
            recommendations.append(f"High performance variance ({bottleneck_analysis['performance_variance']:.1f}ms). Investigate inconsistent execution paths.")
        
        # Function-level recommendations
        if bottleneck_analysis['function_bottlenecks']:
            top_bottleneck = bottleneck_analysis['function_bottlenecks'][0]
            recommendations.append(f"Top time consumer: {top_bottleneck['function']} ({top_bottleneck['total_time']:.3f}s total). Consider optimization.")
        
        if not recommendations:
            recommendations.append("Performance within acceptable parameters. Continue monitoring.")
        
        return recommendations
    
    def save_results(self, results: ProfileResult, filename: str = "agent_selection_profile.json"):
        """Save profiling results to JSON file"""
        # Convert to serializable format
        results_dict = {
            'total_operations': results.total_operations,
            'avg_execution_time': results.avg_execution_time,
            'min_execution_time': results.min_execution_time,
            'max_execution_time': results.max_execution_time,
            'percentile_95_time': results.percentile_95_time,
            'avg_memory_usage': results.avg_memory_usage,
            'peak_memory_usage': results.peak_memory_usage,
            'avg_cpu_usage': results.avg_cpu_usage,
            'throughput_ops_per_sec': results.throughput_ops_per_sec,
            'agent_distribution': results.agent_distribution,
            'input_size_analysis': results.input_size_analysis,
            'bottleneck_analysis': {
                k: v for k, v in results.bottleneck_analysis.items() 
                if k != 'function_bottlenecks'  # Skip complex objects
            },
            'recommendations': results.recommendations,
            'timestamp': time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(results_dict, f, indent=2)
        
        print(f"Results saved to {filename}")
    
    def print_comprehensive_report(self, results: ProfileResult):
        """Print comprehensive performance report"""
        print("\n" + "=" * 100)
        print("AGENT SELECTION SYSTEM - COMPREHENSIVE PERFORMANCE PROFILE")
        print("=" * 100)
        
        print(f"\nEXECUTION PERFORMANCE:")
        print(f"  Total Operations: {results.total_operations:,}")
        print(f"  Average Execution Time: {results.avg_execution_time:.2f}ms (Target: <30ms)")
        print(f"  Minimum Execution Time: {results.min_execution_time:.2f}ms")
        print(f"  Maximum Execution Time: {results.max_execution_time:.2f}ms")
        print(f"  95th Percentile Time: {results.percentile_95_time:.2f}ms (Target: <100ms)")
        print(f"  Throughput: {results.throughput_ops_per_sec:.1f} ops/second")
        
        print(f"\nRESOURCE UTILIZATION:")
        print(f"  Average Memory Usage: {results.avg_memory_usage:.2f}MB")
        print(f"  Peak Memory Usage: {results.peak_memory_usage:.2f}MB")
        print(f"  Average CPU Usage: {results.avg_cpu_usage:.2f}%")
        
        print(f"\nAGENT SELECTION DISTRIBUTION:")
        total_selections = sum(results.agent_distribution.values())
        for agent, count in sorted(results.agent_distribution.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_selections) * 100
            print(f"  {agent}: {count:,} selections ({percentage:.1f}%)")
        
        print(f"\nINPUT SIZE ANALYSIS:")
        print(f"  Small Inputs (<50 chars): {results.input_size_analysis['small_avg']:.2f}ms avg")
        print(f"  Medium Inputs (50-150 chars): {results.input_size_analysis['medium_avg']:.2f}ms avg")
        print(f"  Large Inputs (>150 chars): {results.input_size_analysis['large_avg']:.2f}ms avg")
        
        print(f"\nBOTTLENECK ANALYSIS:")
        print(f"  Slow Operations Rate: {results.bottleneck_analysis['slow_operation_rate']:.2%} (>50ms)")
        print(f"  Memory Pressure Rate: {results.bottleneck_analysis['memory_pressure_rate']:.2%} (>5MB)")
        print(f"  CPU Pressure Rate: {results.bottleneck_analysis['cpu_pressure_rate']:.2%} (>10%)")
        print(f"  Performance Variance: {results.bottleneck_analysis['performance_variance']:.2f}ms")
        print(f"  Outlier Operations: {results.bottleneck_analysis['outlier_count']} (>100ms)")
        
        print(f"\nCRITICAL PATH INSIGHTS:")
        memory_insights = results.critical_path_analysis['memory_insights']
        print(f"  Average Memory Growth: {memory_insights['avg_memory_growth']:.2f}MB per batch")
        print(f"  Peak Memory Growth: {memory_insights['peak_memory_growth']:.2f}MB per batch")
        
        print(f"\nOPTIMIZATION RECOMMENDATIONS:")
        for i, recommendation in enumerate(results.recommendations, 1):
            print(f"  {i}. {recommendation}")
        
        # Performance Assessment
        print(f"\n" + "=" * 100)
        print("PERFORMANCE ASSESSMENT:")
        
        targets_met = 0
        total_targets = 4
        
        # Execution time target
        if results.avg_execution_time <= 30:
            print("  ✅ Execution Time: EXCELLENT (≤30ms)")
            targets_met += 1
        elif results.avg_execution_time <= 50:
            print("  🔶 Execution Time: GOOD (≤50ms)")
        else:
            print("  ❌ Execution Time: NEEDS IMPROVEMENT (>50ms)")
        
        # 95th percentile target
        if results.percentile_95_time <= 100:
            print("  ✅ 95th Percentile: EXCELLENT (≤100ms)")
            targets_met += 1
        elif results.percentile_95_time <= 200:
            print("  🔶 95th Percentile: ACCEPTABLE (≤200ms)")
        else:
            print("  ❌ 95th Percentile: NEEDS IMPROVEMENT (>200ms)")
        
        # Memory efficiency target
        if results.avg_memory_usage <= 2:
            print("  ✅ Memory Efficiency: EXCELLENT (≤2MB)")
            targets_met += 1
        elif results.avg_memory_usage <= 5:
            print("  🔶 Memory Efficiency: ACCEPTABLE (≤5MB)")
        else:
            print("  ❌ Memory Efficiency: NEEDS IMPROVEMENT (>5MB)")
        
        # Throughput target
        if results.throughput_ops_per_sec >= 100:
            print("  ✅ Throughput: EXCELLENT (≥100 ops/sec)")
            targets_met += 1
        elif results.throughput_ops_per_sec >= 50:
            print("  🔶 Throughput: ACCEPTABLE (≥50 ops/sec)")
        else:
            print("  ❌ Throughput: NEEDS IMPROVEMENT (<50 ops/sec)")
        
        print(f"\n  TARGETS MET: {targets_met}/{total_targets}")
        
        if targets_met >= 3:
            print("  🎉 OVERALL ASSESSMENT: EXCELLENT - Performance optimized")
        elif targets_met >= 2:
            print("  👍 OVERALL ASSESSMENT: GOOD - Minor optimizations recommended")
        else:
            print("  ⚠️  OVERALL ASSESSMENT: NEEDS IMPROVEMENT - Significant optimization required")
        
        print("=" * 100)

def main():
    """Main profiling execution"""
    profiler = AgentSelectionProfiler()
    
    # Run comprehensive profile
    results = profiler.run_comprehensive_profile(iterations=50)
    
    # Print results
    profiler.print_comprehensive_report(results)
    
    # Save results
    profiler.save_results(results)
    
    return results

if __name__ == "__main__":
    main()
