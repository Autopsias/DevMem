#!/usr/bin/env python3
"""
Test suite for Claude Code Resource Tracker
"""

import pytest
import time
from unittest.mock import patch

from scripts.claude_code_resource_tracker import (
    ClaudeCodeResourceTracker,
    CoordinationStrategy,
    ResourceMetrics,
    resource_tracker,
)


class TestClaudeCodeResourceTracker:
    """Test cases for ClaudeCodeResourceTracker."""

    def setup_method(self):
        """Set up fresh tracker for each test."""
        self.tracker = ClaudeCodeResourceTracker()

    def test_initialization(self):
        """Test tracker initialization."""
        assert self.tracker.coordination_history == []
        assert self.tracker.current_coordinations == 0
        assert self.tracker.token_usage_history == []
        assert self.tracker.MAX_PARALLEL_AGENTS == 10
        assert self.tracker.BATCH_THRESHOLD == 6

    def test_can_start_coordination_valid_counts(self):
        """Test coordination validation with valid agent counts."""
        # Test valid small count
        can_start, reason = self.tracker.can_start_coordination(2)
        assert can_start is True
        assert "passed" in reason

        # Test valid medium count
        can_start, reason = self.tracker.can_start_coordination(5)
        assert can_start is True

        # Test valid large count
        can_start, reason = self.tracker.can_start_coordination(8)
        assert can_start is True

    def test_can_start_coordination_invalid_counts(self):
        """Test coordination validation with invalid agent counts."""
        # Test zero agents
        can_start, reason = self.tracker.can_start_coordination(0)
        assert can_start is False
        assert "Invalid" in reason

        # Test negative agents
        can_start, reason = self.tracker.can_start_coordination(-1)
        assert can_start is False
        assert "Invalid" in reason

        # Test exceeding limit
        can_start, reason = self.tracker.can_start_coordination(15)
        assert can_start is False
        assert "Exceeds Claude Code limit" in reason

    def test_can_start_coordination_concurrent_limit(self):
        """Test coordination validation with concurrent coordination."""
        # Start a coordination
        self.tracker.start_coordination()

        # Try to start another
        can_start, reason = self.tracker.can_start_coordination(3)
        assert can_start is False
        assert "already in progress" in reason

        # End coordination
        self.tracker.end_coordination()

        # Should work now
        can_start, reason = self.tracker.can_start_coordination(3)
        assert can_start is True

    def test_can_start_coordination_token_threshold(self):
        """Test coordination validation with token threshold."""
        # Mock high token usage
        with patch.object(self.tracker, "_estimate_token_usage", return_value=9000):
            can_start, reason = self.tracker.can_start_coordination(4)
            assert can_start is False
            assert "token usage" in reason and "exceeds warning threshold" in reason

    def test_suggest_batching_strategy_direct(self):
        """Test batching strategy for direct coordination."""
        strategy = self.tracker.suggest_batching_strategy(1)
        assert strategy["strategy"] == CoordinationStrategy.DIRECT
        assert strategy["batches"] == 1
        assert strategy["agents_per_batch"] == 1
        assert "Direct coordination" in strategy["description"]

        strategy = self.tracker.suggest_batching_strategy(2)
        assert strategy["strategy"] == CoordinationStrategy.DIRECT
        assert strategy["agents_per_batch"] == 2

    def test_suggest_batching_strategy_small_batch(self):
        """Test batching strategy for small batch coordination."""
        strategy = self.tracker.suggest_batching_strategy(3)
        assert strategy["strategy"] == CoordinationStrategy.BATCH_SMALL
        assert strategy["batches"] == 1
        assert strategy["agents_per_batch"] == 3
        assert "Small batch" in strategy["description"]

        strategy = self.tracker.suggest_batching_strategy(4)
        assert strategy["strategy"] == CoordinationStrategy.BATCH_SMALL
        assert strategy["agents_per_batch"] == 4

    def test_suggest_batching_strategy_large_batch(self):
        """Test batching strategy for large batch coordination."""
        strategy = self.tracker.suggest_batching_strategy(5)
        assert strategy["strategy"] == CoordinationStrategy.BATCH_LARGE
        assert strategy["batches"] == 1
        assert strategy["agents_per_batch"] == 5
        assert "Large batch" in strategy["description"]

        strategy = self.tracker.suggest_batching_strategy(6)
        assert strategy["strategy"] == CoordinationStrategy.BATCH_LARGE
        assert strategy["agents_per_batch"] == 6

    def test_suggest_batching_strategy_sequential(self):
        """Test batching strategy for sequential coordination."""
        # Test 8 agents (should suggest 2 batches of 4)
        strategy = self.tracker.suggest_batching_strategy(8)
        assert strategy["strategy"] == CoordinationStrategy.SEQUENTIAL
        assert strategy["batches"] == 2
        assert strategy["agents_per_batch"] == 4
        assert strategy["total_agents"] == 8
        assert "Sequential batching" in strategy["description"]

        # Test 10 agents (should suggest 3 batches of 4, with last batch having 2)
        strategy = self.tracker.suggest_batching_strategy(10)
        assert strategy["strategy"] == CoordinationStrategy.SEQUENTIAL
        assert strategy["batches"] == 3
        assert strategy["agents_per_batch"] == 4
        assert strategy["total_agents"] == 10

    def test_estimate_token_usage(self):
        """Test token usage estimation."""
        # Test small coordination
        tokens = self.tracker._estimate_token_usage(2)
        expected = 200 + (2 * 500) + (2 * 50)  # base + agents + overhead
        assert tokens == expected

        # Test larger coordination
        tokens = self.tracker._estimate_token_usage(8)
        expected = 200 + (8 * 500) + min(8 * 50, 500)  # Overhead capped at 500
        assert tokens == expected

    def test_estimate_duration(self):
        """Test duration estimation."""
        # Single agent
        duration = self.tracker._estimate_duration(1)
        assert duration == 1.0

        # Small batch
        duration = self.tracker._estimate_duration(3)
        expected = 2.0 + (3 - 1) * 0.5
        assert duration == expected

        # Large batch
        duration = self.tracker._estimate_duration(7)
        expected = 4.0 + (7 - 4) * 0.3
        assert duration == expected

    def test_log_coordination_performance(self):
        """Test coordination performance logging."""
        # Log a coordination
        self.tracker.log_coordination_performance(
            agent_count=4,
            actual_duration=2.5,
            strategy=CoordinationStrategy.BATCH_SMALL,
            tokens_used=1500,
        )

        assert len(self.tracker.coordination_history) == 1
        assert len(self.tracker.token_usage_history) == 1

        metrics = self.tracker.coordination_history[0]
        assert metrics.agent_count == 4
        assert metrics.estimated_duration == 2.5
        assert metrics.strategy == CoordinationStrategy.BATCH_SMALL
        assert metrics.estimated_tokens == 1500

        # Test without tokens_used (should estimate)
        self.tracker.log_coordination_performance(
            agent_count=2, actual_duration=1.5, strategy=CoordinationStrategy.DIRECT
        )

        assert len(self.tracker.coordination_history) == 2
        metrics = self.tracker.coordination_history[1]
        assert metrics.estimated_tokens == self.tracker._estimate_token_usage(2)

    def test_log_coordination_performance_history_limit(self):
        """Test coordination history size limit."""
        # Add 105 entries to test limit
        for i in range(105):
            self.tracker.log_coordination_performance(
                agent_count=2, actual_duration=1.0, strategy=CoordinationStrategy.DIRECT
            )

        # Should be limited to 100
        assert len(self.tracker.coordination_history) == 100
        assert len(self.tracker.token_usage_history) == 100

    def test_get_performance_summary_empty(self):
        """Test performance summary with no history."""
        summary = self.tracker.get_performance_summary()
        assert "No coordination history available" in summary["message"]

    def test_get_performance_summary_with_data(self):
        """Test performance summary with coordination data."""
        # Add some test data
        strategies = [
            CoordinationStrategy.DIRECT,
            CoordinationStrategy.BATCH_SMALL,
            CoordinationStrategy.DIRECT,
            CoordinationStrategy.BATCH_LARGE,
        ]

        for i, strategy in enumerate(strategies):
            self.tracker.log_coordination_performance(
                agent_count=i + 2,
                actual_duration=float(i + 1),
                strategy=strategy,
                tokens_used=(i + 1) * 500,
            )

        summary = self.tracker.get_performance_summary()

        assert summary["total_coordinations"] == 4
        assert summary["recent_coordinations"] == 4
        assert summary["average_duration"] > 0
        assert summary["average_agents"] > 0
        assert summary["average_tokens"] > 0
        assert "strategy_distribution" in summary
        assert (
            summary["max_agents_coordinated"] == 5
        )  # Last entry has agent_count=i+2 where i=3
        assert summary["total_estimated_tokens"] > 0

    def test_start_end_coordination(self):
        """Test coordination start/end tracking."""
        assert self.tracker.current_coordinations == 0

        self.tracker.start_coordination()
        assert self.tracker.current_coordinations == 1

        self.tracker.start_coordination()
        assert self.tracker.current_coordinations == 2

        self.tracker.end_coordination()
        assert self.tracker.current_coordinations == 1

        self.tracker.end_coordination()
        assert self.tracker.current_coordinations == 0

        # Should not go below 0
        self.tracker.end_coordination()
        assert self.tracker.current_coordinations == 0

    def test_global_resource_tracker_instance(self):
        """Test global resource tracker instance."""
        assert resource_tracker is not None
        assert isinstance(resource_tracker, ClaudeCodeResourceTracker)


