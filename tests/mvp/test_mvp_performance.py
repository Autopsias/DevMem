import pytest
import time
from src.patterns import (
    PatternContext, ConfidenceLevel,
    PatternRegistry, PatternExecutor, PatternStorage,
    SequentialDelegationPattern, ParallelCoordinationPattern, MetaOrchestrationPattern
)

def test_pattern_lookup_performance():
    """Test pattern lookup performance (target: <100ms)"""
    storage = PatternStorage()
    
    # Create test patterns
    patterns = []
    for i in range(100):  # Test with 100 patterns
        if i % 3 == 0:
            pattern = SequentialDelegationPattern(
                f"seq_pattern_{i}",
                f"Sequential Pattern {i}",
                ["validate", "process", "store"]
            )
        elif i % 3 == 1:
            pattern = ParallelCoordinationPattern(
                f"parallel_pattern_{i}",
                f"Parallel Pattern {i}",
                {"cpu", "memory", "network"}
            )
        else:
            pattern = MetaOrchestrationPattern(
                f"meta_pattern_{i}",
                f"Meta Pattern {i}",
                {"auth", "data", "network"}
            )
        patterns.append(pattern)
        storage.store_pattern(pattern)
    
    # Test lookup performance
    total_time = 0
    iterations = 1000  # Test with 1000 lookups
    
    for i in range(iterations):
        pattern_name = patterns[i % len(patterns)].name
        
        start = time.time()
        pattern = storage.get_pattern(pattern_name)
        end = time.time()
        
        assert pattern is not None
        total_time += (end - start) * 1000  # Convert to ms
    
    avg_time = total_time / iterations
    print(f"\nAverage pattern lookup time: {avg_time:.2f}ms")
    assert avg_time < 100, f"Pattern lookup too slow: {avg_time:.2f}ms"

def test_memory_access_performance():
    """Test memory access performance (target: <50ms)"""
    storage = PatternStorage()
    
    # Create test patterns
    for i in range(100):
        pattern = SequentialDelegationPattern(
            f"test_pattern_{i}",
            f"Test Pattern {i}",
            ["validate", "process", "store"]
        )
        storage.store_pattern(pattern)
    
    # Test memory access performance
    total_time = 0
    iterations = 1000
    
    context = PatternContext(
        domain="test",
        agent_type="test",
        attributes={"required_steps": ["validate", "store"]}
    )
    
    for _ in range(iterations):
        start = time.time()
        patterns = storage.find_matching_patterns(context)
        end = time.time()
        
        assert patterns
        total_time += (end - start) * 1000  # Convert to ms
    
    avg_time = total_time / iterations
    print(f"\nAverage memory access time: {avg_time:.2f}ms")
    assert avg_time < 50, f"Memory access too slow: {avg_time:.2f}ms"

def test_end_to_end_performance():
    """Test end-to-end delegation performance (target: <150ms)"""
    registry = PatternRegistry()
    executor = PatternExecutor(registry)
    
    # Create and register test patterns
    patterns = [
        SequentialDelegationPattern(
            "test_seq",
            "Test Sequential Pattern",
            ["validate", "process", "store"]
        ),
        ParallelCoordinationPattern(
            "test_parallel",
            "Test Parallel Pattern",
            {"cpu", "memory", "network"}
        ),
        MetaOrchestrationPattern(
            "test_meta",
            "Test Meta Pattern",
            {"auth", "data", "network"}
        )
    ]
    
    for pattern in patterns:
        registry.register(pattern)
    
    # Test contexts
    contexts = [
        PatternContext(
            domain="test",
            agent_type="sequential",
            attributes={"required_steps": ["validate", "store"]}
        ),
        PatternContext(
            domain="test",
            agent_type="parallel",
            attributes={"required_resources": ["cpu", "memory"]}
        ),
        PatternContext(
            domain="test",
            agent_type="orchestrator",
            attributes={"required_domains": ["auth", "data", "network"]}
        )
    ]
    
    # Build confidence through executions
    for pattern, context in zip(patterns, contexts):
        for _ in range(10):
            success, _ = executor.execute_pattern(pattern, context)
            assert success
    
    # Test end-to-end performance
    total_time = 0
    iterations = 100
    
    for _ in range(iterations):
        for context in contexts:
            start = time.time()
            success, _ = executor.execute_best_pattern(context)
            end = time.time()
            
            assert success
            total_time += (end - start) * 1000  # Convert to ms
    
    avg_time = total_time / (iterations * len(contexts))
    print(f"\nAverage end-to-end time: {avg_time:.2f}ms")
    assert avg_time < 150, f"End-to-end execution too slow: {avg_time:.2f}ms"

def test_context_preservation():
    """Test context preservation rate (target: ≥80%)"""
    registry = PatternRegistry()
    executor = PatternExecutor(registry)
    storage = PatternStorage()
    
    # Create test patterns with context requirements
    patterns = [
        SequentialDelegationPattern(
            "test_seq",
            "Test Sequential Pattern",
            ["validate", "process", "store"]
        ),
        ParallelCoordinationPattern(
            "test_parallel",
            "Test Parallel Pattern",
            {"cpu", "memory", "network"}
        ),
        MetaOrchestrationPattern(
            "test_meta",
            "Test Meta Pattern",
            {"auth", "data", "network"}
        )
    ]
    
    # Store and register patterns
    for pattern in patterns:
        storage.store_pattern(pattern)
        registry.register(pattern)
    
    # Test context preservation
    total_matches = 0
    preserved_matches = 0
    iterations = 100
    
    test_contexts = [
        PatternContext(
            domain="test",
            agent_type="sequential",
            attributes={"required_steps": ["validate", "store"]}
        ),
        PatternContext(
            domain="test",
            agent_type="parallel",
            attributes={"required_resources": ["cpu", "memory"]}
        ),
        PatternContext(
            domain="test",
            agent_type="orchestrator",
            attributes={"required_domains": ["auth", "data"]}
        )
    ]
    
    for _ in range(iterations):
        for context in test_contexts:
            # Get matching patterns
            initial_matches = storage.find_matching_patterns(context)
            total_matches += len(initial_matches)
            
            # Execute pattern
            if initial_matches:
                success, _ = executor.execute_pattern(initial_matches[0], context)
                assert success
            
            # Check pattern still matches
            final_matches = storage.find_matching_patterns(context)
            preserved_matches += len(set(p.name for p in initial_matches) & 
                                  set(p.name for p in final_matches))
    
    preservation_rate = (preserved_matches / total_matches) * 100
    print(f"\nContext preservation rate: {preservation_rate:.1f}%")
    assert preservation_rate >= 80, f"Context preservation too low: {preservation_rate:.1f}%"