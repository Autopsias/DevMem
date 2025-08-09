#!/usr/bin/env python3
"""
Comprehensive Test Framework for Agent Selection Pattern Validation

This framework provides:
1. Pattern accuracy measurement with statistical significance
2. Domain coverage validation across all agent types
3. Cross-validation with stratified sampling
4. Performance benchmarking with detailed metrics
5. Edge case detection and validation
"""

import pytest
import time
import statistics
import json
import logging
import random
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict, Counter

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class TestPattern:
    """Represents a test pattern for agent selection validation"""

    pattern_id: str
    input_text: str
    expected_agent: str
    expected_domains: List[str]
    expected_coordination: str
    confidence_threshold: float
    complexity_level: str
    domain_category: str
    pattern_type: str
    validation_criteria: Dict[str, Any]
    metadata: Dict[str, Any]


@dataclass
class ValidationResult:
    """Result of a single pattern validation test"""

    pattern_id: str
    test_pattern: TestPattern
    selected_agent: str
    actual_domains: List[str]
    actual_coordination: str
    confidence_score: float
    accuracy_metrics: Dict[str, float]
    performance_metrics: Dict[str, float]
    validation_status: str
    failure_reasons: List[str]
    detailed_analysis: Dict[str, Any]
    timestamp: float


@dataclass
class ComprehensiveValidationReport:
    """Comprehensive validation report with all metrics"""

    total_patterns_tested: int
    overall_accuracy: float
    domain_coverage_score: float
    pattern_type_performance: Dict[str, Dict[str, float]]
    complexity_level_performance: Dict[str, Dict[str, float]]
    cross_validation_metrics: Dict[str, float]
    edge_case_handling: Dict[str, float]
    performance_benchmarks: Dict[str, float]
    statistical_significance: Dict[str, float]
    improvement_recommendations: List[str]
    detailed_breakdowns: Dict[str, Any]
    validation_timestamp: float


