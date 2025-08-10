import pytest
import time
import asyncio
from typing import Dict, Any, List
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.validation.performance_optimizer import PerformanceOptimizer
from src.validation.validator import ValidationFramework

class MockValidator:
    async def validate_pattern_execution(self, pattern: Dict[str, Any]) -> Any:
        await asyncio.sleep(0.025)  # Simulate processing
        return type('Result', (), {'success': True})()

class TestPerformanceOptimizer:
    @pytest.fixture
    def optimizer(self) -> PerformanceOptimizer:
        return PerformanceOptimizer()
    
    @pytest.fixture
    def validator(self) -> MockValidator:
        return MockValidator()

    @pytest.fixture
    def test_patterns(self) -> List[Dict[str, Any]]:
        return [
            {"type": pattern_type, "input": f"test_{i}"}
            for pattern_type in ["sequential", "parallel", "meta"]
            for i in range(10)
        ]

    async def test_parallel_validation_performance(
        self,
        optimizer: PerformanceOptimizer,
        validator: MockValidator,
        test_patterns: List[Dict[str, Any]]
    ):
        # Test with larger pattern set to demonstrate parallel advantage
        large_patterns = test_patterns * 10  # 100 patterns
        
        # Test sequential execution first
        optimizer.parallel_validations = False
        sequential_result = await optimizer.optimize_validation_execution(
            large_patterns,
            validator
        )
        
        # Reset cache and test parallel execution
        optimizer._validation_cache.clear()
        optimizer.parallel_validations = True
        parallel_result = await optimizer.optimize_validation_execution(
            large_patterns,
            validator
        )
        
        # Parallel should be faster
        assert parallel_result.execution_time < sequential_result.execution_time
        assert parallel_result.success_rate == 1.0
        assert sequential_result.success_rate == 1.0

    async def test_caching_performance(
        self,
        optimizer: PerformanceOptimizer,
        validator: MockValidator
    ):
        # First execution with empty cache
        patterns = [{"type": "sequential", "input": "test"}] * 5
        start_time = time.time()
        await optimizer.optimize_validation_execution(patterns, validator)
        first_execution = time.time() - start_time
        
        # Second execution with warm cache
        start_time = time.time()
        await optimizer.optimize_validation_execution(patterns, validator)
        second_execution = time.time() - start_time
        
        # Cached execution should be faster
        assert second_execution < first_execution
        
        # Check cache stats
        stats = optimizer.get_performance_stats()
        assert stats["cache_hit_ratio"] > 0.8

    async def test_batch_size_optimization(
        self,
        optimizer: PerformanceOptimizer,
        validator: MockValidator
    ):
        # Generate execution times that are too slow
        slow_times = [0.15] * 5  # 150ms per execution
        optimizer.optimize_batch_size(slow_times)
        assert optimizer.batch_size < 5  # Should reduce batch size
        
        # Generate execution times that are very fast
        fast_times = [0.02] * 5  # 20ms per execution
        optimizer.optimize_batch_size(fast_times)
        assert optimizer.batch_size > 1  # Should increase batch size

    async def test_resource_usage_tracking(
        self,
        optimizer: PerformanceOptimizer,
        validator: MockValidator,
        test_patterns: List[Dict[str, Any]]
    ):
        result = await optimizer.optimize_validation_execution(
            test_patterns,
            validator
        )
        
        # Check resource metrics
        assert "cache_size" in result.resource_usage
        assert "unique_patterns" in result.resource_usage
        
        # Validate resource usage ranges
        assert result.resource_usage["cache_size"] == len(test_patterns)
        assert result.resource_usage["unique_patterns"] == len(test_patterns)