class TestResourceMetrics:
    """Test ResourceMetrics dataclass."""

    def test_resource_metrics_creation(self):
        """Test ResourceMetrics creation."""
        timestamp = time.time()
        metrics = ResourceMetrics(
            agent_count=4,
            estimated_tokens=2000,
            estimated_duration=2.5,
            strategy=CoordinationStrategy.BATCH_SMALL,
            timestamp=timestamp,
        )

        assert metrics.agent_count == 4
        assert metrics.estimated_tokens == 2000
        assert metrics.estimated_duration == 2.5
        assert metrics.strategy == CoordinationStrategy.BATCH_SMALL
        assert metrics.timestamp == timestamp


class TestCoordinationStrategy:
    """Test CoordinationStrategy enum."""

    def test_coordination_strategy_values(self):
        """Test CoordinationStrategy enum values."""
        assert CoordinationStrategy.DIRECT.value == "direct"
        assert CoordinationStrategy.BATCH_SMALL.value == "batch_small"
        assert CoordinationStrategy.BATCH_LARGE.value == "batch_large"
        assert CoordinationStrategy.SEQUENTIAL.value == "sequential"


class TestIntegrationScenarios:
    """Integration test scenarios."""

    def setup_method(self):
        """Set up fresh tracker for each test."""
        self.tracker = ClaudeCodeResourceTracker()

    def test_full_coordination_workflow(self):
        """Test complete coordination workflow."""
        agent_count = 4

        # 1. Check if coordination can start
        can_start, reason = self.tracker.can_start_coordination(agent_count)
        assert can_start is True

        # 2. Get batching strategy
        strategy = self.tracker.suggest_batching_strategy(agent_count)
        assert strategy["strategy"] == CoordinationStrategy.BATCH_SMALL

        # 3. Start coordination
        self.tracker.start_coordination()

        # 4. Simulate coordination execution
        start_time = time.time()
        time.sleep(0.01)  # Minimal sleep for realistic duration
        end_time = time.time()
        actual_duration = end_time - start_time

        # 5. Log performance
        self.tracker.log_coordination_performance(
            agent_count=agent_count,
            actual_duration=actual_duration,
            strategy=strategy["strategy"],
            tokens_used=1800,
        )

        # 6. End coordination
        self.tracker.end_coordination()

        # 7. Verify results
        assert len(self.tracker.coordination_history) == 1
        summary = self.tracker.get_performance_summary()
        assert summary["total_coordinations"] == 1
        assert summary["max_agents_coordinated"] == agent_count

    def test_batching_recommendation_accuracy(self):
        """Test batching recommendation accuracy for various scenarios."""
        test_cases = [
            (2, CoordinationStrategy.DIRECT, 1),
            (4, CoordinationStrategy.BATCH_SMALL, 1),
            (6, CoordinationStrategy.BATCH_LARGE, 1),
            (8, CoordinationStrategy.SEQUENTIAL, 2),
            (12, CoordinationStrategy.SEQUENTIAL, 3),
        ]

        for agent_count, expected_strategy, expected_batches in test_cases:
            strategy = self.tracker.suggest_batching_strategy(agent_count)
            assert strategy["strategy"] == expected_strategy
            assert strategy["batches"] == expected_batches

    def test_resource_validation_edge_cases(self):
        """Test resource validation edge cases."""
        # Test exact limit
        can_start, reason = self.tracker.can_start_coordination(10)
        assert can_start is True

        # Test just over limit
        can_start, reason = self.tracker.can_start_coordination(11)
        assert can_start is False

        # Test token threshold boundary
        with patch.object(self.tracker, "_estimate_token_usage", return_value=8000):
            can_start, reason = self.tracker.can_start_coordination(4)
            assert can_start is True  # Exactly at threshold

        with patch.object(self.tracker, "_estimate_token_usage", return_value=8001):
            can_start, reason = self.tracker.can_start_coordination(4)
            assert can_start is False  # Over threshold


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