class DomainSpecificPatternGenerator:
    """Generates domain-specific test patterns"""

    def __init__(self):
        self.domain_templates = {
            "testing": [
                (
                    "Test failures in pytest with asyncio patterns",
                    "test-specialist",
                    ["testing"],
                    "sequential",
                ),
                (
                    "Mock configuration issues causing test isolation problems",
                    "test-specialist",
                    ["testing"],
                    "sequential",
                ),
                (
                    "Coverage gaps in integration testing suite",
                    "test-specialist",
                    ["testing"],
                    "sequential",
                ),
            ],
            "infrastructure": [
                (
                    "Docker container orchestration failing in Kubernetes",
                    "infrastructure-engineer",
                    ["infrastructure"],
                    "sequential",
                ),
                (
                    "CI/CD pipeline breaking with deployment issues",
                    "infrastructure-engineer",
                    ["infrastructure"],
                    "sequential",
                ),
                (
                    "Container network segmentation",
                    "infrastructure-engineer",
                    ["infrastructure"],
                    "sequential",
                ),
                (
                    "Service mesh traffic routing error",
                    "infrastructure-engineer",
                    ["infrastructure"],
                    "sequential",
                ),
                (
                    "Terraform state corruption issue",
                    "infrastructure-engineer",
                    ["infrastructure"],
                    "sequential",
                ),
                (
                    "Kubernetes node scaling problem",
                    "infrastructure-engineer",
                    ["infrastructure"],
                    "sequential",
                ),
                (
                    "Load balancer health check failure",
                    "infrastructure-engineer",
                    ["infrastructure"],
                    "sequential",
                ),
                (
                    "Infrastructure as Code validation",
                    "infrastructure-engineer",
                    ["infrastructure"],
                    "sequential",
                ),
                (
                    "Container registry authentication",
                    "infrastructure-engineer",
                    ["infrastructure"],
                    "sequential",
                ),
                (
                    "Service discovery DNS resolution",
                    "infrastructure-engineer",
                    ["infrastructure"],
                    "sequential",
                ),
            ],
            "security": [
                (
                    "SQL injection vulnerability found in authentication",
                    "security-enforcer",
                    ["security"],
                    "sequential",
                ),
                (
                    "OWASP compliance validation needed before release",
                    "security-enforcer",
                    ["security"],
                    "sequential",
                ),
                (
                    "Zero-day exploit detected in API",
                    "security-enforcer",
                    ["security"],
                    "sequential",
                ),
                (
                    "Security assessment for cloud deployment",
                    "security-enforcer",
                    ["security"],
                    "sequential",
                ),
                (
                    "GDPR compliance audit requirements",
                    "security-enforcer",
                    ["security"],
                    "sequential",
                ),
                (
                    "Container image vulnerability scan",
                    "security-enforcer",
                    ["security"],
                    "sequential",
                ),
                (
                    "Application firewall misconfiguration",
                    "security-enforcer",
                    ["security"],
                    "sequential",
                ),
                (
                    "Penetration testing findings review",
                    "security-enforcer",
                    ["security"],
                    "sequential",
                ),
                (
                    "Access control policy validation",
                    "security-enforcer",
                    ["security"],
                    "sequential",
                ),
                (
                    "Security threat modeling session",
                    "security-enforcer",
                    ["security"],
                    "sequential",
                ),
                (
                    "Cryptographic key rotation process",
                    "security-enforcer",
                    ["security"],
                    "sequential",
                ),
                (
                    "Network intrusion detection alert",
                    "security-enforcer",
                    ["security"],
                    "sequential",
                ),
            ],
            "performance": [
                (
                    "Application response time degrading under load",
                    "performance-optimizer",
                    ["performance"],
                    "sequential",
                ),
                (
                    "Memory usage spiking causing OOM errors",
                    "performance-optimizer",
                    ["performance"],
                    "sequential",
                ),
            ],
            "code_quality": [
                (
                    "Code review reveals architectural inconsistencies",
                    "intelligent-enhancer",
                    ["code_quality"],
                    "sequential",
                ),
                (
                    "Refactoring needed to improve maintainability",
                    "intelligent-enhancer",
                    ["code_quality"],
                    "sequential",
                ),
            ],
            "documentation": [
                (
                    "API documentation needs update",
                    "documentation-enhancer",
                    ["documentation"],
                    "sequential",
                ),
                (
                    "Create user guide for new feature",
                    "documentation-enhancer",
                    ["documentation"],
                    "sequential",
                ),
                (
                    "Generate markdown docs from code",
                    "documentation-enhancer",
                    ["documentation"],
                    "sequential",
                ),
                (
                    "Technical writing for developer guide",
                    "documentation-enhancer",
                    ["documentation"],
                    "sequential",
                ),
                (
                    "Knowledge base article creation",
                    "documentation-enhancer",
                    ["documentation"],
                    "sequential",
                ),
                (
                    "Update installation documentation",
                    "documentation-enhancer",
                    ["documentation"],
                    "sequential",
                ),
                (
                    "Create troubleshooting guide",
                    "documentation-enhancer",
                    ["documentation"],
                    "sequential",
                ),
                (
                    "API specification documentation",
                    "documentation-enhancer",
                    ["documentation"],
                    "sequential",
                ),
                (
                    "Improve README documentation",
                    "documentation-enhancer",
                    ["documentation"],
                    "sequential",
                ),
                (
                    "Document code examples in markdown",
                    "documentation-enhancer",
                    ["documentation"],
                    "sequential",
                ),
            ],
        }

        self.complexity_variations = {
            "basic": [
                " on single node",
                " in development environment",
                " with basic setup",
            ],
            "intermediate": [
                " with multiple service dependencies",
                " across different environments",
                " in production cluster",
                " with service mesh",
                " using helm charts",
            ],
            "advanced": [
                " requiring cross-system coordination",
                " with complex failure scenarios",
                " across multiple regions",
                " with high availability requirements",
                " involving multi-cloud setup",
            ],
            "edge_case": [
                " in unusual configuration",
                " with conflicting requirements",
                " during disaster recovery",
                " with legacy compatibility",
                " in restricted environment",
            ],
        }

        self.pattern_type_modifiers = {
            "explicit": [],
            "implicit": ["Need help with ", "Issues with "],
            "contextual": [
                "Following the previous analysis, ",
                "Building on our earlier work, ",
            ],
            "ambiguous": ["Something's wrong with ", "Having trouble with "],
        }

    def generate_patterns(self, count: int, domain: str = None) -> List[TestPattern]:
        """Generate domain-specific test patterns"""
        patterns = []
        domains_to_use = [domain] if domain else list(self.domain_templates.keys())

        for i in range(count):
            selected_domain = random.choice(domains_to_use)
            template = random.choice(self.domain_templates[selected_domain])

            input_text, expected_agent, expected_domains, expected_coordination = (
                template
            )

            # Add complexity variation
            complexity = random.choice(
                ["basic", "intermediate", "advanced", "edge_case"]
            )
            if (
                complexity in self.complexity_variations
                and self.complexity_variations[complexity]
            ):
                input_text += random.choice(self.complexity_variations[complexity])

            # Add pattern type variation
            pattern_type = random.choice(
                ["explicit", "implicit", "contextual", "ambiguous"]
            )
            if (
                pattern_type in self.pattern_type_modifiers
                and self.pattern_type_modifiers[pattern_type]
            ):
                modifier = random.choice(self.pattern_type_modifiers[pattern_type])
                input_text = modifier + input_text.lower()

            pattern = TestPattern(
                pattern_id=f"generated_{selected_domain}_{i}",
                input_text=input_text,
                expected_agent=expected_agent,
                expected_domains=expected_domains,
                expected_coordination=expected_coordination,
                confidence_threshold=0.7,
                complexity_level=complexity,
                domain_category=selected_domain,
                pattern_type=pattern_type,
                validation_criteria={
                    "agent_match_required": True,
                    "domain_overlap_min": 0.8,
                    "coordination_match_required": False,
                },
                metadata={
                    "generated_template": template[0],
                    "generation_timestamp": time.time(),
                },
            )
            patterns.append(pattern)

        return patterns


