import pytest
from pathlib import Path
from src.patterns import (
    DelegationPattern, PatternContext, ConfidenceLevel,
    PatternRegistry, PatternExecutor
)
from src.patterns.sequential_mvp import SequentialDelegationPattern
from src.patterns.parallel_mvp import ParallelCoordinationPattern
from src.patterns.meta_orchestration_mvp import MetaOrchestrationPattern

class TestPattern(DelegationPattern):
    def __init__(self, name: str, description: str, domain: str):
        super().__init__(name, description)
        self.domain = domain
        
    def matches(self, context: PatternContext) -> bool:
        return context.domain == self.domain
        
    def execute(self, context: PatternContext) -> bool:
        return True

def test_pattern_registry():
    """Test pattern registry loading and validation"""
    registry = PatternRegistry()
    
    # Register test patterns
    p1 = TestPattern("test1", "Test Pattern 1", "domain1")
    p2 = TestPattern("test2", "Test Pattern 2", "domain2")
    
    registry.register(p1)
    registry.register(p2)
    
    # Test pattern retrieval
    assert registry.get_pattern("test1") == p1
    assert registry.get_pattern("test2") == p2
    
    # Test pattern matching
    context = PatternContext(domain="domain1", agent_type="test")
    matches = registry.find_matching_patterns(context)
    assert len(matches) == 1
    assert matches[0] == p1

def test_delegation_accuracy():
    """Test pattern-based delegation accuracy"""
    registry = PatternRegistry()
    executor = PatternExecutor(registry)
    
    # Register test pattern
    pattern = TestPattern("test", "Test Pattern", "domain1")
    registry.register(pattern)
    
    # Register sequential pattern
    seq_pattern = SequentialDelegationPattern(
        "test_seq",
        "Test Sequential Pattern",
        ["validate", "process", "store"]
    )
    registry.register(seq_pattern)
    
    # Execute simple pattern
    context = PatternContext(domain="domain1", agent_type="test")
    for _ in range(10):
        success, _ = executor.execute_pattern(pattern, context)
        assert success
        
    assert pattern.confidence_score == 1.0
    assert pattern.confidence_level == ConfidenceLevel.HIGH
    
    # Execute sequential pattern
    seq_context = PatternContext(
        domain="sequential",
        agent_type="test",
        attributes={"required_steps": ["validate", "store"]}
    )
    for _ in range(10):
        success, _ = executor.execute_pattern(seq_pattern, seq_context)
        assert success
        
    assert seq_pattern.confidence_score >= 0.6  # MVP target
    assert seq_pattern.confidence_level in [ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH]
    
