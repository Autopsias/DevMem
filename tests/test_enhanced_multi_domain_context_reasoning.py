#!/usr/bin/env python3
"""
Comprehensive test suite for Enhanced Multi-Domain Context Reasoning System.

This test suite validates:
1. Multi-domain pattern recognition with semantic analysis
2. Cross-domain relationship mapping and dependency tracking  
3. Context preservation strategies across agent handoffs
4. Domain-specific optimization for improved coordination accuracy
5. Pattern learning with contextual reinforcement
6. Performance metrics and quality scoring
"""

import pytest
import time
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from enhanced_multi_domain_context_reasoning import (
    EnhancedMultiDomainContextReasoner,
    SemanticAnalyzer,
    CrossDomainRelationshipMapper,
    ContextPreservationManager,
    DomainSpecificOptimizer,
    ContextElement,
    DomainRelationship,
    DomainRelationshipType,
    ContextPreservationStrategy,
    PatternComplexity
)

class TestSemanticAnalyzer:
    """Test semantic analysis capabilities."""
    
    @pytest.fixture
    def analyzer(self):
        return SemanticAnalyzer()
    
    def test_domain_pattern_recognition(self, analyzer):
        """Test recognition of domain-specific patterns."""
        test_cases = [
            ("Docker container testing with async patterns", ['testing', 'infrastructure']),
            ("Security vulnerability requires immediate authentication fix", ['security']),
            ("Performance optimization for bottleneck analysis", ['performance']),
            ("Infrastructure deployment with security compliance", ['infrastructure', 'security'])
        ]
        
        for query, expected_domains in test_cases:
            analysis = analyzer.analyze_semantic_patterns(query)
            detected_domains = list(analysis['domain_scores'].keys())
            
            for expected_domain in expected_domains:
                assert expected_domain in detected_domains, \
                    f"Expected domain '{expected_domain}' not detected in '{query}'"
            
            # Check confidence scores are reasonable
            for domain, data in analysis['domain_scores'].items():
                assert 0.0 <= data['confidence'] <= 1.0, \
                    f"Invalid confidence score for domain '{domain}': {data['confidence']}"
    
    def test_relationship_pattern_detection(self, analyzer):
        """Test detection of domain relationship patterns."""
        test_cases = [
            ("Security testing then performance analysis", 'sequential'),
            ("Coordinate infrastructure and security validation", 'parallel'),
            ("Testing requires Docker environment setup", 'dependent'),
            ("Performance vs security trade-off analysis", 'conflicting')
        ]
        
        for query, expected_relationship in test_cases:
            analysis = analyzer.analyze_semantic_patterns(query)
            relationship_types = [rel['type'] for rel in analysis['relationship_indicators']]
            
            assert expected_relationship in relationship_types, \
                f"Expected relationship '{expected_relationship}' not detected in '{query}'"
    
    def test_semantic_complexity_calculation(self, analyzer):
        """Test semantic complexity scoring."""
        test_cases = [
            ("Fix test", 0.0, 0.4),  # Simple query, low complexity
            ("Docker container security testing coordination", 0.4, 0.8),  # Multi-domain, medium complexity
            ("Comprehensive security infrastructure performance testing coordination analysis", 0.6, 1.0)  # High complexity
        ]
        
        for query, min_complexity, max_complexity in test_cases:
            analysis = analyzer.analyze_semantic_patterns(query)
            complexity = analysis['semantic_complexity']
            
            assert min_complexity <= complexity <= max_complexity, \
                f"Complexity {complexity} not in range [{min_complexity}, {max_complexity}] for '{query}'"