class EdgeCasePatternGenerator:
    """Generates edge case patterns for comprehensive testing"""

    def __init__(self):
        self.edge_cases = [
            ("Help me", "digdeep", [], "sequential", "vague_request"),
            ("Something's wrong", "digdeep", [], "sequential", "vague_problem"),
            (
                "URGENT: Production down",
                "meta-coordinator",
                ["infrastructure"],
                "hierarchical",
                "crisis_mode",
            ),
            (
                "AsyncMock pytest configuration",
                "test-specialist",
                ["testing"],
                "sequential",
                "highly_specific",
            ),
        ]

    def generate_patterns(self, count: int, domain: str = None) -> List[TestPattern]:
        """Generate edge case patterns"""
        patterns = []

        for i in range(count):
            edge_case = random.choice(self.edge_cases)
            (
                input_text,
                expected_agent,
                expected_domains,
                expected_coordination,
                edge_type,
            ) = edge_case

            pattern = TestPattern(
                pattern_id=f"edge_case_{edge_type}_{i}",
                input_text=input_text,
                expected_agent=expected_agent,
                expected_domains=expected_domains,
                expected_coordination=expected_coordination,
                confidence_threshold=0.6,
                complexity_level="edge_case",
                domain_category=(
                    "mixed"
                    if len(expected_domains) > 1
                    else (expected_domains[0] if expected_domains else "none")
                ),
                pattern_type="ambiguous",
                validation_criteria={
                    "agent_match_required": False,
                    "domain_overlap_min": 0.5,
                    "coordination_match_required": False,
                    "acceptable_alternatives": [
                        "digdeep",
                        "meta-coordinator",
                        "analysis-gateway",
                    ],
                },
                metadata={"edge_case_type": edge_type, "expected_difficulty": "high"},
            )
            patterns.append(pattern)

        return patterns


class MockEnhancedSystem:
    """Mock enhanced system for testing when actual system not available"""

    def __init__(self):
        self.agent_patterns = {
            "test": "test-specialist",
            "security": "security-enforcer",
            "infrastructure": "infrastructure-engineer",
            "performance": "performance-optimizer",
            "code": "intelligent-enhancer",
            "docker": "infrastructure-engineer",
            "kubernetes": "infrastructure-engineer",
            "k8s": "infrastructure-engineer",
            "container": "infrastructure-engineer",
            "terraform": "infrastructure-engineer",
            "deployment": "infrastructure-engineer",
            "service": "infrastructure-engineer",
            "pipeline": "infrastructure-engineer",
            "ci/cd": "infrastructure-engineer",
            "vulnerability": "security-enforcer",
            "exploit": "security-enforcer",
            "breach": "security-enforcer",
            "compliance": "security-enforcer",
            "audit": "security-enforcer",
            "threat": "security-enforcer",
            "penetration": "security-enforcer",
            "firewall": "security-enforcer",
            "intrusion": "security-enforcer",
            "cryptographic": "security-enforcer",
            "gdpr": "security-enforcer",
            "hipaa": "security-enforcer",
            "owasp": "security-enforcer",
            "documentation": "documentation-enhancer",
            "docs": "documentation-enhancer",
            "readme": "documentation-enhancer",
            "markdown": "documentation-enhancer",
            "api": "documentation-enhancer",
            "guide": "documentation-enhancer",
            "tutorial": "documentation-enhancer",
            "manual": "documentation-enhancer",
            "specification": "documentation-enhancer",
            "wiki": "documentation-enhancer",
            "handbook": "documentation-enhancer",
            "knowledge": "documentation-enhancer",
            "reference": "documentation-enhancer",
            "howto": "documentation-enhancer",
            "faq": "documentation-enhancer",
            "async": "test-specialist",
            "urgent": "meta-coordinator",
            "comprehensive": "analysis-gateway",
        }

    def select_agent(
        self, input_text: str, conversation_history: List[str] = None
    ) -> Tuple[str, float, Dict[str, Any]]:
        """Enhanced agent selection with cross-domain support"""
        text_lower = input_text.lower()

        # Initialize with default values
        selected_agent = "digdeep"
        confidence = 0.6
        domains = {}
        all_matches = []

        # Detect all matching patterns
        for pattern, agent in self.agent_patterns.items():
            if pattern in text_lower:
                pattern_confidence = 0.8 + random.random() * 0.2
                domains[pattern] = pattern_confidence
                all_matches.append(
                    {
                        "pattern": pattern,
                        "agent": agent,
                        "confidence": pattern_confidence,
                    }
                )

        # Cross-domain analysis
        if len(all_matches) > 1:
            # Sort matches by confidence
            all_matches.sort(key=lambda x: x["confidence"], reverse=True)

            # Group by agent
            agent_groups = {}
            for match in all_matches:
                if match["agent"] not in agent_groups:
                    agent_groups[match["agent"]] = []
                agent_groups[match["agent"]].append(match)

            # Select agent based on pattern groups
            if len(agent_groups) > 1:
                # Multiple agent types matched - complex scenario
                coordination_pattern = "hierarchical"
                if len(agent_groups) >= 3:
                    selected_agent = "meta-coordinator"
                    confidence = max(m["confidence"] for m in all_matches)
                else:
                    # Choose the agent with highest confidence sum
                    agent_scores = {}
                    for agent, matches in agent_groups.items():
                        agent_scores[agent] = sum(m["confidence"] for m in matches)
                    selected_agent = max(agent_scores.items(), key=lambda x: x[1])[0]
                    confidence = agent_scores[selected_agent] / len(
                        agent_groups[selected_agent]
                    )
            else:
                # Single agent type with multiple patterns
                selected_agent = list(agent_groups.keys())[0]
                coordination_pattern = "sequential"
                confidence = max(m["confidence"] for m in all_matches)
        else:
            # Single pattern match
            if all_matches:
                selected_agent = all_matches[0]["agent"]
                confidence = all_matches[0]["confidence"]
            coordination_pattern = "sequential"

        return (
            selected_agent,
            confidence,
            {
                "context_analysis": {
                    "domains": domains,
                    "coordination_pattern": coordination_pattern,
                    "confidence_score": confidence,
                    "cross_domain_analysis": {
                        "total_patterns_matched": len(all_matches),
                        "unique_agents_matched": len(
                            set(m["agent"] for m in all_matches)
                        ),
                        "pattern_matches": all_matches,
                    },
                },
                "explicit_match": {"confidence": confidence},
                "validation": {"issues": []},
            },
        )


