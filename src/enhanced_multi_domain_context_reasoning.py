"""Enhanced Multi-Domain Context Reasoning System for Claude Code Framework.

This module provides advanced context reasoning capabilities for multi-domain scenarios
with improved:

- Multi-domain pattern recognition with semantic analysis
- Cross-domain relationship mapping and dependency tracking
- Context preservation strategies across agent handoffs
- Domain-specific optimization for improved coordination accuracy
- Pattern learning with contextual reinforcement

Author: Pattern Analyzer Agent
Purpose: Advanced multi-domain context reasoning with enhanced pattern detection
"""

import re
import time
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContextPreservationStrategy(Enum):
    """Strategies for preserving context across domain transitions."""

    FULL_TRANSFER = "full_transfer"  # Complete context transfer
    SELECTIVE_TRANSFER = "selective_transfer"  # Domain-relevant context only
    HIERARCHICAL_TRANSFER = "hierarchical_transfer"  # Structured context layers
    ADAPTIVE_TRANSFER = "adaptive_transfer"  # Dynamic context selection


class DomainRelationshipType(Enum):
    """Types of relationships between domains."""

    SEQUENTIAL = "sequential"  # One domain follows another
    PARALLEL = "parallel"  # Domains operate simultaneously
    HIERARCHICAL = "hierarchical"  # Parent-child domain relationship
    SYNERGISTIC = "synergistic"  # Domains enhance each other
    CONFLICTING = "conflicting"  # Domains have opposing requirements
    DEPENDENT = "dependent"  # One domain requires another


class PatternComplexity(Enum):
    """Complexity levels for multi-domain patterns."""

    SIMPLE = "simple"  # Single domain with minor cross-domain elements
    MODERATE = "moderate"  # 2-3 domains with clear relationships
    COMPLEX = "complex"  # 4+ domains or unclear relationships
    CRITICAL = "critical"  # System-wide impact or crisis scenarios


@dataclass
class ContextElement:
    """Individual context element with domain mapping."""

    element_id: str
    content: str
    domain: str
    importance: float  # 0.0 to 1.0
    timestamp: datetime
    dependencies: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DomainRelationship:
    """Relationship between two domains."""

    from_domain: str
    to_domain: str
    relationship_type: DomainRelationshipType
    strength: float  # 0.0 to 1.0
    bidirectional: bool = False
    context_transfer_rules: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MultiDomainPattern:
    """Pattern spanning multiple domains."""

    pattern_id: str
    domains: Set[str]
    complexity: PatternComplexity
    trigger_keywords: Set[str]
    success_indicators: List[str]
    context_requirements: List[str]
    coordination_strategy: str
    success_rate: float = 0.0
    usage_count: int = 0
    last_used: Optional[datetime] = None


@dataclass
class ContextPreservationMetrics:
    """Metrics for context preservation quality."""

    total_elements: int
    preserved_elements: int
    critical_elements_preserved: int
    critical_elements_total: int
    domain_coverage: float
    semantic_coherence: float
    transfer_latency_ms: float