class TestCrossDomainRelationshipMapper:
    """Test cross-domain relationship mapping."""
    
    @pytest.fixture
    def mapper(self):
        return CrossDomainRelationshipMapper()
    
    def test_relationship_registration(self, mapper):
        """Test registering domain relationships."""
        relationship = DomainRelationship(
            from_domain='testing',
            to_domain='infrastructure',
            relationship_type=DomainRelationshipType.DEPENDENT,
            strength=0.8,
            bidirectional=True
        )
        
        mapper.register_relationship(relationship)
        
        # Test forward relationship
        strength = mapper.get_relationship_strength('testing', 'infrastructure')
        assert strength == 0.8, f"Expected strength 0.8, got {strength}"
        
        # Test bidirectional relationship
        reverse_strength = mapper.get_relationship_strength('infrastructure', 'testing')
        assert reverse_strength == 0.8, f"Expected reverse strength 0.8, got {reverse_strength}"
    
    def test_domain_path_finding(self, mapper):
        """Test finding paths between domains."""
        # Set up relationship chain: A -> B -> C
        relationships = [
            DomainRelationship('testing', 'infrastructure', DomainRelationshipType.DEPENDENT, 0.7),
            DomainRelationship('infrastructure', 'security', DomainRelationshipType.SEQUENTIAL, 0.6)
        ]
        
        for rel in relationships:
            mapper.register_relationship(rel)
        
        # Test direct path
        path = mapper.find_domain_path('testing', 'infrastructure')
        assert path == ['testing', 'infrastructure'], f"Expected direct path, got {path}"
        
        # Test indirect path
        path = mapper.find_domain_path('testing', 'security')
        assert path == ['testing', 'infrastructure', 'security'], f"Expected indirect path, got {path}"
        
        # Test no path
        path = mapper.find_domain_path('testing', 'nonexistent')
        assert path == [], f"Expected empty path, got {path}"
    
    def test_related_domains_discovery(self, mapper):
        """Test discovering related domains."""
        relationships = [
            DomainRelationship('testing', 'infrastructure', DomainRelationshipType.DEPENDENT, 0.8),
            DomainRelationship('testing', 'security', DomainRelationshipType.SEQUENTIAL, 0.6),
            DomainRelationship('testing', 'performance', DomainRelationshipType.PARALLEL, 0.4)
        ]
        
        for rel in relationships:
            mapper.register_relationship(rel)
        
        related = mapper.get_related_domains('testing', min_strength=0.5)
        
        # Should return domains with strength >= 0.5, sorted by strength
        assert len(related) == 2, f"Expected 2 related domains, got {len(related)}"
        assert related[0] == ('infrastructure', 0.8), f"Expected ('infrastructure', 0.8), got {related[0]}"
        assert related[1] == ('security', 0.6), f"Expected ('security', 0.6), got {related[1]}"
    
    def test_relationship_strength_updates(self, mapper):
        """Test updating relationship strength based on success."""
        relationship = DomainRelationship(
            'testing', 'infrastructure', DomainRelationshipType.DEPENDENT, 0.5
        )
        mapper.register_relationship(relationship)
        
        # Test successful coordination increases strength
        mapper.update_relationship_strength('testing', 'infrastructure', success=True)
        new_strength = mapper.get_relationship_strength('testing', 'infrastructure')
        assert new_strength > 0.5, f"Expected strength increase, got {new_strength}"
        
        # Test failed coordination decreases strength
        mapper.update_relationship_strength('testing', 'infrastructure', success=False)
        final_strength = mapper.get_relationship_strength('testing', 'infrastructure')
        assert final_strength < new_strength, f"Expected strength decrease, got {final_strength}"

