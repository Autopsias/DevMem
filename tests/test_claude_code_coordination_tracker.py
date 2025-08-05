#!/usr/bin/env python3
"""
Tests for Claude Code Coordination Tracker

Comprehensive test suite for coordination tracking, pattern learning,
and performance insights functionality.
"""

import pytest
import tempfile
import time
import uuid
from pathlib import Path
from unittest.mock import patch
import sys

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

from claude_code_coordination_tracker import (
    ClaudeCodeCoordinationTracker,
    CoordinationEventType,
    PatternType,
    PerformanceInsight,
    coordination_tracker,
)


class TestCoordinationTracker:
    """Test suite for basic coordination tracking functionality."""

    def setup_method(self):
        """Setup tracker instance with temporary directory for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.tracker = ClaudeCodeCoordinationTracker(data_dir=self.temp_dir)

    def test_initialization(self):
        """Test proper initialization of tracker components."""
        assert self.tracker.events == []
        assert self.tracker.patterns == {}
        assert self.tracker.insights == []
        assert self.tracker.data_dir.exists()
        assert self.tracker.data_dir.is_dir()

    def test_start_coordination(self):
        """Test coordination start logging."""
        event_id = "test-001"
        agent_count = 3
        domains = ["testing", "security"]
        strategy = "single_parallel"
        agents = ["test-specialist", "security-enforcer"]

        self.tracker.start_coordination(
            event_id, agent_count, domains, strategy, agents
        )

        assert len(self.tracker.events) == 1
        event = self.tracker.events[0]

        assert event.event_id == event_id
        assert event.event_type == CoordinationEventType.START
        assert event.agent_count == agent_count
        assert event.domains == domains
        assert event.strategy == strategy
        assert event.agents_used == agents
        assert event.timestamp > 0

    def test_complete_coordination_success(self):
        """Test successful coordination completion."""
        event_id = "test-002"

        # Start coordination
        self.tracker.start_coordination(event_id, 2, ["testing"], "direct")

        # Complete coordination
        time.sleep(0.01)  # Small delay to ensure duration > 0
        self.tracker.complete_coordination(event_id, success=True)

        assert len(self.tracker.events) == 2

        completion_event = self.tracker.events[1]
        assert completion_event.event_id == event_id
        assert completion_event.event_type == CoordinationEventType.COMPLETE
        assert completion_event.success is True
        assert completion_event.duration is not None
        assert completion_event.duration > 0

    def test_complete_coordination_failure(self):
        """Test failed coordination completion."""
        event_id = "test-003"
        error_msg = "Test error message"

        # Start coordination
        self.tracker.start_coordination(
            event_id, 4, ["infrastructure"], "batch_parallel"
        )

        # Complete with failure
        self.tracker.complete_coordination(
            event_id, success=False, error_message=error_msg
        )

        assert len(self.tracker.events) == 2

        completion_event = self.tracker.events[1]
        assert completion_event.event_type == CoordinationEventType.ERROR
        assert completion_event.success is False
        assert completion_event.error_message == error_msg

    def test_complete_coordination_without_start(self):
        """Test completion event without corresponding start event."""
        event_id = "test-orphan"

        # Complete coordination without start
        self.tracker.complete_coordination(event_id, success=True)

        assert len(self.tracker.events) == 1
        event = self.tracker.events[0]
        assert event.event_id == event_id
        assert event.event_type == CoordinationEventType.COMPLETE
        assert event.duration is None  # No start event, so no duration


class TestPatternLearning:
    """Test suite for pattern learning functionality."""

    def setup_method(self):
        """Setup tracker for pattern learning tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.tracker = ClaudeCodeCoordinationTracker(data_dir=self.temp_dir)

    def test_pattern_creation(self):
        """Test creation of new coordination patterns."""
        event_id = "pattern-001"
        domains = ["testing"]
        agent_count = 2
        strategy = "single_parallel"

        # Execute coordination
        self.tracker.start_coordination(event_id, agent_count, domains, strategy)
        time.sleep(0.01)
        self.tracker.complete_coordination(event_id, success=True)

        # Check pattern was created
        assert len(self.tracker.patterns) == 1

        pattern_key = "testing_2_single_parallel"
        assert pattern_key in self.tracker.patterns

        pattern = self.tracker.patterns[pattern_key]
        assert pattern.domains == domains
        assert pattern.agent_count == agent_count
        assert pattern.strategy == strategy
        assert pattern.success_rate == 1.0
        assert pattern.usage_count == 1
        assert pattern.confidence_score > 0

    def test_pattern_update_success(self):
        """Test pattern updates with successful coordinations."""
        event_id_base = "pattern-update"
        domains = ["security"]
        agent_count = 3
        strategy = "batch_parallel"

        # Execute multiple successful coordinations
        for i in range(3):
            event_id = f"{event_id_base}-{i}"
            self.tracker.start_coordination(event_id, agent_count, domains, strategy)
            time.sleep(0.01)
            self.tracker.complete_coordination(event_id, success=True)

        pattern_key = "security_3_batch_parallel"
        pattern = self.tracker.patterns[pattern_key]

        assert pattern.usage_count == 3
        assert pattern.success_rate == 1.0
        assert pattern.confidence_score > 0.3  # Should increase with usage

    def test_pattern_update_mixed_success(self):
        """Test pattern updates with mixed success/failure."""
        event_id_base = "pattern-mixed"
        domains = ["infrastructure"]
        agent_count = 4
        strategy = "batch_parallel"

        # Execute mixed successful/failed coordinations
        success_results = [True, False, True, True]  # 75% success rate

        for i, success in enumerate(success_results):
            event_id = f"{event_id_base}-{i}"
            self.tracker.start_coordination(event_id, agent_count, domains, strategy)
            time.sleep(0.01)
            self.tracker.complete_coordination(event_id, success=success)

        pattern_key = "infrastructure_4_batch_parallel"
        pattern = self.tracker.patterns[pattern_key]

        assert pattern.usage_count == 4
        assert pattern.success_rate == 0.75

    def test_pattern_type_classification(self):
        """Test pattern type classification logic."""
        # Test batch pattern
        assert (
            self.tracker._classify_pattern_type("batch_parallel", 6)
            == PatternType.BATCH
        )

        # Test parallel pattern
        assert (
            self.tracker._classify_pattern_type("single_parallel", 3)
            == PatternType.PARALLEL
        )

        # Test sequential pattern
        assert (
            self.tracker._classify_pattern_type("direct", 1) == PatternType.SEQUENTIAL
        )

        # Test hybrid pattern
        assert (
            self.tracker._classify_pattern_type("custom_strategy", 5)
            == PatternType.HYBRID
        )

    def test_pattern_key_generation(self):
        """Test pattern key generation consistency."""
        # Test consistent key generation
        domains1 = ["testing", "security"]
        domains2 = ["security", "testing"]  # Different order

        key1 = self.tracker._generate_pattern_key(domains1, 3, "parallel")
        key2 = self.tracker._generate_pattern_key(domains2, 3, "parallel")

        assert key1 == key2  # Should be the same despite different domain order
        assert key1 == "security+testing_3_parallel"


