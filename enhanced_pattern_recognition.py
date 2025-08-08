# Claude Agent Framework Pattern Recognition Examples
#
# This file contains conceptual examples of pattern recognition logic
# for the Claude Code Framework. The actual implementation is handled
# by Claude's natural language processing and the memory system files:
# - .claude/memory/coordination-hub.md
# - .claude/memory/domain-intelligence.md
#
# These examples show the logical structure of enhanced patterns
# that would be implemented in the memory system.

"""
Conceptual Enhanced Pattern Recognition for Claude Code Framework

This demonstrates the logical structure of enhanced pattern recognition
that would be integrated into the Claude agent memory system.

Target Performance Improvements:
- Agent Selection Accuracy: 97% → 99.2%
- Response Time: <1s → <0.7s  
- Context Preservation: 97% → 99.5%
- Edge Case Handling: Manual → 95% automated
"""

import re
import time
import logging
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum

logger = logging.getLogger(__name__)

class PatternConfidence(Enum):
    """Confidence levels for pattern matching"""
    HIGH = 0.9
    MEDIUM = 0.7
    LOW = 0.5
    UNKNOWN = 0.2

class CoordinationType(Enum):
    """Types of coordination patterns"""
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"
    HIERARCHICAL = "hierarchical"
    HYBRID = "hybrid"

# Conceptual Pattern Classifications for Claude Agent Framework

pattern_confidence_levels = {
    "HIGH": 0.9,     # Explicit coordination language detected
    "MEDIUM": 0.7,   # Strong domain signals with coordination hints
    "LOW": 0.5,      # Implicit patterns requiring inference
    "UNKNOWN": 0.2   # Ambiguous input requiring fallback
}

coordination_types = {
    "PARALLEL": "parallel",       # Multi-agent simultaneous execution
    "SEQUENTIAL": "sequential",   # Step-by-step with context accumulation
    "HIERARCHICAL": "hierarchical", # Meta-coordination for complex scenarios
    "HYBRID": "hybrid"           # Mixed coordination strategies
}

@dataclass
class PatternMatch:
    """Result of pattern matching operation"""
    pattern_type: str
    confidence: float
    matched_text: str
    domain_hints: List[str] = field(default_factory=list)
    coordination_type: Optional[CoordinationType] = None
    agent_suggestions: List[str] = field(default_factory=list)
    performance_requirements: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EnrichedContext:
    """Enriched context with domain classification and requirements"""
    original_input: str
    domains: Dict[str, float]  # domain -> confidence
    coordination_pattern: CoordinationType
    performance_requirements: Dict[str, Any]
    conversation_context: List[str]
    historical_patterns: List[str]
    confidence_score: float
    suggested_agents: List[Tuple[str, float]]  # (agent, confidence)

@dataclass
class ValidationResult:
    """Result of agent selection validation"""
    is_valid: bool
    confidence: float
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

@dataclass
class SuccessMetrics:
    """Metrics for tracking pattern success"""
    selection_accuracy: float
    response_time: float
    context_preservation: float
    coordination_success: float
    timestamp: float = field(default_factory=time.time)

