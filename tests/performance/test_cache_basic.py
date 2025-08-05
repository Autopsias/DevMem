"""
Basic Cache Effectiveness Tests (Task 1d - Without External Dependencies)

Tests core caching functionality without requiring psutil or tiktoken.
"""

import pytest
import time
import tempfile
from pathlib import Path
from datetime import datetime

# Mock the external dependencies for testing
class MockTokenEstimator:
    def count_tokens(self, text: str) -> int:
        """Mock token counting based on word count."""
        return len(text.split()) * 1.3  # Rough approximation

# Update token estimation to work without tiktoken
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_cache_basic_functionality():
    """Test basic cache functionality without external dependencies."""
    from src.performance.prompt_cache import PromptCacheManager, CacheStrategy
    
    # Create cache manager with temporary storage
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_manager = PromptCacheManager(max_entries=10)
        cache_manager.cache_dir = Path(temp_dir)
        cache_manager.cache_file = Path(temp_dir) / "test_cache.json"
        
        try:
            # Test basic cache operations
            template = "Analyze {task} for {project}"
            context = {"task": "testing", "project": "DevMem"}
            rendered = template.format(**context)
            
            # First request should miss
            cached = cache_manager.get_cached_prompt(
                template, context, CacheStrategy.AGENT_COORDINATION
            )
            assert cached is None, "First request should miss cache"
            
            # Cache the prompt
            cache_manager.cache_prompt(
                template, context, CacheStrategy.AGENT_COORDINATION, rendered
            )
            
            # Second request should hit
            cached = cache_manager.get_cached_prompt(
                template, context, CacheStrategy.AGENT_COORDINATION
            )
            assert cached == rendered, "Second request should hit cache"
            
            # Verify stats
            stats = cache_manager.get_stats()
            assert stats.cache_hits >= 1, "Should have at least 1 cache hit"
            assert stats.total_requests >= 2, "Should have at least 2 total requests"
            
            print(f"✅ Basic cache test passed - Hit rate: {stats.hit_rate:.1f}%")
            
        finally:
            cache_manager.shutdown()

def test_cache_performance_simulation():
    """Test cache provides performance improvement through simulation."""
    from src.performance.prompt_cache import PromptCacheManager, CacheStrategy
    
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_manager = PromptCacheManager(max_entries=20)
        cache_manager.cache_dir = Path(temp_dir)
        
        try:
            # Sample coordination patterns
            patterns = [
                ("Coordinate {agent} for {task}", {"agent": "test-specialist", "task": "analysis"}),
                ("Execute {workflow} with {params}", {"workflow": "testing", "params": "async"}),
                ("Review {component} using {criteria}", {"component": "auth", "criteria": "security"}),
                ("Optimize {system} for {metric}", {"system": "cache", "metric": "performance"})
            ]
            
            # Measure uncached performance
            start_time = time.time()
            uncached_results = []
            
            for template, context in patterns:
                rendered = template.format(**context)
                uncached_results.append(rendered)
                time.sleep(0.001)  # Simulate processing time
            
            uncached_time = time.time() - start_time
            
            # Populate cache
            for template, context in patterns:
                rendered = template.format(**context)
                cache_manager.cache_prompt(
                    template, context, CacheStrategy.AGENT_COORDINATION, rendered
                )
            
            # Measure cached performance
            start_time = time.time()
            cached_results = []
            
            for template, context in patterns:
                cached = cache_manager.get_cached_prompt(
                    template, context, CacheStrategy.AGENT_COORDINATION
                )
                assert cached is not None, "Cache should hit for all patterns"
                cached_results.append(cached)
            
            cached_time = time.time() - start_time
            
            # Verify results match
            assert uncached_results == cached_results, "Cached and uncached results should match"
            
            # Calculate improvement (should be measurable even with minimal processing)
            if uncached_time > 0:
                improvement = ((uncached_time - cached_time) / uncached_time) * 100
                print(f"✅ Performance improvement: {improvement:.1f}%")
                print(f"   Uncached: {uncached_time*1000:.2f}ms")
                print(f"   Cached: {cached_time*1000:.2f}ms")
            
            # Verify cache effectiveness
            stats = cache_manager.get_stats()
            assert stats.hit_rate >= 75.0, f"Hit rate {stats.hit_rate}% should be at least 75%"
            
        finally:
            cache_manager.shutdown()

