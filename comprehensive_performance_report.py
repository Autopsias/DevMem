#!/usr/bin/env python3
"""
Comprehensive Performance Report Generator

Consolidates all performance analysis results into a unified report with:
- Executive summary
- Detailed findings
- Optimization roadmap
- Implementation priorities
"""

import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Import analysis modules
try:
    from simple_performance_profiler import SimplePerformanceProfiler, ProfileSummary
    from critical_path_analyzer import CriticalPathAnalyzer, AnalysisResult
    from src.agent_selector import get_agent_selector
except ImportError as e:
    print(f"Warning: Could not import all modules: {e}")
    # Create mock classes for missing dependencies
    class MockProfiler:
        def run_performance_analysis(self, iterations=100):
            return None
    
    class MockAnalyzer:
        def run_comprehensive_analysis(self, iterations=50):
            return None
    
    SimplePerformanceProfiler = MockProfiler
    CriticalPathAnalyzer = MockAnalyzer

@dataclass
class PerformanceIssue:
    """Individual performance issue"""
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # bottleneck, memory, algorithm, etc.
    description: str
    impact_score: float  # 0-10 scale
    current_metric: str
    target_metric: str
    optimization_effort: str  # LOW, MEDIUM, HIGH
    recommendations: List[str]

@dataclass
class OptimizationOpportunity:
    """Specific optimization opportunity"""
    title: str
    description: str
    impact_potential: str  # HIGH, MEDIUM, LOW
    implementation_effort: str  # LOW, MEDIUM, HIGH
    priority_score: int  # 1-10
    technical_approach: List[str]
    expected_improvement: str
    risk_level: str  # LOW, MEDIUM, HIGH

@dataclass
class ComprehensivePerformanceReport:
    """Complete performance analysis report"""
    # Executive Summary
    overall_performance_score: float  # 0-100
    system_status: str  # OPTIMAL, GOOD, NEEDS_IMPROVEMENT, CRITICAL
    key_findings: List[str]
    
    # Performance Metrics
    current_performance: Dict[str, Any]
    target_performance: Dict[str, Any]
    performance_gaps: List[Dict[str, Any]]
    
    # Analysis Results
    performance_issues: List[PerformanceIssue]
    optimization_opportunities: List[OptimizationOpportunity]
    
    # Implementation Plan
    immediate_actions: List[str]
    short_term_optimizations: List[str]
    long_term_improvements: List[str]
    
    # Metadata
    analysis_timestamp: float
    analysis_version: str
    iterations_tested: int

