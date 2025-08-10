import pytest
from pathlib import Path
import sys
from typing import Dict, List, Type, Optional
import asyncio
from unittest.mock import Mock, patch

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.patterns.base import PatternBase
from src.validation.validator import ValidationFramework
from src.patterns.sequential import SequentialPattern
from src.patterns.parallel import ParallelPattern
from src.patterns.meta import MetaOrchestrationPattern

class TestComprehensiveValidation:
    @pytest.fixture
    def validation_framework(self) -> ValidationFramework:
        return ValidationFramework()
    
    @pytest.fixture
    def pattern_registry(self) -> Dict[str, Type[PatternBase]]:
        return {
            "sequential": SequentialPattern,
            "parallel": ParallelPattern,
            "meta": MetaOrchestrationPattern
        }

    async def test_edge_case_pattern_execution(self, validation_framework: ValidationFramework):
        edge_cases = [
            ("empty_input", {"type": "sequential", "input": ""}),
            ("special_chars", {"type": "sequential", "input": "!@#$%^&*()"}),
            ("unicode", {"type": "sequential", "input": "测试"}),
            ("json_input", {"type": "sequential", "input": {"key": "value"}}),
            ("list_input", {"type": "sequential", "input": [1, 2, 3]}),
            ("boolean_input", {"type": "sequential", "input": True})
        ]
        
        for case_name, case_input in edge_cases:
            result = await validation_framework.validate_pattern_execution(case_input)
            assert result.success, f"Edge case {case_name} failed"
            assert result.errors == [], f"Edge case {case_name} had errors"

    async def test_concurrent_pattern_execution(self, validation_framework: ValidationFramework):
        num_concurrent = 25  # Match production requirement
        pattern_inputs = [{"type": "sequential", "input": f"test{i}"} for i in range(num_concurrent)]
        
        async def execute_pattern(input_data: Dict) -> bool:
            result = await validation_framework.validate_pattern_execution(input_data)
            return result.success

        tasks = [execute_pattern(input_data) for input_data in pattern_inputs]
        results = await asyncio.gather(*tasks)
        
        assert all(results), "Not all concurrent executions succeeded"
        assert len(results) == num_concurrent, "Not all patterns executed"

    async def test_cross_environment_consistency(
        self, 
        validation_framework: ValidationFramework,
        pattern_registry: Dict[str, Type[PatternBase]]
    ):
        environments = ["dev", "staging", "production"]
        test_pattern = {"type": "sequential", "input": "test_input"}
        
        results = {}
        for env in environments:
            validation_framework.set_environment(env)
            result = await validation_framework.validate_pattern_execution(test_pattern)
            results[env] = result

        base_result = results["dev"]
        for env in ["staging", "production"]:
            assert results[env].success == base_result.success, f"Inconsistent results in {env}"
            assert results[env].confidence == base_result.confidence, f"Confidence mismatch in {env}"

    def test_pattern_failure_conditions(self, validation_framework: ValidationFramework):
        failure_cases = [
            ("invalid_type", {"type": "nonexistent"}),
            ("missing_input", {}),
            ("invalid_format", "not_a_dict"),
            # Security test cases
            ("dangerous_pattern", {"type": "sequential", "input": "dangerous command"}),
            ("none_input", {"type": "sequential", "input": None}),
            ("oversized_input", {"type": "sequential", "input": "x" * 1100000})
        ]
        
        for case_name, case_input in failure_cases:
            with pytest.raises(ValueError) as exc:
                validation_framework.validate_pattern_structure(case_input)
            assert str(exc.value), f"No error message for {case_name}"
        
        
        for case_name, case_input in failure_cases:
            with pytest.raises(Exception) as exc:
                validation_framework.validate_pattern_structure(case_input)
            assert str(exc.value), f"No error message for {case_name}"

    async def test_statistical_confidence_scoring(self, validation_framework: ValidationFramework):
        executions = 100
        pattern_input = {"type": "sequential", "input": "test"}
        confidences = []
        
        for _ in range(executions):
            result = await validation_framework.validate_pattern_execution(pattern_input)
            confidences.append(result.confidence)
        
        avg_confidence = sum(confidences) / len(confidences)
        confidence_variance = sum((c - avg_confidence) ** 2 for c in confidences) / len(confidences)
        
        assert avg_confidence >= 0.85, "Average confidence below production threshold"
        assert confidence_variance <= 0.02, "Confidence variance exceeds stability threshold"

    async def test_regression_detection(self, validation_framework: ValidationFramework):
        baseline_results = [0.95, 0.94, 0.96, 0.95, 0.93]  # Historical baseline
        degraded_results = [0.89, 0.88, 0.87, 0.89, 0.88]  # Simulated 5%+ degradation
        
        degradation = validation_framework.detect_regression(degraded_results, baseline_results)
        assert degradation >= 0.05, "Failed to detect significant regression"
        
        with pytest.raises(Exception) as exc:
            validation_framework.validate_no_regression(degraded_results, baseline_results)
        assert "Performance regression detected" in str(exc.value)