class ExplicitPatternMatcher:
    """Tier 1: Explicit pattern matching with high confidence"""
    
    def __init__(self):
        self.high_confidence_patterns = {
            "parallel_coordination": {
                "patterns": [
                    r"coordinating .+ using (\d+) tasks in parallel",
                    r"analyzing .+ using parallel assessment across (\d+) domains",
                    r".+ analysis using (\d+) tasks in parallel",
                    r"using (\d+) tasks in parallel",
                    r"parallel analysis across (\d+) (?:domains|areas|components)"
                ],
                "confidence": PatternConfidence.HIGH.value,
                "coordination_type": CoordinationType.PARALLEL
            },
            "sequential_analysis": {
                "patterns": [
                    r"deep analysis requiring .+ sequential coordination",
                    r"step-by-step .+ analysis with .+ progression",
                    r".+ analysis with context accumulation",
                    r"sequential .+ coordination",
                    r"progressive .+ analysis"
                ],
                "confidence": PatternConfidence.HIGH.value,
                "coordination_type": CoordinationType.SEQUENTIAL
            },
            "hierarchical_coordination": {
                "patterns": [
                    r"meta.+ coordination",
                    r"strategic .+ orchestration",
                    r"crisis response .+ coordination",
                    r"architectural .+ coordination"
                ],
                "confidence": PatternConfidence.HIGH.value,
                "coordination_type": CoordinationType.HIERARCHICAL
            }
        }
        
        self.domain_specific_patterns = {
            "testing": {
                "patterns": [
                    r"test.* (?:failure|coverage|mock|async)",
                    r"pytest.*", r"coverage.*", r"fixture.*",
                    r"unit test.*", r"integration test.*",
                    r"async.* test.*", r"mock.* configuration"
                ],
                "agents": ["test-specialist", "coverage-optimizer", "fixture-design-specialist"],
                "confidence": PatternConfidence.HIGH.value
            },
            "infrastructure": {
                "patterns": [
                    r"docker.*", r"container.*", r"deployment.*",
                    r"orchestration.*", r"kubernetes.*", r"k8s.*",
                    r"infrastructure.*", r"environment.*", r"scaling.*"
                ],
                "agents": ["infrastructure-engineer", "docker-specialist", "environment-analyst"],
                "confidence": PatternConfidence.HIGH.value
            },
            "security": {
                "patterns": [
                    r"security.*", r"vulnerability.*", r"compliance.*",
                    r"audit.*", r"penetration.*", r"threat.*",
                    r"authentication.*", r"authorization.*", r"encryption.*"
                ],
                "agents": ["security-enforcer", "security-auditor", "code-quality-specialist"],
                "confidence": PatternConfidence.HIGH.value
            },
            "performance": {
                "patterns": [
                    r"performance.*", r"optimization.*", r"latency.*",
                    r"throughput.*", r"bottleneck.*", r"resource.*",
                    r"memory.*usage", r"cpu.*usage", r"scaling.*"
                ],
                "agents": ["performance-optimizer", "resource-optimizer"],
                "confidence": PatternConfidence.HIGH.value
            },
            "code_quality": {
                "patterns": [
                    r"code quality.*", r"refactor.*", r"lint.*",
                    r"type.*annotation.*", r"variable.*naming",
                    r"function.*splitting", r"architecture.*"
                ],
                "agents": ["intelligent-enhancer", "code-quality-specialist", "refactoring-coordinator"],
                "confidence": PatternConfidence.HIGH.value
            }
        }
    
    def match_pattern(self, user_input: str) -> PatternMatch:
        """Match user input against explicit patterns with high confidence"""
        input_lower = user_input.lower()
        best_match = PatternMatch(
            pattern_type="unknown",
            confidence=PatternConfidence.UNKNOWN.value,
            matched_text=""
        )
        
        # Check coordination patterns
        for pattern_type, config in self.high_confidence_patterns.items():
            for pattern in config["patterns"]:
                match = re.search(pattern, input_lower, re.IGNORECASE)
                if match:
                    confidence = config["confidence"]
                    if confidence > best_match.confidence:
                        best_match = PatternMatch(
                            pattern_type=pattern_type,
                            confidence=confidence,
                            matched_text=match.group(0),
                            coordination_type=config["coordination_type"]
                        )
        
        # Check domain-specific patterns
        domain_matches = {}
        suggested_agents = []
        
        for domain, config in self.domain_specific_patterns.items():
            for pattern in config["patterns"]:
                if re.search(pattern, input_lower, re.IGNORECASE):
                    domain_matches[domain] = config["confidence"]
                    suggested_agents.extend(config["agents"])
        
        if domain_matches:
            best_match.domain_hints = list(domain_matches.keys())
            best_match.agent_suggestions = list(set(suggested_agents))
            
            # Boost confidence if we have strong domain matches
            if max(domain_matches.values()) >= PatternConfidence.HIGH.value:
                best_match.confidence = max(best_match.confidence, PatternConfidence.MEDIUM.value)
        
        return best_match