class ComprehensivePerformanceAnalyzer:
    """Comprehensive performance analysis coordinator"""
    
    def __init__(self):
        self.profiler = SimplePerformanceProfiler()
        self.critical_analyzer = CriticalPathAnalyzer()
        
    def run_full_analysis(self, iterations: int = 150) -> ComprehensivePerformanceReport:
        """Run complete performance analysis suite"""
        print("Starting comprehensive performance analysis...")
        print(f"Testing with {iterations} iterations across multiple analysis types\n")
        
        # Run basic performance profiling
        print("Phase 1: Basic Performance Profiling")
        print("-" * 50)
        try:
            profile_summary = self.profiler.run_performance_analysis(iterations=iterations)
        except Exception as e:
            print(f"Warning: Basic profiling failed: {e}")
            profile_summary = None
        
        # Run critical path analysis
        print("\nPhase 2: Critical Path Analysis")
        print("-" * 50)
        try:
            critical_analysis = self.critical_analyzer.run_comprehensive_analysis(iterations=iterations//3)
        except Exception as e:
            print(f"Warning: Critical path analysis failed: {e}")
            critical_analysis = None
        
        # Consolidate results
        print("\nPhase 3: Consolidating Analysis Results")
        print("-" * 50)
        report = self._consolidate_analysis_results(profile_summary, critical_analysis, iterations)
        
        return report
    
    def _consolidate_analysis_results(self, profile_summary: Optional[ProfileSummary], 
                                    critical_analysis: Optional[AnalysisResult],
                                    iterations: int) -> ComprehensivePerformanceReport:
        """Consolidate all analysis results into comprehensive report"""
        
        # Calculate overall performance score
        overall_score = self._calculate_overall_performance_score(profile_summary, critical_analysis)
        
        # Determine system status
        system_status = self._determine_system_status(overall_score)
        
        # Extract key findings
        key_findings = self._extract_key_findings(profile_summary, critical_analysis)
        
        # Create performance metrics comparison
        current_performance, target_performance, gaps = self._create_performance_comparison(profile_summary, critical_analysis)
        
        # Identify performance issues
        performance_issues = self._identify_performance_issues(profile_summary, critical_analysis)
        
        # Identify optimization opportunities
        optimization_opportunities = self._identify_optimization_opportunities(profile_summary, critical_analysis)
        
        # Create implementation plan
        immediate, short_term, long_term = self._create_implementation_plan(performance_issues, optimization_opportunities)
        
        return ComprehensivePerformanceReport(
            overall_performance_score=overall_score,
            system_status=system_status,
            key_findings=key_findings,
            current_performance=current_performance,
            target_performance=target_performance,
            performance_gaps=gaps,
            performance_issues=performance_issues,
            optimization_opportunities=optimization_opportunities,
            immediate_actions=immediate,
            short_term_optimizations=short_term,
            long_term_improvements=long_term,
            analysis_timestamp=time.time(),
            analysis_version="1.0",
            iterations_tested=iterations
        )
    
    def _calculate_overall_performance_score(self, profile_summary: Optional[ProfileSummary], 
                                           critical_analysis: Optional[AnalysisResult]) -> float:
        """Calculate weighted overall performance score"""
        scores = []
        weights = []
        
        if profile_summary:
            # Basic performance score (weight: 40%)
            basic_score = 100
            if profile_summary.avg_execution_time > 25:
                basic_score -= 30
            elif profile_summary.avg_execution_time > 15:
                basic_score -= 15
            
            if profile_summary.percentile_95_time > 100:
                basic_score -= 20
            elif profile_summary.percentile_95_time > 50:
                basic_score -= 10
            
            if len(profile_summary.bottlenecks) > 3:
                basic_score -= 15
            elif len(profile_summary.bottlenecks) > 1:
                basic_score -= 5
                
            scores.append(max(basic_score, 0))
            weights.append(0.4)
        
        if critical_analysis:
            # Critical path score (weight: 60%)
            critical_score = critical_analysis.performance_score
            scores.append(critical_score)
            weights.append(0.6)
        
        if not scores:
            return 50.0  # Default middle score if no data
        
        # Calculate weighted average
        weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
        total_weight = sum(weights)
        
        return weighted_sum / total_weight if total_weight > 0 else 50.0
    
    def _determine_system_status(self, overall_score: float) -> str:
        """Determine system status based on overall score"""
        if overall_score >= 85:
            return "OPTIMAL"
        elif overall_score >= 70:
            return "GOOD"
        elif overall_score >= 50:
            return "NEEDS_IMPROVEMENT"
        else:
            return "CRITICAL"
    
    def _extract_key_findings(self, profile_summary: Optional[ProfileSummary], 
                            critical_analysis: Optional[AnalysisResult]) -> List[str]:
        """Extract key findings from analysis results"""
        findings = []
        
        if profile_summary:
            # Performance findings
            if profile_summary.avg_execution_time < 15:
                findings.append(f"Excellent response time: {profile_summary.avg_execution_time:.2f}ms average")
            elif profile_summary.avg_execution_time > 30:
                findings.append(f"Slow response time: {profile_summary.avg_execution_time:.2f}ms average (target: <25ms)")
            
            # Throughput findings
            if profile_summary.throughput_ops_per_sec > 1000:
                findings.append(f"High throughput achieved: {profile_summary.throughput_ops_per_sec:.0f} ops/sec")
            elif profile_summary.throughput_ops_per_sec < 100:
                findings.append(f"Low throughput: {profile_summary.throughput_ops_per_sec:.0f} ops/sec (target: >500 ops/sec)")
            
            # Bottleneck findings
            if len(profile_summary.bottlenecks) > 0:
                findings.append(f"Performance bottlenecks detected: {len(profile_summary.bottlenecks)} issues identified")
        
        if critical_analysis:
            # Critical path findings
            if critical_analysis.performance_score < 60:
                findings.append(f"Critical path analysis reveals significant optimization opportunities (score: {critical_analysis.performance_score:.0f}/100)")
            
            # Function-level findings
            if critical_analysis.top_time_consumers:
                top_func = critical_analysis.top_time_consumers[0]
                if top_func.percentage_of_total > 20:
                    findings.append(f"Single function dominance: {top_func.name} consumes {top_func.percentage_of_total:.1f}% of execution time")
        
        if not findings:
            findings.append("Performance analysis completed successfully with no major issues detected")
        
        return findings
    
    def _create_performance_comparison(self, profile_summary: Optional[ProfileSummary], 
                                     critical_analysis: Optional[AnalysisResult]) -> tuple:
        """Create current vs target performance comparison"""
        current = {}
        target = {
            'avg_execution_time_ms': 25.0,
            'percentile_95_time_ms': 100.0,
            'throughput_ops_per_sec': 500.0,
            'memory_efficiency_mb': 5.0,
            'bottleneck_count': 0,
            'performance_score': 85.0
        }
        gaps = []
        
        if profile_summary:
            current.update({
                'avg_execution_time_ms': profile_summary.avg_execution_time,
                'percentile_95_time_ms': profile_summary.percentile_95_time,
                'throughput_ops_per_sec': profile_summary.throughput_ops_per_sec,
                'memory_efficiency_mb': profile_summary.memory_analysis.get('total_memory_growth_mb', 0),
                'bottleneck_count': len(profile_summary.bottlenecks)
            })
        
        if critical_analysis:
            current['performance_score'] = critical_analysis.performance_score
        
        # Calculate gaps
        for metric, target_value in target.items():
            if metric in current:
                current_value = current[metric]
                if target_value == 0:
                    # Avoid division by zero
                    continue
                    
                if metric in ['avg_execution_time_ms', 'percentile_95_time_ms', 'memory_efficiency_mb', 'bottleneck_count']:
                    # Lower is better
                    if current_value > target_value:
                        gap_percentage = ((current_value - target_value) / target_value) * 100
                        gaps.append({
                            'metric': metric,
                            'current': current_value,
                            'target': target_value,
                            'gap_percentage': gap_percentage,
                            'status': 'NEEDS_IMPROVEMENT'
                        })
                else:
                    # Higher is better
                    if current_value < target_value:
                        gap_percentage = ((target_value - current_value) / target_value) * 100
                        gaps.append({
                            'metric': metric,
                            'current': current_value,
                            'target': target_value,
                            'gap_percentage': gap_percentage,
                            'status': 'NEEDS_IMPROVEMENT'
                        })
        
        return current, target, gaps
    
    def _identify_performance_issues(self, profile_summary: Optional[ProfileSummary], 
                                   critical_analysis: Optional[AnalysisResult]) -> List[PerformanceIssue]:
        """Identify specific performance issues"""
        issues = []
        
        if profile_summary:
            # Response time issues
            if profile_summary.avg_execution_time > 30:
                issues.append(PerformanceIssue(
                    severity="CRITICAL",
                    category="response_time",
                    description="Average response time exceeds acceptable limits",
                    impact_score=9.0,
                    current_metric=f"{profile_summary.avg_execution_time:.2f}ms",
                    target_metric="<25ms",
                    optimization_effort="HIGH",
                    recommendations=[
                        "Implement result caching for frequent queries",
                        "Optimize pattern matching algorithms",
                        "Consider async processing for complex queries"
                    ]
                ))
            elif profile_summary.avg_execution_time > 25:
                issues.append(PerformanceIssue(
                    severity="HIGH",
                    category="response_time",
                    description="Average response time approaching limits",
                    impact_score=6.0,
                    current_metric=f"{profile_summary.avg_execution_time:.2f}ms",
                    target_metric="<25ms",
                    optimization_effort="MEDIUM",
                    recommendations=[
                        "Profile and optimize slowest code paths",
                        "Implement early pattern matching for common cases"
                    ]
                ))
            
            # Consistency issues
            if profile_summary.percentile_95_time > profile_summary.avg_execution_time * 3:
                issues.append(PerformanceIssue(
                    severity="MEDIUM",
                    category="consistency",
                    description="High performance variance between requests",
                    impact_score=5.0,
                    current_metric=f"95th percentile: {profile_summary.percentile_95_time:.2f}ms",
                    target_metric="<2x average",
                    optimization_effort="MEDIUM",
                    recommendations=[
                        "Identify and optimize outlier cases",
                        "Implement consistent execution paths",
                        "Add performance monitoring for edge cases"
                    ]
                ))
        
        if critical_analysis:
            # Function-level bottlenecks
            if critical_analysis.top_time_consumers:
                top_func = critical_analysis.top_time_consumers[0]
                if top_func.percentage_of_total > 30:
                    issues.append(PerformanceIssue(
                        severity="CRITICAL",
                        category="algorithmic",
                        description=f"Single function consuming excessive CPU time: {top_func.name}",
                        impact_score=8.5,
                        current_metric=f"{top_func.percentage_of_total:.1f}% of total time",
                        target_metric="<20% per function",
                        optimization_effort="HIGH",
                        recommendations=[
                            f"Optimize {top_func.name} algorithm",
                            "Consider caching or memoization",
                            "Profile function internals for bottlenecks"
                        ]
                    ))
                elif top_func.percentage_of_total > 20:
                    issues.append(PerformanceIssue(
                        severity="HIGH",
                        category="algorithmic",
                        description=f"Function with high CPU usage: {top_func.name}",
                        impact_score=6.0,
                        current_metric=f"{top_func.percentage_of_total:.1f}% of total time",
                        target_metric="<20% per function",
                        optimization_effort="MEDIUM",
                        recommendations=[
                            f"Review {top_func.name} implementation",
                            "Consider algorithmic improvements"
                        ]
                    ))
        
        return issues
    
    def _identify_optimization_opportunities(self, profile_summary: Optional[ProfileSummary], 
                                           critical_analysis: Optional[AnalysisResult]) -> List[OptimizationOpportunity]:
        """Identify specific optimization opportunities"""
        opportunities = []
        
        if profile_summary:
            # Caching opportunities
            if profile_summary.throughput_ops_per_sec > 1000:  # High throughput suggests repeated patterns
                opportunities.append(OptimizationOpportunity(
                    title="Pattern Matching Result Caching",
                    description="High throughput indicates repeated query patterns that could benefit from caching",
                    impact_potential="HIGH",
                    implementation_effort="MEDIUM",
                    priority_score=8,
                    technical_approach=[
                        "Implement LRU cache for pattern matching results",
                        "Cache agent selection decisions for similar queries",
                        "Add cache hit/miss metrics for monitoring"
                    ],
                    expected_improvement="30-50% response time reduction for cached queries",
                    risk_level="LOW"
                ))
            
            # Early termination opportunities
            if any("edge case" in opp.lower() for opp in profile_summary.optimization_opportunities):
                opportunities.append(OptimizationOpportunity(
                    title="Early Pattern Recognition",
                    description="Optimize edge case handling with early pattern recognition",
                    impact_potential="MEDIUM",
                    implementation_effort="MEDIUM",
                    priority_score=6,
                    technical_approach=[
                        "Implement fast-path detection for common patterns",
                        "Add early termination for obvious matches",
                        "Optimize keyword index lookup performance"
                    ],
                    expected_improvement="15-25% response time reduction",
                    risk_level="LOW"
                ))
        
        if critical_analysis:
            # Algorithmic optimizations
            if critical_analysis.optimization_hotspots:
                high_impact_hotspots = [h for h in critical_analysis.optimization_hotspots if h['optimization_potential'] == 'HIGH']
                if len(high_impact_hotspots) >= 2:
                    opportunities.append(OptimizationOpportunity(
                        title="Core Algorithm Optimization",
                        description=f"Multiple high-impact bottlenecks detected ({len(high_impact_hotspots)} functions)",
                        impact_potential="HIGH",
                        implementation_effort="HIGH",
                        priority_score=9,
                        technical_approach=[
                            "Refactor core pattern matching algorithms",
                            "Implement more efficient data structures",
                            "Optimize regular expression usage",
                            "Consider parallel processing for independent operations"
                        ],
                        expected_improvement="50-70% overall performance improvement",
                        risk_level="MEDIUM"
                    ))
            
            # Memory optimization
            if any(path.optimization_potential > 0.01 for path in critical_analysis.critical_paths):
                opportunities.append(OptimizationOpportunity(
                    title="Memory Usage Optimization",
                    description="Critical paths showing memory allocation bottlenecks",
                    impact_potential="MEDIUM",
                    implementation_effort="MEDIUM",
                    priority_score=5,
                    technical_approach=[
                        "Reduce object creation in hot paths",
                        "Implement object pooling for frequently used objects",
                        "Optimize data structure choices"
                    ],
                    expected_improvement="10-20% memory efficiency improvement",
                    risk_level="LOW"
                ))
        
        # Sort by priority score
        opportunities.sort(key=lambda x: x.priority_score, reverse=True)
        
        return opportunities
    
    def _create_implementation_plan(self, issues: List[PerformanceIssue], 
                                  opportunities: List[OptimizationOpportunity]) -> tuple:
        """Create prioritized implementation plan"""
        immediate = []
        short_term = []
        long_term = []
        
        # Immediate actions (critical issues)
        critical_issues = [issue for issue in issues if issue.severity == "CRITICAL"]
        for issue in critical_issues:
            immediate.extend(issue.recommendations[:2])  # Top 2 recommendations per critical issue
        
        # Short-term optimizations (high-impact, medium effort)
        high_impact_opportunities = [opp for opp in opportunities if opp.impact_potential == "HIGH" and opp.implementation_effort in ["LOW", "MEDIUM"]]
        for opp in high_impact_opportunities[:3]:  # Top 3
            short_term.extend(opp.technical_approach[:2])
        
        # Medium priority issues
        medium_issues = [issue for issue in issues if issue.severity in ["HIGH", "MEDIUM"]]
        for issue in medium_issues[:2]:  # Top 2 medium issues
            short_term.extend(issue.recommendations[:1])
        
        # Long-term improvements
        high_effort_opportunities = [opp for opp in opportunities if opp.implementation_effort == "HIGH"]
        for opp in high_effort_opportunities:
            long_term.extend(opp.technical_approach)
        
        # Add strategic improvements
        long_term.extend([
            "Implement comprehensive monitoring and alerting system",
            "Develop performance regression testing suite",
            "Consider architectural improvements for scalability",
            "Evaluate alternative algorithms and data structures"
        ])
        
        return immediate[:5], short_term[:8], long_term[:6]  # Limit to manageable numbers
    
    def print_comprehensive_report(self, report: ComprehensivePerformanceReport):
        """Print detailed comprehensive performance report"""
        print("\n" + "=" * 140)
        print("COMPREHENSIVE AGENT SELECTION SYSTEM PERFORMANCE ANALYSIS")
        print("=" * 140)
        
        # Executive Summary
        print("\n📊 EXECUTIVE SUMMARY")
        print(f"  Overall Performance Score: {report.overall_performance_score:.1f}/100")
        print(f"  System Status: {report.system_status}")
        print(f"  Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(report.analysis_timestamp))}")
        print(f"  Test Iterations: {report.iterations_tested:,}")
        
        # Status indicator
        status_indicators = {
            "OPTIMAL": "🎉 System performing excellently",
            "GOOD": "✅ System performing well with minor optimization opportunities",
            "NEEDS_IMPROVEMENT": "⚠️  System needs performance improvements",
            "CRITICAL": "🚨 System requires immediate optimization"
        }
        print(f"  {status_indicators.get(report.system_status, 'Unknown status')}")
        
        print("\n🔍 KEY FINDINGS:")
        for i, finding in enumerate(report.key_findings, 1):
            print(f"  {i}. {finding}")
        
        # Performance Metrics
        print("\n📊 PERFORMANCE METRICS COMPARISON:")
        print(f"  {'Metric':<30} {'Current':<15} {'Target':<15} {'Status':<15}")
        print(f"  {'-' * 30} {'-' * 15} {'-' * 15} {'-' * 15}")
        
        for metric, current_val in report.current_performance.items():
            target_val = report.target_performance.get(metric, 'N/A')
            
            # Find gap status
            gap_info = next((gap for gap in report.performance_gaps if gap['metric'] == metric), None)
            status = gap_info['status'] if gap_info else '✅ MEETS TARGET'
            
            print(f"  {metric:<30} {str(current_val):<15} {str(target_val):<15} {status:<15}")
        
        # Performance Issues
        print("\n⚠️  PERFORMANCE ISSUES IDENTIFIED:")
        if report.performance_issues:
            for i, issue in enumerate(report.performance_issues, 1):
                severity_indicators = {
                    "CRITICAL": "🚨",
                    "HIGH": "🔴",
                    "MEDIUM": "🟡",
                    "LOW": "🟢"
                }
                indicator = severity_indicators.get(issue.severity, "❓")
                
                print(f"  {i:2d}. {indicator} [{issue.severity}] {issue.description}")
                print(f"      Category: {issue.category.title()}")
                print(f"      Current: {issue.current_metric} | Target: {issue.target_metric}")
                print(f"      Impact Score: {issue.impact_score}/10 | Effort: {issue.optimization_effort}")
                print("      Top Recommendations:")
                for rec in issue.recommendations[:2]:
                    print(f"        • {rec}")
                print()
        else:
            print("  ✅ No significant performance issues detected")
        
        # Optimization Opportunities
        print("💡 OPTIMIZATION OPPORTUNITIES:")
        if report.optimization_opportunities:
            for i, opp in enumerate(report.optimization_opportunities, 1):
                impact_indicators = {
                    "HIGH": "🔥",
                    "MEDIUM": "🟡",
                    "LOW": "🟢"
                }
                indicator = impact_indicators.get(opp.impact_potential, "❓")
                
                print(f"  {i:2d}. {indicator} {opp.title} (Priority: {opp.priority_score}/10)")
                print(f"      {opp.description}")
                print(f"      Impact: {opp.impact_potential} | Effort: {opp.implementation_effort} | Risk: {opp.risk_level}")
                print(f"      Expected Improvement: {opp.expected_improvement}")
                print("      Key Approaches:")
                for approach in opp.technical_approach[:2]:
                    print(f"        • {approach}")
                print()
        else:
            print("  ✅ System is well-optimized - no major opportunities identified")
        
        # Implementation Roadmap
        print("🛣️  IMPLEMENTATION ROADMAP:")
        
        print("  IMMEDIATE ACTIONS (This Week):")
        if report.immediate_actions:
            for action in report.immediate_actions:
                print(f"    • {action}")
        else:
            print("    ✅ No immediate actions required")
        
        print("\n  SHORT-TERM OPTIMIZATIONS (Next 1-2 Months):")
        if report.short_term_optimizations:
            for optimization in report.short_term_optimizations:
                print(f"    • {optimization}")
        else:
            print("    ✅ No short-term optimizations identified")
        
        print("\n  LONG-TERM IMPROVEMENTS (Next 3-6 Months):")
        if report.long_term_improvements:
            for improvement in report.long_term_improvements:
                print(f"    • {improvement}")
        else:
            print("    ✅ System architecture is solid for long-term")
        
        # Performance Targets
        print("\n🎯 PERFORMANCE TARGETS:")
        print("  • Response Time: <25ms average, <100ms 95th percentile")
        print("  • Throughput: >500 operations per second")
        print("  • Memory Efficiency: <5MB growth per batch")
        print("  • Consistency: <2x variance between min/max response times")
        print("  • Reliability: >99.5% successful agent selections")
        
        # Next Steps
        print("\n📝 RECOMMENDED NEXT STEPS:")
        print("  1. Address immediate performance issues identified above")
        print("  2. Implement top 2-3 optimization opportunities")
        print("  3. Set up continuous performance monitoring")
        print("  4. Create performance regression testing suite")
        print("  5. Schedule regular performance reviews (monthly)")
        
        print("=" * 140)
    
    def save_report(self, report: ComprehensivePerformanceReport, filename: str = "comprehensive_performance_report.json"):
        """Save comprehensive report to JSON file"""
        # Convert to serializable format
        report_dict = asdict(report)
        
        with open(filename, 'w') as f:
            json.dump(report_dict, f, indent=2, default=str)
        
        print(f"\nComprehensive performance report saved to: {filename}")

def main():
    """Main execution for comprehensive performance analysis"""
    analyzer = ComprehensivePerformanceAnalyzer()
    
    # Run full analysis
    report = analyzer.run_full_analysis(iterations=200)
    
    # Print comprehensive report
    analyzer.print_comprehensive_report(report)
    
    # Save report
    analyzer.save_report(report)
    
    return report

if __name__ == "__main__":
    main()
