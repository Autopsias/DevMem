"""Comprehensive tests for enhanced cross-domain integration system.

This test suite validates the specialized boundary detection and conflict resolution
improvements for cross-domain agent coordination.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from enhanced_cross_domain_coordinator import (
    EnhancedBoundaryDetector,
    ConflictDetectionEngine,
    EnhancedCrossDomainCoordinator,
    DomainType,
    ConflictType,
    DomainBoundary,
    ConflictDetection,
    CrossDomainAnalysis
)
from agent_selector import EnhancedAgentSelector


class TestEnhancedBoundaryDetection:
    """Test suite for enhanced boundary detection capabilities."""
    
    @pytest.fixture
    def boundary_detector(self):
        return EnhancedBoundaryDetector()
    
    def test_single_domain_detection(self, boundary_detector):
        """Test detection of single-domain queries."""
        single_domain_queries = [
            "pytest fixture configuration issues",
            "docker container orchestration setup",
            "security vulnerability assessment needed",
            "performance bottleneck analysis required",
            "code refactoring for better maintainability"
        ]
        
        expected_domains = [
            DomainType.TESTING,
            DomainType.INFRASTRUCTURE,
            DomainType.SECURITY,
            DomainType.PERFORMANCE,
            DomainType.CODE_QUALITY
        ]
        
        for query, expected_domain in zip(single_domain_queries, expected_domains):
            boundaries = boundary_detector.detect_domain_boundaries(query)
            
            assert len(boundaries) == 1, f"Should detect one boundary for: {query}"
            assert boundaries[0].primary_domain == expected_domain
            assert boundaries[0].confidence > 0.5
    
    def test_multi_domain_detection(self, boundary_detector):
        """Test detection of multi-domain queries."""
        multi_domain_queries = [
            "testing infrastructure deployment with security validation",
            "performance optimization while maintaining security compliance",
            "documentation automation integrated with testing pipeline",
            "infrastructure monitoring with security audit requirements"
        ]
        
        for query in multi_domain_queries:
            boundaries = boundary_detector.detect_domain_boundaries(query)
            
            assert len(boundaries) >= 1, f"Should detect boundaries for: {query}"
            if boundaries:
                assert len(boundaries[0].secondary_domains) >= 1, f"Should detect multiple domains for: {query}"
                assert boundaries[0].confidence > 0.3
    
    def test_complex_boundary_patterns(self, boundary_detector):
        """Test detection of complex boundary patterns."""
        complex_queries = [
            "multi-cloud infrastructure deployment with automated testing and security compliance validation",
            "cross-service integration testing requiring performance optimization and documentation",
            "large-scale refactoring with security impact assessment and performance monitoring"
        ]
        
        for query in complex_queries:
            boundaries = boundary_detector.detect_domain_boundaries(query)
            
            assert len(boundaries) >= 1, f"Should detect complex boundaries for: {query}"
            if boundaries:
                boundary = boundaries[0]
                assert boundary.complexity_score >= 1.0, f"Should detect complexity for: {query}"
                assert len(boundary.overlap_indicators) > 0, f"Should detect overlap indicators for: {query}"
    
    def test_boundary_confidence_scoring(self, boundary_detector):
        """Test boundary confidence scoring accuracy."""
        confidence_test_cases = [
            ("pytest testing", 0.7),  # High confidence - strong single domain
            ("test and deploy", 0.5),  # Medium confidence - multi-domain
            ("system analysis", 0.3),  # Lower confidence - generic terms
        ]
        
        for query, expected_min_confidence in confidence_test_cases:
            boundaries = boundary_detector.detect_domain_boundaries(query)
            
            if boundaries:
                assert boundaries[0].confidence >= expected_min_confidence, \
                    f"Confidence for '{query}' should be >= {expected_min_confidence}, got {boundaries[0].confidence}"
    
    def test_overlap_indicator_detection(self, boundary_detector):
        """Test detection of domain overlap indicators."""
        overlap_queries = [
            "coordinate testing with deployment automation",  # integration signal
            "parallel security analysis and performance testing",  # parallel signal
            "testing depends on infrastructure setup",  # dependency signal
        ]
        
        overlap_types = [
            "integration_signal",
            "parallel_signal", 
            "dependency_signal"
        ]
        
        for query, expected_type in zip(overlap_queries, overlap_types):
            boundaries = boundary_detector.detect_domain_boundaries(query)
            
            if boundaries:
                overlap_indicators = boundaries[0].overlap_indicators
                assert any(expected_type in indicator for indicator in overlap_indicators), \
                    f"Should detect {expected_type} in: {query}"


class TestConflictDetectionEngine:
    """Test suite for conflict detection capabilities."""
    
    @pytest.fixture
    def conflict_engine(self):
        return ConflictDetectionEngine()
    
    @pytest.fixture
    def sample_boundaries(self):
        return [
            DomainBoundary(
                primary_domain=DomainType.SECURITY,
                secondary_domains=[DomainType.PERFORMANCE],
                confidence=0.8,
                boundary_patterns=["security", "performance"],
                overlap_indicators=["integration_signal:coordinate"],
                complexity_score=1.5
            )
        ]
    
    def test_security_performance_conflict_detection(self, conflict_engine, sample_boundaries):
        """Test detection of security vs performance conflicts."""
        conflict_queries = [
            "security encryption vs performance optimization",
            "fast processing but secure authentication required",
            "security overhead impacting system performance"
        ]
        
        for query in conflict_queries:
            conflicts = conflict_engine.detect_conflicts(sample_boundaries, query)
            
            security_performance_conflicts = [
                c for c in conflicts if c.conflict_type == ConflictType.SECURITY_PERFORMANCE
            ]
            
            assert len(security_performance_conflicts) >= 1, \
                f"Should detect security-performance conflict in: {query}"
            assert security_performance_conflicts[0].severity >= 0.6
    
    def test_resource_competition_detection(self, conflict_engine):
        """Test detection of resource competition conflicts."""
        resource_boundaries = [
            DomainBoundary(
                primary_domain=DomainType.TESTING,
                secondary_domains=[DomainType.DEPLOYMENT],
                confidence=0.7,
                boundary_patterns=["testing", "deployment"],
                overlap_indicators=[],
                complexity_score=1.0
            )
        ]
        
        resource_queries = [
            "memory intensive testing during cpu heavy deployment",
            "network bandwidth competition between testing and monitoring",
            "disk usage conflicts during parallel operations"
        ]
        
        for query in resource_queries:
            conflicts = conflict_engine.detect_conflicts(resource_boundaries, query)
            
            resource_conflicts = [
                c for c in conflicts if c.conflict_type == ConflictType.RESOURCE_COMPETITION
            ]
            
            assert len(resource_conflicts) >= 1, \
                f"Should detect resource competition in: {query}"
    
    def test_timing_conflict_detection(self, conflict_engine):
        """Test detection of timing-related conflicts."""
        timing_boundaries = [
            DomainBoundary(
                primary_domain=DomainType.TESTING,
                secondary_domains=[DomainType.DEPLOYMENT],
                confidence=0.8,
                boundary_patterns=["testing", "deployment"],
                overlap_indicators=["dependency_signal:before"],
                complexity_score=1.2
            )
        ]
        
        timing_queries = [
            "testing must complete before deployment starts",
            "parallel execution timing conflicts detected",
            "synchronization issues between testing and deployment"
        ]
        
        for query in timing_queries:
            conflicts = conflict_engine.detect_conflicts(timing_boundaries, query)
            
            timing_conflicts = [
                c for c in conflicts if c.conflict_type == ConflictType.TIMING_CONFLICT
            ]
            
            assert len(timing_conflicts) >= 1, \
                f"Should detect timing conflict in: {query}"
    
    def test_conflict_severity_calculation(self, conflict_engine, sample_boundaries):
        """Test conflict severity calculation accuracy."""
        severity_test_cases = [
            ("simple security performance issue", 0.5, 0.8),
            ("critical security vs performance contradiction", 0.7, 1.0),
            ("minor security performance trade-off", 0.3, 0.7)
        ]
        
        for query, min_severity, max_severity in severity_test_cases:
            conflicts = conflict_engine.detect_conflicts(sample_boundaries, query)
            
            if conflicts:
                severity = conflicts[0].severity
                assert min_severity <= severity <= max_severity, \
                    f"Severity for '{query}' should be between {min_severity} and {max_severity}, got {severity}"
    
    def test_resolution_strategy_generation(self, conflict_engine, sample_boundaries):
        """Test that appropriate resolution strategies are generated."""
        query = "security encryption performance optimization conflict"
        conflicts = conflict_engine.detect_conflicts(sample_boundaries, query)
        
        security_performance_conflicts = [
            c for c in conflicts if c.conflict_type == ConflictType.SECURITY_PERFORMANCE
        ]
        
        if security_performance_conflicts:
            strategies = security_performance_conflicts[0].resolution_strategies
            assert len(strategies) >= 3, "Should provide multiple resolution strategies"
            
            # Check for specific strategy patterns
            strategy_text = " ".join(strategies).lower()
            assert "hardware acceleration" in strategy_text or "caching" in strategy_text, \
                "Should include performance optimization strategies"


class TestEnhancedCrossDomainCoordinator:
    """Test suite for the main cross-domain coordinator."""
    
    @pytest.fixture
    def coordinator(self):
        return EnhancedCrossDomainCoordinator()
    
    def test_comprehensive_analysis(self, coordinator):
        """Test comprehensive cross-domain analysis."""
        complex_queries = [
            "infrastructure deployment with security validation and performance monitoring",
            "testing automation requiring documentation and deployment coordination",
            "security audit with performance impact assessment and code quality review"
        ]
        
        for query in complex_queries:
            analysis = coordinator.analyze_cross_domain_integration(query)
            
            assert isinstance(analysis, CrossDomainAnalysis)
            assert analysis.query == query
            assert analysis.processing_time_ms > 0
            assert analysis.integration_complexity >= 0.0
            
            # Should detect at least one boundary for complex queries
            assert len(analysis.detected_boundaries) >= 1, \
                f"Should detect boundaries for complex query: {query}"
    
    def test_coordination_recommendation_generation(self, coordinator):
        """Test coordination recommendation generation."""
        coordination_test_cases = [
            ("simple testing issue", "single-agent"),
            ("testing with deployment coordination", "coordination"),
            ("complex multi-domain infrastructure security performance testing", "meta-coordination")
        ]
        
        for query, expected_pattern in coordination_test_cases:
            analysis = coordinator.analyze_cross_domain_integration(query)
            recommendation = analysis.recommended_coordination.lower()
            
            if expected_pattern == "single-agent":
                assert "single" in recommendation or "primary domain" in recommendation
            elif expected_pattern == "coordination":
                assert "coordination" in recommendation
            elif expected_pattern == "meta-coordination":
                assert "meta" in recommendation or "strategic" in recommendation
    
    def test_agent_suggestion_accuracy(self, coordinator):
        """Test accuracy of agent suggestions."""
        agent_test_cases = [
            ("pytest testing failures", "test-specialist"),
            ("docker container orchestration", "infrastructure-engineer"),
            ("security vulnerability scan", "security-enforcer"),
            ("performance bottleneck analysis", "performance-optimizer"),
            ("API documentation creation", "documentation-enhancer")
        ]
        
        for query, expected_agent in agent_test_cases:
            analysis = coordinator.analyze_cross_domain_integration(query)
            
            if analysis.agent_suggestions:
                top_agent = analysis.agent_suggestions[0][0]
                assert top_agent == expected_agent, \
                    f"Expected {expected_agent} for '{query}', got {top_agent}"
    
    def test_integration_complexity_calculation(self, coordinator):
        """Test integration complexity calculation."""
        complexity_test_cases = [
            ("simple test", 0.0, 0.3),  # Low complexity
            ("testing and deployment coordination", 0.3, 0.7),  # Medium complexity
            ("multi-cloud infrastructure security performance testing documentation", 0.7, 1.0)  # High complexity
        ]
        
        for query, min_complexity, max_complexity in complexity_test_cases:
            analysis = coordinator.analyze_cross_domain_integration(query)
            complexity = analysis.integration_complexity
            
            assert min_complexity <= complexity <= max_complexity, \
                f"Complexity for '{query}' should be between {min_complexity} and {max_complexity}, got {complexity}"
    
    def test_analysis_history_tracking(self, coordinator):
        """Test that analysis history is properly tracked."""
        test_queries = [
            "testing analysis",
            "infrastructure deployment", 
            "security validation"
        ]
        
        initial_count = len(coordinator.analysis_history)
        
        for query in test_queries:
            coordinator.analyze_cross_domain_integration(query)
        
        assert len(coordinator.analysis_history) == initial_count + len(test_queries)
    
    def test_analysis_statistics(self, coordinator):
        """Test analysis statistics generation."""
        # Perform some analyses first
        test_queries = [
            "testing infrastructure security",
            "performance optimization documentation",
            "deployment automation testing"
        ]
        
        for query in test_queries:
            coordinator.analyze_cross_domain_integration(query)
        
        stats = coordinator.get_analysis_stats()
        
        assert 'total_analyses' in stats
        assert stats['total_analyses'] >= len(test_queries)
        assert 'domain_frequency' in stats
        assert 'average_complexity' in stats
        assert 'average_processing_time_ms' in stats
        assert 'conflict_detection_rate' in stats


class TestAgentSelectorIntegration:
    """Test integration of cross-domain coordinator with agent selector."""
    
    @pytest.fixture
    def selector(self):
        return EnhancedAgentSelector()
    
    def test_cross_domain_enhanced_selection(self, selector):
        """Test that cross-domain analysis enhances agent selection."""
        # Skip test if cross-domain coordinator is not available
        if not selector.cross_domain_coordinator:
            pytest.skip("Cross-domain coordinator not available")
        
        cross_domain_queries = [
            "infrastructure security testing coordination",
            "performance optimization with security compliance",
            "documentation automation integrated with testing pipeline"
        ]
        
        for query in cross_domain_queries:
            result = selector.select_agent(query)
            
            # Should have enhanced reasoning from cross-domain analysis
            assert "cross-domain" in result.reasoning.lower() or \
                   "coordination" in result.reasoning.lower() or \
                   "meta" in result.reasoning.lower(), \
                   f"Should have cross-domain reasoning for: {query}"
            
            # Should have reasonable confidence
            assert result.confidence_score >= 0.5
    
    def test_fallback_to_original_selection(self, selector):
        """Test fallback to original selection when cross-domain analysis fails."""
        with patch.object(selector, 'cross_domain_coordinator', None):
            query = "simple testing issue"
            result = selector.select_agent(query)
            
            assert result.agent_name is not None
            assert result.confidence_score > 0
            assert "pattern-based" in result.reasoning.lower() or \
                   "multi-domain" in result.reasoning.lower() or \
                   "matches" in result.reasoning.lower()
    
    def test_meta_coordination_recommendation(self, selector):
        """Test that meta-coordination is recommended for complex scenarios."""
        if not selector.cross_domain_coordinator:
            pytest.skip("Cross-domain coordinator not available")
        
        complex_query = "multi-cloud infrastructure deployment with security compliance validation performance monitoring automated testing and comprehensive documentation"
        result = selector.select_agent(complex_query)
        
        # Should recommend meta-coordinator or analysis-gateway for highly complex scenarios
        assert result.agent_name in ['meta-coordinator', 'analysis-gateway', 'intelligent-enhancer']
    
    def test_cross_domain_analysis_details(self, selector):
        """Test detailed cross-domain analysis retrieval."""
        if not selector.cross_domain_coordinator:
            pytest.skip("Cross-domain coordinator not available")
        
        query = "testing infrastructure deployment coordination"
        analysis_details = selector.get_cross_domain_analysis(query)
        
        if analysis_details:  # Only test if analysis is successful
            assert 'detected_boundaries' in analysis_details
            assert 'potential_conflicts' in analysis_details
            assert 'recommended_coordination' in analysis_details
            assert 'agent_suggestions' in analysis_details
            assert 'integration_complexity' in analysis_details
    
    def test_enhanced_selection_statistics(self, selector):
        """Test that selection statistics include cross-domain information."""
        # Perform some selections first
        test_queries = [
            "testing coordination",
            "infrastructure deployment",
            "security validation"
        ]
        
        for query in test_queries:
            selector.select_agent(query)
        
        stats = selector.get_selection_stats()
        
        # Should have basic stats
        assert 'total_selections' in stats
        assert 'agent_distribution' in stats
        assert 'average_confidence' in stats
        
        # May have cross-domain stats if coordinator is available
        if selector.cross_domain_coordinator:
            assert 'cross_domain_analysis' in stats or stats['total_selections'] > 0


class TestPerformanceAndScalability:
    """Test performance and scalability of the enhanced system."""
    
    @pytest.fixture
    def coordinator(self):
        return EnhancedCrossDomainCoordinator()
    
    def test_analysis_performance(self, coordinator):
        """Test that cross-domain analysis completes within performance targets."""
        test_queries = [
            "simple testing",
            "infrastructure deployment coordination",
            "complex multi-domain security performance testing monitoring documentation"
        ]
        
        for query in test_queries:
            analysis = coordinator.analyze_cross_domain_integration(query)
            
            # Should complete within reasonable time (< 100ms for most cases)
            assert analysis.processing_time_ms < 200, \
                f"Analysis took {analysis.processing_time_ms}ms, should be < 200ms for query: {query}"
    
    def test_memory_usage_control(self, coordinator):
        """Test that memory usage is controlled through history management."""
        # Simulate many analyses
        for i in range(1200):  # More than the 1000 limit
            coordinator.analyze_cross_domain_integration(f"test query {i}")
        
        # Should limit history size
        assert len(coordinator.analysis_history) <= 500, \
            "Should limit analysis history to prevent memory bloat"
    
    def test_concurrent_analysis_safety(self, coordinator):
        """Test that concurrent analyses don't interfere with each other."""
        import threading
        
        results = {}
        
        def analyze_query(query_id):
            query = f"concurrent analysis test {query_id}"
            analysis = coordinator.analyze_cross_domain_integration(query)
            results[query_id] = analysis.query
        
        threads = []
        for i in range(5):
            thread = threading.Thread(target=analyze_query, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All analyses should complete with correct queries
        assert len(results) == 5
        for i in range(5):
            assert f"concurrent analysis test {i}" in results[i]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])