class TestContextPreservationManager:
    """Test context preservation across domain transitions."""
    
    @pytest.fixture
    def manager(self):
        mapper = CrossDomainRelationshipMapper()
        return ContextPreservationManager(mapper)
    
    @pytest.fixture
    def sample_context_elements(self):
        return [
            ContextElement(
                element_id="test1",
                content="Async test failure in container",
                domain="testing",
                importance=0.9,
                timestamp=datetime.now()
            ),
            ContextElement(
                element_id="infra1",
                content="Docker networking configuration",
                domain="infrastructure",
                importance=0.7,
                timestamp=datetime.now()
            ),
            ContextElement(
                element_id="sec1",
                content="Authentication vulnerability detected",
                domain="security",
                importance=0.8,
                timestamp=datetime.now()
            ),
            ContextElement(
                element_id="perf1",
                content="High memory usage observed",
                domain="performance",
                importance=0.5,
                timestamp=datetime.now()
            )
        ]
    
    def test_full_transfer_strategy(self, manager, sample_context_elements):
        """Test full context transfer strategy."""
        preserved, metrics = manager.preserve_context(
            sample_context_elements, 'testing', 'infrastructure',
            ContextPreservationStrategy.FULL_TRANSFER
        )
        
        assert len(preserved) == len(sample_context_elements), \
            f"Expected {len(sample_context_elements)} elements, got {len(preserved)}"
        
        assert metrics.preserved_elements == metrics.total_elements, \
            "Full transfer should preserve all elements"
    
    def test_selective_transfer_strategy(self, manager, sample_context_elements):
        """Test selective context transfer strategy."""
        # Set up relationship to influence selection
        relationship = DomainRelationship(
            'testing', 'infrastructure', DomainRelationshipType.DEPENDENT, 0.8
        )
        manager.relationship_mapper.register_relationship(relationship)
        
        preserved, metrics = manager.preserve_context(
            sample_context_elements, 'testing', 'infrastructure',
            ContextPreservationStrategy.SELECTIVE_TRANSFER
        )
        
        # Should preserve high-importance and relevant elements
        assert len(preserved) >= 2, f"Expected at least 2 preserved elements, got {len(preserved)}"
        assert len(preserved) < len(sample_context_elements), \
            "Selective transfer should reduce context size"
        
        # Check that critical elements are preserved
        critical_preserved = sum(1 for e in preserved if e.importance >= 0.8)
        assert critical_preserved >= 2, f"Expected at least 2 critical elements, got {critical_preserved}"
    
    def test_hierarchical_transfer_strategy(self, manager, sample_context_elements):
        """Test hierarchical context transfer strategy."""
        preserved, metrics = manager.preserve_context(
            sample_context_elements, 'testing', 'security',
            ContextPreservationStrategy.HIERARCHICAL_TRANSFER
        )
        
        # Should preserve elements in hierarchical layers
        critical_elements = [e for e in preserved if e.importance >= 0.8]
        assert len(critical_elements) >= 2, \
            f"Expected at least 2 critical elements, got {len(critical_elements)}"
        
        # Check that preserved elements are sorted by importance
        importances = [e.importance for e in preserved]
        assert importances == sorted(importances, reverse=True), \
            "Hierarchical transfer should preserve by importance order"
    
    def test_context_preservation_metrics(self, manager, sample_context_elements):
        """Test context preservation metrics calculation."""
        preserved, metrics = manager.preserve_context(
            sample_context_elements, 'testing', 'infrastructure',
            ContextPreservationStrategy.SELECTIVE_TRANSFER
        )
        
        # Check metric ranges
        assert metrics.total_elements == len(sample_context_elements)
        assert 0 <= metrics.preserved_elements <= metrics.total_elements
        assert 0 <= metrics.critical_elements_preserved <= metrics.critical_elements_total
        assert 0.0 <= metrics.domain_coverage <= 1.0
        assert 0.0 <= metrics.semantic_coherence <= 1.0
        assert metrics.transfer_latency_ms >= 0
        
        # Test quality score calculation
        quality_score = manager.get_preservation_quality_score(metrics)
        assert 0.0 <= quality_score <= 1.0, f"Invalid quality score: {quality_score}"

