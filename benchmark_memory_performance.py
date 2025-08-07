#!/usr/bin/env python3
"""
Memory Lookup Performance Benchmark

Comprehensive benchmark for memory lookup performance in the consolidated Claude Code system.
Tests memory lookup speed, pattern resolution, cache effectiveness, and system resource usage.
"""

import time
import os
import json
import resource
from pathlib import Path
from typing import Dict, List, Tuple, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from dataclasses import dataclass
from collections import defaultdict
import statistics


@dataclass
class BenchmarkResult:
    """Individual benchmark result"""
    operation: str
    latency_ms: float
    memory_usage_mb: float
    cpu_percent: float
    success: bool
    metadata: Dict[str, Any]


@dataclass
class BenchmarkSummary:
    """Summary of benchmark results"""
    operation_type: str
    total_operations: int
    avg_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    success_rate: float
    avg_memory_mb: float
    peak_memory_mb: float
    avg_cpu_percent: float
    peak_cpu_percent: float


class MemoryBenchmark:
    """Memory lookup performance benchmark suite"""
    
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.claude_dir = project_dir / ".claude"
        self.memory_dir = self.claude_dir / "memory"
        self.settings_file = self.claude_dir / "settings.json"
        
        # Initialize system monitoring (simplified without psutil)
        self.results: List[BenchmarkResult] = []
        
        # Cache for memory content
        self._memory_cache: Dict[str, str] = {}
        self._pattern_cache: Dict[str, List[str]] = {}
        
    def load_settings(self) -> Dict[str, Any]:
        """Load Claude Code settings"""
        try:
            with open(self.settings_file) as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load settings: {e}")
            return {}
    
    def benchmark_file_access(self, iterations: int = 100) -> List[BenchmarkResult]:
        """Benchmark raw file access performance"""
        print(f"\n🔍 Benchmarking file access performance ({iterations} iterations)...")
        results = []
        
        memory_files = list(self.memory_dir.rglob("*.md"))
        
        for i in range(iterations):
            start_time = time.perf_counter()
            start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # KB to MB
            start_cpu = time.process_time()
            
            try:
                # Simulate memory file access pattern
                file_to_read = memory_files[i % len(memory_files)]
                with open(file_to_read, 'r') as f:
                    content = f.read()
                
                success = len(content) > 0
                
            except Exception as e:
                success = False
                print(f"File access error: {e}")
            
            end_time = time.perf_counter()
            end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # KB to MB
            end_cpu = time.process_time()
            
            result = BenchmarkResult(
                operation="file_access",
                latency_ms=(end_time - start_time) * 1000,
                memory_usage_mb=max(0, end_memory - start_memory),
                cpu_percent=(end_cpu - start_cpu) * 100,  # Convert to percentage
                success=success,
                metadata={"file": str(file_to_read), "iteration": i}
            )
            results.append(result)
        
        return results
    
    def benchmark_memory_lookup(self, iterations: int = 50) -> List[BenchmarkResult]:
        """Benchmark memory lookup and parsing performance"""
        print(f"\n🧠 Benchmarking memory lookup performance ({iterations} iterations)...")
        results = []
        
        # Test patterns from agent coordination
        lookup_patterns = [
            "agent-coordination-patterns.md",
            "domains/testing-patterns.md",
            "domains/infrastructure-patterns.md",
            "domains/security-patterns.md"
        ]
        
        for i in range(iterations):
            pattern = lookup_patterns[i % len(lookup_patterns)]
            
            start_time = time.perf_counter()
            start_memory = self.process.memory_info().rss / 1024 / 1024
            start_cpu = self.process.cpu_percent()
            
            try:
                # Simulate memory lookup with parsing
                file_path = self.memory_dir / pattern
                content = self._load_memory_file(file_path)
                parsed_data = self._parse_memory_content(content)
                
                success = len(parsed_data) > 0
                
            except Exception as e:
                success = False
                print(f"Memory lookup error: {e}")
            
            end_time = time.perf_counter()
            end_memory = self.process.memory_info().rss / 1024 / 1024
            end_cpu = self.process.cpu_percent()
            
            result = BenchmarkResult(
                operation="memory_lookup",
                latency_ms=(end_time - start_time) * 1000,
                memory_usage_mb=end_memory - start_memory,
                cpu_percent=max(start_cpu, end_cpu),
                success=success,
                metadata={"pattern": pattern, "iteration": i}
            )
            results.append(result)
        
        return results
    
    def benchmark_pattern_resolution(self, iterations: int = 100) -> List[BenchmarkResult]:
        """Benchmark pattern matching and resolution performance"""
        print(f"\n🔍 Benchmarking pattern resolution ({iterations} iterations)...")
        results = []
        
        # Test patterns for agent selection
        test_patterns = [
            ("async testing issues with mock configuration", ["test-specialist", "async-pattern-fixer"]),
            ("docker orchestration performance problems", ["infrastructure-engineer", "docker-specialist"]),
            ("security vulnerability in authentication", ["security-enforcer", "security-auditor"]),
            ("coverage gaps requiring architecture changes", ["coverage-optimizer", "pattern-analyzer"]),
            ("integration testing with environment sync", ["integration-validator", "environment-synchronizer"])
        ]
        
        for i in range(iterations):
            pattern_input, expected_agents = test_patterns[i % len(test_patterns)]
            
            start_time = time.perf_counter()
            start_memory = self.process.memory_info().rss / 1024 / 1024
            start_cpu = self.process.cpu_percent()
            
            try:
                # Simulate pattern resolution
                resolved_agents = self._resolve_agent_patterns(pattern_input)
                
                # Check if resolution matches expectations
                success = any(agent in resolved_agents for agent in expected_agents)
                
            except Exception as e:
                success = False
                print(f"Pattern resolution error: {e}")
            
            end_time = time.perf_counter()
            end_memory = self.process.memory_info().rss / 1024 / 1024
            end_cpu = self.process.cpu_percent()
            
            result = BenchmarkResult(
                operation="pattern_resolution",
                latency_ms=(end_time - start_time) * 1000,
                memory_usage_mb=end_memory - start_memory,
                cpu_percent=max(start_cpu, end_cpu),
                success=success,
                metadata={
                    "input": pattern_input,
                    "expected": expected_agents,
                    "resolved": resolved_agents,
                    "iteration": i
                }
            )
            results.append(result)
        
        return results
    
    def benchmark_cache_effectiveness(self, iterations: int = 200) -> List[BenchmarkResult]:
        """Benchmark caching system effectiveness"""
        print(f"\n⚡ Benchmarking cache effectiveness ({iterations} iterations)...")
        results = []
        
        # Clear cache for baseline
        self._memory_cache.clear()
        self._pattern_cache.clear()
        
        cache_test_files = list(self.memory_dir.rglob("*.md"))
        
        for i in range(iterations):
            file_path = cache_test_files[i % len(cache_test_files)]
            cache_key = str(file_path)
            
            start_time = time.perf_counter()
            start_memory = self.process.memory_info().rss / 1024 / 1024
            start_cpu = self.process.cpu_percent()
            
            try:
                # Test cache hit/miss patterns
                is_cache_hit = cache_key in self._memory_cache
                
                if is_cache_hit:
                    content = self._memory_cache[cache_key]
                else:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    self._memory_cache[cache_key] = content
                
                success = len(content) > 0
                
            except Exception as e:
                success = False
                print(f"Cache test error: {e}")
            
            end_time = time.perf_counter()
            end_memory = self.process.memory_info().rss / 1024 / 1024
            end_cpu = self.process.cpu_percent()
            
            result = BenchmarkResult(
                operation="cache_access",
                latency_ms=(end_time - start_time) * 1000,
                memory_usage_mb=end_memory - start_memory,
                cpu_percent=max(start_cpu, end_cpu),
                success=success,
                metadata={
                    "file": str(file_path),
                    "cache_hit": is_cache_hit,
                    "cache_size": len(self._memory_cache),
                    "iteration": i
                }
            )
            results.append(result)
        
        return results
    
    def benchmark_concurrent_access(self, threads: int = 10, iterations_per_thread: int = 20) -> List[BenchmarkResult]:
        """Benchmark concurrent memory access performance"""
        print(f"\n⚙️ Benchmarking concurrent access ({threads} threads, {iterations_per_thread} iterations each)...")
        results = []
        
        def worker_thread(thread_id: int) -> List[BenchmarkResult]:
            """Worker thread for concurrent testing"""
            thread_results = []
            memory_files = list(self.memory_dir.rglob("*.md"))
            
            for i in range(iterations_per_thread):
                start_time = time.perf_counter()
                start_memory = self.process.memory_info().rss / 1024 / 1024
                start_cpu = self.process.cpu_percent()
                
                try:
                    # Concurrent memory access
                    file_path = memory_files[(thread_id + i) % len(memory_files)]
                    content = self._load_memory_file(file_path)
                    parsed = self._parse_memory_content(content)
                    
                    success = len(parsed) > 0
                    
                except Exception as e:
                    success = False
                    print(f"Concurrent access error (thread {thread_id}): {e}")
                
                end_time = time.perf_counter()
                end_memory = self.process.memory_info().rss / 1024 / 1024
                end_cpu = self.process.cpu_percent()
                
                result = BenchmarkResult(
                    operation="concurrent_access",
                    latency_ms=(end_time - start_time) * 1000,
                    memory_usage_mb=end_memory - start_memory,
                    cpu_percent=max(start_cpu, end_cpu),
                    success=success,
                    metadata={
                        "thread_id": thread_id,
                        "file": str(file_path),
                        "iteration": i
                    }
                )
                thread_results.append(result)
            
            return thread_results
        
        # Execute concurrent benchmark
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(worker_thread, i) for i in range(threads)]
            
            for future in as_completed(futures):
                try:
                    thread_results = future.result()
                    results.extend(thread_results)
                except Exception as e:
                    print(f"Thread execution error: {e}")
        
        return results
    
    def _load_memory_file(self, file_path: Path) -> str:
        """Load memory file with caching"""
        cache_key = str(file_path)
        
        if cache_key in self._memory_cache:
            return self._memory_cache[cache_key]
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        self._memory_cache[cache_key] = content
        return content
    
    def _parse_memory_content(self, content: str) -> Dict[str, Any]:
        """Parse memory content for patterns"""
        # Simplified parsing simulation
        lines = content.split('\n')
        patterns = {
            'agents': [line for line in lines if 'agent' in line.lower()],
            'patterns': [line for line in lines if 'pattern' in line.lower()],
            'coordination': [line for line in lines if 'coordination' in line.lower()],
            'performance': [line for line in lines if 'performance' in line.lower()]
        }
        return patterns
    
    def _resolve_agent_patterns(self, input_text: str) -> List[str]:
        """Simulate agent pattern resolution"""
        input_lower = input_text.lower()
        agents = []
        
        # Simple pattern matching simulation
        if 'async' in input_lower and 'test' in input_lower:
            agents.extend(['test-specialist', 'async-pattern-fixer'])
        if 'docker' in input_lower and 'infrastructure' in input_lower:
            agents.extend(['infrastructure-engineer', 'docker-specialist'])
        if 'security' in input_lower:
            agents.extend(['security-enforcer', 'security-auditor'])
        if 'coverage' in input_lower:
            agents.extend(['coverage-optimizer', 'test-specialist'])
        if 'performance' in input_lower:
            agents.extend(['performance-optimizer', 'resource-optimizer'])
        
        return list(set(agents))  # Remove duplicates
    
    def calculate_summary(self, results: List[BenchmarkResult], operation_type: str) -> BenchmarkSummary:
        """Calculate benchmark summary statistics"""
        if not results:
            return BenchmarkSummary(
                operation_type=operation_type,
                total_operations=0,
                avg_latency_ms=0, p50_latency_ms=0, p95_latency_ms=0, p99_latency_ms=0,
                success_rate=0, avg_memory_mb=0, peak_memory_mb=0,
                avg_cpu_percent=0, peak_cpu_percent=0
            )
        
        latencies = [r.latency_ms for r in results]
        memories = [r.memory_usage_mb for r in results]
        cpus = [r.cpu_percent for r in results]
        successes = [r.success for r in results]
        
        return BenchmarkSummary(
            operation_type=operation_type,
            total_operations=len(results),
            avg_latency_ms=statistics.mean(latencies),
            p50_latency_ms=statistics.median(latencies),
            p95_latency_ms=statistics.quantiles(latencies, n=20)[18] if len(latencies) > 1 else latencies[0],
            p99_latency_ms=statistics.quantiles(latencies, n=100)[98] if len(latencies) > 1 else latencies[0],
            success_rate=sum(successes) / len(successes),
            avg_memory_mb=statistics.mean(memories),
            peak_memory_mb=max(memories),
            avg_cpu_percent=statistics.mean(cpus),
            peak_cpu_percent=max(cpus)
        )
    
    def run_full_benchmark(self) -> Dict[str, BenchmarkSummary]:
        """Run complete benchmark suite"""
        print("\n🚀 Starting Memory Lookup Performance Benchmark Suite\n")
        print(f"📍 Project Directory: {self.project_dir}")
        print(f"🧠 Memory Directory: {self.memory_dir}")
        
        # System baseline
        print(f"\n📊 System Baseline:")
        print(f"   CPU Count: {psutil.cpu_count()} cores")
        print(f"   Memory Total: {psutil.virtual_memory().total / 1024 / 1024 / 1024:.1f} GB")
        print(f"   Memory Available: {psutil.virtual_memory().available / 1024 / 1024 / 1024:.1f} GB")
        
        summaries = {}
        
        # File Access Benchmark
        file_results = self.benchmark_file_access(iterations=100)
        summaries['file_access'] = self.calculate_summary(file_results, 'file_access')
        
        # Memory Lookup Benchmark
        lookup_results = self.benchmark_memory_lookup(iterations=50)
        summaries['memory_lookup'] = self.calculate_summary(lookup_results, 'memory_lookup')
        
        # Pattern Resolution Benchmark
        pattern_results = self.benchmark_pattern_resolution(iterations=100)
        summaries['pattern_resolution'] = self.calculate_summary(pattern_results, 'pattern_resolution')
        
        # Cache Effectiveness Benchmark
        cache_results = self.benchmark_cache_effectiveness(iterations=200)
        summaries['cache_effectiveness'] = self.calculate_summary(cache_results, 'cache_effectiveness')
        
        # Concurrent Access Benchmark
        concurrent_results = self.benchmark_concurrent_access(threads=10, iterations_per_thread=20)
        summaries['concurrent_access'] = self.calculate_summary(concurrent_results, 'concurrent_access')
        
        return summaries
    
    def generate_report(self, summaries: Dict[str, BenchmarkSummary]) -> str:
        """Generate comprehensive benchmark report"""
        report_lines = []
        
        report_lines.append("# Memory Lookup Performance Benchmark Report")
        report_lines.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Project: {self.project_dir.name}")
        report_lines.append("")
        
        report_lines.append("## Executive Summary")
        report_lines.append("")
        
        # Overall performance assessment
        total_ops = sum(s.total_operations for s in summaries.values())
        avg_success_rate = statistics.mean([s.success_rate for s in summaries.values()])
        avg_latency = statistics.mean([s.avg_latency_ms for s in summaries.values()])
        
        report_lines.append(f"- **Total Operations Tested**: {total_ops:,}")
        report_lines.append(f"- **Overall Success Rate**: {avg_success_rate:.1%}")
        report_lines.append(f"- **Average Latency**: {avg_latency:.2f}ms")
        report_lines.append("")
        
        # Performance targets from settings
        settings = self.load_settings()
        targets = settings.get('agents', {}).get('performance_targets', {})
        target_latency = targets.get('agent_selection_time_ms', 1000)
        
        if avg_latency <= target_latency:
            report_lines.append(f"✅ **Performance Target Met**: Average latency ({avg_latency:.2f}ms) is within target ({target_latency}ms)")
        else:
            report_lines.append(f"⚠️ **Performance Target Missed**: Average latency ({avg_latency:.2f}ms) exceeds target ({target_latency}ms)")
        
        report_lines.append("")
        
        # Detailed results for each benchmark
        for operation, summary in summaries.items():
            report_lines.append(f"## {operation.replace('_', ' ').title()} Results")
            report_lines.append("")
            
            report_lines.append(f"- **Operations**: {summary.total_operations:,}")
            report_lines.append(f"- **Success Rate**: {summary.success_rate:.1%}")
            report_lines.append("")
            
            report_lines.append("### Latency Metrics")
            report_lines.append(f"- Average: {summary.avg_latency_ms:.2f}ms")
            report_lines.append(f"- Median (P50): {summary.p50_latency_ms:.2f}ms")
            report_lines.append(f"- P95: {summary.p95_latency_ms:.2f}ms")
            report_lines.append(f"- P99: {summary.p99_latency_ms:.2f}ms")
            report_lines.append("")
            
            report_lines.append("### Resource Usage")
            report_lines.append(f"- Average Memory: {summary.avg_memory_mb:.2f}MB")
            report_lines.append(f"- Peak Memory: {summary.peak_memory_mb:.2f}MB")
            report_lines.append(f"- Average CPU: {summary.avg_cpu_percent:.1f}%")
            report_lines.append(f"- Peak CPU: {summary.peak_cpu_percent:.1f}%")
            report_lines.append("")
        
        # Performance Analysis
        report_lines.append("## Performance Analysis")
        report_lines.append("")
        
        # Cache effectiveness analysis
        cache_summary = summaries.get('cache_effectiveness')
        if cache_summary:
            cache_hit_improvement = cache_summary.p50_latency_ms
            file_access_p50 = summaries['file_access'].p50_latency_ms
            cache_improvement_pct = ((file_access_p50 - cache_hit_improvement) / file_access_p50) * 100
            
            report_lines.append(f"### Cache Effectiveness")
            report_lines.append(f"- Cache improves lookup speed by approximately {cache_improvement_pct:.1f}%")
            report_lines.append(f"- File access median: {file_access_p50:.2f}ms")
            report_lines.append(f"- Cached access median: {cache_hit_improvement:.2f}ms")
            report_lines.append("")
        
        # Concurrent performance analysis
        concurrent_summary = summaries.get('concurrent_access')
        single_summary = summaries.get('memory_lookup')
        if concurrent_summary and single_summary:
            concurrent_overhead = ((concurrent_summary.avg_latency_ms - single_summary.avg_latency_ms) / single_summary.avg_latency_ms) * 100
            
            report_lines.append(f"### Concurrent Access Performance")
            report_lines.append(f"- Concurrent access overhead: {concurrent_overhead:.1f}%")
            report_lines.append(f"- Single-threaded average: {single_summary.avg_latency_ms:.2f}ms")
            report_lines.append(f"- Multi-threaded average: {concurrent_summary.avg_latency_ms:.2f}ms")
            report_lines.append("")
        
        # Recommendations
        report_lines.append("## Recommendations")
        report_lines.append("")
        
        if avg_latency > target_latency:
            report_lines.append("### Performance Optimization")
            report_lines.append("- Consider implementing more aggressive caching strategies")
            report_lines.append("- Optimize memory file parsing algorithms")
            report_lines.append("- Pre-load frequently accessed patterns")
            report_lines.append("")
        
        if cache_summary and cache_summary.avg_latency_ms > 5.0:
            report_lines.append("### Cache Optimization")
            report_lines.append("- Implement memory-based caching for frequently accessed files")
            report_lines.append("- Consider LRU cache eviction policies")
            report_lines.append("- Add cache warming on system startup")
            report_lines.append("")
        
        if concurrent_summary and concurrent_summary.success_rate < 0.95:
            report_lines.append("### Concurrency Improvements")
            report_lines.append("- Add thread-safe memory access patterns")
            report_lines.append("- Implement proper resource locking")
            report_lines.append("- Consider connection pooling for file access")
            report_lines.append("")
        
        report_lines.append("## System Configuration")
        report_lines.append("")
        report_lines.append(f"- Memory files found: {len(list(self.memory_dir.rglob('*.md')))}")
        report_lines.append(f"- Cache size during test: {len(self._memory_cache)} entries")
        report_lines.append(f"- Pattern cache size: {len(self._pattern_cache)} entries")
        report_lines.append("")
        
        return "\n".join(report_lines)


def main():
    """Main benchmark execution"""
    project_dir = Path("/Users/ricardocarvalho/DeveloperFolder/DevMem")
    
    # Verify project structure
    if not project_dir.exists():
        print(f"❌ Project directory not found: {project_dir}")
        return
    
    memory_dir = project_dir / ".claude" / "memory"
    if not memory_dir.exists():
        print(f"❌ Memory directory not found: {memory_dir}")
        return
    
    # Initialize and run benchmarks
    benchmark = MemoryBenchmark(project_dir)
    
    try:
        summaries = benchmark.run_full_benchmark()
        report = benchmark.generate_report(summaries)
        
        # Save report
        report_file = project_dir / "memory_performance_benchmark_report.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"\n✅ Benchmark completed successfully!")
        print(f"📄 Report saved to: {report_file}")
        print("\n" + "="*80)
        print(report)
        
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        raise


if __name__ == "__main__":
    main()