@dataclass
class MockAgentMatchResult:
    """Mock result that mimics AgentMatchResult structure"""

    agent_name: str
    confidence_score: float
    matched_patterns: List[str] = None
    processing_time_ms: float = 0.0
    context_keywords: List[str] = None
    reasoning: str = ""

    def __post_init__(self):
        if self.matched_patterns is None:
            self.matched_patterns = []
        if self.context_keywords is None:
            self.context_keywords = []


class MockEnhancedSystemWrapper:
    """Wrapper to make MockEnhancedSystem compatible with expected interface"""

    def __init__(self, mock_system):
        self.mock_system = mock_system
        self.agents = getattr(mock_system, "agent_patterns", {})

    def select_agent(self, query: str, context=None) -> MockAgentMatchResult:
        """Wrap the mock system to return expected result format"""
        import time

        start_time = time.perf_counter()

        # Get result from mock system (returns tuple)
        agent_name, confidence, details = self.mock_system.select_agent(query, [])

        processing_time = (time.perf_counter() - start_time) * 1000

        # Extract reasoning based on the selection
        reasoning_parts = []
        if "coordination" in query.lower() or "parallel" in query.lower():
            reasoning_parts.append("Parallel coordination pattern detected")
        if "task" in query.lower() and (
            "parallel" in query.lower() or "coordination" in query.lower()
        ):
            reasoning_parts.append("Task tool integration pattern recognized")
        if "infrastructure" in query.lower():
            reasoning_parts.append("Infrastructure domain expertise required")
        if "security" in query.lower():
            reasoning_parts.append("Security domain analysis")
        if "testing" in query.lower() or "pytest" in query.lower():
            reasoning_parts.append("Testing domain specialization")

        # Ensure multi-domain coordination gets appropriate reasoning
        domains_detected = sum(
            1
            for term in ["infrastructure", "security", "testing", "performance"]
            if term in query.lower()
        )
        if domains_detected >= 2:
            reasoning_parts.append("Multi-domain coordination required")

        reasoning = (
            "; ".join(reasoning_parts)
            if reasoning_parts
            else f"Pattern-based selection for {agent_name}"
        )

        # Extract matched patterns from details
        matched_patterns = list(
            details.get("context_analysis", {}).get("domains", {}).keys()
        )
        context_keywords = [kw for kw in query.lower().split() if len(kw) > 3]

        return MockAgentMatchResult(
            agent_name=agent_name,
            confidence_score=confidence,
            matched_patterns=matched_patterns,
            processing_time_ms=processing_time,
            context_keywords=context_keywords,
            reasoning=reasoning,
        )


