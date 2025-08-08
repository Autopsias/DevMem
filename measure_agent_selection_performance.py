#!/usr/bin/env python3
"""
Agent Selection Performance Measurement System

Measures and benchmarks agent selection accuracy, response time,
and context preservation for the Enhanced Pattern Recognition System.

Usage:
    python measure_agent_selection_performance.py --mode [baseline|enhanced|comparison]
    python measure_agent_selection_performance.py --benchmark --iterations 100
"""

import argparse
import json
import time
import statistics
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
from enhanced_pattern_recognition import (
    EnhancedPatternRecognitionSystem, 
    SuccessMetrics,
    PatternConfidence
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class TestCase:
    """Test case for agent selection benchmarking"""
    input_text: str
    expected_agent: str
    expected_domains: List[str]
    expected_coordination: str
    difficulty_level: str  # "easy", "medium", "hard", "edge_case"
    description: str

@dataclass
class BenchmarkResult:
    """Result of a single benchmark test"""
    test_case: TestCase
    selected_agent: str
    confidence: float
    response_time: float
    accuracy_score: float  # 0.0 to 1.0
    context_preservation: float
    domains_detected: Dict[str, float]
    coordination_detected: str
    validation_issues: List[str]
    details: Dict[str, Any]

@dataclass
class PerformanceReport:
    """Comprehensive performance report"""
    total_tests: int
    accuracy_rate: float
    avg_response_time: float
    avg_confidence: float
    context_preservation_rate: float
    difficulty_breakdown: Dict[str, Dict[str, float]]
    agent_performance: Dict[str, Dict[str, float]]
    pattern_effectiveness: Dict[str, float]
    edge_case_handling: float
    recommendations: List[str]

class AgentSelectionBenchmark:
    """Benchmark suite for agent selection performance"""
    
    def __init__(self):
        self.enhanced_system = EnhancedPatternRecognitionSystem()
        self.test_cases = self._create_test_cases()
        
    def _create_test_cases(self) -> List[TestCase]:
        """Create comprehensive test cases for benchmarking"""
        return [
            # Easy cases - explicit patterns
            TestCase(
                input_text="Coordinating comprehensive analysis using 3 tasks in parallel: security assessment, performance analysis, testing evaluation",
                expected_agent="analysis-gateway",
                expected_domains=["security", "performance", "testing"],
                expected_coordination="parallel",
                difficulty_level="easy",
                description="Explicit parallel coordination with clear domains"
            ),
            TestCase(
                input_text="Test failures with pytest async patterns and mock configuration",
                expected_agent="test-specialist",
                expected_domains=["testing"],
                expected_coordination="sequential",
                difficulty_level="easy",
                description="Clear testing domain with specific technologies"
            ),
            TestCase(
                input_text="Docker container orchestration issues with Kubernetes scaling",
                expected_agent="infrastructure-engineer",
                expected_domains=["infrastructure"],
                expected_coordination="sequential",
                difficulty_level="easy",
                description="Clear infrastructure domain with container focus"
            ),
            TestCase(
                input_text="Security vulnerability assessment with compliance validation",
                expected_agent="security-enforcer",
                expected_domains=["security"],
                expected_coordination="sequential",
                difficulty_level="easy",
                description="Clear security domain with specific requirements"
            ),
            
            # Medium cases - implicit patterns
            TestCase(
                input_text="Performance bottlenecks affecting user experience, need analysis",
                expected_agent="performance-optimizer",
                expected_domains=["performance"],
                expected_coordination="sequential",
                difficulty_level="medium",
                description="Performance focus with implicit requirements"
            ),
            TestCase(
                input_text="Code quality issues with architecture problems and naming conventions",
                expected_agent="intelligent-enhancer",
                expected_domains=["code_quality"],
                expected_coordination="sequential",
                difficulty_level="medium",
                description="Code quality focus with multiple aspects"
            ),
            TestCase(
                input_text="Complex system integration requiring testing and infrastructure coordination",
                expected_agent="analysis-gateway",
                expected_domains=["testing", "infrastructure"],
                expected_coordination="parallel",
                difficulty_level="medium",
                description="Multi-domain integration scenario"
            ),
            TestCase(
                input_text="Deployment pipeline failures causing production issues",
                expected_agent="infrastructure-engineer",
                expected_domains=["infrastructure"],
                expected_coordination="sequential",
                difficulty_level="medium",
                description="Infrastructure focus with pipeline context"
            ),
            
            # Hard cases - ambiguous or complex
            TestCase(
                input_text="System-wide performance degradation with security implications and testing gaps",
                expected_agent="meta-coordinator",
                expected_domains=["performance", "security", "testing"],
                expected_coordination="hierarchical",
                difficulty_level="hard",
                description="Complex multi-domain crisis requiring orchestration"
            ),
            TestCase(
                input_text="Architecture refactoring with performance implications, security concerns, and testing challenges",
                expected_agent="meta-coordinator",
                expected_domains=["code_quality", "performance", "security", "testing"],
                expected_coordination="hierarchical",
                difficulty_level="hard",
                description="Comprehensive architecture changes across all domains"
            ),
            TestCase(
                input_text="Production incident requiring immediate response and comprehensive analysis",
                expected_agent="meta-coordinator",
                expected_domains=["infrastructure", "performance", "security"],
                expected_coordination="hierarchical",
                difficulty_level="hard",
                description="Crisis response requiring strategic coordination"
            ),
            TestCase(
                input_text="Optimization project spanning code quality, performance, and infrastructure",
                expected_agent="analysis-gateway",
                expected_domains=["code_quality", "performance", "infrastructure"],
                expected_coordination="parallel",
                difficulty_level="hard",
                description="Multi-domain optimization project"
            ),
            
            # Edge cases - unusual or boundary conditions
            TestCase(
                input_text="Need help with something",
                expected_agent="digdeep",
                expected_domains=[],
                expected_coordination="sequential",
                difficulty_level="edge_case",
                description="Extremely vague request requiring deep analysis"
            ),
            TestCase(
                input_text="Python typing annotations for async functions in testing framework",
                expected_agent="test-specialist",
                expected_domains=["testing", "code_quality"],
                expected_coordination="sequential",
                difficulty_level="edge_case",
                description="Specific technical question crossing domains"
            ),
            TestCase(
                input_text="FastMCP server implementation with Qdrant vector database integration",
                expected_agent="intelligent-enhancer",
                expected_domains=["infrastructure", "code_quality"],
                expected_coordination="sequential",
                difficulty_level="edge_case",
                description="Project-specific implementation requiring context"
            ),
            TestCase(
                input_text="How to improve agent selection accuracy in Claude Code Framework",
                expected_agent="intelligent-enhancer",
                expected_domains=["code_quality"],
                expected_coordination="sequential",
                difficulty_level="edge_case",
                description="Meta-question about the framework itself"
            ),
            
            # Performance-sensitive cases
            TestCase(
                input_text="Urgent: Production system down, need immediate analysis",
                expected_agent="meta-coordinator",
                expected_domains=["infrastructure", "performance"],
                expected_coordination="hierarchical",
                difficulty_level="hard",
                description="Time-critical scenario requiring fast response"
            ),
            TestCase(
                input_text="Quick security scan needed before deployment",
                expected_agent="security-enforcer",
                expected_domains=["security"],
                expected_coordination="sequential",
                difficulty_level="medium",
                description="Fast security assessment requirement"
            ),
            TestCase(
                input_text="Simple test fix for async function",
                expected_agent="test-specialist",
                expected_domains=["testing"],
                expected_coordination="sequential",
                difficulty_level="easy",
                description="Simple, fast testing task"
            ),
            
            # Context-sensitive cases
            TestCase(
                input_text="Following up on the previous infrastructure analysis, need security review",
                expected_agent="security-enforcer",
                expected_domains=["security", "infrastructure"],
                expected_coordination="sequential",
                difficulty_level="medium",
                description="Context-dependent follow-up task"
            ),
            TestCase(
                input_text="Now let's optimize the performance of that solution",
                expected_agent="performance-optimizer",
                expected_domains=["performance"],
                expected_coordination="sequential",
                difficulty_level="medium",
                description="Context-dependent performance optimization"
            ),
        ]
    
    def run_single_test(self, test_case: TestCase, 
                       conversation_history: List[str] = None) -> BenchmarkResult:
        """Run a single benchmark test"""
        start_time = time.time()
        
        try:
            # Run agent selection
            selected_agent, confidence, details = self.enhanced_system.select_agent(
                test_case.input_text, conversation_history
            )
            
            response_time = time.time() - start_time
            
            # Calculate accuracy score
            accuracy_score = self._calculate_accuracy(test_case, selected_agent, details)
            
            # Calculate context preservation (based on domain detection accuracy)
            context_preservation = self._calculate_context_preservation(test_case, details)
            
            return BenchmarkResult(
                test_case=test_case,
                selected_agent=selected_agent,
                confidence=confidence,
                response_time=response_time,
                accuracy_score=accuracy_score,
                context_preservation=context_preservation,
                domains_detected=details.get('context_analysis', {}).get('domains', {}),
                coordination_detected=details.get('context_analysis', {}).get('coordination_pattern', ''),
                validation_issues=details.get('validation', {}).get('issues', []),
                details=details
            )
            
        except Exception as e:
            logger.error(f"Error in test case '{test_case.description}': {str(e)}")
            return BenchmarkResult(
                test_case=test_case,
                selected_agent="error",
                confidence=0.0,
                response_time=999.0,
                accuracy_score=0.0,
                context_preservation=0.0,
                domains_detected={},
                coordination_detected="error",
                validation_issues=[f"Test error: {str(e)}"],
                details={"error": str(e)}
            )
    
    def _calculate_accuracy(self, test_case: TestCase, selected_agent: str, 
                          details: Dict[str, Any]) -> float:
        """Calculate accuracy score based on expected vs actual results"""
        score = 0.0
        
        # Agent selection accuracy (50% weight)
        if selected_agent == test_case.expected_agent:
            score += 0.5
        elif selected_agent in details.get('suggested_alternatives', []):
            score += 0.3  # Partial credit for reasonable alternatives
        
        # Domain detection accuracy (30% weight)
        detected_domains = set(details.get('context_analysis', {}).get('domains', {}).keys())
        expected_domains = set(test_case.expected_domains)
        
        if expected_domains:
            domain_overlap = len(detected_domains.intersection(expected_domains))
            domain_accuracy = domain_overlap / len(expected_domains)
            score += domain_accuracy * 0.3
        else:
            score += 0.3 if not detected_domains else 0.1  # Penalty for false positives
        
        # Coordination pattern accuracy (20% weight)
        detected_coordination = details.get('context_analysis', {}).get('coordination_pattern', '')
        if detected_coordination == test_case.expected_coordination:
            score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_context_preservation(self, test_case: TestCase, 
                                      details: Dict[str, Any]) -> float:
        """Calculate context preservation score"""
        # Base preservation score
        base_score = 0.8
        
        # Boost for correct domain detection
        detected_domains = set(details.get('context_analysis', {}).get('domains', {}).keys())
        expected_domains = set(test_case.expected_domains)
        
        if expected_domains:
            domain_accuracy = len(detected_domains.intersection(expected_domains)) / len(expected_domains)
            base_score += domain_accuracy * 0.2
        
        # Penalty for validation issues
        validation_issues = len(details.get('validation', {}).get('issues', []))
        base_score -= validation_issues * 0.05
        
        return max(min(base_score, 1.0), 0.0)
    
    def run_benchmark(self, iterations: int = 1) -> PerformanceReport:
        """Run comprehensive benchmark suite"""
        logger.info(f"Starting benchmark with {len(self.test_cases)} test cases, {iterations} iterations")
        
        all_results = []
        
        for iteration in range(iterations):
            logger.info(f"Running iteration {iteration + 1}/{iterations}")
            
            for i, test_case in enumerate(self.test_cases):
                # Simulate conversation history for context-sensitive cases
                conversation_history = []
                if "following up" in test_case.input_text.lower() or "now let's" in test_case.input_text.lower():
                    conversation_history = [
                        "Previous infrastructure analysis completed successfully",
                        "Docker containerization implemented with scaling configuration"
                    ]
                
                result = self.run_single_test(test_case, conversation_history)
                all_results.append(result)
                
                if (i + 1) % 5 == 0:
                    logger.info(f"Completed {i + 1}/{len(self.test_cases)} test cases")
        
        # Generate comprehensive report
        return self._generate_performance_report(all_results)
    
    def _generate_performance_report(self, results: List[BenchmarkResult]) -> PerformanceReport:
        """Generate comprehensive performance report from benchmark results"""
        # Overall metrics
        total_tests = len(results)
        accuracy_scores = [r.accuracy_score for r in results]
        response_times = [r.response_time for r in results]
        confidences = [r.confidence for r in results]
        context_preservations = [r.context_preservation for r in results]
        
        accuracy_rate = statistics.mean(accuracy_scores)
        avg_response_time = statistics.mean(response_times)
        avg_confidence = statistics.mean(confidences)
        context_preservation_rate = statistics.mean(context_preservations)
        
        # Difficulty breakdown
        difficulty_breakdown = {}
        for difficulty in ["easy", "medium", "hard", "edge_case"]:
            diff_results = [r for r in results if r.test_case.difficulty_level == difficulty]
            if diff_results:
                difficulty_breakdown[difficulty] = {
                    "count": len(diff_results),
                    "accuracy": statistics.mean([r.accuracy_score for r in diff_results]),
                    "avg_response_time": statistics.mean([r.response_time for r in diff_results]),
                    "context_preservation": statistics.mean([r.context_preservation for r in diff_results])
                }
        
        # Agent performance breakdown
        agent_performance = {}
        agent_results = {}
        for result in results:
            agent = result.selected_agent
            if agent not in agent_results:
                agent_results[agent] = []
            agent_results[agent].append(result)
        
        for agent, agent_res in agent_results.items():
            agent_performance[agent] = {
                "selections": len(agent_res),
                "accuracy": statistics.mean([r.accuracy_score for r in agent_res]),
                "avg_response_time": statistics.mean([r.response_time for r in agent_res]),
                "avg_confidence": statistics.mean([r.confidence for r in agent_res])
            }
        
        # Pattern effectiveness
        pattern_effectiveness = {
            "explicit_patterns": statistics.mean([
                r.accuracy_score for r in results 
                if r.details.get('explicit_match', {}).get('confidence', 0) >= 0.8
            ]) if any(r.details.get('explicit_match', {}).get('confidence', 0) >= 0.8 for r in results) else 0.0,
            "context_analysis": statistics.mean([
                r.accuracy_score for r in results 
                if r.details.get('context_analysis', {}).get('confidence_score', 0) >= 0.7
            ]) if any(r.details.get('context_analysis', {}).get('confidence_score', 0) >= 0.7 for r in results) else 0.0,
            "fallback_decisions": statistics.mean([
                r.accuracy_score for r in results 
                if r.confidence < 0.7
            ]) if any(r.confidence < 0.7 for r in results) else 1.0
        }
        
        # Edge case handling
        edge_case_results = [r for r in results if r.test_case.difficulty_level == "edge_case"]
        edge_case_handling = statistics.mean([r.accuracy_score for r in edge_case_results]) if edge_case_results else 0.0
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            accuracy_rate, avg_response_time, difficulty_breakdown, 
            pattern_effectiveness, edge_case_handling
        )
        
        return PerformanceReport(
            total_tests=total_tests,
            accuracy_rate=accuracy_rate,
            avg_response_time=avg_response_time,
            avg_confidence=avg_confidence,
            context_preservation_rate=context_preservation_rate,
            difficulty_breakdown=difficulty_breakdown,
            agent_performance=agent_performance,
            pattern_effectiveness=pattern_effectiveness,
            edge_case_handling=edge_case_handling,
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, accuracy_rate: float, avg_response_time: float,
                                difficulty_breakdown: Dict, pattern_effectiveness: Dict,
                                edge_case_handling: float) -> List[str]:
        """Generate recommendations based on benchmark results"""
        recommendations = []
        
        # Accuracy recommendations
        if accuracy_rate < 0.9:
            recommendations.append(f"Overall accuracy ({accuracy_rate:.2%}) below target (90%). Consider enhancing pattern matching.")
        
        if accuracy_rate >= 0.95:
            recommendations.append(f"Excellent accuracy achieved ({accuracy_rate:.2%}). System performing above target.")
        
        # Response time recommendations
        if avg_response_time > 1.0:
            recommendations.append(f"Average response time ({avg_response_time:.3f}s) exceeds 1s target. Optimize pattern matching pipeline.")
        
        if avg_response_time <= 0.7:
            recommendations.append(f"Excellent response time ({avg_response_time:.3f}s) meets enhanced target. Performance optimized.")
        
        # Difficulty-specific recommendations
        for difficulty, metrics in difficulty_breakdown.items():
            if metrics['accuracy'] < 0.8:
                recommendations.append(f"Low accuracy for {difficulty} cases ({metrics['accuracy']:.2%}). Enhance {difficulty}-specific patterns.")
        
        # Pattern effectiveness recommendations
        if pattern_effectiveness.get('explicit_patterns', 0) < 0.9:
            recommendations.append("Explicit pattern matching needs improvement. Review and expand pattern libraries.")
        
        if pattern_effectiveness.get('fallback_decisions', 0) < 0.7:
            recommendations.append("Fallback decision tree needs enhancement. Improve edge case handling logic.")
        
        # Edge case recommendations
        if edge_case_handling < 0.6:
            recommendations.append(f"Edge case handling ({edge_case_handling:.2%}) needs significant improvement.")
        
        if not recommendations:
            recommendations.append("System performance meets all targets. Continue monitoring and occasional optimization.")
        
        return recommendations
    
    def save_report(self, report: PerformanceReport, filename: str):
        """Save performance report to JSON file"""
        report_dict = asdict(report)
        
        with open(filename, 'w') as f:
            json.dump(report_dict, f, indent=2, default=str)
        
        logger.info(f"Performance report saved to {filename}")
    
    def print_summary_report(self, report: PerformanceReport):
        """Print a human-readable summary report"""
        print("\n" + "=" * 80)
        print("ENHANCED PATTERN RECOGNITION SYSTEM - PERFORMANCE REPORT")
        print("=" * 80)
        
        print(f"\nOVERALL PERFORMANCE:")
        print(f"  Total Tests: {report.total_tests}")
        print(f"  Accuracy Rate: {report.accuracy_rate:.2%} (Target: 99.2%)")
        print(f"  Avg Response Time: {report.avg_response_time:.3f}s (Target: <0.7s)")
        print(f"  Avg Confidence: {report.avg_confidence:.3f}")
        print(f"  Context Preservation: {report.context_preservation_rate:.2%} (Target: 99.5%)")
        
        print(f"\nDIFFICULTY BREAKDOWN:")
        for difficulty, metrics in report.difficulty_breakdown.items():
            print(f"  {difficulty.upper()}:")
            print(f"    Tests: {metrics['count']}")
            print(f"    Accuracy: {metrics['accuracy']:.2%}")
            print(f"    Avg Response Time: {metrics['avg_response_time']:.3f}s")
            print(f"    Context Preservation: {metrics['context_preservation']:.2%}")
        
        print(f"\nAGENT PERFORMANCE:")
        for agent, metrics in report.agent_performance.items():
            print(f"  {agent}:")
            print(f"    Selections: {metrics['selections']}")
            print(f"    Accuracy: {metrics['accuracy']:.2%}")
            print(f"    Avg Response Time: {metrics['avg_response_time']:.3f}s")
            print(f"    Avg Confidence: {metrics['avg_confidence']:.3f}")
        
        print(f"\nPATTERN EFFECTIVENESS:")
        for pattern_type, effectiveness in report.pattern_effectiveness.items():
            print(f"  {pattern_type.replace('_', ' ').title()}: {effectiveness:.2%}")
        
        print(f"\nEDGE CASE HANDLING: {report.edge_case_handling:.2%}")
        
        print(f"\nRECOMMENDATIONS:")
        for i, rec in enumerate(report.recommendations, 1):
            print(f"  {i}. {rec}")
        
        # Performance assessment
        print(f"\n" + "=" * 80)
        print("PERFORMANCE ASSESSMENT:")
        
        targets_met = 0
        total_targets = 4
        
        if report.accuracy_rate >= 0.992:  # 99.2%
            print("  ✅ Accuracy Target: EXCEEDED")
            targets_met += 1
        elif report.accuracy_rate >= 0.97:  # Current 97%
            print("  🔶 Accuracy Target: MAINTAINED (meets current standard)")
        else:
            print("  ❌ Accuracy Target: BELOW STANDARD")
        
        if report.avg_response_time <= 0.7:
            print("  ✅ Response Time Target: ACHIEVED")
            targets_met += 1
        elif report.avg_response_time <= 1.0:
            print("  🔶 Response Time Target: ACCEPTABLE (meets current standard)")
        else:
            print("  ❌ Response Time Target: NEEDS IMPROVEMENT")
        
        if report.context_preservation_rate >= 0.995:  # 99.5%
            print("  ✅ Context Preservation Target: EXCEEDED")
            targets_met += 1
        elif report.context_preservation_rate >= 0.97:
            print("  🔶 Context Preservation Target: MAINTAINED")
        else:
            print("  ❌ Context Preservation Target: BELOW STANDARD")
        
        if report.edge_case_handling >= 0.95:  # 95%
            print("  ✅ Edge Case Handling Target: ACHIEVED")
            targets_met += 1
        elif report.edge_case_handling >= 0.6:
            print("  🔶 Edge Case Handling Target: ACCEPTABLE")
        else:
            print("  ❌ Edge Case Handling Target: NEEDS IMPROVEMENT")
        
        print(f"\n  TARGETS MET: {targets_met}/{total_targets}")
        
        if targets_met >= 3:
            print("  🎉 OVERALL ASSESSMENT: EXCELLENT - Ready for production deployment")
        elif targets_met >= 2:
            print("  👍 OVERALL ASSESSMENT: GOOD - Minor improvements recommended")
        else:
            print("  ⚠️  OVERALL ASSESSMENT: NEEDS WORK - Significant improvements required")
        
        print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="Agent Selection Performance Measurement")
    parser.add_argument('--mode', choices=['benchmark', 'single', 'comparison'], 
                       default='benchmark', help='Measurement mode')
    parser.add_argument('--iterations', type=int, default=1, 
                       help='Number of benchmark iterations')
    parser.add_argument('--output', type=str, default='performance_report.json',
                       help='Output file for detailed report')
    parser.add_argument('--verbose', action='store_true', 
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    benchmark = AgentSelectionBenchmark()
    
    if args.mode == 'benchmark':
        logger.info("Running comprehensive benchmark suite")
        report = benchmark.run_benchmark(iterations=args.iterations)
        
        # Print summary
        benchmark.print_summary_report(report)
        
        # Save detailed report
        benchmark.save_report(report, args.output)
        
    elif args.mode == 'single':
        logger.info("Running single test case")
        test_case = benchmark.test_cases[0]  # Use first test case
        result = benchmark.run_single_test(test_case)
        
        print(f"\nSingle Test Result:")
        print(f"  Input: {test_case.input_text}")
        print(f"  Expected Agent: {test_case.expected_agent}")
        print(f"  Selected Agent: {result.selected_agent}")
        print(f"  Accuracy Score: {result.accuracy_score:.3f}")
        print(f"  Confidence: {result.confidence:.3f}")
        print(f"  Response Time: {result.response_time:.3f}s")
        print(f"  Context Preservation: {result.context_preservation:.3f}")
        
    elif args.mode == 'comparison':
        logger.info("Running comparison between current and enhanced systems")
        # This would compare against baseline system if available
        logger.warning("Comparison mode not fully implemented - running enhanced benchmark")
        report = benchmark.run_benchmark(iterations=args.iterations)
        benchmark.print_summary_report(report)

if __name__ == "__main__":
    main()