class SemanticAnalyzer:
    """Semantic analysis for context understanding."""

    def __init__(self):
        self.domain_semantics = self._build_domain_semantics()
        self.relationship_patterns = self._build_relationship_patterns()
        self.context_indicators = self._build_context_indicators()

    def _build_domain_semantics(self) -> Dict[str, Dict[str, List[str]]]:
        """Build semantic patterns for each domain."""
        return {
            "testing": {
                "core_concepts": [
                    "test",
                    "spec",
                    "assertion",
                    "mock",
                    "fixture",
                    "coverage",
                    "validation",
                ],
                "actions": [
                    "run",
                    "execute",
                    "validate",
                    "verify",
                    "check",
                    "assert",
                    "mock",
                ],
                "quality_indicators": [
                    "comprehensive",
                    "thorough",
                    "complete",
                    "robust",
                    "reliable",
                ],
                "problem_indicators": [
                    "failing",
                    "broken",
                    "incomplete",
                    "flaky",
                    "unstable",
                ],
            },
            "infrastructure": {
                "core_concepts": [
                    "docker",
                    "container",
                    "deployment",
                    "orchestration",
                    "scaling",
                    "networking",
                ],
                "actions": [
                    "deploy",
                    "orchestrate",
                    "scale",
                    "configure",
                    "manage",
                    "monitor",
                ],
                "quality_indicators": [
                    "scalable",
                    "resilient",
                    "efficient",
                    "stable",
                    "robust",
                ],
                "problem_indicators": [
                    "failing",
                    "unstable",
                    "slow",
                    "bottleneck",
                    "resource",
                ],
            },
            "security": {
                "core_concepts": [
                    "authentication",
                    "authorization",
                    "encryption",
                    "vulnerability",
                    "compliance",
                ],
                "actions": [
                    "secure",
                    "encrypt",
                    "authenticate",
                    "authorize",
                    "validate",
                    "audit",
                ],
                "quality_indicators": [
                    "secure",
                    "compliant",
                    "validated",
                    "encrypted",
                    "protected",
                ],
                "problem_indicators": [
                    "vulnerable",
                    "insecure",
                    "exposed",
                    "breach",
                    "weak",
                ],
            },
            "performance": {
                "core_concepts": [
                    "latency",
                    "throughput",
                    "bottleneck",
                    "optimization",
                    "resource",
                    "memory",
                ],
                "actions": [
                    "optimize",
                    "tune",
                    "improve",
                    "accelerate",
                    "monitor",
                    "profile",
                ],
                "quality_indicators": [
                    "fast",
                    "efficient",
                    "optimized",
                    "scalable",
                    "responsive",
                ],
                "problem_indicators": [
                    "slow",
                    "bottleneck",
                    "inefficient",
                    "memory leak",
                    "high latency",
                ],
            },
        }

    def _build_relationship_patterns(self) -> Dict[str, List[str]]:
        """Build patterns that indicate domain relationships."""
        return {
            "sequential": [
                r"(\w+)\s+then\s+(\w+)",
                r"after\s+(\w+)\s+.*\s+(\w+)",
                r"(\w+)\s+followed\s+by\s+(\w+)",
            ],
            "parallel": [
                r"(\w+)\s+and\s+(\w+)\s+(simultaneously|parallel|together)",
                r"coordinate\s+(\w+)\s+with\s+(\w+)",
                r"(\w+)\s+while\s+(\w+)",
            ],
            "dependent": [
                r"(\w+)\s+requires?\s+(\w+)",
                r"(\w+)\s+depends?\s+on\s+(\w+)",
                r"(\w+)\s+needs?\s+(\w+)",
            ],
            "conflicting": [
                r"(\w+)\s+vs\s+(\w+)",
                r"(\w+)\s+conflicts?\s+with\s+(\w+)",
                r"trade.?off\s+between\s+(\w+)\s+and\s+(\w+)",
            ],
        }

    def _build_context_indicators(self) -> Dict[str, List[str]]:
        """Build indicators for context importance."""
        return {
            "critical": [
                "critical",
                "essential",
                "vital",
                "crucial",
                "mandatory",
                "required",
            ],
            "high": ["important", "significant", "major", "key", "primary"],
            "medium": ["relevant", "useful", "helpful", "supporting", "secondary"],
            "low": ["minor", "optional", "supplementary", "nice-to-have"],
        }

    def analyze_semantic_patterns(self, text: str) -> Dict[str, Any]:
        """Analyze semantic patterns in text."""
        text_lower = text.lower()
        results = {
            "domain_scores": {},
            "relationship_indicators": [],
            "context_importance": {},
            "semantic_complexity": 0.0,
        }

        # Calculate domain scores based on semantic patterns
        for domain, patterns in self.domain_semantics.items():
            score = 0.0
            matches = []

            for category, keywords in patterns.items():
                category_matches = sum(
                    1 for keyword in keywords if keyword in text_lower
                )
                score += category_matches * self._get_category_weight(category)
                if category_matches > 0:
                    matches.extend([kw for kw in keywords if kw in text_lower])

            # Also check for domain name in text
            if domain in text_lower:
                score += 2.0
                matches.append(domain)

            if score > 0:
                results["domain_scores"][domain] = {
                    "score": score,
                    "matches": matches,
                    "confidence": min(
                        score / 8.0, 1.0
                    ),  # Adjusted normalization for better sensitivity
                }

        # Detect relationship indicators
        for rel_type, patterns in self.relationship_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text_lower)
                for match in matches:
                    results["relationship_indicators"].append(
                        {
                            "type": rel_type,
                            "match": match.group(),
                            "position": match.span(),
                        }
                    )

        # Calculate context importance
        for importance, indicators in self.context_indicators.items():
            count = sum(1 for indicator in indicators if indicator in text_lower)
            if count > 0:
                results["context_importance"][importance] = count

        # Calculate semantic complexity
        domain_count = len(results["domain_scores"])
        relationship_count = len(results["relationship_indicators"])
        results["semantic_complexity"] = min(
            (domain_count * 0.3 + relationship_count * 0.2), 1.0
        )

        return results

    def _get_category_weight(self, category: str) -> float:
        """Get weight for semantic category."""
        weights = {
            "core_concepts": 3.0,
            "actions": 2.0,
            "quality_indicators": 1.5,
            "problem_indicators": 2.5,
        }
        return weights.get(category, 1.0)


