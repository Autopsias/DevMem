#!/usr/bin/env python3
"""
Critical Path Analysis for Agent Selection System

Deep analysis of performance bottlenecks focusing on:
- Function-level profiling
- Critical execution paths
- Resource usage patterns
- Optimization hotspots
"""

import time
import cProfile
import pstats
import io
import sys
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from pathlib import Path
from collections import defaultdict

# Import agent selector
try:
    from src.agent_selector import EnhancedAgentSelector, get_agent_selector
    MOCK_MODE = False
except ImportError:
    print("Warning: Using mock agent selector for analysis")
    MOCK_MODE = True
    
    class MockResult:
        def __init__(self):
            self.agent_name = "test-specialist"
            self.confidence_score = 0.8
            self.matched_patterns = []
            self.processing_time_ms = 5.0
            self.context_keywords = []
            self.reasoning = "Mock selection"
    
    class MockAgentSelector:
        def __init__(self):
            self.agents = {}
            self.keyword_index = {}
            self.pattern_cache = {}
            self.selection_history = []
            
        def select_agent(self, query: str, context=None):
            # Simulate different processing paths
            if len(query) > 100:
                time.sleep(0.008)  # Complex query
            elif len(query) < 5:
                time.sleep(0.012)  # Edge case handling
            else:
                time.sleep(0.003)  # Normal processing
            return MockResult()
    
    def get_agent_selector():
        return MockAgentSelector()

@dataclass
class FunctionProfile:
    """Profile data for a single function"""
    name: str
    filename: str
    line_number: int
    total_time: float
    cumulative_time: float
    call_count: int
    time_per_call: float
    percentage_of_total: float

@dataclass
class CriticalPath:
    """Critical execution path analysis"""
    path_name: str
    total_time: float
    function_sequence: List[FunctionProfile]
    bottleneck_functions: List[FunctionProfile]
    optimization_potential: float

@dataclass
class AnalysisResult:
    """Complete critical path analysis results"""
    total_execution_time: float
    total_function_calls: int
    critical_paths: List[CriticalPath]
    top_time_consumers: List[FunctionProfile]
    optimization_hotspots: List[Dict[str, Any]]
    recommendations: List[str]
    performance_score: float

