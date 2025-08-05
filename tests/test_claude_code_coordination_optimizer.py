#!/usr/bin/env python3
"""
Tests for Claude Code Coordination Optimizer

Comprehensive test suite validating intelligent batching and coordination patterns.
"""

import pytest
import sys
from pathlib import Path

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

from claude_code_coordination_optimizer import (
    ClaudeCodeCoordinationOptimizer,
    CoordinationStrategy,
    AgentCompatibility,
)


class TestClaudeCodeCoordinationOptimizer:
    """Test suite for coordination optimizer functionality"""

    def setup_method(self):
        """Setup optimizer instance for each test"""
        self.optimizer = ClaudeCodeCoordinationOptimizer()

    def test_initialization(self):
        """Test proper initialization of optimizer components"""
        assert self.optimizer.agent_compatibility_map is not None
        assert self.optimizer.domain_agent_mapping is not None
        assert len(self.optimizer.agent_compatibility_map) > 0
        assert len(self.optimizer.domain_agent_mapping) > 0

    def test_agent_compatibility_structure(self):
        """Test agent compatibility data structure"""
        for agent_name, compatibility in self.optimizer.agent_compatibility_map.items():
            assert isinstance(compatibility, AgentCompatibility)
            assert compatibility.agent_name == agent_name
            assert isinstance(compatibility.primary_domains, set)
            assert isinstance(compatibility.secondary_domains, set)
            assert isinstance(compatibility.avg_response_time, float)
            assert 0.0 <= compatibility.compatibility_score <= 1.0

    def test_optimize_task_batch_size_basic(self):
        """Test basic batch size optimization logic"""
        # Test small agent counts
        batch_size, num_batches = self.optimizer.optimize_task_batch_size(2)
        assert batch_size == 2
        assert num_batches == 1

        batch_size, num_batches = self.optimizer.optimize_task_batch_size(4)
        assert batch_size == 4
        assert num_batches == 1

    def test_optimize_task_batch_size_large_counts(self):
        """Test batch optimization for large agent counts"""
        # Test research-validated 4-agent batch optimization
        batch_size, num_batches = self.optimizer.optimize_task_batch_size(6)
        assert batch_size == 4
        assert num_batches == 2

        batch_size, num_batches = self.optimizer.optimize_task_batch_size(8)
        assert batch_size == 4
        assert num_batches == 2

        batch_size, num_batches = self.optimizer.optimize_task_batch_size(10)
        assert batch_size == 4
        assert num_batches == 3

    def test_optimize_task_batch_size_complexity_adjustment(self):
        """Test complexity-based batch size adjustments"""
        # High complexity should reduce batch size
        batch_size, num_batches = self.optimizer.optimize_task_batch_size(8, "high")
        assert batch_size == 3  # Reduced from 4

        # Low complexity keeps optimal
        batch_size, num_batches = self.optimizer.optimize_task_batch_size(8, "low")
        assert batch_size == 4

        # Medium complexity keeps optimal
        batch_size, num_batches = self.optimizer.optimize_task_batch_size(8, "medium")
        assert batch_size == 4

    def test_suggest_coordination_pattern_single_parallel(self):
        """Test single parallel strategy suggestion"""
        # Small agent counts should use single parallel
        strategy = self.optimizer.suggest_coordination_pattern(2, ["testing"])
        assert strategy == CoordinationStrategy.SINGLE_PARALLEL

        strategy = self.optimizer.suggest_coordination_pattern(
            4, ["testing", "security"]
        )
        assert strategy == CoordinationStrategy.SINGLE_PARALLEL

    def test_suggest_coordination_pattern_batch_parallel(self):
        """Test batch parallel strategy suggestion"""
        # Large agent counts should use batch parallel
        strategy = self.optimizer.suggest_coordination_pattern(6, ["testing"])
        assert strategy == CoordinationStrategy.BATCH_PARALLEL

        strategy = self.optimizer.suggest_coordination_pattern(
            8, ["testing", "security"]
        )
        assert strategy == CoordinationStrategy.BATCH_PARALLEL

        # Multiple complex domains should trigger batch parallel
        strategy = self.optimizer.suggest_coordination_pattern(
            4, ["testing", "security", "infrastructure", "performance"]
        )
        assert strategy == CoordinationStrategy.BATCH_PARALLEL

    def test_get_best_agents_for_domains_basic(self):
        """Test basic agent selection for domains"""
        agents = self.optimizer.get_best_agents_for_domains(["testing"])
        assert len(agents) > 0
        assert "test-specialist" in agents  # Should prioritize primary domain match

    def test_get_best_agents_for_domains_multiple(self):
        """Test agent selection for multiple domains"""
        domains = ["testing", "security", "infrastructure"]
        agents = self.optimizer.get_best_agents_for_domains(domains, max_agents=6)

        assert len(agents) <= 6
        assert len(agents) > 0

        # Should include agents from different domains
        agent_domains = set()
        for agent in agents:
            if agent in self.optimizer.agent_compatibility_map:
                agent_info = self.optimizer.agent_compatibility_map[agent]
                agent_domains.update(agent_info.primary_domains)

        # Should cover multiple requested domains
        assert len(agent_domains.intersection(set(domains))) > 0

    def test_get_best_agents_for_domains_max_limit(self):
        """Test agent selection respects max_agents limit"""
        agents = self.optimizer.get_best_agents_for_domains(
            ["testing", "security", "infrastructure", "performance"], max_agents=3
        )
        assert len(agents) <= 3

    def test_get_coordination_strategy_logic_complete(self):
        """Test complete coordination strategy logic"""
        domains = ["testing", "security"]
        agent_count = 6

        result = self.optimizer.get_coordination_strategy_logic(agent_count, domains)

        # Verify all expected fields
        assert "strategy" in result
        assert "batch_size" in result
        assert "num_batches" in result
        assert "recommended_agents" in result
        assert "total_agents" in result
        assert "domains" in result
        assert "estimated_time" in result
        assert "confidence_score" in result

        # Verify data types and values
        assert result["strategy"] in ["single_parallel", "batch_parallel"]
        assert isinstance(result["batch_size"], int)
        assert isinstance(result["num_batches"], int)
        assert isinstance(result["recommended_agents"], list)
        assert result["total_agents"] == agent_count
        assert result["domains"] == domains
        assert isinstance(result["estimated_time"], float)
        assert 0.0 <= result["confidence_score"] <= 1.0

    def test_coordination_strategy_logic_large_scale(self):
        """Test coordination logic for large-scale scenarios"""
        domains = ["testing", "security", "infrastructure", "performance", "quality"]
        agent_count = 10

        result = self.optimizer.get_coordination_strategy_logic(agent_count, domains)

        # Should use batch parallel for large scale
        assert result["strategy"] == "batch_parallel"
        assert result["num_batches"] > 1
        assert len(result["recommended_agents"]) > 0

    def test_confidence_score_calculation(self):
        """Test confidence score calculation logic"""
        # Perfect domain coverage should give high confidence
        domains = ["testing"]
        agents = ["test-specialist"]
        confidence = self.optimizer._calculate_confidence_score(domains, agents)
        assert confidence > 0.8

        # No agents should give zero confidence
        confidence = self.optimizer._calculate_confidence_score(domains, [])
        assert confidence == 0.0

        # No domains should give zero confidence
        confidence = self.optimizer._calculate_confidence_score([], agents)
        assert confidence == 0.0

    def test_coordination_time_estimation(self):
        """Test coordination time estimation"""
        # Single parallel should be higher per agent
        single_time = self.optimizer._estimate_coordination_time(
            4, CoordinationStrategy.SINGLE_PARALLEL
        )
        batch_time = self.optimizer._estimate_coordination_time(
            4, CoordinationStrategy.BATCH_PARALLEL
        )

        # Both should be positive
        assert single_time > 0
        assert batch_time > 0

        # Time should increase with agent count
        small_time = self.optimizer._estimate_coordination_time(
            2, CoordinationStrategy.SINGLE_PARALLEL
        )
        large_time = self.optimizer._estimate_coordination_time(
            8, CoordinationStrategy.SINGLE_PARALLEL
        )
        assert large_time > small_time

    def test_domain_agent_mapping_completeness(self):
        """Test domain to agent mapping completeness"""
        expected_domains = [
            "testing",
            "security",
            "infrastructure",
            "performance",
            "quality",
            "coordination",
        ]

        for domain in expected_domains:
            assert domain in self.optimizer.domain_agent_mapping
            assert len(self.optimizer.domain_agent_mapping[domain]) > 0

    def test_research_validated_patterns(self):
        """Test research-validated patterns are implemented"""
        # Research-validated 4-agent batch optimization
        batch_size, _ = self.optimizer.optimize_task_batch_size(8, "medium")
        assert batch_size == 4

        # >6 agent coordination should use batch parallel
        strategy = self.optimizer.suggest_coordination_pattern(7, ["testing"])
        assert strategy == CoordinationStrategy.BATCH_PARALLEL

    def test_edge_cases(self):
        """Test edge cases and error conditions"""
        # Empty domains list
        agents = self.optimizer.get_best_agents_for_domains([])
        assert len(agents) == 0

        # Zero agent count
        batch_size, num_batches = self.optimizer.optimize_task_batch_size(0)
        assert batch_size >= 0
        assert num_batches >= 0

        # Non-existent domain
        agents = self.optimizer.get_best_agents_for_domains(["non_existent_domain"])
        # Should handle gracefully without error
        assert isinstance(agents, list)


