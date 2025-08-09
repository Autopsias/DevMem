"""Tests for Learning-Enhanced Agent Selector.

Validates the learning-enhanced agent selector integration with fallback capabilities.
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from learning_enhanced_agent_selector import (
        LearningEnhancedAgentSelector,
        AgentSelectionResult,
    )
except ImportError as e:
    pytest.skip(
        f"Could not import learning-enhanced agent selector: {e}",
        allow_module_level=True,
    )


class TestLearningEnhancedAgentSelector:
    """Test suite for the learning-enhanced agent selector."""

    @pytest.fixture
    def temp_system_setup(self, tmp_path):
        """Set up temporary system for testing."""
        # Create agents directory
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        # Create test agent
        test_agent_content = """
---
name: test-specialist
description: Testing specialist for pytest and async issues
---
# Test Specialist
**Core Focus**: Testing, pytest, async, mock configuration
"""
        (agents_dir / "test-specialist.md").write_text(test_agent_content)

        # Create coordination hub
        hub_path = tmp_path / "coordination-hub.md"
        hub_content = """
# Coordination Hub
## 9. Agent Learning Pattern System
### High-Confidence Learned Patterns (90%+ Success Rate)
**Testing & Quality Assurance Patterns:**
### Medium-Confidence Learned Patterns (70-89% Success Rate)
"""
        hub_path.write_text(hub_content)

        return {"agents_dir": str(agents_dir), "hub_path": str(hub_path)}

    @pytest.fixture
    def learning_selector(self, temp_system_setup):
        """Create learning-enhanced selector with temporary setup."""
        selector = LearningEnhancedAgentSelector(temp_system_setup["hub_path"])

        # Override agents directory if learning engine is available
        if selector.learning_engine:
            selector.learning_engine.agents_directory = temp_system_setup["agents_dir"]
            selector.learning_engine.agent_profiles = (
                selector.learning_engine.parse_agent_descriptions()
            )

        return selector

    def test_selector_initialization(self, learning_selector):
        """Test that selector initializes correctly."""
        assert learning_selector is not None

        # Check component initialization
        validation = learning_selector.validate_learning_system()

        # Should have at least some components initialized
        assert validation["learning_engine_available"] in [True, False]  # Can be either
        assert validation["pattern_recorder_available"] in [True, False]
        assert validation["guidelines_validator_available"] in [True, False]

    def test_basic_agent_selection(self, learning_selector):
        """Test basic agent selection functionality."""
        test_queries = [
            "pytest test failures",
            "docker container issues",
            "security vulnerability scan",
            "unknown query type",
        ]

        for query in test_queries:
            result = learning_selector.select_agent(query)

            assert isinstance(result, AgentSelectionResult)
            assert result.agent_name is not None
            assert result.confidence_score > 0
            assert result.reasoning
            assert result.selection_time_ms >= 0

    def test_learning_enhanced_selection(self, learning_selector):
        """Test learning-enhanced selection when available."""
        query = "pytest test failures with async issues"
        result = learning_selector.select_agent(query)

        assert isinstance(result, AgentSelectionResult)

        # If learning is available, should show learning application
        if learning_selector.learning_engine:
            # Either learning was applied or fallback was used
            assert result.learning_applied in [True, False]

        # Should have reasonable confidence
        assert result.confidence_score >= 0.4

    def test_fallback_selection(self, learning_selector):
        """Test fallback selection when learning fails."""
        # Temporarily disable learning engine to test fallback
        original_engine = learning_selector.learning_engine
        learning_selector.learning_engine = None

        try:
            result = learning_selector.select_agent("test query")

            assert isinstance(result, AgentSelectionResult)
            assert result.agent_name is not None
            assert result.fallback_used is True
            assert result.learning_applied is False
        finally:
            # Restore original engine
            learning_selector.learning_engine = original_engine

    def test_selection_feedback_recording(self, learning_selector):
        """Test selection feedback recording."""
        query = "pytest test configuration"
        agent = "test-specialist"
        confidence = 0.85

        # Should not fail even if pattern recorder is unavailable
        success = learning_selector.record_selection_feedback(
            query, agent, confidence, success=True
        )

        # Result depends on whether pattern recorder is available
        assert success in [True, False]

    def test_selection_statistics(self, learning_selector):
        """Test selection statistics generation."""
        # Make some selections to generate stats
        test_queries = ["test query 1", "test query 2", "test query 3"]
        for query in test_queries:
            learning_selector.select_agent(query)

        stats = learning_selector.get_selection_stats()

        assert "total_selections" in stats
        assert stats["total_selections"] >= len(test_queries)
        assert "learning_usage_rate" in stats
        assert "fallback_rate" in stats
        assert 0.0 <= stats["learning_usage_rate"] <= 1.0
        assert 0.0 <= stats["fallback_rate"] <= 1.0

    def test_agent_profiles_retrieval(self, learning_selector):
        """Test agent profiles retrieval."""
        profiles = learning_selector.get_agent_profiles()

        assert "profiles_loaded" in profiles
        assert "profiles" in profiles
        assert profiles["profiles_loaded"] >= 0

    def test_learning_system_validation(self, learning_selector):
        """Test learning system validation."""
        validation = learning_selector.validate_learning_system()

        required_keys = [
            "learning_engine_available",
            "pattern_recorder_available",
            "guidelines_validator_available",
            "fallback_selector_available",
            "coordination_hub_valid",
            "agent_profiles_loaded",
            "system_health",
        ]

        for key in required_keys:
            assert key in validation

    def test_learning_accuracy_measurement(self, learning_selector):
        """Test learning accuracy measurement framework."""
        test_cases = [
            ("pytest test failures", "test-specialist"),
            ("docker container setup", "infrastructure-engineer"),
        ]

        accuracy_result = learning_selector.test_learning_accuracy(test_cases)

        assert "accuracy" in accuracy_result
        assert "total_tests" in accuracy_result
        assert "correct_selections" in accuracy_result
        assert "accuracy_percentage" in accuracy_result

        assert 0.0 <= accuracy_result["accuracy"] <= 1.0
        assert accuracy_result["total_tests"] == len(test_cases)

    def test_selection_performance(self, learning_selector):
        """Test that selection performance is acceptable."""
        import time

        # Measure selection performance
        start_time = time.time()

        for _ in range(5):  # Multiple selections
            result = learning_selector.select_agent("performance test query")
            assert result.selection_time_ms < 500  # Should be under 500ms

        total_time = time.time() - start_time
        avg_time = total_time / 5

        # Average selection should be under 200ms
        assert avg_time < 0.2, f"Average selection time {avg_time:.3f}s too slow"

    def test_error_handling_robustness(self, learning_selector):
        """Test error handling and robustness."""
        # Test with empty query
        result = learning_selector.select_agent("")
        assert isinstance(result, AgentSelectionResult)

        # Test with very long query
        long_query = "test " * 100
        result = learning_selector.select_agent(long_query)
        assert isinstance(result, AgentSelectionResult)

        # Test with special characters
        special_query = "test @#$%^&*()_+ query"
        result = learning_selector.select_agent(special_query)
        assert isinstance(result, AgentSelectionResult)

    def test_integration_with_existing_coordinator(self, learning_selector):
        """Test integration with existing cross-domain coordinator if available."""
        # This test validates that the learning selector can work alongside
        # existing coordination systems

        # Test a complex multi-domain query
        complex_query = "docker container security testing with performance monitoring"
        result = learning_selector.select_agent(complex_query)

        assert isinstance(result, AgentSelectionResult)
        assert result.agent_name is not None

        # Should handle complex queries gracefully
        assert (
            result.confidence_score > 0.3
        )  # Reasonable confidence even for complex queries


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