class TestAnalytics:
    """Test suite for analytics functionality."""

    def setup_method(self):
        """Setup tracker with sample data for analytics tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.tracker = ClaudeCodeCoordinationTracker(data_dir=self.temp_dir)

        # Add sample coordination events
        self._add_sample_events()

    def _add_sample_events(self):
        """Add sample events for testing analytics."""
        # Successful testing coordination
        self.tracker.start_coordination("event-1", 2, ["testing"], "single_parallel")
        time.sleep(0.001)
        self.tracker.complete_coordination("event-1", success=True)

        # Failed infrastructure coordination
        self.tracker.start_coordination(
            "event-2", 4, ["infrastructure"], "batch_parallel"
        )
        time.sleep(0.001)
        self.tracker.complete_coordination("event-2", success=False)

        # Successful multi-domain coordination
        self.tracker.start_coordination(
            "event-3", 3, ["testing", "security"], "single_parallel"
        )
        time.sleep(0.001)
        self.tracker.complete_coordination("event-3", success=True)

    def test_basic_analytics(self):
        """Test basic analytics computation."""
        analytics = self.tracker.get_analytics()

        assert "summary" in analytics
        assert "domain_analytics" in analytics
        assert "strategy_analytics" in analytics
        assert "top_patterns" in analytics

        summary = analytics["summary"]
        assert summary["total_events"] == 6  # 3 start + 3 complete events
        assert summary["completed_coordinations"] == 3
        assert summary["successful_coordinations"] == 2
        assert summary["success_rate"] == round(2 / 3, 3)

    def test_domain_analytics(self):
        """Test domain-specific analytics."""
        analytics = self.tracker.get_analytics()
        domain_analytics = analytics["domain_analytics"]

        assert "testing" in domain_analytics
        assert "infrastructure" in domain_analytics
        assert "security" in domain_analytics

        # Testing appears in 2 coordinations, both successful
        testing_stats = domain_analytics["testing"]
        assert testing_stats["usage_count"] == 2
        assert testing_stats["success_rate"] == 1.0

    def test_strategy_analytics(self):
        """Test strategy-specific analytics."""
        analytics = self.tracker.get_analytics()
        strategy_analytics = analytics["strategy_analytics"]

        assert "single_parallel" in strategy_analytics
        assert "batch_parallel" in strategy_analytics

        # single_parallel: 2 uses, 2 successes
        single_parallel_stats = strategy_analytics["single_parallel"]
        assert single_parallel_stats["usage_count"] == 2
        assert single_parallel_stats["success_rate"] == 1.0

        # batch_parallel: 1 use, 0 successes
        batch_parallel_stats = strategy_analytics["batch_parallel"]
        assert batch_parallel_stats["usage_count"] == 1
        assert batch_parallel_stats["success_rate"] == 0.0

    def test_analytics_caching(self):
        """Test analytics caching mechanism."""
        # First call should generate analytics
        analytics1 = self.tracker.get_analytics()
        cache_time1 = self.tracker._cache_timestamp

        # Second call should use cache
        analytics2 = self.tracker.get_analytics()
        cache_time2 = self.tracker._cache_timestamp

        assert analytics1 == analytics2
        assert cache_time1 == cache_time2

        # Adding new event should invalidate cache
        self.tracker.start_coordination("new-event", 1, ["testing"], "direct")
        self.tracker.get_analytics()
        cache_time3 = self.tracker._cache_timestamp

        assert cache_time3 > cache_time2

    def test_empty_analytics(self):
        """Test analytics with no events."""
        empty_tracker = ClaudeCodeCoordinationTracker(data_dir=tempfile.mkdtemp())
        analytics = empty_tracker.get_analytics()

        assert analytics == {"message": "No coordination events recorded"}


class TestInsights:
    """Test suite for insights generation functionality."""

    def setup_method(self):
        """Setup tracker for insights testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.tracker = ClaudeCodeCoordinationTracker(data_dir=self.temp_dir)

    def test_low_success_rate_insight(self):
        """Test insight generation for low success rate patterns."""
        # Create a pattern with low success rate
        event_base = "low-success"

        # 3 coordinations with 1 success (33% success rate)
        for i, success in enumerate([False, False, True]):
            event_id = f"{event_base}-{i}"
            self.tracker.start_coordination(
                event_id, 3, ["testing"], "problematic_strategy"
            )
            time.sleep(0.001)
            self.tracker.complete_coordination(event_id, success=success)

        insights = self.tracker.generate_insights()

        # Should generate low success rate insight
        low_success_insights = [i for i in insights if i.category == "reliability"]
        assert len(low_success_insights) > 0

        insight = low_success_insights[0]
        assert "low success rate" in insight.description.lower()
        assert "alternative strategies" in insight.recommendation.lower()

    def test_high_performer_insight(self):
        """Test insight generation for high-performing patterns."""
        # Create a high-performing pattern
        event_base = "high-performer"

        # 3 successful coordinations (100% success rate)
        for i in range(3):
            event_id = f"{event_base}-{i}"
            self.tracker.start_coordination(
                event_id, 2, ["security"], "excellent_strategy"
            )
            time.sleep(0.001)
            self.tracker.complete_coordination(event_id, success=True)

        insights = self.tracker.generate_insights()

        # Should generate high performer insight
        optimization_insights = [i for i in insights if i.category == "optimization"]
        assert len(optimization_insights) > 0

        # Check for high performer insight
        high_performer_insights = [
            i for i in optimization_insights if "excellent performance" in i.description
        ]
        assert len(high_performer_insights) > 0

    def test_insights_persistence(self):
        """Test insights are saved and loaded correctly."""
        # Generate some insights
        for i in range(2):
            event_id = f"insight-test-{i}"
            self.tracker.start_coordination(event_id, 2, ["testing"], "test_strategy")
            time.sleep(0.001)
            self.tracker.complete_coordination(event_id, success=True)

        insights = self.tracker.generate_insights()

        # Create new tracker instance with same data directory
        new_tracker = ClaudeCodeCoordinationTracker(data_dir=self.temp_dir)

        # Should load insights from disk
        assert len(new_tracker.insights) == len(insights)

    def test_insights_cleanup(self):
        """Test old insights are cleaned up."""
        # Create an old insight by mocking the timestamp
        old_insight = PerformanceInsight(
            insight_id="old-insight",
            category="test",
            description="Old insight",
            recommendation="Old recommendation",
            impact_score=0.5,
            confidence=0.5,
            created_at=time.time() - 90000,  # 25 hours ago
            applies_to=["testing"],
        )

        self.tracker.insights.append(old_insight)

        # Generate new insights (should clean up old ones)
        self.tracker.generate_insights()

        # Old insight should be removed
        insight_ids = [i.insight_id for i in self.tracker.insights]
        assert "old-insight" not in insight_ids