class TestDomainSpecificOptimizer:
    """Test domain-specific optimization."""
    
    @pytest.fixture
    def optimizer(self):
        return DomainSpecificOptimizer()
    
    def test_domain_optimization_strategies(self, optimizer):
        """Test optimization strategies for different domains."""
        test_cases = [
            ('testing', 'async test failures in Docker container', ['test-specialist']),
            ('infrastructure', 'Docker container orchestration scaling issues', ['infrastructure-engineer']),
            ('security', 'authentication vulnerability analysis needed', ['security-auditor']),
            ('performance', 'latency optimization for API endpoints', ['performance-optimizer'])
        ]
        
        available_agents = [
            'test-specialist', 'infrastructure-engineer', 'security-auditor', 
            'performance-optimizer', 'analysis-gateway'
        ]
        
        for domain, query, expected_agents in test_cases:
            result = optimizer.optimize_for_domain(domain, query, available_agents)
            
            assert result['domain'] == domain
            assert len(result['optimal_agents']) >= 1
            assert any(agent in expected_agents for agent in result['optimal_agents'])
            assert 0.0 <= result['confidence'] <= 1.0
            assert result['coordination_strategy'] in ['sequential', 'parallel', 'hierarchical']
    
    def test_coordination_request_analysis(self, optimizer):
        """Test analysis of coordination requests."""
        domain_config = optimizer.domain_optimizations['testing']
        
        # Test high priority keyword match
        high_priority_query = "async testing with mock fixtures and coverage analysis"
        analysis = optimizer._analyze_coordination_request(high_priority_query, domain_config)
        
        assert len(analysis['priority_keyword_matches']) >= 2, \
            f"Expected priority matches, got {analysis['priority_keyword_matches']}"
        assert analysis['priority_score'] > 0.5, \
            f"Expected high priority score, got {analysis['priority_score']}"
        
        # Test complexity detection
        complex_query = "comprehensive systematic end-to-end testing coordination"
        analysis = optimizer._analyze_coordination_request(complex_query, domain_config)
        
        assert analysis['complexity_score'] > 0.3, \
            f"Expected complexity detection, got {analysis['complexity_score']}"
    
    def test_performance_baseline_management(self, optimizer):
        """Test performance baseline tracking."""
        domain = 'testing'
        
        # Get initial baseline
        baseline = optimizer.get_domain_performance_baseline(domain)
        assert 'avg_response_time_ms' in baseline
        assert 'success_rate' in baseline
        
        # Update with new metrics
        new_metrics = {
            'avg_response_time_ms': 1200.0,
            'success_rate': 0.92
        }
        optimizer.update_performance_baseline(domain, new_metrics)
        
        updated_baseline = optimizer.get_domain_performance_baseline(domain)
        
        # Should show some movement toward new metrics
        assert updated_baseline['avg_response_time_ms'] != baseline['avg_response_time_ms']
        assert updated_baseline['success_rate'] != baseline['success_rate']

class TestEnhancedMultiDomainContextReasoner:
    """Test the main enhanced multi-domain context reasoner."""
    
    @pytest.fixture
    def reasoner(self):
        return EnhancedMultiDomainContextReasoner()
    
    def test_simple_single_domain_analysis(self, reasoner):
        """Test analysis of simple single-domain queries."""
        query = "Fix failing test case"
        analysis = reasoner.analyze_multi_domain_query(query)
        
        assert analysis['primary_domain'] in ['testing', 'general']
        assert analysis['pattern_complexity'] in [PatternComplexity.SIMPLE, PatternComplexity.MODERATE]
        assert analysis['coordination_strategy']['approach'] in ['direct_agent', 'sequential_coordination']
        assert 0.0 <= analysis['reasoning_confidence'] <= 1.0
        assert analysis['analysis_time_ms'] > 0
    
    def test_moderate_multi_domain_analysis(self, reasoner):
        """Test analysis of moderate multi-domain queries."""
        query = "Docker container performance testing with security validation"
        analysis = reasoner.analyze_multi_domain_query(query)
        
        assert len(analysis['secondary_domains']) >= 1
        assert analysis['pattern_complexity'] in [PatternComplexity.MODERATE, PatternComplexity.COMPLEX]
        assert analysis['coordination_strategy']['agent_count'] >= 2
        assert len(analysis['domain_relationships']) >= 1
    
    def test_complex_multi_domain_analysis(self, reasoner):
        """Test analysis of complex multi-domain queries."""
        query = "Comprehensive security infrastructure performance testing coordination analysis using parallel assessment across multiple domains"
        analysis = reasoner.analyze_multi_domain_query(query)
        
        assert len(analysis['secondary_domains']) >= 2
        assert analysis['pattern_complexity'] in [PatternComplexity.COMPLEX, PatternComplexity.CRITICAL]
        assert analysis['coordination_strategy']['approach'] in ['parallel_coordination', 'hierarchical_meta_coordination']
        assert len(analysis['coordination_strategy']['selected_agents']) >= 3
    
    def test_domain_relationship_analysis(self, reasoner):
        """Test analysis of domain relationships."""
        query = "Infrastructure security testing requires performance monitoring"
        analysis = reasoner.analyze_multi_domain_query(query)
        
        relationships = analysis['domain_relationships']
        assert len(relationships) >= 1
        
        for rel in relationships:
            assert 'from_domain' in rel
            assert 'to_domain' in rel
            assert 0.0 <= rel['strength'] <= 1.0
            assert isinstance(rel['path'], list)
            assert rel['path_length'] >= 0
    
    def test_coordination_strategy_generation(self, reasoner):
        """Test coordination strategy generation."""
        test_cases = [
            ("Simple test fix", ['direct_agent']),
            ("Docker testing coordination", ['sequential_coordination', 'parallel_coordination']),
            ("Multi-domain crisis response", ['hierarchical_meta_coordination', 'parallel_coordination'])
        ]
        
        for query, expected_approaches in test_cases:
            analysis = reasoner.analyze_multi_domain_query(query)
            strategy = analysis['coordination_strategy']
            
            assert strategy['approach'] in expected_approaches, \
                f"Unexpected approach '{strategy['approach']}' for query '{query}'"
            assert len(strategy['selected_agents']) >= 1
            assert strategy['estimated_execution_time_ms'] > 0
    
    def test_context_preservation_strategy_selection(self, reasoner):
        """Test selection of context preservation strategies."""
        test_cases = [
            (PatternComplexity.SIMPLE, 1, 'full_transfer'),
            (PatternComplexity.MODERATE, 2, 'hierarchical_transfer'),
            (PatternComplexity.COMPLEX, 3, 'selective_transfer'),
            (PatternComplexity.CRITICAL, 4, 'adaptive_transfer')
        ]
        
        for complexity, domain_count, expected_strategy in test_cases:
            strategy = reasoner._select_context_preservation_strategy(complexity, domain_count)
            assert strategy.value == expected_strategy, \
                f"Expected {expected_strategy}, got {strategy.value} for complexity {complexity} and {domain_count} domains"
    
    def test_reasoning_performance_tracking(self, reasoner):
        """Test performance metrics tracking."""
        queries = [
            "Test Docker container performance",
            "Security analysis for infrastructure deployment",
            "Comprehensive multi-domain coordination analysis"
        ]
        
        for query in queries:
            reasoner.analyze_multi_domain_query(query)
        
        metrics = reasoner.get_reasoning_metrics()
        
        assert 'analysis_time_ms' in metrics
        assert metrics['analysis_time_ms']['count'] == len(queries)
        assert metrics['analysis_time_ms']['avg'] > 0
        assert metrics['analysis_time_ms']['min'] > 0
        assert metrics['analysis_time_ms']['max'] >= metrics['analysis_time_ms']['min']