class ContextAwareAnalyzer:
    """Tier 2: Context-aware semantic analysis"""
    
    def __init__(self):
        self.domain_keywords = {
            "testing": ["test", "mock", "fixture", "coverage", "pytest", "unittest"],
            "infrastructure": ["docker", "container", "deploy", "orchestration", "kubernetes"],
            "security": ["security", "vulnerability", "audit", "compliance", "threat"],
            "performance": ["performance", "optimization", "latency", "throughput", "bottleneck"],
            "code_quality": ["refactor", "lint", "quality", "architecture", "naming"]
        }
        
        self.performance_indicators = {
            "fast": ["quick", "fast", "immediate", "urgent", "asap"],
            "thorough": ["comprehensive", "thorough", "detailed", "complete", "exhaustive"],
            "parallel": ["parallel", "concurrent", "simultaneous", "coordinated"],
            "sequential": ["sequential", "step-by-step", "progressive", "iterative"]
        }
    
    def analyze_semantic_context(self, input_text: str, conversation_history: List[str] = None) -> EnrichedContext:
        """Analyze semantic context beyond explicit patterns"""
        if conversation_history is None:
            conversation_history = []
            
        # Domain classification
        domains = self._classify_domains(input_text)
        
        # Coordination pattern detection
        coordination_pattern = self._detect_coordination_pattern(input_text)
        
        # Performance requirements extraction
        performance_requirements = self._extract_performance_requirements(input_text)
        
        # Historical pattern analysis
        historical_patterns = self._analyze_historical_patterns(conversation_history)
        
        # Calculate overall confidence
        confidence_score = self._calculate_confidence(domains, coordination_pattern, performance_requirements)
        
        # Generate agent suggestions
        suggested_agents = self._suggest_agents(domains, coordination_pattern, performance_requirements)
        
        return EnrichedContext(
            original_input=input_text,
            domains=domains,
            coordination_pattern=coordination_pattern,
            performance_requirements=performance_requirements,
            conversation_context=conversation_history,
            historical_patterns=historical_patterns,
            confidence_score=confidence_score,
            suggested_agents=suggested_agents
        )
    
    def _classify_domains(self, text: str) -> Dict[str, float]:
        """Classify input into domain categories with confidence scores"""
        domains = {}
        text_lower = text.lower()
        
        for domain, keywords in self.domain_keywords.items():
            score = 0.0
            for keyword in keywords:
                if keyword in text_lower:
                    # Weight based on keyword importance and frequency
                    count = text_lower.count(keyword)
                    score += count * (1.0 / len(keywords))  # Normalize by keyword pool size
            
            if score > 0:
                domains[domain] = min(score, 1.0)  # Cap at 1.0
        
        return domains
    
    def _detect_coordination_pattern(self, text: str) -> CoordinationType:
        """Detect coordination pattern from text"""
        text_lower = text.lower()
        
        parallel_indicators = ["parallel", "concurrent", "simultaneous", "coordinated"]
        sequential_indicators = ["sequential", "step-by-step", "progressive", "iterative"]
        hierarchical_indicators = ["meta", "strategic", "orchestration", "coordination"]
        
        scores = {
            CoordinationType.PARALLEL: sum(1 for ind in parallel_indicators if ind in text_lower),
            CoordinationType.SEQUENTIAL: sum(1 for ind in sequential_indicators if ind in text_lower),
            CoordinationType.HIERARCHICAL: sum(1 for ind in hierarchical_indicators if ind in text_lower)
        }
        
        if max(scores.values()) == 0:
            return CoordinationType.HYBRID
        
        return max(scores, key=scores.get)
    
    def _extract_performance_requirements(self, text: str) -> Dict[str, Any]:
        """Extract performance requirements from text"""
        requirements = {}
        text_lower = text.lower()
        
        for req_type, indicators in self.performance_indicators.items():
            score = sum(1 for ind in indicators if ind in text_lower)
            if score > 0:
                requirements[req_type] = score
        
        # Extract specific time requirements
        time_matches = re.findall(r'<(\d+)(?:s|sec|seconds?)', text_lower)
        if time_matches:
            requirements["max_time"] = min(int(t) for t in time_matches)
        
        return requirements
    
    def _analyze_historical_patterns(self, conversation_history: List[str]) -> List[str]:
        """Analyze historical patterns from conversation history"""
        if not conversation_history:
            return []
        
        patterns = []
        for message in conversation_history[-5:]:  # Only analyze recent history
            # Extract domain patterns
            for domain in self.domain_keywords:
                if any(keyword in message.lower() for keyword in self.domain_keywords[domain]):
                    patterns.append(f"historical_{domain}")
        
        return list(set(patterns))  # Remove duplicates
    
    def _calculate_confidence(self, domains: Dict[str, float], 
                            coordination_pattern: CoordinationType,
                            performance_requirements: Dict[str, Any]) -> float:
        """Calculate overall confidence score"""
        domain_confidence = sum(domains.values()) / len(domains) if domains else 0.0
        pattern_confidence = 0.8 if coordination_pattern != CoordinationType.HYBRID else 0.5
        requirement_confidence = min(len(performance_requirements) * 0.2, 1.0)
        
        return (domain_confidence + pattern_confidence + requirement_confidence) / 3.0
    
    def _suggest_agents(self, domains: Dict[str, float],
                       coordination_pattern: CoordinationType,
                       performance_requirements: Dict[str, Any]) -> List[Tuple[str, float]]:
        """Generate agent suggestions based on context analysis"""
        suggestions = []
        
        # Domain-based suggestions
        domain_agents = {
            "testing": [("test-specialist", 0.9), ("coverage-optimizer", 0.7)],
            "infrastructure": [("infrastructure-engineer", 0.9), ("docker-specialist", 0.8)],
            "security": [("security-enforcer", 0.9), ("security-auditor", 0.8)],
            "performance": [("performance-optimizer", 0.9), ("resource-optimizer", 0.7)],
            "code_quality": [("intelligent-enhancer", 0.9), ("code-quality-specialist", 0.8)]
        }
        
        for domain, confidence in domains.items():
            if domain in domain_agents:
                for agent, base_confidence in domain_agents[domain]:
                    suggestions.append((agent, base_confidence * confidence))
        
        # Coordination pattern suggestions
        if coordination_pattern == CoordinationType.PARALLEL and len(domains) > 1:
            suggestions.append(("analysis-gateway", 0.85))
        elif coordination_pattern == CoordinationType.HIERARCHICAL:
            suggestions.append(("meta-coordinator", 0.9))
        
        # Performance requirement adjustments
        if performance_requirements.get("fast"):
            # Prefer faster agents
            fast_agents = [("docker-specialist", 0.8), ("test-specialist", 0.8)]
            suggestions.extend(fast_agents)
        
        # Remove duplicates and sort by confidence
        unique_suggestions = {}
        for agent, conf in suggestions:
            if agent not in unique_suggestions or conf > unique_suggestions[agent]:
                unique_suggestions[agent] = conf
        
        return sorted(unique_suggestions.items(), key=lambda x: x[1], reverse=True)