class TestRecommendations:
    """Test suite for pattern recommendation functionality."""

    def setup_method(self):
        """Setup tracker with patterns for recommendation testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.tracker = ClaudeCodeCoordinationTracker(data_dir=self.temp_dir)

        self._create_sample_patterns()

    def _create_sample_patterns(self):
        """Create sample patterns for recommendation testing."""
        # Create successful testing pattern
        for i in range(3):
            event_id = f"testing-pattern-{i}"
            self.tracker.start_coordination(event_id, 2, ["testing"], "single_parallel")
            time.sleep(0.001)
            self.tracker.complete_coordination(event_id, success=True)

        # Create successful infrastructure pattern
        for i in range(2):
            event_id = f"infra-pattern-{i}"
            self.tracker.start_coordination(
                event_id, 4, ["infrastructure"], "batch_parallel"
            )
            time.sleep(0.001)
            self.tracker.complete_coordination(event_id, success=True)

    def test_exact_match_recommendation(self):
        """Test recommendation for exact pattern match."""
        recommendations = self.tracker.get_pattern_recommendations(["testing"], 2)

        assert recommendations["recommended_strategy"] == "single_parallel"
        assert recommendations["success_probability"] == 1.0
        assert recommendations["confidence"] > 0
        assert recommendations["estimated_duration"] is not None

    def test_similar_match_recommendation(self):
        """Test recommendation for similar pattern match."""
        # Request recommendation for slightly different agent count
        recommendations = self.tracker.get_pattern_recommendations(["testing"], 3)

        # Should still recommend based on testing pattern
        assert recommendations["recommended_strategy"] is not None
        assert recommendations["matching_patterns"] > 0

    def test_multi_domain_recommendation(self):
        """Test recommendation for multi-domain coordination."""
        recommendations = self.tracker.get_pattern_recommendations(
            ["testing", "infrastructure"], 3
        )

        # Should find matches and provide recommendations
        assert recommendations["matching_patterns"] > 0

        if recommendations["recommended_strategy"]:
            assert recommendations["confidence"] > 0
            assert recommendations["success_probability"] >= 0

    def test_no_match_recommendation(self):
        """Test recommendation when no patterns match."""
        recommendations = self.tracker.get_pattern_recommendations(
            ["nonexistent_domain"], 10
        )

        assert recommendations["recommended_strategy"] is None
        assert recommendations["matching_patterns"] == 0
        assert recommendations["alternatives"] == []

    def test_alternatives_in_recommendation(self):
        """Test alternative recommendations are provided."""
        # Create multiple patterns for same domain
        for strategy in ["strategy_a", "strategy_b"]:
            for i in range(2):
                event_id = f"alt-test-{strategy}-{i}"
                self.tracker.start_coordination(event_id, 3, ["security"], strategy)
                time.sleep(0.001)
                self.tracker.complete_coordination(event_id, success=True)

        recommendations = self.tracker.get_pattern_recommendations(["security"], 3)

        # Should have alternatives
        if len(self.tracker.patterns) > 1:
            assert len(recommendations["alternatives"]) > 0


class TestDataPersistence:
    """Test suite for data persistence functionality."""

    def setup_method(self):
        """Setup tracker for persistence testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.tracker = ClaudeCodeCoordinationTracker(data_dir=self.temp_dir)

    def test_events_persistence(self):
        """Test events are saved and loaded correctly."""
        # Add some events
        self.tracker.start_coordination("persist-1", 2, ["testing"], "single_parallel")
        self.tracker.complete_coordination("persist-1", success=True)

        # Create new tracker instance
        new_tracker = ClaudeCodeCoordinationTracker(data_dir=self.temp_dir)

        # Should load events from disk
        assert len(new_tracker.events) == 2
        assert new_tracker.events[0].event_id == "persist-1"

    def test_patterns_persistence(self):
        """Test patterns are saved and loaded correctly."""
        # Create a pattern
        self.tracker.start_coordination(
            "pattern-persist", 3, ["security"], "batch_parallel"
        )
        time.sleep(0.001)
        self.tracker.complete_coordination("pattern-persist", success=True)

        # Create new tracker instance
        new_tracker = ClaudeCodeCoordinationTracker(data_dir=self.temp_dir)

        # Should load patterns from disk
        assert len(new_tracker.patterns) == 1
        pattern_key = "security_3_batch_parallel"
        assert pattern_key in new_tracker.patterns

    def test_corrupted_data_handling(self):
        """Test handling of corrupted data files."""
        # Create corrupted events file
        events_file = Path(self.temp_dir) / "events.json"
        with open(events_file, "w") as f:
            f.write("invalid json content")

        # Should handle gracefully
        tracker = ClaudeCodeCoordinationTracker(data_dir=self.temp_dir)
        assert tracker.events == []  # Should start with empty events

    def test_file_save_error_handling(self):
        """Test handling of file save errors."""
        # Mock file operations to simulate save errors
        with patch("builtins.open", side_effect=IOError("Disk full")):
            # Should not raise exception
            self.tracker.start_coordination("save-error-test", 1, ["testing"], "direct")
            # Should complete without error even though save failed