class CriticalPathAnalyzer:
    """Advanced critical path analysis for agent selection system"""
    
    def __init__(self):
        self.selector = get_agent_selector()
        self.profile_data = None
        
    def create_analysis_queries(self) -> List[Tuple[str, str, str]]:
        """Create queries designed to exercise different code paths"""
        return [
            # Fast path queries - should hit keyword index quickly
            ("test", "fast_path", "Single keyword, should hit index fast"),
            ("docker", "fast_path", "Infrastructure keyword, index lookup"),
            ("security", "fast_path", "Security keyword, direct match"),
            
            # Medium complexity - pattern matching
            ("test failures with async", "pattern_match", "Multiple keywords, pattern evaluation"),
            ("docker container issues", "pattern_match", "Domain-specific pattern matching"),
            ("security vulnerability scan", "pattern_match", "Security pattern recognition"),
            
            # Complex analysis - full processing pipeline
            ("Complex multi-domain analysis requiring testing infrastructure and security coordination", "full_pipeline", "Multi-domain, full context analysis"),
            ("Performance bottlenecks affecting user experience with security implications", "full_pipeline", "Complex context evaluation"),
            
            # Edge cases - fallback processing
            ("", "edge_case", "Empty query, fallback logic"),
            ("?", "edge_case", "Minimal input, edge handling"),
            ("help me with something", "edge_case", "Vague query, requires inference"),
            ("x" * 300, "edge_case", "Very long query, stress test"),
            
            # Cache behavior tests
            ("pytest mock fixture", "cache_test", "Repeated technical query"),
            ("kubernetes deployment", "cache_test", "Repeated infrastructure query"),
        ]
    
    def profile_execution_paths(self, iterations: int = 50) -> pstats.Stats:
        """Profile different execution paths with detailed function-level analysis"""
        queries = self.create_analysis_queries()
        
        # Create profiler
        profiler = cProfile.Profile()
        
        print(f"Profiling {len(queries)} query types with {iterations} iterations each...")
        
        # Profile execution
        profiler.enable()
        
        for iteration in range(iterations):
            for query, path_type, description in queries:
                # Execute agent selection
                self.selector.select_agent(query)
                
                # Add some variance to simulate real usage
                if iteration % 10 == 0:
                    time.sleep(0.0001)  # Simulate occasional system load
        
        profiler.disable()
        
        # Analyze results
        stats = pstats.Stats(profiler)
        return stats
    
    def analyze_function_profiles(self, stats: pstats.Stats) -> List[FunctionProfile]:
        """Extract and analyze function-level performance data"""
        function_profiles = []
        
        # Get total time for percentage calculations
        total_time = stats.total_tt
        
        # Extract function statistics
        for func_key, (cc, nc, tt, ct, callers) in stats.stats.items():
            filename, line_number, func_name = func_key
            
            # Skip built-in functions and focus on our code
            if not filename.endswith('.py') or '/site-packages/' in filename:
                continue
                
            # Calculate derived metrics
            time_per_call = tt / cc if cc > 0 else 0
            percentage = (tt / total_time * 100) if total_time > 0 else 0
            
            function_profiles.append(FunctionProfile(
                name=func_name,
                filename=filename.split('/')[-1],  # Just filename, not full path
                line_number=line_number,
                total_time=tt,
                cumulative_time=ct,
                call_count=cc,
                time_per_call=time_per_call,
                percentage_of_total=percentage
            ))
        
        # Sort by total time descending
        function_profiles.sort(key=lambda x: x.total_time, reverse=True)
        
        return function_profiles
    
    def identify_critical_paths(self, function_profiles: List[FunctionProfile]) -> List[CriticalPath]:
        """Identify critical execution paths and bottlenecks"""
        critical_paths = []
        
        # Group functions by logical execution paths
        path_groups = {
            'Agent Selection Core': [],
            'Pattern Matching': [],
            'Context Analysis': [], 
            'Keyword Processing': [],
            'Fallback Logic': []
        }
        
        # Categorize functions into logical paths
        for profile in function_profiles:
            func_name_lower = profile.name.lower()
            
            if any(keyword in func_name_lower for keyword in ['select_agent', 'get_agent']):
                path_groups['Agent Selection Core'].append(profile)
            elif any(keyword in func_name_lower for keyword in ['pattern', 'match', 'regex']):
                path_groups['Pattern Matching'].append(profile)
            elif any(keyword in func_name_lower for keyword in ['context', 'analyze', 'calculate']):
                path_groups['Context Analysis'].append(profile)
            elif any(keyword in func_name_lower for keyword in ['keyword', 'extract', 'index']):
                path_groups['Keyword Processing'].append(profile)
            elif any(keyword in func_name_lower for keyword in ['fallback', 'default', 'detect']):
                path_groups['Fallback Logic'].append(profile)
        
        # Create critical path analysis for each group
        for path_name, functions in path_groups.items():
            if not functions:
                continue
                
            # Calculate path metrics
            total_path_time = sum(f.total_time for f in functions)
            
            # Identify bottlenecks (functions taking >10% of path time)
            bottlenecks = [f for f in functions if f.total_time > total_path_time * 0.1]
            
            # Calculate optimization potential (time in bottleneck functions)
            optimization_potential = sum(f.total_time for f in bottlenecks)
            
            critical_paths.append(CriticalPath(
                path_name=path_name,
                total_time=total_path_time,
                function_sequence=functions[:10],  # Top 10 functions in path
                bottleneck_functions=bottlenecks,
                optimization_potential=optimization_potential
            ))
        
        # Sort by total time descending
        critical_paths.sort(key=lambda x: x.total_time, reverse=True)
        
        return critical_paths
    
    def identify_optimization_hotspots(self, function_profiles: List[FunctionProfile],
                                     critical_paths: List[CriticalPath]) -> List[Dict[str, Any]]:
        """Identify specific optimization opportunities"""
        hotspots = []
        
        # High-frequency, high-time functions
        for profile in function_profiles[:15]:  # Top 15 functions
            if profile.call_count > 100 and profile.total_time > 0.001:  # Frequent and slow
                hotspots.append({
                    'type': 'High Frequency Bottleneck',
                    'function': profile.name,
                    'location': f"{profile.filename}:{profile.line_number}",
                    'impact': profile.total_time,
                    'call_count': profile.call_count,
                    'time_per_call': profile.time_per_call,
                    'optimization_potential': 'HIGH',
                    'recommendation': f"Optimize {profile.name} - called {profile.call_count} times, {profile.time_per_call:.6f}s per call"
                })
        
        # Low-frequency, high-time functions (possibly complex algorithms)
        for profile in function_profiles:
            if profile.call_count < 50 and profile.time_per_call > 0.001:  # Infrequent but slow
                hotspots.append({
                    'type': 'Complex Algorithm',
                    'function': profile.name,
                    'location': f"{profile.filename}:{profile.line_number}",
                    'impact': profile.total_time,
                    'call_count': profile.call_count,
                    'time_per_call': profile.time_per_call,
                    'optimization_potential': 'MEDIUM',
                    'recommendation': f"Review {profile.name} algorithm - {profile.time_per_call:.6f}s per call"
                })
        
        # Critical path bottlenecks
        for path in critical_paths:
            if path.optimization_potential > 0.005:  # Significant optimization potential
                hotspots.append({
                    'type': 'Critical Path Bottleneck',
                    'function': path.path_name,
                    'location': 'Multiple functions',
                    'impact': path.optimization_potential,
                    'call_count': len(path.bottleneck_functions),
                    'time_per_call': path.optimization_potential / len(path.bottleneck_functions) if path.bottleneck_functions else 0,
                    'optimization_potential': 'HIGH',
                    'recommendation': f"Optimize {path.path_name} critical path - {len(path.bottleneck_functions)} bottleneck functions"
                })
        
        # Sort by impact descending
        hotspots.sort(key=lambda x: x['impact'], reverse=True)
        
        return hotspots[:10]  # Top 10 hotspots
    
    def generate_optimization_recommendations(self, function_profiles: List[FunctionProfile],
                                           critical_paths: List[CriticalPath],
                                           hotspots: List[Dict[str, Any]]) -> List[str]:
        """Generate specific, actionable optimization recommendations"""
        recommendations = []
        
        # Overall performance assessment
        total_time = sum(f.total_time for f in function_profiles)
        if total_time > 1.0:  # > 1 second total time in profiling
            recommendations.append(f"CRITICAL: Total execution time ({total_time:.3f}s) is high - investigate major bottlenecks")
        
        # Function-specific recommendations
        top_functions = function_profiles[:5]
        for func in top_functions:
            if func.percentage_of_total > 20:  # Single function taking >20% of time
                recommendations.append(f"HIGH PRIORITY: {func.name} consumes {func.percentage_of_total:.1f}% of execution time - critical optimization target")
            elif func.call_count > 500 and func.time_per_call > 0.0001:
                recommendations.append(f"MEDIUM PRIORITY: {func.name} called {func.call_count} times - consider caching or algorithm optimization")
        
        # Critical path recommendations
        for path in critical_paths[:3]:  # Top 3 paths
            if path.optimization_potential > 0.01:  # >10ms optimization potential
                recommendations.append(f"OPTIMIZE PATH: {path.path_name} has {path.optimization_potential:.3f}s optimization potential")
        
        # Hotspot recommendations
        for hotspot in hotspots[:3]:  # Top 3 hotspots
            if hotspot['optimization_potential'] == 'HIGH':
                recommendations.append(f"HOTSPOT: {hotspot['recommendation']}")
        
        # Pattern-specific recommendations
        pattern_functions = [f for f in function_profiles if 'pattern' in f.name.lower() or 'match' in f.name.lower()]
        if pattern_functions:
            total_pattern_time = sum(f.total_time for f in pattern_functions)
            if total_pattern_time > total_time * 0.3:  # Pattern matching >30% of time
                recommendations.append("ALGORITHM: Pattern matching consumes significant time - consider regex optimization or caching")
        
        # Memory/IO recommendations (based on function names)
        io_functions = [f for f in function_profiles if any(keyword in f.name.lower() for keyword in ['read', 'write', 'load', 'save'])]
        if io_functions:
            total_io_time = sum(f.total_time for f in io_functions)
            if total_io_time > total_time * 0.2:  # IO >20% of time
                recommendations.append("IO OPTIMIZATION: File/memory operations consume significant time - consider caching or lazy loading")
        
        # Fallback recommendations
        if not recommendations:
            recommendations.append("MONITORING: Performance appears optimal - continue regular profiling to detect regressions")
        
        return recommendations
    
    def calculate_performance_score(self, function_profiles: List[FunctionProfile],
                                  critical_paths: List[CriticalPath],
                                  hotspots: List[Dict[str, Any]]) -> float:
        """Calculate overall performance score (0-100)"""
        score = 100.0
        
        # Deduct for high time-consuming functions
        for func in function_profiles[:5]:
            if func.percentage_of_total > 30:
                score -= 20  # Major bottleneck
            elif func.percentage_of_total > 15:
                score -= 10  # Significant bottleneck
            elif func.percentage_of_total > 5:
                score -= 5   # Minor bottleneck
        
        # Deduct for critical path issues
        for path in critical_paths:
            if path.optimization_potential > 0.01:
                score -= 10
            elif path.optimization_potential > 0.005:
                score -= 5
        
        # Deduct for high-impact hotspots
        high_impact_hotspots = [h for h in hotspots if h['optimization_potential'] == 'HIGH']
        score -= len(high_impact_hotspots) * 5
        
        return max(score, 0.0)
    
    def run_comprehensive_analysis(self, iterations: int = 100) -> AnalysisResult:
        """Run complete critical path analysis"""
        print("Starting comprehensive critical path analysis...")
        
        # Profile execution
        print("Profiling execution paths...")
        stats = self.profile_execution_paths(iterations)
        
        # Analyze function profiles
        print("Analyzing function profiles...")
        function_profiles = self.analyze_function_profiles(stats)
        
        # Identify critical paths
        print("Identifying critical paths...")
        critical_paths = self.identify_critical_paths(function_profiles)
        
        # Find optimization hotspots
        print("Identifying optimization hotspots...")
        hotspots = self.identify_optimization_hotspots(function_profiles, critical_paths)
        
        # Generate recommendations
        print("Generating optimization recommendations...")
        recommendations = self.generate_optimization_recommendations(function_profiles, critical_paths, hotspots)
        
        # Calculate performance score
        performance_score = self.calculate_performance_score(function_profiles, critical_paths, hotspots)
        
        return AnalysisResult(
            total_execution_time=stats.total_tt,
            total_function_calls=stats.total_calls,
            critical_paths=critical_paths,
            top_time_consumers=function_profiles[:10],
            optimization_hotspots=hotspots,
            recommendations=recommendations,
            performance_score=performance_score
        )
    
    def print_detailed_analysis_report(self, result: AnalysisResult):
        """Print comprehensive critical path analysis report"""
        print("\n" + "=" * 120)
        print("CRITICAL PATH ANALYSIS - AGENT SELECTION SYSTEM")
        print("=" * 120)
        
        print(f"\n📊 EXECUTION OVERVIEW:")
        print(f"  Total Execution Time: {result.total_execution_time:.6f} seconds")
        print(f"  Total Function Calls: {result.total_function_calls:,}")
        print(f"  Average Time Per Call: {result.total_execution_time/result.total_function_calls:.9f} seconds")
        print(f"  Performance Score: {result.performance_score:.1f}/100")
        
        print(f"\n🔥 TOP TIME CONSUMERS:")
        for i, func in enumerate(result.top_time_consumers, 1):
            print(f"  {i:2d}. {func.name}")
            print(f"      Location: {func.filename}:{func.line_number}")
            print(f"      Total Time: {func.total_time:.6f}s ({func.percentage_of_total:.1f}% of total)")
            print(f"      Calls: {func.call_count:,} | Time/Call: {func.time_per_call:.9f}s")
            print()
        
        print(f"🛤️  CRITICAL EXECUTION PATHS:")
        for i, path in enumerate(result.critical_paths, 1):
            print(f"  {i}. {path.path_name}")
            print(f"     Total Time: {path.total_time:.6f}s")
            print(f"     Functions: {len(path.function_sequence)}")
            print(f"     Bottlenecks: {len(path.bottleneck_functions)}")
            print(f"     Optimization Potential: {path.optimization_potential:.6f}s")
            
            if path.bottleneck_functions:
                print(f"     Top Bottlenecks:")
                for bottleneck in path.bottleneck_functions[:3]:
                    print(f"       - {bottleneck.name}: {bottleneck.total_time:.6f}s")
            print()
        
        print(f"🎯 OPTIMIZATION HOTSPOTS:")
        for i, hotspot in enumerate(result.optimization_hotspots, 1):
            print(f"  {i:2d}. {hotspot['type']}: {hotspot['function']}")
            print(f"      Location: {hotspot['location']}")
            print(f"      Impact: {hotspot['impact']:.6f}s | Calls: {hotspot['call_count']}")
            print(f"      Priority: {hotspot['optimization_potential']}")
            print(f"      Action: {hotspot['recommendation']}")
            print()
        
        print(f"📝 OPTIMIZATION RECOMMENDATIONS:")
        for i, rec in enumerate(result.recommendations, 1):
            print(f"  {i:2d}. {rec}")
        
        # Performance assessment
        print(f"\n" + "=" * 120)
        print("PERFORMANCE ASSESSMENT:")
        
        if result.performance_score >= 90:
            print("  🎉 EXCELLENT: Performance is optimal with minimal bottlenecks")
        elif result.performance_score >= 75:
            print("  ✅ GOOD: Performance is acceptable with minor optimization opportunities")
        elif result.performance_score >= 60:
            print("  ⚠️  MODERATE: Performance has room for improvement with identified bottlenecks")
        else:
            print("  🚨 POOR: Performance needs significant optimization")
        
        # Key insights
        print(f"\nKEY INSIGHTS:")
        top_func = result.top_time_consumers[0] if result.top_time_consumers else None
        if top_func and top_func.percentage_of_total > 20:
            print(f"  • Single function dominance: {top_func.name} consumes {top_func.percentage_of_total:.1f}% of execution time")
        
        high_impact_paths = [p for p in result.critical_paths if p.optimization_potential > 0.01]
        if high_impact_paths:
            print(f"  • Critical path bottlenecks: {len(high_impact_paths)} paths with significant optimization potential")
        
        high_priority_hotspots = [h for h in result.optimization_hotspots if h['optimization_potential'] == 'HIGH']
        if high_priority_hotspots:
            print(f"  • High-priority optimizations: {len(high_priority_hotspots)} functions require immediate attention")
        
        print("=" * 120)

def main():
    """Main execution for critical path analysis"""
    analyzer = CriticalPathAnalyzer()
    
    # Run comprehensive analysis
    result = analyzer.run_comprehensive_analysis(iterations=50)
    
    # Print detailed report
    analyzer.print_detailed_analysis_report(result)
    
    return result

if __name__ == "__main__":
    main()