class CrossDomainRelationshipMapper:
    """Maps relationships between domains based on patterns and history."""

    def __init__(self):
        self.relationship_registry: Dict[Tuple[str, str], DomainRelationship] = {}
        self.pattern_history: List[MultiDomainPattern] = []
        self.success_metrics: Dict[str, float] = defaultdict(float)

    def register_relationship(self, relationship: DomainRelationship):
        """Register a domain relationship."""
        key = (relationship.from_domain, relationship.to_domain)
        self.relationship_registry[key] = relationship

        # If bidirectional, register reverse relationship
        if relationship.bidirectional:
            reverse_key = (relationship.to_domain, relationship.from_domain)
            reverse_rel = DomainRelationship(
                from_domain=relationship.to_domain,
                to_domain=relationship.from_domain,
                relationship_type=relationship.relationship_type,
                strength=relationship.strength,
                bidirectional=False,
                context_transfer_rules=relationship.context_transfer_rules,
            )
            self.relationship_registry[reverse_key] = reverse_rel

    def get_relationship_strength(self, from_domain: str, to_domain: str) -> float:
        """Get relationship strength between domains."""
        key = (from_domain, to_domain)
        if key in self.relationship_registry:
            return self.relationship_registry[key].strength
        return 0.0

    def find_domain_path(
        self, from_domain: str, to_domain: str, max_hops: int = 3
    ) -> List[str]:
        """Find path between domains using relationship graph."""
        if from_domain == to_domain:
            return [from_domain]

        visited = set()
        queue = deque([(from_domain, [from_domain])])

        while queue and len(queue[0][1]) <= max_hops:
            current_domain, path = queue.popleft()

            if current_domain in visited:
                continue
            visited.add(current_domain)

            # Check direct connections
            for (source, target), relationship in self.relationship_registry.items():
                if source == current_domain and target not in visited:
                    new_path = path + [target]
                    if target == to_domain:
                        return new_path
                    queue.append((target, new_path))

        return []  # No path found

    def get_related_domains(
        self, domain: str, min_strength: float = 0.3
    ) -> List[Tuple[str, float]]:
        """Get domains related to given domain above minimum strength."""
        related = []
        for (source, target), relationship in self.relationship_registry.items():
            if source == domain and relationship.strength >= min_strength:
                related.append((target, relationship.strength))

        return sorted(related, key=lambda x: x[1], reverse=True)

    def update_relationship_strength(
        self,
        from_domain: str,
        to_domain: str,
        success: bool,
        learning_rate: float = 0.1,
    ):
        """Update relationship strength based on coordination success."""
        key = (from_domain, to_domain)
        if key in self.relationship_registry:
            current_strength = self.relationship_registry[key].strength
            if success:
                new_strength = min(1.0, current_strength + learning_rate)
            else:
                new_strength = max(0.0, current_strength - learning_rate * 0.5)

            self.relationship_registry[key].strength = new_strength


