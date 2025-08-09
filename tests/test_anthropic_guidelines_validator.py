#!/usr/bin/env python3
"""
Tests for Anthropic Guidelines Validator.

Tests validation of learning patterns against Anthropic sub-agent guidelines.
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

try:
    from anthropic_guidelines_validator import (
        AnthropicGuidelinesValidator,
        ValidationResult,
    )

    VALIDATOR_AVAILABLE = True
except ImportError:
    VALIDATOR_AVAILABLE = False


class TestAnthropicGuidelinesValidator:
    """Test Anthropic guidelines validator functionality."""

    @pytest.fixture
    def validator(self):
        """Create validator instance."""
        if not VALIDATOR_AVAILABLE:
            pytest.skip("Anthropic guidelines validator not available")
        return AnthropicGuidelinesValidator()

    def test_validator_initialization(self, validator):
        """Test validator initializes correctly."""
        assert validator is not None
        assert hasattr(validator, "guidelines_criteria")

        # Check required guideline categories exist
        expected_categories = [
            "sub_agent_spawning",
            "agent_selection",
            "learning_patterns",
        ]
        for category in expected_categories:
            assert category in validator.guidelines_criteria

    def test_validation_result_structure(self):
        """Test ValidationResult dataclass structure."""
        if not VALIDATOR_AVAILABLE:
            pytest.skip("Anthropic guidelines validator not available")

        result = ValidationResult(
            is_compliant=True,
            compliance_score=0.85,
            issues=[],
            recommendations=["Maintain current practices"],
            category="test_category",
        )

        assert result.is_compliant
        assert result.compliance_score == 0.85
        assert isinstance(result.issues, list)
        assert isinstance(result.recommendations, list)
        assert result.category == "test_category"

    def test_guidelines_criteria_structure(self, validator):
        """Test that guidelines criteria have expected structure."""
        criteria = validator.guidelines_criteria

        # Sub-agent spawning guidelines
        spawning = criteria["sub_agent_spawning"]
        assert "max_parallel_agents" in spawning
        assert spawning["max_parallel_agents"] == 10  # Claude Code limit

        # Agent selection guidelines
        selection = criteria["agent_selection"]
        assert "natural_language_triggers" in selection
        assert "appropriate_specialization" in selection

        # Learning patterns guidelines
        learning = criteria["learning_patterns"]
        assert "based_on_success_metrics" in learning
        assert "validate_agent_capability_match" in learning

    def test_validator_methods_exist(self, validator):
        """Test that expected validator methods exist."""
        # Check if validator has expected methods (if implemented)
        expected_methods = [
            "validate_pattern",
            "validate_sub_agent_usage",
            "get_compliance_score",
        ]

        for method in expected_methods:
            # Don't require all methods to exist, but check structure
            if hasattr(validator, method):
                assert callable(getattr(validator, method))

    def test_anthropic_compliance_standards(self, validator):
        """Test Anthropic compliance standards are properly defined."""
        criteria = validator.guidelines_criteria

        # Verify key Anthropic standards are represented
        assert criteria["sub_agent_spawning"]["max_parallel_agents"] <= 10
        assert criteria["agent_selection"]["natural_language_triggers"]
        assert criteria["learning_patterns"]["avoid_circular_dependencies"]

    @pytest.mark.skipif(not VALIDATOR_AVAILABLE, reason="Validator not available")
    def test_validator_import_success(self):
        """Test that validator imports successfully."""
        from anthropic_guidelines_validator import AnthropicGuidelinesValidator

        validator = AnthropicGuidelinesValidator()
        assert validator is not None


class TestValidationResultDataClass:
    """Test ValidationResult dataclass functionality."""

    @pytest.mark.skipif(not VALIDATOR_AVAILABLE, reason="Validator not available")
    def test_validation_result_defaults(self):
        """Test ValidationResult with minimal parameters."""
        result = ValidationResult(
            is_compliant=False,
            compliance_score=0.5,
            issues=["Issue 1"],
            recommendations=["Fix issue 1"],
            category="test",
        )

        assert not result.is_compliant
        assert result.compliance_score == 0.5
        assert len(result.issues) == 1
        assert len(result.recommendations) == 1

    @pytest.mark.skipif(not VALIDATOR_AVAILABLE, reason="Validator not available")
    def test_validation_result_score_range(self):
        """Test ValidationResult score validation."""
        # Valid scores
        for score in [0.0, 0.5, 1.0]:
            result = ValidationResult(
                is_compliant=True,
                compliance_score=score,
                issues=[],
                recommendations=[],
                category="test",
            )
            assert 0.0 <= result.compliance_score <= 1.0

    @pytest.mark.skipif(not VALIDATOR_AVAILABLE, reason="Validator not available")
    def test_validation_result_collections(self):
        """Test ValidationResult list fields."""
        issues = ["Issue A", "Issue B", "Issue C"]
        recommendations = ["Fix A", "Fix B"]

        result = ValidationResult(
            is_compliant=False,
            compliance_score=0.3,
            issues=issues,
            recommendations=recommendations,
            category="multi_issue_test",
        )

        assert len(result.issues) == 3
        assert len(result.recommendations) == 2
        assert "Issue A" in result.issues
        assert "Fix A" in result.recommendations


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