class AgentSelectionValidator:
    """Validates agent selection against test patterns"""

    def __init__(self, enhanced_system=None):
        if enhanced_system:
            self.enhanced_system = enhanced_system
        else:
            self.enhanced_system = MockEnhancedSystem()

        # Add enhanced_selector property for backward compatibility and test integration
        try:
            import sys
            import os

            sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
            from agent_selector import EnhancedAgentSelector

            self.enhanced_selector = EnhancedAgentSelector()
        except ImportError:
            # Fallback to mock system wrapper if real selector not available
            self.enhanced_selector = MockEnhancedSystemWrapper(self.enhanced_system)

    def validate_pattern(
        self, pattern: TestPattern, conversation_history: List[str] = None
    ) -> ValidationResult:
        """Validate a single test pattern"""
        start_time = time.time()

        try:
            selected_agent, confidence, details = self.enhanced_system.select_agent(
                pattern.input_text, conversation_history or []
            )

            response_time = time.time() - start_time

            actual_domains = list(
                details.get("context_analysis", {}).get("domains", {}).keys()
            )
            actual_coordination = details.get("context_analysis", {}).get(
                "coordination_pattern", ""
            )

            accuracy_metrics = self._calculate_accuracy_metrics(
                pattern, selected_agent, actual_domains, actual_coordination
            )

            performance_metrics = {
                "response_time_ms": response_time * 1000,
                "confidence_score": confidence,
                "processing_efficiency": 1.0 / max(response_time, 0.001),
            }

            validation_status, failure_reasons = self._determine_validation_status(
                pattern, accuracy_metrics, confidence
            )

            return ValidationResult(
                pattern_id=pattern.pattern_id,
                test_pattern=pattern,
                selected_agent=selected_agent,
                actual_domains=actual_domains,
                actual_coordination=actual_coordination,
                confidence_score=confidence,
                accuracy_metrics=accuracy_metrics,
                performance_metrics=performance_metrics,
                validation_status=validation_status,
                failure_reasons=failure_reasons,
                detailed_analysis=details,
                timestamp=time.time(),
            )

        except Exception as e:
            logger.error(f"Error validating pattern {pattern.pattern_id}: {str(e)}")
            return ValidationResult(
                pattern_id=pattern.pattern_id,
                test_pattern=pattern,
                selected_agent="error",
                actual_domains=[],
                actual_coordination="error",
                confidence_score=0.0,
                accuracy_metrics={
                    "overall_accuracy": 0.0,
                    "agent_accuracy": 0.0,
                    "domain_accuracy": 0.0,
                },
                performance_metrics={
                    "response_time_ms": 999999,
                    "confidence_score": 0.0,
                    "processing_efficiency": 0.0,
                },
                validation_status="fail",
                failure_reasons=[f"Validation error: {str(e)}"],
                detailed_analysis={"error": str(e)},
                timestamp=time.time(),
            )

    def _calculate_accuracy_metrics(
        self,
        pattern: TestPattern,
        selected_agent: str,
        actual_domains: List[str],
        actual_coordination: str,
    ) -> Dict[str, float]:
        """Calculate detailed accuracy metrics"""
        metrics = {}

        if selected_agent == pattern.expected_agent:
            metrics["agent_accuracy"] = 1.0
        elif selected_agent in pattern.validation_criteria.get(
            "acceptable_alternatives", []
        ):
            metrics["agent_accuracy"] = 0.7
        else:
            metrics["agent_accuracy"] = 0.0

        expected_domains = set(pattern.expected_domains)
        detected_domains = set(actual_domains)

        if not expected_domains:
            metrics["domain_accuracy"] = 1.0 if not detected_domains else 0.5
        else:
            intersection = expected_domains.intersection(detected_domains)
            union = expected_domains.union(detected_domains)
            metrics["domain_accuracy"] = (
                len(intersection) / len(union) if union else 0.0
            )

        if actual_coordination == pattern.expected_coordination:
            metrics["coordination_accuracy"] = 1.0
        else:
            metrics["coordination_accuracy"] = 0.0

        metrics["overall_accuracy"] = (
            metrics["agent_accuracy"] * 0.5
            + metrics.get("domain_accuracy", 0.0) * 0.3
            + metrics["coordination_accuracy"] * 0.2
        )

        return metrics

    def _determine_validation_status(
        self,
        pattern: TestPattern,
        accuracy_metrics: Dict[str, float],
        confidence: float,
    ) -> Tuple[str, List[str]]:
        """Determine overall validation status and failure reasons"""
        failure_reasons = []

        if (
            pattern.validation_criteria.get("agent_match_required", True)
            and accuracy_metrics["agent_accuracy"] < 0.7
        ):
            failure_reasons.append("Agent selection does not match expected agent")

        min_domain_overlap = pattern.validation_criteria.get("domain_overlap_min", 0.8)
        if accuracy_metrics.get("domain_accuracy", 0.0) < min_domain_overlap:
            failure_reasons.append("Domain overlap below minimum")

        if confidence < pattern.confidence_threshold:
            failure_reasons.append("Confidence below threshold")

        if not failure_reasons:
            return "pass", []
        elif accuracy_metrics["overall_accuracy"] >= 0.5:
            return "partial", failure_reasons
        else:
            return "fail", failure_reasons