class ContextPreservationManager:
    """Manages context preservation across domain transitions."""

    def __init__(self, relationship_mapper: CrossDomainRelationshipMapper):
        self.relationship_mapper = relationship_mapper
        self.preservation_strategies = self._build_preservation_strategies()
        self.context_cache: Dict[str, List[ContextElement]] = {}
        self.transfer_history: List[Dict[str, Any]] = []

    def _build_preservation_strategies(self) -> Dict[str, callable]:
        """Build context preservation strategies."""
        return {
            ContextPreservationStrategy.FULL_TRANSFER.value: self._full_transfer,
            ContextPreservationStrategy.SELECTIVE_TRANSFER.value: self._selective_transfer,
            ContextPreservationStrategy.HIERARCHICAL_TRANSFER.value: self._hierarchical_transfer,
            ContextPreservationStrategy.ADAPTIVE_TRANSFER.value: self._adaptive_transfer,
        }

    def preserve_context(
        self,
        context_elements: List[ContextElement],
        from_domain: str,
        to_domain: str,
        strategy: ContextPreservationStrategy = ContextPreservationStrategy.ADAPTIVE_TRANSFER,
    ) -> Tuple[List[ContextElement], ContextPreservationMetrics]:
        """Preserve context across domain transition."""
        start_time = time.time()

        # Select preservation strategy
        strategy_func = self.preservation_strategies[strategy.value]
        preserved_elements = strategy_func(context_elements, from_domain, to_domain)

        # Calculate metrics
        metrics = self._calculate_preservation_metrics(
            context_elements, preserved_elements, from_domain, to_domain, start_time
        )

        # Record transfer for learning
        self.transfer_history.append(
            {
                "from_domain": from_domain,
                "to_domain": to_domain,
                "strategy": strategy.value,
                "metrics": metrics,
                "timestamp": datetime.now(),
            }
        )

        # Cache preserved context
        cache_key = f"{from_domain}_{to_domain}_{int(time.time())}"
        self.context_cache[cache_key] = preserved_elements

        return preserved_elements, metrics

    def _full_transfer(
        self, context_elements: List[ContextElement], from_domain: str, to_domain: str
    ) -> List[ContextElement]:
        """Transfer all context elements."""
        return context_elements.copy()

    def _selective_transfer(
        self, context_elements: List[ContextElement], from_domain: str, to_domain: str
    ) -> List[ContextElement]:
        """Transfer only domain-relevant context elements."""
        relationship_strength = self.relationship_mapper.get_relationship_strength(
            from_domain, to_domain
        )
        importance_threshold = max(0.3, 1.0 - relationship_strength)

        preserved = []
        for element in context_elements:
            # Keep high-importance elements
            if element.importance >= importance_threshold:
                preserved.append(element)
            # Keep elements relevant to target domain
            elif element.domain == to_domain or to_domain in element.dependencies:
                preserved.append(element)

        return preserved

    def _hierarchical_transfer(
        self, context_elements: List[ContextElement], from_domain: str, to_domain: str
    ) -> List[ContextElement]:
        """Transfer context using hierarchical importance structure."""
        # Sort by importance
        sorted_elements = sorted(
            context_elements, key=lambda x: x.importance, reverse=True
        )

        # Create hierarchical layers
        critical_layer = [e for e in sorted_elements if e.importance >= 0.8]
        high_layer = [e for e in sorted_elements if 0.6 <= e.importance < 0.8]
        medium_layer = [e for e in sorted_elements if 0.4 <= e.importance < 0.6]

        # Always preserve critical layer
        preserved = critical_layer.copy()

        # Add high layer if domains are strongly related
        relationship_strength = self.relationship_mapper.get_relationship_strength(
            from_domain, to_domain
        )
        if relationship_strength >= 0.6:
            preserved.extend(high_layer)

        # Add medium layer if domains are moderately related and complexity is high
        if relationship_strength >= 0.4 and len(context_elements) > 10:
            preserved.extend(medium_layer)

        return preserved

    def _adaptive_transfer(
        self, context_elements: List[ContextElement], from_domain: str, to_domain: str
    ) -> List[ContextElement]:
        """Adaptively select context preservation strategy based on context analysis."""
        # Analyze context characteristics
        total_elements = len(context_elements)
        avg_importance = sum(e.importance for e in context_elements) / max(
            total_elements, 1
        )
        domain_diversity = len(set(e.domain for e in context_elements))
        relationship_strength = self.relationship_mapper.get_relationship_strength(
            from_domain, to_domain
        )

        # Select strategy based on analysis
        if total_elements <= 5 or avg_importance >= 0.8:
            return self._full_transfer(context_elements, from_domain, to_domain)
        elif relationship_strength >= 0.7 and domain_diversity <= 3:
            return self._hierarchical_transfer(context_elements, from_domain, to_domain)
        else:
            return self._selective_transfer(context_elements, from_domain, to_domain)

    def _calculate_preservation_metrics(
        self,
        original: List[ContextElement],
        preserved: List[ContextElement],
        from_domain: str,
        to_domain: str,
        start_time: float,
    ) -> ContextPreservationMetrics:
        """Calculate context preservation quality metrics."""
        total_elements = len(original)
        preserved_count = len(preserved)

        # Count critical elements
        critical_original = sum(1 for e in original if e.importance >= 0.8)
        critical_preserved = sum(1 for e in preserved if e.importance >= 0.8)

        # Calculate domain coverage
        original_domains = set(e.domain for e in original)
        preserved_domains = set(e.domain for e in preserved)
        domain_coverage = len(preserved_domains) / max(len(original_domains), 1)

        # Calculate semantic coherence (simplified)
        semantic_coherence = min(1.0, preserved_count / max(total_elements * 0.7, 1))

        # Calculate transfer latency
        transfer_latency_ms = (time.time() - start_time) * 1000

        return ContextPreservationMetrics(
            total_elements=total_elements,
            preserved_elements=preserved_count,
            critical_elements_preserved=critical_preserved,
            critical_elements_total=critical_original,
            domain_coverage=domain_coverage,
            semantic_coherence=semantic_coherence,
            transfer_latency_ms=transfer_latency_ms,
        )

    def get_preservation_quality_score(
        self, metrics: ContextPreservationMetrics
    ) -> float:
        """Calculate overall preservation quality score."""
        # Weighted scoring
        preservation_ratio = metrics.preserved_elements / max(metrics.total_elements, 1)
        critical_preservation = (
            metrics.critical_elements_preserved
            / max(metrics.critical_elements_total, 1)
            if metrics.critical_elements_total > 0
            else 1.0
        )

        # Combine metrics with weights
        score = (
            preservation_ratio * 0.3
            + critical_preservation * 0.4
            + metrics.domain_coverage * 0.2
            + metrics.semantic_coherence * 0.1
        )

        return min(score, 1.0)