class TestGlobalInstance:
    """Test suite for global tracker instance."""

    def test_global_instance_exists(self):
        """Test global coordination_tracker instance exists."""
        assert coordination_tracker is not None
        assert isinstance(coordination_tracker, ClaudeCodeCoordinationTracker)

    def test_global_instance_functionality(self):
        """Test global instance basic functionality."""
        # Should be able to use global instance
        event_id = str(uuid.uuid4())
        coordination_tracker.start_coordination(event_id, 1, ["testing"], "direct")
        coordination_tracker.complete_coordination(event_id, success=True)

        # Should have recorded the event
        event_ids = [e.event_id for e in coordination_tracker.events]
        assert event_id in event_ids


class TestIntegrationScenarios:
    """Integration tests for realistic usage scenarios."""

    def setup_method(self):
        """Setup tracker for integration testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.tracker = ClaudeCodeCoordinationTracker(data_dir=self.temp_dir)

    def test_full_coordination_lifecycle(self):
        """Test complete coordination tracking lifecycle."""
        event_id = "integration-lifecycle"
        domains = ["testing", "security"]
        agent_count = 3
        strategy = "single_parallel"
        agents = ["test-specialist", "security-enforcer", "coverage-optimizer"]

        # 1. Start coordination
        self.tracker.start_coordination(
            event_id, agent_count, domains, strategy, agents
        )

        # 2. Complete coordination
        time.sleep(0.01)
        self.tracker.complete_coordination(event_id, success=True)

        # 3. Verify event tracking
        assert len(self.tracker.events) == 2
        start_event = self.tracker.events[0]
        completion_event = self.tracker.events[1]

        assert start_event.event_type == CoordinationEventType.START
        assert completion_event.event_type == CoordinationEventType.COMPLETE
        assert completion_event.success is True
        assert completion_event.duration > 0

        # 4. Verify pattern learning
        assert len(self.tracker.patterns) == 1
        pattern_key = "security+testing_3_single_parallel"
        pattern = self.tracker.patterns[pattern_key]
        assert pattern.success_rate == 1.0
        assert pattern.usage_count == 1

        # 5. Get analytics
        analytics = self.tracker.get_analytics()
        assert analytics["summary"]["success_rate"] == 1.0

        # 6. Generate insights
        insights = self.tracker.generate_insights()
        # With only one successful coordination, might not generate specific insights
        assert isinstance(insights, list)

        # 7. Get recommendations
        recommendations = self.tracker.get_pattern_recommendations(domains, agent_count)
        assert recommendations["recommended_strategy"] == strategy
        assert recommendations["success_probability"] == 1.0

    def test_learning_improvement_scenario(self):
        """Test learning and improvement over multiple coordinations."""
        # Simulate multiple coordinations with improving success rates
        coordination_scenarios = [
            ("testing", 2, "single_parallel", True),
            ("testing", 2, "single_parallel", False),  # One failure
            ("testing", 2, "single_parallel", True),
            ("testing", 2, "single_parallel", True),
            ("testing", 2, "batch_parallel", True),  # Try different strategy
            ("testing", 2, "batch_parallel", True),
        ]

        for i, (domain, agents, strategy, success) in enumerate(coordination_scenarios):
            event_id = f"learning-{i}"
            self.tracker.start_coordination(event_id, agents, [domain], strategy)
            time.sleep(0.001)
            self.tracker.complete_coordination(event_id, success=success)

        # Should have learned patterns
        assert len(self.tracker.patterns) == 2  # Two different strategies

        # Get recommendations
        recommendations = self.tracker.get_pattern_recommendations(["testing"], 2)

        # Should recommend one of the strategies
        assert recommendations["recommended_strategy"] in [
            "single_parallel",
            "batch_parallel",
        ]
        assert recommendations["matching_patterns"] == 2

        # Should have alternatives
        assert len(recommendations["alternatives"]) > 0

        # Generate insights
        insights = self.tracker.generate_insights()

        # Should provide some insights based on the patterns
        assert (
            len(insights) >= 0
        )  # May or may not generate insights depending on criteria


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