def test_parallel_coordination():
    """Test parallel task coordination with meta-orchestration"""
    registry = PatternRegistry()
    executor = PatternExecutor(registry)
    
    # Register parallel pattern
    parallel_pattern = ParallelCoordinationPattern(
        "test_parallel",
        "Test Parallel Pattern",
        {"cpu", "memory", "network"}
    )
    registry.register(parallel_pattern)
    
    # Register meta-orchestration pattern
    meta_pattern = MetaOrchestrationPattern(
        "test_meta",
        "Test Meta Pattern",
        {"cpu", "memory", "network", "storage", "compute"}
    )
    registry.register(meta_pattern)
    
    # Build parallel pattern confidence
    context = PatternContext(
        domain="test",
        agent_type="parallel",
        attributes={"required_resources": ["cpu", "memory"]}
    )
    
    for _ in range(10):
        success, msg = executor.execute_pattern(parallel_pattern, context)
        assert success
        
    assert parallel_pattern.confidence_score >= 0.65  # MVP target
    
    # Build meta pattern confidence
    meta_context = PatternContext(
        domain="test",
        agent_type="orchestrator",
        attributes={"required_domains": ["cpu", "memory", "network"]}
    )
    
    for _ in range(10):
        success, msg = executor.execute_pattern(meta_pattern, meta_context)
        assert success
        
    assert meta_pattern.confidence_score >= 0.5  # MVP target
    
    # Test parallel execution with multiple resources
    multi_context = PatternContext(
        domain="test",
        agent_type="parallel",
        attributes={"required_resources": ["cpu", "memory", "network"]}
    )
    
    success, msg = executor.execute_best_pattern(multi_context)
    assert success
    
    # Test meta-orchestration with multiple domains
    multi_domain_context = PatternContext(
        domain="test",
        agent_type="orchestrator",
        attributes={"required_domains": ["cpu", "memory", "network", "storage"]}
    )
    
    success, msg = executor.execute_best_pattern(multi_domain_context)
    assert success
    
    # Register multiple patterns for parallel execution
    patterns = [
        ParallelCoordinationPattern(
            f"parallel{i}",
            f"Parallel Pattern {i}",
            {"cpu", "memory", "network"}
        )
        for i in range(3)
    ]
    
    # Register multiple meta patterns
    meta_patterns = [
        MetaOrchestrationPattern(
            f"meta{i}",
            f"Meta Pattern {i}",
            {"cpu", "memory", "network", "storage", "compute"}
        )
        for i in range(3)
    ]
    
    # Register and build confidence for all patterns
    all_patterns = patterns + meta_patterns
    for p in all_patterns:
        registry.register(p)
        if isinstance(p, ParallelCoordinationPattern):
            ctx = PatternContext(
                domain="test",
                agent_type="parallel",
                attributes={"required_resources": ["cpu"]}
            )
        else:
            ctx = PatternContext(
                domain="test",
                agent_type="orchestrator",
                attributes={"required_domains": ["cpu", "memory", "network"]}
            )
        for _ in range(10):
            success, _ = executor.execute_pattern(p, ctx)
            assert success
            
    # Execute patterns in parallel
    parallel_contexts = [
        PatternContext(
            domain="test",
            agent_type="parallel",
            attributes={"required_resources": ["cpu"]}
        )
        for _ in range(3)
    ]
    
    meta_contexts = [
        PatternContext(
            domain="test",
            agent_type="orchestrator",
            attributes={"required_domains": ["cpu", "memory", "network"]}
        )
        for _ in range(3)
    ]
    
    # Test both parallel and meta-orchestration execution
    results = []
    for ctx in parallel_contexts + meta_contexts:
        success, msg = executor.execute_best_pattern(ctx)
        results.append(success)
        
    assert all(results)

def test_memory_integration():
    """Test memory system integration"""
    from src.patterns.mvp_pattern_storage import PatternStorage
    
    # Create storage and patterns
    storage = PatternStorage()
    registry = PatternRegistry()
    executor = PatternExecutor(registry)
    
    # Create and store patterns
    patterns = [
        SequentialDelegationPattern(
            "seq_pattern",
            "Sequential Pattern",
            ["validate", "process", "store"]
        ),
        ParallelCoordinationPattern(
            "parallel_pattern",
            "Parallel Pattern",
            {"cpu", "memory", "network"}
        ),
        MetaOrchestrationPattern(
            "meta_pattern",
            "Meta Pattern",
            {"auth", "data", "network", "compute"}
        )
    ]
    
    # Store in both systems
    for pattern in patterns:
        storage.store_pattern(pattern)
        registry.register(pattern)
        
    # Build confidence through execution
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
    
    for pattern, context in zip(patterns, contexts):
        for _ in range(10):
            success, _ = executor.execute_pattern(pattern, context)
            assert success
            
    # Verify memory integration
    for i, pattern in enumerate(patterns):
        # Test storage retrieval
        stored = storage.get_pattern(pattern.name)
        assert stored == pattern
        assert stored.confidence_score >= 0.5  # MVP target
        
        # Test pattern matching
        matches = storage.find_matching_patterns(contexts[i])
        assert pattern in matches
        
        # Test registry integration
        reg_pattern = registry.get_pattern(pattern.name)
        assert reg_pattern == pattern
        assert reg_pattern.confidence_score == stored.confidence_score