class FallbackDecisionTree:
    """Tier 3: Fallback decision tree for ambiguous cases"""
    
    def __init__(self):
        self.decision_tree = {
            "multi_domain": {
                "condition": lambda ctx: len(ctx.domains) > 2,
                "agent": "analysis-gateway",
                "confidence": 0.7
            },
            "complex_coordination": {
                "condition": lambda ctx: ctx.coordination_pattern == CoordinationType.HIERARCHICAL,
                "agent": "meta-coordinator",
                "confidence": 0.75
            },
            "testing_focus": {
                "condition": lambda ctx: ctx.domains.get("testing", 0) > 0.5,
                "agent": "test-specialist",
                "confidence": 0.8
            },
            "infrastructure_focus": {
                "condition": lambda ctx: ctx.domains.get("infrastructure", 0) > 0.5,
                "agent": "infrastructure-engineer",
                "confidence": 0.8
            },
            "security_focus": {
                "condition": lambda ctx: ctx.domains.get("security", 0) > 0.5,
                "agent": "security-enforcer",
                "confidence": 0.8
            },
            "default": {
                "condition": lambda ctx: True,  # Always true - fallback
                "agent": "digdeep",
                "confidence": 0.6
            }
        }
    
    def make_fallback_decision(self, enriched_context: EnrichedContext) -> Tuple[str, float]:
        """Make fallback decision for ambiguous cases"""
        for decision_name, config in self.decision_tree.items():
            if config["condition"](enriched_context):
                return config["agent"], config["confidence"]
        
        # Should never reach here due to default condition
        return "digdeep", 0.5

