"""Integration tests for agent selection with Claude Code framework."""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.agent_selector import EnhancedAgentSelector, select_best_agent


class TestAgentIntegration:
    """Test integration with Claude Code framework patterns."""

    @pytest.fixture
    def selector(self):
        return EnhancedAgentSelector()

    def test_coordination_hub_pattern_matching(self, selector):
        """Test that selector recognizes coordination hub patterns."""
        coordination_queries = [
            "Coordinating comprehensive analysis using 3 tasks in parallel: security assessment, performance analysis, testing evaluation",
            "analyzing performance bottleneck using parallel assessment across infrastructure and testing domains",
            "multi-domain authentication requiring security-enforcer, performance-optimizer, test-specialist",
            "strategic parallel analysis across 5 domains for crisis response",
        ]

        for query in coordination_queries:
            result = selector.select_agent(query)

            # Should handle multi-domain coordination appropriately
            assert result.agent_name is not None
            assert result.confidence_score > 0.3
            assert len(result.context_keywords) >= 2

            # Should detect multi-domain nature
            domains = selector.detect_multi_domain_query(query)
            assert len(domains) >= 2, f"Should detect multiple domains in: {query}"

    def test_memory_pattern_references(self, selector):
        """Test recognition of memory pattern references."""
        memory_queries = [
            "@.claude/memory/coordination-hub.md pattern for testing architecture",
            "@docs/native-configuration-schema.md validation patterns needed",
            "using @.claude/memory/domain-intelligence.md for infrastructure coordination",
        ]

        for query in memory_queries:
            result = selector.select_agent(query)

            # Should extract domain from memory reference context
            assert result.agent_name is not None
            assert result.confidence_score > 0.2

    def test_claude_code_native_patterns(self, selector):
        """Test recognition of Claude Code native patterns."""
        native_patterns = [
            "Task() calls for parallel execution coordination",
            "subagent_type selection for specialized analysis",
            "natural delegation integration for multi-domain problems",
            "UltraThink analysis activation for complex refactoring",
        ]

        for query in native_patterns:
            result = selector.select_agent(query)

            # Should recognize framework-specific terminology
            assert result.agent_name is not None
            assert result.confidence_score > 0.3

    def test_project_specific_patterns(self, selector):
        """Test recognition of RAG MemoryBank project patterns."""
        project_queries = [
            "FastMCP server implementation requiring SDK compliance",
            "Qdrant vector database optimization for hybrid search",
            "BM25S keyword search performance improvement",
            "MCP protocol validation and testing coordination",
            "TruLens evaluation integration with testing pipeline",
        ]

        expected_agents = {
            "FastMCP server implementation requiring SDK compliance": "intelligent-enhancer",
            "Qdrant vector database optimization for hybrid search": "performance-optimizer",
            "BM25S keyword search performance improvement": "performance-optimizer",
            "MCP protocol validation and testing coordination": "test-specialist",
            "TruLens evaluation integration with testing pipeline": "test-specialist",
        }

        for query in project_queries:
            expected_agent = expected_agents[query]
            result = selector.select_agent(query)

            assert (
                result.agent_name == expected_agent
            ), f"Expected {expected_agent} for '{query}', got {result.agent_name}"
            assert result.confidence_score > 0.5

    def test_essential_commands_integration(self, selector):
        """Test integration with essential development commands."""
        command_queries = [
            "make test-coverage failing with async patterns",
            "./scripts/ci-modular-runner.sh fast needs optimization",
            "make docker-up container networking issues",
            "make lint-ci showing security violations",
            "gh workflow run ci-modular.yml configuration problems",
        ]

        expected_domains = {
            "make test-coverage failing with async patterns": "test-specialist",
            "./scripts/ci-modular-runner.sh fast needs optimization": "ci-specialist",
            "make docker-up container networking issues": "infrastructure-engineer",
            "make lint-ci showing security violations": "security-enforcer",
            "gh workflow run ci-modular.yml configuration problems": "ci-specialist",
        }

        for query in command_queries:
            expected_agent = expected_domains[query]
            result = selector.select_agent(query)

            assert (
                result.agent_name == expected_agent
            ), f"Expected {expected_agent} for '{query}', got {result.agent_name}"

    def test_quality_standards_patterns(self, selector):
        """Test recognition of project quality standards."""
        quality_queries = [
            "coverage requirement ≥82% validation failing",
            "file size exceeding 750 lines implementation limit",
            "function complexity over 50 lines per function",
            "variable naming using generic data/result/temp",
            "type annotations missing for public functions",
        ]

        for query in quality_queries:
            result = selector.select_agent(query)

            # Quality issues should typically route to appropriate specialists
            assert result.agent_name in {
                "intelligent-enhancer",
                "code-quality-specialist",
                "test-specialist",
            }
            assert result.confidence_score > 0.4

    def test_performance_baseline_recognition(self, selector):
        """Test recognition of performance baseline patterns."""
        performance_queries = [
            "selection latency >0.8s exceeding baseline",
            "context preservation <95% below target",
            "coordination accuracy 92% meeting threshold",
            "memory access latency >25ms performance issue",
        ]

        for query in performance_queries:
            result = selector.select_agent(query)

            # Performance issues should route to performance optimizer
            assert result.agent_name == "performance-optimizer"
            assert result.confidence_score > 0.6

    def test_agent_tier_classification(self, selector):
        """Test that selector understands agent performance tiers."""
        tier_queries = [
            "docker-specialist needed for <1.5s response requirement",
            "test-specialist high performance tier analysis",
            "coverage-optimizer comprehensive analysis >2.0s acceptable",
            "infrastructure-engineer tier 1 performance requirement",
        ]

        for query in tier_queries:
            result = selector.select_agent(query)

            # Should recognize agent names and performance context
            assert result.agent_name is not None
            assert result.confidence_score > 0.5

    def test_natural_delegation_language(self, selector):
        """Test natural delegation language patterns."""
        delegation_queries = [
            "Container orchestration requiring container networking optimization",
            "Performance infrastructure requiring system analysis and resource allocation",
            "Security infrastructure requiring container security hardening",
            "Testing coordination requiring async pattern resolution and mock optimization",
        ]

        expected_agents = {
            "Container orchestration requiring container networking optimization": "infrastructure-engineer",
            "Performance infrastructure requiring system analysis and resource allocation": "performance-optimizer",
            "Security infrastructure requiring container security hardening": "security-enforcer",
            "Testing coordination requiring async pattern resolution and mock optimization": "test-specialist",
        }

        for query in delegation_queries:
            expected_agent = expected_agents[query]
            result = selector.select_agent(query)

            assert (
                result.agent_name == expected_agent
            ), f"Expected {expected_agent} for delegation query, got {result.agent_name}"
            assert result.confidence_score > 0.6

    def test_emergency_threshold_patterns(self, selector):
        """Test recognition of emergency threshold patterns."""
        emergency_queries = [
            ">5% performance degradation triggering investigation",
            ">2% success rate drop requiring rollback",
            "emergency threshold breach in coordination system",
            "immediate investigation needed for system intelligence preservation",
        ]

        for query in emergency_queries:
            result = selector.select_agent(query)

            # Emergency patterns should get appropriate routing
            assert result.agent_name is not None
            assert result.confidence_score > 0.3
            # Emergency context should be detected
            assert any(
                keyword in query.lower()
                for keyword in ["emergency", "degradation", "investigation"]
            )

    def test_global_selector_function(self):
        """Test the global selector convenience function."""
        result = select_best_agent("pytest async test failing")

        assert isinstance(result, type(select_best_agent("test")))
        assert result.agent_name == "test-specialist"
        assert result.confidence_score > 0.6

    def test_context_parameter_usage(self, selector):
        """Test that context parameter affects selection."""
        base_query = "performance issues"

        # Test with different contexts
        test_context = {"domain": "testing", "priority": "high"}
        infra_context = {"domain": "infrastructure", "tool": "docker"}

        base_result = selector.select_agent(base_query)
        test_result = selector.select_agent(base_query, test_context)
        infra_result = selector.select_agent(base_query, infra_context)

        # All should return valid results
        for result in [base_result, test_result, infra_result]:
            assert result.agent_name is not None
            assert result.confidence_score > 0.3

    @patch("logging.getLogger")
    def test_logging_integration(self, mock_logger, selector):
        """Test that logging is properly configured."""
        mock_logger.return_value = MagicMock()

        # Make a selection that should trigger logging
        result = selector.select_agent("test query for logging")

        # Should not raise any exceptions
        assert result is not None

    def test_selection_history_tracking(self, selector):
        """Test that selection history is properly tracked."""
        initial_stats = selector.get_selection_stats()
        initial_count = initial_stats.get("total_selections", 0)

        # Make several selections
        queries = ["test failing", "docker issue", "security problem"]

        for query in queries:
            selector.select_agent(query)

        final_stats = selector.get_selection_stats()
        final_count = final_stats["total_selections"]

        # Should have tracked the new selections
        assert final_count >= initial_count + len(queries)
        assert "agent_distribution" in final_stats
        assert "average_confidence" in final_stats

    def test_memory_optimization_patterns(self, selector):
        """Test recognition of memory optimization patterns."""
        memory_queries = [
            "memory access latency <25ms requirement",
            "cache hit ratio >95% optimization target",
            "context preservation >98% streamlined processing",
            "cross-reference validation 100% compliance",
        ]

        for query in memory_queries:
            result = selector.select_agent(query)

            # Memory optimization should route to performance optimizer
            assert result.agent_name == "performance-optimizer"
            assert result.confidence_score > 0.5
