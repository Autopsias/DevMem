"""Tests for agent selection edge cases and variations."""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.agent_selector import EnhancedAgentSelector, AgentMatchResult


class TestAgentSelectionEdgeCases:
    """Test suite for edge cases in agent selection."""
    
    @pytest.fixture
    def selector(self):
        return EnhancedAgentSelector()
    
    def test_empty_query(self, selector):
        """Test handling of empty queries."""
        result = selector.select_agent("")
        
        assert result.agent_name == 'intelligent-enhancer'
        assert result.confidence_score <= 0.2
        assert "empty" in result.reasoning.lower()
    
    def test_very_short_query(self, selector):
        """Test handling of very short queries."""
        result = selector.select_agent("hi")
        
        assert result.agent_name == 'intelligent-enhancer'
        assert result.confidence_score <= 0.2
        assert "short" in result.reasoning.lower()
    
    def test_multi_domain_query(self, selector):
        """Test queries that span multiple domains."""
        query = "docker container security performance testing with pytest"
        result = selector.select_agent(query)
        
        # Should detect multiple domains but still select best match
        assert result.agent_name is not None
        assert result.confidence_score > 0.3
        assert len(result.context_keywords) >= 3
    
    def test_ambiguous_query(self, selector):
        """Test handling of ambiguous queries."""
        ambiguous_queries = [
            "something is broken",
            "need help",
            "fix this",
            "not working",
            "issues with the system"
        ]
        
        for query in ambiguous_queries:
            result = selector.select_agent(query)
            
            # Should still return a result
            assert result.agent_name is not None
            assert 0.0 <= result.confidence_score <= 1.0
            assert result.processing_time_ms >= 0
    
    def test_technical_jargon_query(self, selector):
        """Test queries with heavy technical jargon."""
        jargon_queries = [
            "asyncio event loop pytest-asyncio fixture configuration",
            "kubernetes ingress controller networking policies",
            "OAuth2 PKCE flow JWT token validation middleware",
            "memory profiling heap dumps gc optimization",
            "AST parsing type annotation metaclass refactoring"
        ]
        
        for query in jargon_queries:
            result = selector.select_agent(query)
            
            # Should handle technical terms well
            assert result.agent_name is not None
            assert result.confidence_score > 0.4  # Should be fairly confident with technical terms
            assert len(result.context_keywords) >= 2
    
    def test_natural_language_variations(self, selector):
        """Test different natural language expressions of same intent."""
        test_cases = [
            # Testing variations
            [
                "test is failing",
                "tests are broken", 
                "testing framework not working",
                "pytest configuration issues"
            ],
            # Infrastructure variations
            [
                "docker container won't start",
                "container orchestration problems",
                "service deployment failing",
                "infrastructure scaling issues"
            ],
            # Security variations
            [
                "security vulnerability found",
                "credential leak detected",
                "authentication not working",
                "security audit needed"
            ]
        ]
        
        for variations in test_cases:
            agents_selected = []
            for query in variations:
                result = selector.select_agent(query)
                agents_selected.append(result.agent_name)
            
            # Most variations should select the same agent or related agents
            most_common = max(set(agents_selected), key=agents_selected.count)
            consistency_ratio = agents_selected.count(most_common) / len(agents_selected)
            
            assert consistency_ratio >= 0.6, f"Inconsistent agent selection for variations: {agents_selected}"
    
    def test_keyword_stemming_and_variations(self, selector):
        """Test that keyword variations are handled correctly."""
        stemming_cases = [
            ("testing framework", "test framework"),
            ("container orchestration", "containers orchestrate"),
            ("security scanning", "secure scan"),
            ("performance optimization", "optimize performance"),
            ("code refactoring", "refactor code")
        ]
        
        for original, variation in stemming_cases:
            result1 = selector.select_agent(original)
            result2 = selector.select_agent(variation)
            
            # Should select the same agent for related variations
            assert result1.agent_name == result2.agent_name, \
                f"Different agents for '{original}' ({result1.agent_name}) vs '{variation}' ({result2.agent_name})"
    
    def test_context_based_disambiguation(self, selector):
        """Test that context helps disambiguate similar queries."""
        context_cases = [
            ("performance issues", "test performance", "test-specialist"),
            ("performance issues", "docker performance", "infrastructure-engineer"),
            ("performance issues", "code performance", "performance-optimizer"),
        ]
        
        for base_query, context_query, expected_agent in context_cases:
            result = selector.select_agent(context_query)
            
            # Context should help select more appropriate agent
            assert result.agent_name == expected_agent or result.confidence_score > 0.6, \
                f"Context query '{context_query}' didn't improve selection: got {result.agent_name}"
    
    def test_compound_queries(self, selector):
        """Test queries with multiple actions or complex requirements."""
        compound_queries = [
            "fix failing tests and improve coverage",
            "deploy container and setup monitoring",
            "audit security and optimize performance",
            "refactor code and add type annotations",
            "configure CI pipeline and run tests"
        ]
        
        for query in compound_queries:
            result = selector.select_agent(query)
            
            # Should still select appropriate primary agent
            assert result.agent_name is not None
            assert result.confidence_score > 0.4
            assert len(result.context_keywords) >= 2
    
    def test_negative_queries(self, selector):
        """Test queries with negative or problem-focused language."""
        negative_queries = [
            "tests not passing",
            "container won't start",
            "security breach detected",
            "performance is terrible",
            "code is messy and needs cleanup"
        ]
        
        for query in negative_queries:
            result = selector.select_agent(query)
            
            # Should still identify appropriate domain despite negative framing
            assert result.agent_name is not None
            assert result.confidence_score > 0.3
    
    def test_question_format_queries(self, selector):
        """Test queries formatted as questions."""
        question_queries = [
            "How do I fix this test failure?",
            "What's wrong with my container setup?",
            "Can you help secure this application?",
            "Why is the performance so slow?",
            "Should I refactor this code?"
        ]
        
        for query in question_queries:
            result = selector.select_agent(query)
            
            # Should extract domain from question format
            assert result.agent_name is not None
            assert result.confidence_score > 0.3
    
    def test_imperative_queries(self, selector):
        """Test queries in imperative/command format."""
        imperative_queries = [
            "Run the test suite",
            "Deploy the containers", 
            "Scan for vulnerabilities",
            "Optimize the database queries",
            "Clean up this messy code"
        ]
        
        for query in imperative_queries:
            result = selector.select_agent(query)
            
            # Should identify action and domain
            assert result.agent_name is not None
            assert result.confidence_score > 0.4
    
    def test_misspelled_queries(self, selector):
        """Test handling of common misspellings."""
        # Note: Current implementation doesn't handle misspellings,
        # but should gracefully degrade
        misspelled_queries = [
            "teset failing",  # test
            "dokcer container",  # docker
            "secruity scan",  # security
            "perfomance issue",  # performance
            "refacctor code"  # refactor
        ]
        
        for query in misspelled_queries:
            result = selector.select_agent(query)
            
            # Should still return a result, even if not optimal
            assert result.agent_name is not None
            assert result.confidence_score >= 0.1
    
    def test_special_characters_and_symbols(self, selector):
        """Test queries with special characters and symbols."""
        special_queries = [
            "test@failing with $variables",
            "docker-compose.yml configuration",
            "API/security & authentication",
            "performance: CPU > 80%",
            "code_refactoring.py needed!"
        ]
        
        for query in special_queries:
            result = selector.select_agent(query)
            
            # Should handle special characters gracefully
            assert result.agent_name is not None
            assert result.confidence_score >= 0.2
    
    def test_very_long_queries(self, selector):
        """Test handling of very long, detailed queries."""
        long_query = """
        I have a complex issue with my pytest test suite where the async tests are failing
        intermittently due to mock configuration problems. The test coverage is also dropping
        because some integration tests aren't running properly. The fixtures seem to be
        incorrectly configured and there might be some race conditions in the async test
        execution. Additionally, the CI pipeline is failing because of these test issues
        and I need to resolve this quickly for the production deployment.
        """
        
        result = selector.select_agent(long_query)
        
        # Should extract key concepts from long text
        assert result.agent_name == 'test-specialist'  # Primary domain is testing
        assert result.confidence_score > 0.6
        assert 'test' in result.context_keywords
        assert 'async' in result.context_keywords
        assert 'mock' in result.context_keywords
    
    def test_multiple_suggestions(self, selector):
        """Test getting multiple agent suggestions."""
        query = "docker container testing performance"
        suggestions = selector.get_agent_suggestions(query, top_n=3)
        
        assert len(suggestions) <= 3
        assert all(isinstance(s, AgentMatchResult) for s in suggestions)
        
        # Should be sorted by confidence
        confidences = [s.confidence_score for s in suggestions]
        assert confidences == sorted(confidences, reverse=True)
        
        # Should include relevant agents
        suggested_agents = [s.agent_name for s in suggestions]
        relevant_agents = {'infrastructure-engineer', 'test-specialist', 'performance-optimizer'}
        assert len(set(suggested_agents) & relevant_agents) >= 2
    
    def test_selection_statistics(self, selector):
        """Test selection statistics tracking."""
        # Make several selections
        test_queries = [
            "test failing",
            "docker issue",
            "security problem",
            "performance slow",
            "refactor code"
        ]
        
        for query in test_queries:
            selector.select_agent(query)
        
        stats = selector.get_selection_stats()
        
        assert 'total_selections' in stats
        assert stats['total_selections'] >= 5
        assert 'agent_distribution' in stats
        assert 'average_confidence' in stats
        assert 'average_processing_time_ms' in stats
        assert 0.0 <= stats['average_confidence'] <= 1.0
        assert stats['average_processing_time_ms'] >= 0.0