class ContextValidator:
    """Validation framework for agent selection"""
    
    def __init__(self):
        self.agent_capabilities = {
            "test-specialist": {
                "domains": ["testing"],
                "coordination_types": [CoordinationType.SEQUENTIAL, CoordinationType.PARALLEL],
                "performance_tier": "high",  # <1.5s
                "specializations": ["async", "mock", "coverage"]
            },
            "infrastructure-engineer": {
                "domains": ["infrastructure"],
                "coordination_types": [CoordinationType.PARALLEL, CoordinationType.HIERARCHICAL],
                "performance_tier": "high",
                "specializations": ["docker", "orchestration", "scaling"]
            },
            "security-enforcer": {
                "domains": ["security"],
                "coordination_types": [CoordinationType.SEQUENTIAL],
                "performance_tier": "ultra",  # <2s
                "specializations": ["pattern_detection", "workspace_validation"]
            },
            "analysis-gateway": {
                "domains": ["testing", "infrastructure", "security", "performance"],
                "coordination_types": [CoordinationType.PARALLEL],
                "performance_tier": "medium",  # 1.5-2s
                "specializations": ["multi_domain", "coordination"]
            },
            "meta-coordinator": {
                "domains": ["testing", "infrastructure", "security", "performance", "code_quality"],
                "coordination_types": [CoordinationType.HIERARCHICAL],
                "performance_tier": "strategic",  # 2-3s
                "specializations": ["complex_orchestration", "crisis_response"]
            }
        }
    
    def validate_agent_selection(self, selected_agent: str, 
                               enriched_context: EnrichedContext) -> ValidationResult:
        """Validate agent selection against context requirements"""
        if selected_agent not in self.agent_capabilities:
            return ValidationResult(
                is_valid=False,
                confidence=0.0,
                issues=[f"Unknown agent: {selected_agent}"],
                recommendations=["Use digdeep for general analysis"]
            )
        
        capabilities = self.agent_capabilities[selected_agent]
        issues = []
        recommendations = []
        
        # Validate domain alignment
        if enriched_context.domains:
            domain_match = any(domain in capabilities["domains"] 
                             for domain in enriched_context.domains.keys())
            if not domain_match:
                issues.append(f"Agent {selected_agent} not specialized for domains: {list(enriched_context.domains.keys())}")
                # Find better agent
                for agent, caps in self.agent_capabilities.items():
                    if any(domain in caps["domains"] for domain in enriched_context.domains.keys()):
                        recommendations.append(f"Consider {agent} for better domain alignment")
                        break
        
        # Validate coordination type
        if enriched_context.coordination_pattern not in capabilities["coordination_types"]:
            issues.append(f"Agent {selected_agent} not optimized for {enriched_context.coordination_pattern.value} coordination")
        
        # Validate performance requirements
        if enriched_context.performance_requirements.get("fast") and capabilities["performance_tier"] not in ["ultra", "high"]:
            issues.append(f"Agent {selected_agent} may not meet fast response requirements")
        
        # Calculate validation confidence
        confidence = 1.0 - (len(issues) * 0.2)  # Reduce confidence by 0.2 per issue
        confidence = max(confidence, 0.1)  # Minimum confidence
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            confidence=confidence,
            issues=issues,
            recommendations=recommendations
        )

