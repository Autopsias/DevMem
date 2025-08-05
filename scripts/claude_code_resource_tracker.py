#!/usr/bin/env python3
"""
Claude Code Resource Tracker
Simple resource tracking to prevent system overload during coordination.
"""

import time
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class CoordinationStrategy(Enum):
    """Coordination strategy types."""

    DIRECT = "direct"
    BATCH_SMALL = "batch_small"
    BATCH_LARGE = "batch_large"
    SEQUENTIAL = "sequential"


@dataclass
class ResourceMetrics:
    """Resource usage metrics."""

    agent_count: int
    estimated_tokens: int
    estimated_duration: float
    strategy: CoordinationStrategy
    timestamp: float


class ClaudeCodeResourceTracker:
    """Simple resource tracking for Claude Code coordination."""

    def __init__(self):
        self.coordination_history: List[ResourceMetrics] = []
        self.current_coordinations: int = 0
        self.token_usage_history: List[Tuple[float, int]] = []

        # Claude Code limits and thresholds
        self.MAX_PARALLEL_AGENTS = 10  # Claude Code's documented limit
        self.BATCH_THRESHOLD = 6  # When to suggest batching
        self.TOKEN_WARNING_THRESHOLD = 8000  # Conservative token warning
        self.AVERAGE_TOKENS_PER_AGENT = 500  # Rough estimation

    def can_start_coordination(self, agent_count: int) -> Tuple[bool, str]:
        """
        Validate if coordination can start based on resource constraints.

        Args:
            agent_count: Number of agents to coordinate

        Returns:
            Tuple of (can_start, reason)
        """
        if agent_count <= 0:
            return False, "Invalid agent count"

        if agent_count > self.MAX_PARALLEL_AGENTS:
            return (
                False,
                f"Exceeds Claude Code limit of {self.MAX_PARALLEL_AGENTS} agents",
            )

        # Check current system load
        if self.current_coordinations > 0:
            return False, "Another coordination is already in progress"

        # Estimate token usage
        estimated_tokens = self._estimate_token_usage(agent_count)
        if estimated_tokens > self.TOKEN_WARNING_THRESHOLD:
            return (
                False,
                f"Estimated token usage ({estimated_tokens}) exceeds warning threshold",
            )

        return True, "Resource validation passed"

    def suggest_batching_strategy(self, agent_count: int) -> Dict[str, Any]:
        """
        Suggest batching strategy for large coordinations.

        Args:
            agent_count: Number of agents to coordinate

        Returns:
            Dictionary with strategy recommendations
        """
        if agent_count <= 2:
            return {
                "strategy": CoordinationStrategy.DIRECT,
                "description": "Direct coordination - single agent or simple pair",
                "batches": 1,
                "agents_per_batch": agent_count,
                "estimated_duration": self._estimate_duration(agent_count),
            }

        if agent_count <= 4:
            return {
                "strategy": CoordinationStrategy.BATCH_SMALL,
                "description": "Small batch coordination - optimal for Claude Code",
                "batches": 1,
                "agents_per_batch": agent_count,
                "estimated_duration": self._estimate_duration(agent_count),
            }

        if agent_count <= self.BATCH_THRESHOLD:
            return {
                "strategy": CoordinationStrategy.BATCH_LARGE,
                "description": "Large batch coordination - approaching limits",
                "batches": 1,
                "agents_per_batch": agent_count,
                "estimated_duration": self._estimate_duration(agent_count),
            }

        # For >6 agents, suggest batching
        optimal_batch_size = 4  # Research-validated from S1.1
        batches = (agent_count + optimal_batch_size - 1) // optimal_batch_size

        return {
            "strategy": CoordinationStrategy.SEQUENTIAL,
            "description": f"Sequential batching recommended - {batches} batches of ~{optimal_batch_size} agents",
            "batches": batches,
            "agents_per_batch": optimal_batch_size,
            "total_agents": agent_count,
            "estimated_duration": self._estimate_duration(agent_count)
            * batches
            * 0.8,  # Overlap factor
        }

    def _estimate_token_usage(self, agent_count: int) -> int:
        """Estimate token usage for coordination."""
        base_tokens = 200  # Context overhead
        agent_tokens = agent_count * self.AVERAGE_TOKENS_PER_AGENT
        coordination_overhead = min(agent_count * 50, 500)  # Coordination overhead

        return base_tokens + agent_tokens + coordination_overhead

    def _estimate_duration(self, agent_count: int) -> float:
        """Estimate coordination duration in seconds."""
        if agent_count <= 1:
            return 1.0
        elif agent_count <= 4:
            return 2.0 + (agent_count - 1) * 0.5
        else:
            return 4.0 + (agent_count - 4) * 0.3

    def log_coordination_performance(
        self,
        agent_count: int,
        actual_duration: float,
        strategy: CoordinationStrategy,
        tokens_used: Optional[int] = None,
    ) -> None:
        """
        Log coordination performance for learning.

        Args:
            agent_count: Number of agents used
            actual_duration: Actual time taken in seconds
            strategy: Strategy used for coordination
            tokens_used: Actual tokens used (if available)
        """
        estimated_tokens = tokens_used or self._estimate_token_usage(agent_count)

        metrics = ResourceMetrics(
            agent_count=agent_count,
            estimated_tokens=estimated_tokens,
            estimated_duration=actual_duration,
            strategy=strategy,
            timestamp=time.time(),
        )

        self.coordination_history.append(metrics)

        # Track token usage over time
        self.token_usage_history.append((time.time(), estimated_tokens))

        # Keep history manageable (last 100 entries)
        if len(self.coordination_history) > 100:
            self.coordination_history = self.coordination_history[-100:]

        if len(self.token_usage_history) > 100:
            self.token_usage_history = self.token_usage_history[-100:]

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for analysis."""
        if not self.coordination_history:
            return {"message": "No coordination history available"}

        recent_history = self.coordination_history[-20:]  # Last 20 coordinations

        avg_duration = sum(m.estimated_duration for m in recent_history) / len(
            recent_history
        )
        avg_agents = sum(m.agent_count for m in recent_history) / len(recent_history)
        avg_tokens = sum(m.estimated_tokens for m in recent_history) / len(
            recent_history
        )

        strategy_counts: Dict[str, int] = {}
        for metrics in recent_history:
            strategy = metrics.strategy.value
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1

        return {
            "total_coordinations": len(self.coordination_history),
            "recent_coordinations": len(recent_history),
            "average_duration": round(avg_duration, 2),
            "average_agents": round(avg_agents, 1),
            "average_tokens": round(avg_tokens),
            "strategy_distribution": strategy_counts,
            "max_agents_coordinated": max(
                m.agent_count for m in self.coordination_history
            ),
            "total_estimated_tokens": sum(
                m.estimated_tokens for m in self.coordination_history
            ),
        }

    def start_coordination(self) -> None:
        """Mark start of coordination."""
        self.current_coordinations += 1

    def end_coordination(self) -> None:
        """Mark end of coordination."""
        self.current_coordinations = max(0, self.current_coordinations - 1)


# Global instance for use across the system
resource_tracker = ClaudeCodeResourceTracker()


def main():
    """Example usage and testing."""
    tracker = ClaudeCodeResourceTracker()

    # Test scenarios
    test_cases = [2, 4, 6, 8, 12]

    print("Claude Code Resource Tracker - Test Results")
    print("=" * 50)

    for agent_count in test_cases:
        can_start, reason = tracker.can_start_coordination(agent_count)
        strategy = tracker.suggest_batching_strategy(agent_count)

        print(f"\nAgent Count: {agent_count}")
        print(f"Can Start: {can_start} - {reason}")
        print(f"Strategy: {strategy['strategy'].value}")
        print(f"Description: {strategy['description']}")
        if "batches" in strategy:
            print(f"Batches: {strategy['batches']}")
        print(f"Estimated Duration: {strategy['estimated_duration']:.1f}s")

    print("\nPerformance Summary:")
    print(tracker.get_performance_summary())


if __name__ == "__main__":
    main()