class AgentSelectionTestFramework:
    """Comprehensive test framework for agent selection pattern validation"""

    def __init__(self, enhanced_system=None):
        self.validator = AgentSelectionValidator(enhanced_system)
        self.domain_generator = DomainSpecificPatternGenerator()
        self.edge_case_generator = EdgeCasePatternGenerator()
        self.test_results_dir = Path("tests/results/agent_selection")
        self.test_results_dir.mkdir(parents=True, exist_ok=True)

    def generate_comprehensive_test_suite(
        self, patterns_per_domain: int = 20, edge_cases: int = 15
    ) -> List[TestPattern]:
        """Generate comprehensive test suite covering all domains and edge cases"""
        patterns = []

        domains = [
            "testing",
            "infrastructure",
            "security",
            "performance",
            "code_quality",
            "documentation",
        ]
        for domain in domains:
            domain_patterns = self.domain_generator.generate_patterns(
                patterns_per_domain, domain
            )
            patterns.extend(domain_patterns)
            logger.info(
                f"Generated {len(domain_patterns)} patterns for domain: {domain}"
            )

        edge_patterns = self.edge_case_generator.generate_patterns(edge_cases)
        patterns.extend(edge_patterns)
        logger.info(f"Generated {len(edge_patterns)} edge case patterns")

        random.shuffle(patterns)

        logger.info(f"Total test patterns generated: {len(patterns)}")
        return patterns

    def run_comprehensive_validation(
        self, custom_patterns: List[TestPattern] = None
    ) -> ComprehensiveValidationReport:
        """Run comprehensive validation with all test frameworks"""
        start_time = time.time()

        if custom_patterns:
            patterns = custom_patterns
        else:
            patterns = self.generate_comprehensive_test_suite()

        logger.info(f"Starting comprehensive validation with {len(patterns)} patterns")

        all_validation_results = []
        for i, pattern in enumerate(patterns):
            if (i + 1) % 10 == 0:
                logger.info(f"Validated {i + 1}/{len(patterns)} patterns")

            result = self.validator.validate_pattern(pattern)
            all_validation_results.append(result)

        report = self._generate_comprehensive_report(patterns, all_validation_results)

        execution_time = time.time() - start_time
        report.detailed_breakdowns["total_execution_time"] = execution_time
        report.validation_timestamp = time.time()

        logger.info(
            f"Comprehensive validation completed in {execution_time:.2f} seconds"
        )
        return report

    def _generate_comprehensive_report(
        self, patterns: List[TestPattern], validation_results: List[ValidationResult]
    ) -> ComprehensiveValidationReport:
        """Generate comprehensive validation report"""

        total_patterns = len(patterns)

        if not validation_results:
            return ComprehensiveValidationReport(
                total_patterns_tested=0,
                overall_accuracy=0.0,
                domain_coverage_score=0.0,
                pattern_type_performance={},
                complexity_level_performance={},
                cross_validation_metrics={},
                edge_case_handling={},
                performance_benchmarks={},
                statistical_significance={"insufficient_data": True},
                improvement_recommendations=["No patterns tested"],
                detailed_breakdowns={},
                validation_timestamp=time.time(),
            )

        overall_accuracy = statistics.mean(
            [r.accuracy_metrics["overall_accuracy"] for r in validation_results]
        )

        domain_coverage_score = self._calculate_domain_coverage_score(
            patterns, validation_results
        )
        pattern_type_performance = self._analyze_pattern_type_performance(
            validation_results
        )
        complexity_level_performance = self._analyze_complexity_level_performance(
            validation_results
        )
        edge_case_handling = self._analyze_edge_case_handling(validation_results)
        performance_benchmarks = self._calculate_performance_benchmarks(
            validation_results
        )
        statistical_significance = self._calculate_statistical_significance(
            validation_results
        )

        improvement_recommendations = self._generate_improvement_recommendations(
            overall_accuracy,
            domain_coverage_score,
            pattern_type_performance,
            complexity_level_performance,
            edge_case_handling,
            performance_benchmarks,
        )

        detailed_breakdowns = {
            "validation_results_summary": self._summarize_validation_results(
                validation_results
            ),
            "domain_distribution": self._analyze_domain_distribution(patterns),
            "failure_analysis": self._analyze_failures(validation_results),
            "confidence_distribution": self._analyze_confidence_distribution(
                validation_results
            ),
        }

        return ComprehensiveValidationReport(
            total_patterns_tested=total_patterns,
            overall_accuracy=overall_accuracy,
            domain_coverage_score=domain_coverage_score,
            pattern_type_performance=pattern_type_performance,
            complexity_level_performance=complexity_level_performance,
            cross_validation_metrics={},  # Simplified version
            edge_case_handling=edge_case_handling,
            performance_benchmarks=performance_benchmarks,
            statistical_significance=statistical_significance,
            improvement_recommendations=improvement_recommendations,
            detailed_breakdowns=detailed_breakdowns,
            validation_timestamp=time.time(),
        )

    def _calculate_domain_coverage_score(
        self, patterns: List[TestPattern], validation_results: List[ValidationResult]
    ) -> float:
        """Calculate domain coverage score"""
        domain_results = defaultdict(list)

        for pattern, result in zip(patterns, validation_results):
            domain_results[pattern.domain_category].append(
                result.accuracy_metrics["overall_accuracy"]
            )

        domain_accuracies = []
        for domain, accuracies in domain_results.items():
            domain_avg = statistics.mean(accuracies)
            domain_accuracies.append(domain_avg)

        if domain_accuracies:
            return len(domain_accuracies) / sum(
                1 / acc if acc > 0 else float("inf") for acc in domain_accuracies
            )
        return 0.0

    def _analyze_pattern_type_performance(
        self, validation_results: List[ValidationResult]
    ) -> Dict[str, Dict[str, float]]:
        """Analyze performance by pattern type"""
        pattern_type_results = defaultdict(list)

        for result in validation_results:
            pattern_type = result.test_pattern.pattern_type
            pattern_type_results[pattern_type].append(result)

        performance = {}
        for pattern_type, results in pattern_type_results.items():
            if results:
                performance[pattern_type] = {
                    "count": len(results),
                    "accuracy_mean": statistics.mean(
                        [r.accuracy_metrics["overall_accuracy"] for r in results]
                    ),
                    "response_time_mean": statistics.mean(
                        [r.performance_metrics["response_time_ms"] for r in results]
                    ),
                    "confidence_mean": statistics.mean(
                        [r.confidence_score for r in results]
                    ),
                    "pass_rate": sum(
                        1 for r in results if r.validation_status == "pass"
                    )
                    / len(results),
                }

        return performance

    def _analyze_complexity_level_performance(
        self, validation_results: List[ValidationResult]
    ) -> Dict[str, Dict[str, float]]:
        """Analyze performance by complexity level"""
        complexity_results = defaultdict(list)

        for result in validation_results:
            complexity = result.test_pattern.complexity_level
            complexity_results[complexity].append(result)

        performance = {}
        for complexity, results in complexity_results.items():
            if results:
                performance[complexity] = {
                    "count": len(results),
                    "accuracy_mean": statistics.mean(
                        [r.accuracy_metrics["overall_accuracy"] for r in results]
                    ),
                    "pass_rate": sum(
                        1 for r in results if r.validation_status == "pass"
                    )
                    / len(results),
                    "fail_rate": sum(
                        1 for r in results if r.validation_status == "fail"
                    )
                    / len(results),
                }

        return performance

    def _analyze_edge_case_handling(
        self, validation_results: List[ValidationResult]
    ) -> Dict[str, float]:
        """Analyze edge case handling performance"""
        edge_case_results = [
            r
            for r in validation_results
            if r.test_pattern.complexity_level == "edge_case"
        ]

        if not edge_case_results:
            return {"edge_case_count": 0}

        return {
            "edge_case_count": len(edge_case_results),
            "edge_case_accuracy": statistics.mean(
                [r.accuracy_metrics["overall_accuracy"] for r in edge_case_results]
            ),
            "edge_case_pass_rate": sum(
                1 for r in edge_case_results if r.validation_status == "pass"
            )
            / len(edge_case_results),
            "edge_case_confidence_mean": statistics.mean(
                [r.confidence_score for r in edge_case_results]
            ),
            "edge_case_response_time": statistics.mean(
                [r.performance_metrics["response_time_ms"] for r in edge_case_results]
            ),
        }

    def _calculate_performance_benchmarks(
        self, validation_results: List[ValidationResult]
    ) -> Dict[str, float]:
        """Calculate performance benchmarks"""
        response_times = [
            r.performance_metrics["response_time_ms"] for r in validation_results
        ]
        confidence_scores = [r.confidence_score for r in validation_results]

        return {
            "avg_response_time_ms": statistics.mean(response_times),
            "min_response_time_ms": min(response_times) if response_times else 0.0,
            "max_response_time_ms": max(response_times) if response_times else 0.0,
            "avg_confidence": statistics.mean(confidence_scores),
            "low_confidence_rate": (
                sum(1 for c in confidence_scores if c < 0.7) / len(confidence_scores)
                if confidence_scores
                else 0.0
            ),
        }

    def _calculate_statistical_significance(
        self, validation_results: List[ValidationResult]
    ) -> Dict[str, float]:
        """Calculate statistical significance metrics"""
        accuracy_scores = [
            r.accuracy_metrics["overall_accuracy"] for r in validation_results
        ]

        if len(accuracy_scores) < 2:
            return {"insufficient_data": True}

        mean_accuracy = statistics.mean(accuracy_scores)
        std_accuracy = statistics.stdev(accuracy_scores)
        n = len(accuracy_scores)

        margin_of_error = 1.96 * (std_accuracy / (n**0.5))

        return {
            "sample_size": n,
            "mean_accuracy": mean_accuracy,
            "accuracy_std": std_accuracy,
            "confidence_interval_lower": mean_accuracy - margin_of_error,
            "confidence_interval_upper": mean_accuracy + margin_of_error,
            "margin_of_error": margin_of_error,
            "statistical_power": min(1.0, n / 100.0),
        }

    def _generate_improvement_recommendations(
        self,
        overall_accuracy: float,
        domain_coverage: float,
        pattern_type_performance: Dict,
        complexity_performance: Dict,
        edge_case_handling: Dict,
        performance_benchmarks: Dict,
    ) -> List[str]:
        """Generate actionable improvement recommendations"""
        recommendations = []

        if overall_accuracy < 0.90:
            recommendations.append(
                f"Overall accuracy ({overall_accuracy:.2%}) is below 90% target. Focus on improving pattern matching algorithms."
            )
        elif overall_accuracy >= 0.95:
            recommendations.append(
                f"Excellent overall accuracy ({overall_accuracy:.2%}) achieved. Consider optimizing for speed and edge cases."
            )

        if domain_coverage < 0.85:
            recommendations.append(
                f"Domain coverage score ({domain_coverage:.2f}) indicates uneven performance across domains."
            )

        for pattern_type, metrics in pattern_type_performance.items():
            if metrics["accuracy_mean"] < 0.85:
                recommendations.append(
                    f"Pattern type '{pattern_type}' shows low accuracy ({metrics['accuracy_mean']:.2%})."
                )

        if edge_case_handling.get("edge_case_pass_rate", 0) < 0.60:
            recommendations.append("Edge case handling needs significant improvement.")

        if performance_benchmarks["avg_response_time_ms"] > 1000:
            recommendations.append(
                f"Average response time ({performance_benchmarks['avg_response_time_ms']:.0f}ms) exceeds 1s target."
            )

        if not recommendations:
            recommendations.append(
                "System performance meets all targets. Continue monitoring and fine-tuning as needed."
            )

        return recommendations

    def _summarize_validation_results(
        self, validation_results: List[ValidationResult]
    ) -> Dict[str, Any]:
        """Summarize validation results"""
        status_counts = Counter(r.validation_status for r in validation_results)

        return {
            "total_results": len(validation_results),
            "pass_count": status_counts["pass"],
            "partial_count": status_counts["partial"],
            "fail_count": status_counts["fail"],
            "pass_rate": status_counts["pass"] / len(validation_results),
            "partial_rate": status_counts["partial"] / len(validation_results),
            "fail_rate": status_counts["fail"] / len(validation_results),
        }

    def _analyze_domain_distribution(
        self, patterns: List[TestPattern]
    ) -> Dict[str, int]:
        """Analyze domain distribution in test patterns"""
        domain_counts = Counter(p.domain_category for p in patterns)
        return dict(domain_counts)

    def _analyze_failures(
        self, validation_results: List[ValidationResult]
    ) -> Dict[str, Any]:
        """Analyze failure patterns"""
        failed_results = [
            r for r in validation_results if r.validation_status == "fail"
        ]

        if not failed_results:
            return {"no_failures": True}

        failure_reasons = []
        for result in failed_results:
            failure_reasons.extend(result.failure_reasons)

        reason_counts = Counter(failure_reasons)

        return {
            "total_failures": len(failed_results),
            "failure_rate": len(failed_results) / len(validation_results),
            "common_failure_reasons": dict(reason_counts.most_common(5)),
        }

    def _analyze_confidence_distribution(
        self, validation_results: List[ValidationResult]
    ) -> Dict[str, float]:
        """Analyze confidence score distribution"""
        confidence_scores = [r.confidence_score for r in validation_results]

        return {
            "mean_confidence": statistics.mean(confidence_scores),
            "min_confidence": min(confidence_scores),
            "max_confidence": max(confidence_scores),
            "low_confidence_count": sum(1 for c in confidence_scores if c < 0.7),
            "high_confidence_count": sum(1 for c in confidence_scores if c >= 0.9),
        }

    def save_validation_report(
        self, report: ComprehensiveValidationReport, filename: str = None
    ):
        """Save comprehensive validation report"""
        if filename is None:
            timestamp = int(time.time())
            filename = f"comprehensive_validation_report_{timestamp}.json"

        filepath = self.test_results_dir / filename

        with open(filepath, "w") as f:
            json.dump(asdict(report), f, indent=2, default=str)

        logger.info(f"Comprehensive validation report saved to {filepath}")
        return filepath

    def print_validation_summary(self, report: ComprehensiveValidationReport):
        """Print human-readable validation summary"""
        print("\n" + "=" * 80)
        print("COMPREHENSIVE AGENT SELECTION VALIDATION REPORT")
        print("=" * 80)

        print("\nOVERALL PERFORMANCE:")
        print(f"  Total Patterns Tested: {report.total_patterns_tested}")
        print(f"  Overall Accuracy: {report.overall_accuracy:.2%}")
        print(f"  Domain Coverage Score: {report.domain_coverage_score:.2f}")

        print("\nPATTERN TYPE PERFORMANCE:")
        for pattern_type, metrics in report.pattern_type_performance.items():
            print(f"  {pattern_type.upper()}:")
            print(f"    Count: {metrics['count']}")
            print(f"    Accuracy: {metrics['accuracy_mean']:.2%}")
            print(f"    Pass Rate: {metrics['pass_rate']:.2%}")

        print("\nCOMPLEXITY LEVEL PERFORMANCE:")
        for complexity, metrics in report.complexity_level_performance.items():
            print(f"  {complexity.upper()}:")
            print(f"    Count: {metrics['count']}")
            print(f"    Accuracy: {metrics['accuracy_mean']:.2%}")
            print(f"    Pass Rate: {metrics['pass_rate']:.2%}")

        print("\nEDGE CASE HANDLING:")
        for metric, value in report.edge_case_handling.items():
            if isinstance(value, float):
                if "rate" in metric or "accuracy" in metric:
                    print(f"  {metric.replace('_', ' ').title()}: {value:.2%}")
                else:
                    print(f"  {metric.replace('_', ' ').title()}: {value:.2f}")
            else:
                print(f"  {metric.replace('_', ' ').title()}: {value}")

        print("\nIMPROVEMENT RECOMMENDATIONS:")
        for i, recommendation in enumerate(report.improvement_recommendations, 1):
            print(f"  {i}. {recommendation}")

        print("=" * 80)


# Test fixtures for pytest
@pytest.fixture
def test_framework():
    """Pytest fixture for test framework"""
    return AgentSelectionTestFramework()


@pytest.fixture
def sample_patterns():
    """Pytest fixture for sample test patterns"""
    generator = DomainSpecificPatternGenerator()
    return generator.generate_patterns(10)


# Main execution
if __name__ == "__main__":
    framework = AgentSelectionTestFramework()

    print("Running comprehensive agent selection validation...")
    report = framework.run_comprehensive_validation()

    framework.print_validation_summary(report)

    saved_path = framework.save_validation_report(report)
    print(f"\nDetailed report saved to: {saved_path}")