class DomainSpecificOptimizer:
    """Optimizes coordination patterns for specific domains."""

    def __init__(self):
        self.domain_optimizations = self._build_domain_optimizations()
        self.optimization_history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.performance_baselines: Dict[str, Dict[str, float]] = {}

    def _build_domain_optimizations(self) -> Dict[str, Dict[str, Any]]:
        """Build domain-specific optimization rules."""
        return {
            "testing": {
                "priority_keywords": [
                    "async",
                    "mock",
                    "fixture",
                    "coverage",
                    "integration",
                ],
                "coordination_preference": "sequential",  # Testing often requires sequential execution
                "context_retention": 0.9,  # High context retention for test debugging
                "parallel_threshold": 3,  # Can handle 3+ parallel test coordinators
                "optimization_focus": ["execution_speed", "result_accuracy"],
            },
            "infrastructure": {
                "priority_keywords": [
                    "docker",
                    "container",
                    "deployment",
                    "scaling",
                    "networking",
                ],
                "coordination_preference": "hierarchical",  # Infrastructure has clear hierarchies
                "context_retention": 0.8,  # Medium-high context retention
                "parallel_threshold": 5,  # Can handle complex parallel coordination
                "optimization_focus": ["resource_efficiency", "reliability"],
            },
            "security": {
                "priority_keywords": [
                    "vulnerability",
                    "authentication",
                    "encryption",
                    "compliance",
                ],
                "coordination_preference": "sequential",  # Security requires careful sequential validation
                "context_retention": 0.95,  # Very high context retention for security audits
                "parallel_threshold": 2,  # Limited parallel coordination for security
                "optimization_focus": ["thoroughness", "compliance_validation"],
            },
            "performance": {
                "priority_keywords": [
                    "latency",
                    "throughput",
                    "bottleneck",
                    "optimization",
                ],
                "coordination_preference": "parallel",  # Performance analysis benefits from parallel execution
                "context_retention": 0.85,  # High context retention for performance correlation
                "parallel_threshold": 4,  # Good parallel coordination capability
                "optimization_focus": ["speed", "resource_usage"],
            },
        }

    def optimize_for_domain(
        self, domain: str, coordination_request: str, available_agents: List[str]
    ) -> Dict[str, Any]:
        """Optimize coordination strategy for specific domain."""
        if domain not in self.domain_optimizations:
            return self._default_optimization(coordination_request, available_agents)

        domain_config = self.domain_optimizations[domain]

        # Analyze coordination request
        request_analysis = self._analyze_coordination_request(
            coordination_request, domain_config
        )

        # Select optimal agents
        optimal_agents = self._select_optimal_agents(
            available_agents, domain, request_analysis
        )

        # Determine coordination strategy
        coordination_strategy = self._determine_coordination_strategy(
            domain_config, request_analysis
        )

        # Calculate optimization confidence
        confidence = self._calculate_optimization_confidence(
            domain, request_analysis, optimal_agents
        )

        optimization_result = {
            "domain": domain,
            "optimal_agents": optimal_agents,
            "coordination_strategy": coordination_strategy,
            "context_retention_target": domain_config["context_retention"],
            "parallel_capability": domain_config["parallel_threshold"],
            "optimization_focus": domain_config["optimization_focus"],
            "confidence": confidence,
            "analysis": request_analysis,
        }

        # Record optimization for learning
        self.optimization_history[domain].append(
            {
                "request": coordination_request,
                "result": optimization_result,
                "timestamp": datetime.now(),
            }
        )

        return optimization_result

    def _analyze_coordination_request(
        self, request: str, domain_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze coordination request for domain-specific patterns."""
        request_lower = request.lower()

        # Check for priority keywords
        priority_matches = [
            keyword
            for keyword in domain_config["priority_keywords"]
            if keyword in request_lower
        ]

        # Detect complexity indicators
        complexity_indicators = [
            "comprehensive",
            "complex",
            "multi-step",
            "end-to-end",
            "systematic",
            "thorough",
            "complete",
        ]
        complexity_matches = [
            ind for ind in complexity_indicators if ind in request_lower
        ]

        # Detect parallel coordination signals
        parallel_indicators = [
            "parallel",
            "simultaneously",
            "coordinate",
            "multiple",
            "tasks in parallel",
            "concurrent",
        ]
        parallel_matches = [ind for ind in parallel_indicators if ind in request_lower]

        return {
            "priority_keyword_matches": priority_matches,
            "priority_score": len(priority_matches)
            / len(domain_config["priority_keywords"]),
            "complexity_indicators": complexity_matches,
            "complexity_score": min(len(complexity_matches) / 3.0, 1.0),
            "parallel_indicators": parallel_matches,
            "parallel_score": min(len(parallel_matches) / 2.0, 1.0),
        }

    def _select_optimal_agents(
        self, available_agents: List[str], domain: str, analysis: Dict[str, Any]
    ) -> List[str]:
        """Select optimal agents based on domain optimization."""
        # Priority agents for each domain
        domain_priorities = {
            "testing": [
                "test-specialist",
                "coverage-optimizer",
                "fixture-design-specialist",
            ],
            "infrastructure": [
                "infrastructure-engineer",
                "docker-specialist",
                "environment-analyst",
            ],
            "security": [
                "security-auditor",
                "security-enforcer",
                "code-quality-specialist",
            ],
            "performance": ["performance-optimizer", "resource-optimizer"],
        }

        priority_agents = domain_priorities.get(domain, [])
        selected_agents = []

        # Add priority agents first
        for agent in priority_agents:
            if agent in available_agents:
                selected_agents.append(agent)

        # Add complementary agents based on analysis
        if analysis["parallel_score"] > 0.5 and len(selected_agents) < 3:
            # Add coordination agents for parallel execution
            coordination_agents = ["analysis-gateway", "meta-coordinator"]
            for agent in coordination_agents:
                if agent in available_agents and agent not in selected_agents:
                    selected_agents.append(agent)
                    break

        return selected_agents[:5]  # Limit to 5 agents for efficiency

    def _determine_coordination_strategy(
        self, domain_config: Dict[str, Any], analysis: Dict[str, Any]
    ) -> str:
        """Determine optimal coordination strategy."""
        base_preference = domain_config["coordination_preference"]

        # Override based on analysis
        if analysis["parallel_score"] > 0.7:
            return "parallel"
        elif analysis["complexity_score"] > 0.8:
            return "hierarchical"
        else:
            return base_preference

    def _calculate_optimization_confidence(
        self, domain: str, analysis: Dict[str, Any], selected_agents: List[str]
    ) -> float:
        """Calculate confidence in optimization decisions."""
        # Base confidence from domain match
        base_confidence = 0.7

        # Boost from priority keyword matches
        priority_boost = analysis["priority_score"] * 0.2

        # Boost from having optimal agents available
        agent_boost = min(len(selected_agents) / 3.0, 1.0) * 0.1

        # Penalty for high complexity without sufficient analysis
        complexity_penalty = max(0, (analysis["complexity_score"] - 0.5) * 0.15)

        confidence = base_confidence + priority_boost + agent_boost - complexity_penalty

        return min(max(confidence, 0.0), 1.0)

    def _default_optimization(
        self, coordination_request: str, available_agents: List[str]
    ) -> Dict[str, Any]:
        """Default optimization for unknown domains."""
        return {
            "domain": "unknown",
            "optimal_agents": available_agents[:3],  # Use first 3 available agents
            "coordination_strategy": "sequential",
            "context_retention_target": 0.8,
            "parallel_capability": 2,
            "optimization_focus": ["general_effectiveness"],
            "confidence": 0.5,
            "analysis": {"note": "Default optimization applied"},
        }

    def get_domain_performance_baseline(self, domain: str) -> Dict[str, float]:
        """Get performance baseline metrics for domain."""
        if domain not in self.performance_baselines:
            # Set default baselines
            self.performance_baselines[domain] = {
                "avg_response_time_ms": 1500.0,
                "success_rate": 0.85,
                "context_preservation": 0.85,
                "coordination_accuracy": 0.80,
            }

        return self.performance_baselines[domain]

    def update_performance_baseline(self, domain: str, metrics: Dict[str, float]):
        """Update performance baseline with new metrics."""
        if domain not in self.performance_baselines:
            self.performance_baselines[domain] = metrics.copy()
        else:
            # Use exponential moving average for updates
            alpha = 0.1  # Learning rate
            for metric, value in metrics.items():
                if metric in self.performance_baselines[domain]:
                    current = self.performance_baselines[domain][metric]
                    self.performance_baselines[domain][metric] = (
                        1 - alpha
                    ) * current + alpha * value
                else:
                    self.performance_baselines[domain][metric] = value


class EnhancedMultiDomainContextReasoner:
    """Main class for enhanced multi-domain context reasoning."""

    def __init__(self, coordination_hub_path: Optional[str] = None):
        self.semantic_analyzer = SemanticAnalyzer()
        self.relationship_mapper = CrossDomainRelationshipMapper()
        self.context_manager = ContextPreservationManager(self.relationship_mapper)
        self.domain_optimizer = DomainSpecificOptimizer()

        # Initialize with default domain relationships
        self._initialize_default_relationships()

        # Performance tracking
        self.reasoning_metrics: Dict[str, List[float]] = defaultdict(list)

    def _initialize_default_relationships(self):
        """Initialize default domain relationships."""
        relationships = [
            # Testing relationships
            DomainRelationship(
                "testing", "infrastructure", DomainRelationshipType.DEPENDENT, 0.7
            ),
            DomainRelationship(
                "testing", "security", DomainRelationshipType.SEQUENTIAL, 0.6
            ),
            DomainRelationship(
                "testing", "performance", DomainRelationshipType.PARALLEL, 0.8
            ),
            # Infrastructure relationships
            DomainRelationship(
                "infrastructure", "security", DomainRelationshipType.HIERARCHICAL, 0.9
            ),
            DomainRelationship(
                "infrastructure", "performance", DomainRelationshipType.SYNERGISTIC, 0.8
            ),
            # Security relationships
            DomainRelationship(
                "security", "performance", DomainRelationshipType.CONFLICTING, 0.6
            ),
            # Bidirectional relationships
            DomainRelationship(
                "testing",
                "infrastructure",
                DomainRelationshipType.SYNERGISTIC,
                0.7,
                True,
            ),
        ]

        for relationship in relationships:
            self.relationship_mapper.register_relationship(relationship)

    def analyze_multi_domain_query(self, query: str) -> Dict[str, Any]:
        """Comprehensive analysis of multi-domain query."""
        start_time = time.time()

        # Semantic analysis
        semantic_analysis = self.semantic_analyzer.analyze_semantic_patterns(query)

        # Identify primary and secondary domains
        domain_scores = semantic_analysis["domain_scores"]
        sorted_domains = sorted(
            domain_scores.items(), key=lambda x: x[1]["confidence"], reverse=True
        )

        primary_domain = sorted_domains[0][0] if sorted_domains else "general"
        # Lower threshold for secondary domain detection to catch more multi-domain scenarios
        secondary_domains = [
            d[0] for d in sorted_domains[1:] if d[1]["confidence"] >= 0.2
        ]

        # Analyze domain relationships
        domain_relationships = self._analyze_domain_relationships(
            primary_domain, secondary_domains
        )

        # Determine pattern complexity
        complexity = self._determine_pattern_complexity(
            semantic_analysis, domain_relationships
        )

        # Generate coordination strategy
        coordination_strategy = self._generate_coordination_strategy(
            primary_domain, secondary_domains, complexity, query
        )

        # Calculate reasoning confidence
        confidence = self._calculate_reasoning_confidence(
            semantic_analysis, domain_relationships, coordination_strategy
        )

        analysis_time = (time.time() - start_time) * 1000
        self.reasoning_metrics["analysis_time_ms"].append(analysis_time)

        return {
            "query": query,
            "primary_domain": primary_domain,
            "secondary_domains": secondary_domains,
            "semantic_analysis": semantic_analysis,
            "domain_relationships": domain_relationships,
            "pattern_complexity": complexity,
            "coordination_strategy": coordination_strategy,
            "reasoning_confidence": confidence,
            "analysis_time_ms": analysis_time,
            "timestamp": datetime.now().isoformat(),
        }

    def _analyze_domain_relationships(
        self, primary_domain: str, secondary_domains: List[str]
    ) -> List[Dict[str, Any]]:
        """Analyze relationships between identified domains."""
        relationships = []

        for secondary_domain in secondary_domains:
            # Get direct relationship
            strength = self.relationship_mapper.get_relationship_strength(
                primary_domain, secondary_domain
            )

            # Find relationship path
            path = self.relationship_mapper.find_domain_path(
                primary_domain, secondary_domain
            )

            # Get related domains
            related = self.relationship_mapper.get_related_domains(secondary_domain)

            relationships.append(
                {
                    "from_domain": primary_domain,
                    "to_domain": secondary_domain,
                    "strength": strength,
                    "path": path,
                    "path_length": len(path) - 1 if len(path) > 1 else 0,
                    "related_domains": related[:3],  # Top 3 related domains
                }
            )

        return relationships

    def _determine_pattern_complexity(
        self,
        semantic_analysis: Dict[str, Any],
        domain_relationships: List[Dict[str, Any]],
    ) -> PatternComplexity:
        """Determine the complexity level of the multi-domain pattern."""
        domain_count = len(semantic_analysis["domain_scores"])
        relationship_count = len(semantic_analysis["relationship_indicators"])
        semantic_complexity = semantic_analysis["semantic_complexity"]

        # Calculate relationship complexity
        avg_path_length = sum(rel["path_length"] for rel in domain_relationships) / max(
            len(domain_relationships), 1
        )

        # Determine complexity level with adjusted thresholds
        if domain_count <= 1 and relationship_count <= 1 and semantic_complexity <= 0.4:
            return PatternComplexity.SIMPLE
        elif domain_count <= 2 and semantic_complexity <= 0.6 and avg_path_length <= 1:
            return PatternComplexity.MODERATE
        elif domain_count <= 4 and semantic_complexity <= 0.8:
            return PatternComplexity.COMPLEX
        else:
            return PatternComplexity.CRITICAL

    def _generate_coordination_strategy(
        self,
        primary_domain: str,
        secondary_domains: List[str],
        complexity: PatternComplexity,
        query: str,
    ) -> Dict[str, Any]:
        """Generate optimal coordination strategy."""
        # Get domain optimization
        available_agents = (
            self._get_available_agents()
        )  # This would come from agent registry
        domain_optimization = self.domain_optimizer.optimize_for_domain(
            primary_domain, query, available_agents
        )

        # Determine coordination approach based on complexity
        if complexity == PatternComplexity.SIMPLE:
            approach = "direct_agent"
            agent_count = 1
        elif complexity == PatternComplexity.MODERATE:
            approach = "sequential_coordination"
            agent_count = min(3, len(secondary_domains) + 1)
        elif complexity == PatternComplexity.COMPLEX:
            approach = "parallel_coordination"
            agent_count = min(5, len(secondary_domains) + 2)
        else:  # CRITICAL
            approach = "hierarchical_meta_coordination"
            agent_count = min(7, len(secondary_domains) + 3)

        # Select agents based on domain optimization
        selected_agents = domain_optimization["optimal_agents"][:agent_count]

        # Determine context preservation strategy
        context_strategy = self._select_context_preservation_strategy(
            complexity, len(secondary_domains)
        )

        return {
            "approach": approach,
            "selected_agents": selected_agents,
            "agent_count": agent_count,
            "coordination_preference": domain_optimization["coordination_strategy"],
            "context_preservation_strategy": context_strategy.value,
            "context_retention_target": domain_optimization["context_retention_target"],
            "parallel_capability": domain_optimization["parallel_capability"],
            "optimization_focus": domain_optimization["optimization_focus"],
            "estimated_execution_time_ms": self._estimate_execution_time(
                approach, agent_count, complexity
            ),
        }

    def _select_context_preservation_strategy(
        self, complexity: PatternComplexity, domain_count: int
    ) -> ContextPreservationStrategy:
        """Select optimal context preservation strategy."""
        if complexity == PatternComplexity.SIMPLE:
            return ContextPreservationStrategy.FULL_TRANSFER
        elif complexity == PatternComplexity.MODERATE and domain_count <= 2:
            return ContextPreservationStrategy.HIERARCHICAL_TRANSFER
        elif complexity == PatternComplexity.CRITICAL or domain_count >= 4:
            return ContextPreservationStrategy.ADAPTIVE_TRANSFER
        else:
            return ContextPreservationStrategy.SELECTIVE_TRANSFER

    def _estimate_execution_time(
        self, approach: str, agent_count: int, complexity: PatternComplexity
    ) -> float:
        """Estimate execution time for coordination strategy."""
        base_times = {
            "direct_agent": 800,
            "sequential_coordination": 1500,
            "parallel_coordination": 1200,
            "hierarchical_meta_coordination": 2000,
        }

        base_time = base_times.get(approach, 1500)

        # Adjust for agent count
        agent_factor = 1.0 + (agent_count - 1) * 0.15

        # Adjust for complexity
        complexity_factors = {
            PatternComplexity.SIMPLE: 0.8,
            PatternComplexity.MODERATE: 1.0,
            PatternComplexity.COMPLEX: 1.3,
            PatternComplexity.CRITICAL: 1.8,
        }
        complexity_factor = complexity_factors[complexity]

        return base_time * agent_factor * complexity_factor

    def _calculate_reasoning_confidence(
        self,
        semantic_analysis: Dict[str, Any],
        domain_relationships: List[Dict[str, Any]],
        coordination_strategy: Dict[str, Any],
    ) -> float:
        """Calculate confidence in reasoning decisions."""
        # Base confidence from semantic analysis
        semantic_confidence = min(semantic_analysis["semantic_complexity"] + 0.3, 1.0)

        # Relationship confidence
        if domain_relationships:
            avg_relationship_strength = sum(
                rel["strength"] for rel in domain_relationships
            ) / len(domain_relationships)
        else:
            avg_relationship_strength = 0.5

        # Strategy confidence (based on agent availability and approach suitability)
        strategy_confidence = (
            0.8  # This would be calculated based on actual agent availability
        )

        # Combine confidences
        overall_confidence = (
            semantic_confidence * 0.4
            + avg_relationship_strength * 0.3
            + strategy_confidence * 0.3
        )

        return min(max(overall_confidence, 0.0), 1.0)

    def _get_available_agents(self) -> List[str]:
        """Get list of available agents (mock implementation)."""
        return [
            "analysis-gateway",
            "meta-coordinator",
            "test-specialist",
            "infrastructure-engineer",
            "security-auditor",
            "performance-optimizer",
            "docker-specialist",
            "coverage-optimizer",
            "security-enforcer",
        ]

    def get_reasoning_metrics(self) -> Dict[str, Dict[str, float]]:
        """Get performance metrics for reasoning system."""
        metrics = {}
        for metric_name, values in self.reasoning_metrics.items():
            if values:
                metrics[metric_name] = {
                    "avg": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "count": len(values),
                }
        return metrics


# Example usage and testing functions
def example_usage():
    """Demonstrate enhanced multi-domain context reasoning."""
    reasoner = EnhancedMultiDomainContextReasoner()

    # Example queries for testing
    test_queries = [
        "Analyze Docker container performance issues affecting test execution",
        "Security vulnerability in authentication system requires immediate testing and infrastructure updates",
        "Comprehensive analysis using 3 tasks in parallel: security assessment, performance optimization, testing validation",
        "Infrastructure deployment pipeline needs security hardening and performance monitoring",
    ]

    print("Enhanced Multi-Domain Context Reasoning Examples:")
    print("=" * 60)

    for i, query in enumerate(test_queries, 1):
        print(f"\nExample {i}: {query}")
        print("-" * 50)

        analysis = reasoner.analyze_multi_domain_query(query)

        print(f"Primary Domain: {analysis['primary_domain']}")
        print(f"Secondary Domains: {analysis['secondary_domains']}")
        print(f"Pattern Complexity: {analysis['pattern_complexity'].value}")
        print(f"Coordination Approach: {analysis['coordination_strategy']['approach']}")
        print(
            f"Selected Agents: {analysis['coordination_strategy']['selected_agents']}"
        )
        print(f"Reasoning Confidence: {analysis['reasoning_confidence']:.2f}")
        print(f"Analysis Time: {analysis['analysis_time_ms']:.1f}ms")


if __name__ == "__main__":
    example_usage()
