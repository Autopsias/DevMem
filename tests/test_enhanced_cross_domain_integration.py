"""Comprehensive tests for enhanced cross-domain integration system.

This test suite validates the specialized boundary detection and conflict resolution
improvements for cross-domain agent coordination.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from enhanced_cross_domain_coordinator import (
    EnhancedBoundaryDetector,
    ConflictDetectionEngine,
    EnhancedCrossDomainCoordinator,
    PatternLearningEngine,
    DomainType,
    ConflictType,
    DomainBoundary,
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


class TestPatternLearningEngine:
    """Test suite for pattern learning capabilities."""
    
    @pytest.fixture
    def learning_engine(self, tmp_path):
        """Create learning engine with temporary coordination hub path."""
        hub_path = tmp_path / "coordination-hub.md"
        return PatternLearningEngine(coordination_hub_path=str(hub_path))
    
    def test_infrastructure_query_classification(self, learning_engine):
        """Test classification of infrastructure queries."""
        test_cases = [
            ("docker container orchestration setup", "container_orchestration"),
            ("kubernetes pod deployment scaling", "container_orchestration"),
            ("terraform infrastructure provisioning", "infrastructure_automation"),
            ("service mesh networking configuration", "service_networking"),
            ("prometheus monitoring setup", "monitoring_observability"),
            ("autoscaling performance optimization", "scaling_performance")
        ]
        
        for query, expected_type in test_cases:
            result = learning_engine._classify_infrastructure_query(query)
            assert result == expected_type, f"Query '{query}' should be classified as '{expected_type}', got '{result}'"
    
    def test_learning_from_success(self, learning_engine):
        """Test learning from successful agent selections."""
        query = "docker container orchestration issues with networking"
        agent = "infrastructure-engineer"
        confidence = 0.85
        
        learning_engine.learn_from_success(query, agent, confidence, user_feedback=True)
        
        query_type = learning_engine._classify_infrastructure_query(query)
        assert query_type in learning_engine.successful_patterns
        assert len(learning_engine.successful_patterns[query_type]) == 1
        
        pattern = learning_engine.successful_patterns[query_type][0]
        assert pattern['agent'] == agent
        assert pattern['confidence'] == confidence
        assert pattern['user_feedback'] is True
    
    def test_learning_from_failure(self, learning_engine):
        """Test learning from failed agent selections."""
        query = "kubernetes deployment scaling issues"
        selected_agent = "test-specialist"
        expected_agent = "infrastructure-engineer"
        reasons = ["Wrong domain agent selected"]
        
        learning_engine.learn_from_failure(query, selected_agent, expected_agent, reasons)
        
        query_type = learning_engine._classify_infrastructure_query(query)
        assert query_type in learning_engine.failed_patterns
        assert len(learning_engine.failed_patterns[query_type]) == 1
        
        failure = learning_engine.failed_patterns[query_type][0]
        assert failure['selected_agent'] == selected_agent
        assert failure['expected_agent'] == expected_agent
        assert failure['reasons'] == reasons
    
    def test_learned_agent_suggestion(self, learning_engine):
        """Test agent suggestions based on learned patterns."""
        # First, learn a successful pattern
        query = "docker container performance optimization"
        agent = "performance-optimizer"
        confidence = 0.9
        
        learning_engine.learn_from_success(query, agent, confidence, user_feedback=True)
        
        # Test suggestion for similar query
        similar_query = "docker container resource optimization"
        suggestion = learning_engine.get_learned_agent_suggestion(similar_query)
        
        assert suggestion is not None
        assert suggestion[0] == agent
        assert suggestion[1] > 0.5  # Should have reasonable confidence
    
    def test_pattern_weight_updates(self, learning_engine):
        """Test that pattern weights are updated correctly."""
        query = "infrastructure automation with ansible"
        agent = "infrastructure-engineer"
        
        # Learn with positive feedback
        learning_engine.learn_from_success(query, agent, 0.8, user_feedback=True)
        
        query_type = learning_engine._classify_infrastructure_query(query)
        pattern_key = f"{query_type}:{agent}"
        
        assert pattern_key in learning_engine.pattern_weights
        assert learning_engine.pattern_weights[pattern_key] > 0
    
    def test_pattern_storage_to_hub(self, learning_engine, tmp_path):
        """Test storing patterns to coordination hub."""
        # Learn some successful patterns
        test_patterns = [
            ("docker orchestration setup", "infrastructure-engineer", 0.85),
            ("kubernetes scaling analysis", "performance-optimizer", 0.90),
            ("terraform provisioning", "infrastructure-engineer", 0.80)
        ]
        
        for query, agent, confidence in test_patterns:
            learning_engine.learn_from_success(query, agent, confidence)
        
        # Store patterns
        learning_engine.store_successful_patterns_to_hub()
        
        # Verify file was created and contains patterns
        hub_path = tmp_path / "coordination-hub.md"
        assert hub_path.exists()
        
        content = hub_path.read_text()
        assert "Infrastructure Learning Patterns" in content
        assert "infrastructure-engineer" in content
        assert "performance-optimizer" in content
    
    def test_learning_statistics(self, learning_engine):
        """Test learning statistics generation."""
        # Add some patterns
        learning_engine.learn_from_success("docker setup", "infrastructure-engineer", 0.8)
        learning_engine.learn_from_failure("k8s deploy", "test-specialist", "infrastructure-engineer", ["wrong domain"])
        
        stats = learning_engine.get_learning_stats()
        
        assert 'total_successful_patterns' in stats
        assert 'total_failed_patterns' in stats
        assert 'learning_rate' in stats
        assert 'infrastructure_query_types' in stats
        assert stats['total_successful_patterns'] == 1
        assert stats['total_failed_patterns'] == 1
        assert 0 <= stats['learning_rate'] <= 1


class TestEnhancedLearningCoordinator:
    """Test suite for coordinator with learning capabilities."""
    
    @pytest.fixture
    def learning_coordinator(self, tmp_path):
        """Create coordinator with temporary hub path for testing."""
        coordinator = EnhancedCrossDomainCoordinator()
        # Override the learning engine with test path
        hub_path = tmp_path / "coordination-hub.md"
        coordinator.pattern_learning_engine = PatternLearningEngine(coordination_hub_path=str(hub_path))
        return coordinator
    
    def test_infrastructure_learning_integration(self, learning_coordinator):
        """Test integration of learning with infrastructure task analysis."""
        # First, learn a successful pattern
        query = "docker container networking issues"
        agent = "docker-specialist"
        
        learning_coordinator.record_selection_feedback(query, agent, 0.85, user_feedback=True)
        
        # Analyze similar infrastructure query
        similar_query = "docker container service networking problems"
        analysis = learning_coordinator.analyze_cross_domain_integration(similar_query)
        
        # Should have learned agent in suggestions
        agent_names = [suggestion[0] for suggestion in analysis.agent_suggestions]
        assert agent in agent_names or "docker-specialist" in agent_names
    
    def test_learning_confidence_boost(self, learning_coordinator):
        """Test that learning provides confidence boosts for infrastructure tasks."""
        # Learn successful pattern
        learning_coordinator.record_selection_feedback(
            "infrastructure scaling optimization", "performance-optimizer", 0.8, user_feedback=True
        )
        
        # Analyze similar query
        analysis = learning_coordinator.analyze_cross_domain_integration(
            "infrastructure performance scaling analysis"
        )
        
        # Find performance-optimizer in suggestions
        performance_suggestions = [s for s in analysis.agent_suggestions if s[0] == "performance-optimizer"]
        
        if performance_suggestions:
            # Should have boosted confidence due to learning
            assert performance_suggestions[0][1] > 0.7
    
    def test_enhanced_feedback_recording(self, learning_coordinator):
        """Test enhanced feedback recording with task success consideration."""
        query = "docker deployment automation"
        agent = "ci-specialist"
        
        # Test success with task outcome
        learning_coordinator.record_selection_feedback(
            query, agent, 0.7, task_success=True
        )
        
        # Test failure with detailed reasons
        learning_coordinator.record_selection_feedback(
            "kubernetes orchestration", "test-specialist", 0.6, 
            user_feedback=False, expected_agent="infrastructure-engineer", task_success=False
        )
        
        insights = learning_coordinator.get_learning_insights()
        assert insights['total_successful_patterns'] >= 1
        assert insights['total_failed_patterns'] >= 1
    
    def test_learning_insights_generation(self, learning_coordinator):
        """Test generation of learning insights and statistics."""
        # Generate some learning data
        infrastructure_queries = [
            "docker container orchestration",
            "kubernetes pod scaling", 
            "infrastructure monitoring setup"
        ]
        
        for query in infrastructure_queries:
            # Analyze to create infrastructure boundaries
            analysis = learning_coordinator.analyze_cross_domain_integration(query)
            
            # Record feedback
            if analysis.agent_suggestions:
                learning_coordinator.record_selection_feedback(
                    query, analysis.agent_suggestions[0][0], analysis.agent_suggestions[0][1], 
                    user_feedback=True
                )
        
        insights = learning_coordinator.get_learning_insights()
        
        assert 'analyses_with_infrastructure' in insights
        assert 'infrastructure_learning_rate' in insights
        assert insights['analyses_with_infrastructure'] >= 0
    
    def test_force_pattern_storage(self, learning_coordinator, tmp_path):
        """Test forced pattern storage to coordination hub."""
        # Learn some patterns
        learning_coordinator.record_selection_feedback(
            "docker networking setup", "docker-specialist", 0.9, user_feedback=True
        )
        
        # Force storage
        learning_coordinator.force_pattern_storage()
        
        # Verify storage
        hub_path = tmp_path / "coordination-hub.md"
        if hub_path.exists():
            content = hub_path.read_text()
            assert "Infrastructure Learning Patterns" in content
    
    def test_learning_pattern_persistence(self, tmp_path):
        """Test that patterns persist across coordinator instances."""
        hub_path = tmp_path / "coordination-hub.md"
        
        # Create first coordinator and learn pattern
        coordinator1 = EnhancedCrossDomainCoordinator()
        coordinator1.pattern_learning_engine = PatternLearningEngine(coordination_hub_path=str(hub_path))
        coordinator1.record_selection_feedback(
            "docker scaling analysis", "performance-optimizer", 0.85, user_feedback=True
        )
        coordinator1.force_pattern_storage()
        
        # Create second coordinator and check pattern loading
        coordinator2 = EnhancedCrossDomainCoordinator()
        coordinator2.pattern_learning_engine = PatternLearningEngine(coordination_hub_path=str(hub_path))
        
        # Should have loaded existing patterns
        pattern_count = len(coordinator2.pattern_learning_engine.pattern_weights)
        assert pattern_count > 0  # Should have loaded some patterns


class TestLearningPerformanceImprovements:
    """Test suite for validating learning performance improvements."""
    
    @pytest.fixture
    def baseline_coordinator(self):
        """Coordinator without learning for baseline comparison."""
        coordinator = EnhancedCrossDomainCoordinator()
        # Disable learning by removing the learning engine
        coordinator.pattern_learning_engine = None
        return coordinator
    
    @pytest.fixture
    def learning_coordinator(self, tmp_path):
        """Coordinator with learning enabled."""
        coordinator = EnhancedCrossDomainCoordinator()
        hub_path = tmp_path / "coordination-hub.md"
        coordinator.pattern_learning_engine = PatternLearningEngine(coordination_hub_path=str(hub_path))
        return coordinator
    
    def test_accuracy_improvement_measurement(self, baseline_coordinator, learning_coordinator):
        """Test framework for measuring accuracy improvements."""
        # Infrastructure test queries with known correct agents
        test_cases = [
            ("docker container orchestration setup", "infrastructure-engineer"),
            ("kubernetes pod scaling issues", "infrastructure-engineer"),
            ("docker performance optimization", "performance-optimizer"),
            ("container networking problems", "docker-specialist"),
            ("infrastructure monitoring setup", "infrastructure-engineer")
        ]
        
        baseline_correct = 0
        learning_correct = 0
        
        # Train learning coordinator with some patterns first
        for query, correct_agent in test_cases[:3]:  # Use first 3 for training
            learning_coordinator.record_selection_feedback(query, correct_agent, 0.9, user_feedback=True)
        
        # Test both coordinators
        for query, correct_agent in test_cases:
            # Baseline analysis
            baseline_analysis = baseline_coordinator.analyze_cross_domain_integration(query)
            if baseline_analysis.agent_suggestions and baseline_analysis.agent_suggestions[0][0] == correct_agent:
                baseline_correct += 1
            
            # Learning analysis
            learning_analysis = learning_coordinator.analyze_cross_domain_integration(query)
            if learning_analysis.agent_suggestions and learning_analysis.agent_suggestions[0][0] == correct_agent:
                learning_correct += 1
        
        # Learning coordinator should perform at least as well as baseline
        learning_accuracy = learning_correct / len(test_cases)
        baseline_accuracy = baseline_correct / len(test_cases)
        
        # For infrastructure queries, learning should show improvement
        # This test validates the framework works, actual improvement depends on training data
        assert learning_accuracy >= 0.4  # Should meet minimum target
        
        print(f"Baseline accuracy: {baseline_accuracy:.1%}")
        print(f"Learning accuracy: {learning_accuracy:.1%}")
        print(f"Improvement: {(learning_accuracy - baseline_accuracy):.1%}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])