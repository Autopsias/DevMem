#!/usr/bin/env python3
"""Test script for enhanced cross-domain boundary detection improvements.

This script validates the improvements to:
1. Better detection of multi-domain queries
2. Smarter coordination between specialized agents
3. Improved confidence scoring for domain boundaries
4. Enhanced handling of overlapping domains
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agent_selector import EnhancedAgentSelector
from enhanced_cross_domain_coordinator import (
    get_cross_domain_coordinator,
    analyze_cross_domain_query,
)


def test_multi_domain_detection():
    """Test improved multi-domain query detection."""
    print("\n=== Testing Multi-Domain Query Detection ===")

    selector = EnhancedAgentSelector()

    test_queries = [
        # Simple single domain
        "Fix test failures in pytest",
        # Clear multi-domain
        "Coordinate infrastructure security and performance testing across multiple domains",
        # Implicit multi-domain with coordination signals
        "Comprehensive analysis of container deployment with security hardening",
        # Complex cross-domain with conflicts
        "Infrastructure testing coordination requiring security performance optimization",
        # Documentation cross-domain
        "Create technical documentation for testing infrastructure and security patterns",
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        domains = selector.detect_multi_domain_query(query)
        print(f"Detected domains: {domains}")

        # Test cross-domain analysis
        analysis = analyze_cross_domain_query(query)
        print(f"Cross-domain boundaries: {len(analysis.detected_boundaries)}")
        if analysis.detected_boundaries:
            boundary = analysis.detected_boundaries[0]
            print(f"  Primary: {boundary.primary_domain.value}")
            print(f"  Secondary: {[d.value for d in boundary.secondary_domains]}")
            print(f"  Confidence: {boundary.confidence:.3f}")
            print(f"  Complexity: {boundary.complexity_score:.3f}")

        print(f"Potential conflicts: {len(analysis.potential_conflicts)}")
        for conflict in analysis.potential_conflicts:
            print(f"  {conflict.conflict_type.value}: {conflict.severity:.3f}")

    return True


def test_agent_coordination():
    """Test smarter coordination between specialized agents."""
    print("\n=== Testing Agent Coordination ===")

    selector = EnhancedAgentSelector()

    coordination_queries = [
        "Infrastructure testing requiring security validation and performance optimization",
        "Documentation creation for testing infrastructure with security guidelines",
        "Performance testing coordination with infrastructure scaling and security audit",
        "Cross-domain analysis requiring systematic coordination across 4 domains",
    ]

    for query in coordination_queries:
        print(f"\nQuery: {query}")
        result = selector.select_agent(query)
        print(f"Selected agent: {result.agent_name}")
        print(f"Confidence: {result.confidence_score:.3f}")
        print(f"Reasoning: {result.reasoning}")

        # Get multiple suggestions to see coordination
        suggestions = selector.get_agent_suggestions(query, top_n=5)
        print("Top suggestions:")
        for suggestion in suggestions:
            print(f"  {suggestion.agent_name}: {suggestion.confidence_score:.3f}")

    return True


def test_confidence_scoring():
    """Test improved confidence scoring for domain boundaries."""
    print("\n=== Testing Confidence Scoring ===")

    coordinator = get_cross_domain_coordinator()

    # Test queries with varying clarity and complexity
    confidence_test_queries = [
        # High confidence - very clear single domain
        "Run pytest tests with coverage analysis",
        # Medium confidence - clear multi-domain
        "Docker container deployment with security scanning",
        # Lower confidence - vague multi-domain
        "Improve system performance and reliability",
        # High confidence - explicit coordination request
        "Coordinate comprehensive infrastructure security testing with performance validation",
        # Medium confidence - implicit coordination
        "End-to-end testing and deployment pipeline optimization",
    ]

    for query in confidence_test_queries:
        print(f"\nQuery: {query}")
        analysis = coordinator.analyze_cross_domain_integration(query)

        if analysis.detected_boundaries:
            boundary = analysis.detected_boundaries[0]
            print(f"Confidence: {boundary.confidence:.3f}")
            print(
                f"Domains: {boundary.primary_domain.value} + {[d.value for d in boundary.secondary_domains]}"
            )
            print(f"Overlap indicators: {len(boundary.overlap_indicators)}")
        else:
            print("No boundaries detected")

        print("Agent suggestions:")
        for agent, conf in analysis.agent_suggestions[:3]:
            print(f"  {agent}: {conf:.3f}")

    return True


def test_overlapping_domains():
    """Test enhanced handling of overlapping domains."""
    print("\n=== Testing Overlapping Domain Handling ===")

    coordinator = get_cross_domain_coordinator()

    overlap_queries = [
        # Security vs Performance conflict
        "Optimize application performance while maintaining security compliance",
        # Testing vs Deployment speed conflict
        "Fast deployment pipeline with comprehensive testing coverage",
        # Infrastructure vs Security integration
        "Container orchestration with security hardening and compliance validation",
        # Documentation vs Testing coordination
        "Create testing documentation with automated validation and infrastructure guides",
    ]

    for query in overlap_queries:
        print(f"\nQuery: {query}")
        analysis = coordinator.analyze_cross_domain_integration(query)

        print(f"Integration complexity: {analysis.integration_complexity:.3f}")
        print(f"Coordination recommendation: {analysis.recommended_coordination}")

        if analysis.potential_conflicts:
            print("Detected conflicts:")
            for conflict in analysis.potential_conflicts:
                print(f"  {conflict.conflict_type.value}: {conflict.severity:.3f}")
                print(f"    Domains: {[d.value for d in conflict.involved_domains]}")
                print(
                    f"    Resolution strategies: {len(conflict.resolution_strategies)}"
                )
                if conflict.resolution_strategies:
                    print(f"      - {conflict.resolution_strategies[0]}")

        print("Agent suggestions for conflict resolution:")
        for agent, conf in analysis.agent_suggestions[:4]:
            print(f"  {agent}: {conf:.3f}")

    return True


def test_learning_system():
    """Test pattern learning and coordination improvement."""
    print("\n=== Testing Learning System ===")

    coordinator = get_cross_domain_coordinator()
    selector = EnhancedAgentSelector()

    # Simulate some successful patterns
    learning_queries = [
        "Docker container orchestration with kubernetes deployment",
        "Infrastructure security hardening with compliance validation",
        "Performance optimization with resource scaling analysis",
        "Testing coordination with infrastructure validation",
    ]

    for query in learning_queries:
        analysis = coordinator.analyze_cross_domain_integration(query)
        if analysis.agent_suggestions:
            best_agent = analysis.agent_suggestions[0][0]
            confidence = analysis.agent_suggestions[0][1]

            # Record successful feedback
            coordinator.record_selection_feedback(
                query, best_agent, confidence, user_feedback=True, task_success=True
            )
            print(f"Recorded success: {query} -> {best_agent} ({confidence:.3f})")

    # Get learning insights
    learning_insights = coordinator.get_learning_insights()
    print("\nLearning insights:")
    print(
        f"  Total successful patterns: {learning_insights.get('total_successful_patterns', 0)}"
    )
    print(f"  Learning rate: {learning_insights.get('learning_rate', 0.0):.1%}")
    print(
        f"  Cross-domain learning effectiveness: {learning_insights.get('cross_domain_learning_effectiveness', 0.0):.3f}"
    )

    # Get selector learning insights
    selector_insights = selector.get_learning_insights()
    print(
        f"  Recent cross-domain usage rate: {selector_insights.get('recent_cross_domain_usage_rate', 0.0):.3f}"
    )

    return True


def main():
    """Run all improvement validation tests."""
    print("Cross-Domain Boundary Detection Improvements Validation")
    print("=" * 60)

    tests = [
        test_multi_domain_detection,
        test_agent_coordination,
        test_confidence_scoring,
        test_overlapping_domains,
        test_learning_system,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print(f"✓ {test.__name__} passed")
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            results.append(False)

    print("\n=== Summary ===")
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("🎉 All cross-domain boundary detection improvements working correctly!")
        return 0
    else:
        print("⚠️  Some improvements need attention")
        return 1


if __name__ == "__main__":
    exit(main())