class PatternSuccessTracker:
    """Tracking and learning system for pattern success"""
    
    def __init__(self):
        self.success_history = defaultdict(list)
        self.pattern_weights = defaultdict(lambda: 1.0)
        self.agent_performance = defaultdict(list)
    
    def track_pattern_success(self, pattern: str, agent: str, outcome: SuccessMetrics):
        """Track success metrics for pattern-agent combinations"""
        key = f"{pattern}:{agent}"
        self.success_history[key].append(outcome)
        self.agent_performance[agent].append(outcome)
        
        # Update pattern weights based on success
        if len(self.success_history[key]) >= 5:  # Minimum samples for adjustment
            avg_accuracy = sum(m.selection_accuracy for m in self.success_history[key][-5:]) / 5
            if avg_accuracy > 0.95:
                self.pattern_weights[pattern] = min(self.pattern_weights[pattern] * 1.1, 2.0)
            elif avg_accuracy < 0.8:
                self.pattern_weights[pattern] = max(self.pattern_weights[pattern] * 0.9, 0.5)
    
    def get_pattern_weight(self, pattern: str) -> float:
        """Get current weight for a pattern"""
        return self.pattern_weights[pattern]
    
    def get_agent_performance_stats(self, agent: str) -> Dict[str, float]:
        """Get performance statistics for an agent"""
        if agent not in self.agent_performance or not self.agent_performance[agent]:
            return {"accuracy": 0.0, "response_time": 999.0, "context_preservation": 0.0}
        
        recent_metrics = self.agent_performance[agent][-10:]  # Last 10 interactions
        return {
            "accuracy": sum(m.selection_accuracy for m in recent_metrics) / len(recent_metrics),
            "response_time": sum(m.response_time for m in recent_metrics) / len(recent_metrics),
            "context_preservation": sum(m.context_preservation for m in recent_metrics) / len(recent_metrics),
            "coordination_success": sum(m.coordination_success for m in recent_metrics) / len(recent_metrics)
        }