class TestPatternComplexityDetection:
    """Test pattern complexity detection accuracy."""
    
    @pytest.fixture
    def reasoner(self):
        return EnhancedMultiDomainContextReasoner()
    
    def test_simple_pattern_detection(self, reasoner):
        """Test detection of simple patterns."""
        simple_queries = [
            "Fix test",
            "Run Docker container",
            "Check security logs",
            "Optimize query performance"
        ]
        
        for query in simple_queries:
            analysis = reasoner.analyze_multi_domain_query(query)
            complexity = analysis['pattern_complexity']
            
            assert complexity in [PatternComplexity.SIMPLE, PatternComplexity.MODERATE], \
                f"Expected simple/moderate complexity for '{query}', got {complexity}"
    
    def test_complex_pattern_detection(self, reasoner):
        """Test detection of complex patterns."""
        complex_queries = [
            "Comprehensive security infrastructure performance testing coordination analysis",
            "Multi-domain crisis response requiring systematic parallel coordination across testing security infrastructure performance domains",
            "End-to-end system validation with cross-domain dependency resolution and conflict management"
        ]
        
        for query in complex_queries:
            analysis = reasoner.analyze_multi_domain_query(query)
            complexity = analysis['pattern_complexity']
            
            assert complexity in [PatternComplexity.COMPLEX, PatternComplexity.CRITICAL], \
                f"Expected complex/critical complexity for '{query}', got {complexity}"