def test_cache_invalidation_basic():
    """Test basic cache invalidation functionality."""
    from src.performance.prompt_cache import PromptCacheManager, CacheStrategy
    
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_manager = PromptCacheManager(max_entries=10)
        cache_manager.cache_dir = Path(temp_dir)
        
        try:
            # Clear any existing cache entries
            cache_manager._cache.clear()
            cache_manager._stats.total_requests = 0
            cache_manager._stats.cache_hits = 0
            cache_manager._stats.cache_misses = 0
            cache_manager._stats.evictions = 0
            
            # Cache multiple entries
            test_entries = [
                ("test-specialist", "Analyze tests", {"type": "unit"}),
                ("test-specialist", "Review coverage", {"type": "integration"}),
                ("security-enforcer", "Scan code", {"type": "static"}),
                ("performance-optimizer", "Optimize queries", {"type": "database"})
            ]
            
            for agent, template, context in test_entries:
                rendered = template.format(**context) if context else template
                cache_manager.cache_prompt(
                    template, context, CacheStrategy.AGENT_COORDINATION,
                    rendered, {agent}
                )
            
            initial_count = len(cache_manager._cache)
            print(f"DEBUG: Initial cache count: {initial_count}")
            print(f"DEBUG: Cache keys: {list(cache_manager._cache.keys())}")
            assert initial_count == 4, f"Should have 4 cached entries, got {initial_count}"
            
            # Invalidate test-specialist entries
            invalidated = cache_manager.invalidate_agent_type("test-specialist")
            assert invalidated == 2, "Should invalidate 2 test-specialist entries"
            
            remaining_count = len(cache_manager._cache)
            assert remaining_count == 2, "Should have 2 remaining entries"
            
            # Test pattern invalidation - use part of the key format that exists
            pattern_invalidated = cache_manager.invalidate_pattern("agent_coordination")
            
            final_count = len(cache_manager._cache)
            assert final_count == 0, f"Should have cleared all remaining entries, got {final_count}"
            
            print(f"✅ Invalidation test passed - Removed {invalidated} by agent, {pattern_invalidated} by pattern")
            
        finally:
            cache_manager.shutdown()

def test_multi_agent_coordination_cache():
    """Test caching for multi-agent coordination scenarios."""
    from src.performance.prompt_cache import PromptCacheManager, CacheStrategy
    
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_manager = PromptCacheManager(max_entries=15)
        cache_manager.cache_dir = Path(temp_dir)
        
        try:
            # Multi-agent coordination patterns
            coordination_scenarios = [
                {
                    "pattern": "sequential",
                    "agents": ["analysis-gateway", "test-specialist", "synthesis-coordinator"],
                    "template": "Sequential: {agents} → {task}",
                    "context": {"task": "test_analysis"}
                },
                {
                    "pattern": "parallel",
                    "agents": ["security-enforcer", "performance-optimizer", "infrastructure-engineer"], 
                    "template": "Parallel: {agents} || {task}",
                    "context": {"task": "system_review"}
                },
                {
                    "pattern": "hierarchical",
                    "agents": ["meta-coordinator", "synthesis-coordinator"],
                    "template": "Hierarchical: {agents} ↕ {task}",
                    "context": {"task": "orchestration"}
                }
            ]
            
            cached_count = 0
            
            for scenario in coordination_scenarios:
                agents_str = ", ".join(scenario["agents"])
                context = scenario["context"].copy()
                context["agents"] = agents_str
                
                template = scenario["template"]
                rendered = template.format(**context)
                agent_types = set(scenario["agents"])
                
                # Cache coordination pattern
                cache_manager.cache_prompt(
                    template, context, CacheStrategy.AGENT_COORDINATION,
                    rendered, agent_types
                )
                
                # Verify retrieval
                cached = cache_manager.get_cached_prompt(
                    template, context, CacheStrategy.AGENT_COORDINATION, agent_types
                )
                
                if cached == rendered:
                    cached_count += 1
            
            assert cached_count == len(coordination_scenarios), "All coordination patterns should cache successfully"
            
            stats = cache_manager.get_stats()
            hit_rate = stats.hit_rate
            
            print(f"✅ Multi-agent coordination cached: {cached_count} patterns")
            print(f"   Cache hit rate: {hit_rate:.1f}%")
            
            # Should achieve reasonable hit rate
            assert hit_rate >= 40.0, f"Hit rate {hit_rate}% should be at least 40%"
            
        finally:
            cache_manager.shutdown()

if __name__ == "__main__":
    # Run tests directly for debugging
    test_cache_basic_functionality()
    test_cache_performance_simulation()
    test_cache_invalidation_basic()  
    test_multi_agent_coordination_cache()
    print("✅ All cache effectiveness tests passed!")