class TestIntegrationScenarios:
    """Integration tests for realistic coordination scenarios"""

    def setup_method(self):
        """Setup optimizer for integration tests"""
        self.optimizer = ClaudeCodeCoordinationOptimizer()

    def test_scenario_complex_debugging(self):
        """Test complex debugging scenario coordination"""
        domains = ["testing", "security", "infrastructure", "performance"]
        agent_count = 8

        result = self.optimizer.get_coordination_strategy_logic(agent_count, domains)

        # Should use batch parallel for complex multi-domain issue
        assert result["strategy"] == "batch_parallel"
        assert result["confidence_score"] > 0.7  # Should have good coverage
        assert len(result["recommended_agents"]) > 0

    def test_scenario_simple_test_fix(self):
        """Test simple test fix scenario coordination"""
        domains = ["testing"]
        agent_count = 2

        result = self.optimizer.get_coordination_strategy_logic(agent_count, domains)

        # Should use single parallel for simple case
        assert result["strategy"] == "single_parallel"
        assert "test-specialist" in result["recommended_agents"]

    def test_scenario_infrastructure_crisis(self):
        """Test infrastructure crisis scenario coordination"""
        domains = ["infrastructure", "performance", "security", "coordination"]
        agent_count = 12

        result = self.optimizer.get_coordination_strategy_logic(agent_count, domains)

        # Should use batch parallel with good coverage
        assert result["strategy"] == "batch_parallel"
        assert result["num_batches"] >= 3
        assert result["confidence_score"] > 0.6


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