class TestPerformanceRequirements:
    """Test performance requirements compliance."""
    
    @pytest.fixture
    def reasoner(self):
        return EnhancedMultiDomainContextReasoner()
    
    def test_analysis_performance_targets(self, reasoner):
        """Test that analysis meets performance targets."""
        # Performance targets based on coordination-hub.md
        target_times = {
            'simple': 500,    # ms
            'moderate': 1000, # ms  
            'complex': 2000   # ms
        }
        
        test_cases = [
            ("Fix test", 'simple'),
            ("Docker security testing coordination", 'moderate'),
            ("Comprehensive multi-domain analysis with parallel coordination", 'complex')
        ]
        
        for query, category in test_cases:
            start_time = time.time()
            analysis = reasoner.analyze_multi_domain_query(query)
            total_time_ms = (time.time() - start_time) * 1000
            
            target_time = target_times[category]
            assert total_time_ms < target_time, \
                f"Query '{query}' took {total_time_ms:.1f}ms, expected <{target_time}ms"
            
            # Also check reported analysis time
            assert analysis['analysis_time_ms'] > 0
            assert analysis['analysis_time_ms'] < target_time
    
    def test_context_preservation_performance(self, reasoner):
        """Test context preservation performance targets."""
        # Create sample context with varying complexity
        sample_contexts = [
            # Simple context (5 elements)
            [ContextElement(f"elem_{i}", f"content_{i}", "testing", 0.5, datetime.now()) 
             for i in range(5)],
            # Moderate context (15 elements)
            [ContextElement(f"elem_{i}", f"content_{i}", "testing", 0.5, datetime.now()) 
             for i in range(15)],
            # Complex context (30 elements)
            [ContextElement(f"elem_{i}", f"content_{i}", "testing", 0.5, datetime.now()) 
             for i in range(30)]
        ]
        
        performance_targets = [50, 100, 200]  # ms
        
        for context_elements, target_time in zip(sample_contexts, performance_targets):
            start_time = time.time()
            preserved, metrics = reasoner.context_manager.preserve_context(
                context_elements, 'testing', 'infrastructure'
            )
            total_time_ms = (time.time() - start_time) * 1000
            
            assert total_time_ms < target_time, \
                f"Context preservation took {total_time_ms:.1f}ms for {len(context_elements)} elements, expected <{target_time}ms"
            
            # Check reported transfer latency
            assert metrics.transfer_latency_ms < target_time

class TestIntegrationScenarios:
    """Test realistic integration scenarios."""
    
    @pytest.fixture
    def reasoner(self):
        return EnhancedMultiDomainContextReasoner()
    
    def test_testing_infrastructure_coordination(self, reasoner):
        """Test coordination between testing and infrastructure domains."""
        query = "Docker container test failures require infrastructure analysis and performance monitoring"
        analysis = reasoner.analyze_multi_domain_query(query)
        
        # Should detect multiple domains
        all_domains = [analysis['primary_domain']] + analysis['secondary_domains']
        assert 'testing' in all_domains or 'infrastructure' in all_domains
        assert len(all_domains) >= 2
        
        # Should suggest appropriate coordination
        strategy = analysis['coordination_strategy']
        assert len(strategy['selected_agents']) >= 2
        assert strategy['approach'] in ['sequential_coordination', 'parallel_coordination']
    
    def test_security_performance_conflict_resolution(self, reasoner):
        """Test handling of security vs performance conflicts."""
        query = "Security encryption requirements conflict with performance optimization goals"
        analysis = reasoner.analyze_multi_domain_query(query)
        
        # Should detect conflict relationship
        semantic_analysis = analysis['semantic_analysis']
        relationship_indicators = [rel['type'] for rel in semantic_analysis['relationship_indicators']]
        assert 'conflicting' in relationship_indicators
        
        # Should suggest appropriate coordination strategy
        assert analysis['pattern_complexity'] in [PatternComplexity.MODERATE, PatternComplexity.COMPLEX]
        assert analysis['reasoning_confidence'] > 0.5  # Should be confident about conflict detection
    
    def test_crisis_scenario_coordination(self, reasoner):
        """Test coordination for crisis scenarios."""
        query = "Critical system failure affecting security infrastructure performance testing requiring immediate comprehensive analysis"
        analysis = reasoner.analyze_multi_domain_query(query)
        
        # Should recognize as critical complexity
        assert analysis['pattern_complexity'] == PatternComplexity.CRITICAL
        
        # Should suggest meta-coordination
        strategy = analysis['coordination_strategy']
        assert strategy['approach'] in ['hierarchical_meta_coordination', 'parallel_coordination']
        assert len(strategy['selected_agents']) >= 3
        
        # Should have high confidence for clear crisis patterns
        assert analysis['reasoning_confidence'] > 0.6

if __name__ == "__main__":
    pytest.main(["-v", __file__])