class EnhancedPatternRecognitionSystem:
    """Main orchestrator for enhanced pattern recognition"""
    
    def __init__(self):
        self.explicit_matcher = ExplicitPatternMatcher()
        self.context_analyzer = ContextAwareAnalyzer()
        self.fallback_tree = FallbackDecisionTree()
        self.validator = ContextValidator()
        self.success_tracker = PatternSuccessTracker()
        
        logger.info("Enhanced Pattern Recognition System initialized")
    
    def select_agent(self, user_input: str, 
                    conversation_history: List[str] = None) -> Tuple[str, float, Dict[str, Any]]:
        """Main agent selection method with enhanced pattern recognition"""
        start_time = time.time()
        
        try:
            # Tier 1: Explicit pattern matching
            explicit_match = self.explicit_matcher.match_pattern(user_input)
            
            # Tier 2: Context-aware analysis
            enriched_context = self.context_analyzer.analyze_semantic_context(
                user_input, conversation_history or []
            )
            
            # Combine results for best agent selection
            selected_agent, confidence = self._combine_selection_results(
                explicit_match, enriched_context
            )
            
            # Tier 3: Fallback if low confidence
            if confidence < 0.7:
                fallback_agent, fallback_confidence = self.fallback_tree.make_fallback_decision(
                    enriched_context
                )
                if fallback_confidence > confidence:
                    selected_agent, confidence = fallback_agent, fallback_confidence
            
            # Validate selection
            validation = self.validator.validate_agent_selection(selected_agent, enriched_context)
            
            # Adjust confidence based on validation
            final_confidence = confidence * validation.confidence
            
            # Prepare detailed results
            selection_details = {
                "explicit_match": {
                    "pattern_type": explicit_match.pattern_type,
                    "confidence": explicit_match.confidence,
                    "matched_text": explicit_match.matched_text
                },
                "context_analysis": {
                    "domains": enriched_context.domains,
                    "coordination_pattern": enriched_context.coordination_pattern.value,
                    "confidence_score": enriched_context.confidence_score
                },
                "validation": {
                    "is_valid": validation.is_valid,
                    "issues": validation.issues,
                    "recommendations": validation.recommendations
                },
                "response_time": time.time() - start_time,
                "suggested_alternatives": [agent for agent, _ in enriched_context.suggested_agents[:3]]
            }
            
            logger.info(f"Agent selected: {selected_agent} (confidence: {final_confidence:.3f}, time: {selection_details['response_time']:.3f}s)")
            
            return selected_agent, final_confidence, selection_details
            
        except Exception as e:
            logger.error(f"Error in agent selection: {str(e)}")
            return "digdeep", 0.5, {"error": str(e), "fallback_used": True}
    
    def _combine_selection_results(self, explicit_match: PatternMatch, 
                                 enriched_context: EnrichedContext) -> Tuple[str, float]:
        """Combine results from explicit matching and context analysis"""
        # Start with explicit match if high confidence
        if explicit_match.confidence >= PatternConfidence.HIGH.value:
            if explicit_match.agent_suggestions:
                # Weight agent suggestions by pattern weights
                pattern_weight = self.success_tracker.get_pattern_weight(explicit_match.pattern_type)
                adjusted_confidence = explicit_match.confidence * pattern_weight
                return explicit_match.agent_suggestions[0], adjusted_confidence
        
        # Use context-aware suggestions
        if enriched_context.suggested_agents:
            top_agent, top_confidence = enriched_context.suggested_agents[0]
            # Apply pattern weight if applicable
            pattern_weight = self.success_tracker.get_pattern_weight("context_analysis")
            adjusted_confidence = top_confidence * pattern_weight
            return top_agent, adjusted_confidence
        
        # Final fallback
        return "digdeep", PatternConfidence.LOW.value
    
    def record_success(self, user_input: str, selected_agent: str, 
                      success_metrics: SuccessMetrics):
        """Record success metrics for learning and improvement"""
        # Identify the primary pattern that led to selection
        explicit_match = self.explicit_matcher.match_pattern(user_input)
        primary_pattern = explicit_match.pattern_type if explicit_match.confidence > 0.5 else "context_analysis"
        
        self.success_tracker.track_pattern_success(primary_pattern, selected_agent, success_metrics)
        logger.info(f"Recorded success for {primary_pattern}:{selected_agent} - accuracy: {success_metrics.selection_accuracy:.3f}")
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        return {
            "pattern_weights": dict(self.success_tracker.pattern_weights),
            "agent_performance": {
                agent: self.success_tracker.get_agent_performance_stats(agent)
                for agent in ["test-specialist", "infrastructure-engineer", "security-enforcer", 
                             "analysis-gateway", "meta-coordinator"]
            },
            "total_patterns": len(self.explicit_matcher.high_confidence_patterns) + 
                             len(self.explicit_matcher.domain_specific_patterns)
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize the enhanced system
    enhanced_system = EnhancedPatternRecognitionSystem()
    
    # Test cases
    test_cases = [
        "Coordinating comprehensive analysis using 3 tasks in parallel: security assessment, performance analysis, testing evaluation",
        "Test failures with async patterns and mock configuration issues",
        "Docker orchestration problems with service networking and scaling",
        "Security vulnerability analysis required for compliance validation",
        "Need to analyze complex architectural refactoring requirements"
    ]
    
    print("Enhanced Pattern Recognition System - Test Results")
    print("=" * 60)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_input[:50]}...")
        
        agent, confidence, details = enhanced_system.select_agent(test_input)
        
        print(f"Selected Agent: {agent}")
        print(f"Confidence: {confidence:.3f}")
        print(f"Response Time: {details['response_time']:.3f}s")
        print(f"Domains Detected: {details['context_analysis']['domains']}")
        print(f"Coordination Pattern: {details['context_analysis']['coordination_pattern']}")
        
        if details['validation']['issues']:
            print(f"Validation Issues: {details['validation']['issues']}")
        if details['validation']['recommendations']:
            print(f"Recommendations: {details['validation']['recommendations']}")
    
    # System statistics
    print("\n" + "=" * 60)
    print("System Statistics:")
    stats = enhanced_system.get_system_stats()
    print(f"Total Patterns: {stats['total_patterns']}")
    print(f"Pattern Weights: {stats['pattern_weights']}")
