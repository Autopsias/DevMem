import pytest
from src.patterns import PatternContext, ConfidenceLevel
from src.patterns.parallel_mvp import ParallelCoordinationPattern

def test_parallel_pattern_matching():
    """Test parallel pattern matching logic"""
    pattern = ParallelCoordinationPattern(
        "test_parallel",
        "Test Parallel Pattern",
        {"cpu", "memory", "network"}
    )
    
    # Test matching context
    context = PatternContext(
        domain="test",
        agent_type="parallel",
        attributes={"required_resources": ["cpu", "memory"]}
    )
    assert pattern.matches(context)
    
    # Test non-matching context
    context = PatternContext(
        domain="test",
        agent_type="parallel",
        attributes={"required_resources": ["gpu"]}
    )
    assert not pattern.matches(context)
    
    # Test context without resources
    context = PatternContext(
        domain="test",
        agent_type="parallel",
        attributes={}
    )
    assert not pattern.matches(context)

def test_parallel_pattern_execution():
    """Test parallel pattern execution"""
    pattern = ParallelCoordinationPattern(
        "test_parallel",
        "Test Parallel Pattern",
        {"cpu", "memory", "network"}
    )
    
    # Test successful execution
    context = PatternContext(
        domain="test",
        agent_type="parallel",
        attributes={"required_resources": ["cpu", "memory"]}
    )
    assert pattern.execute(context)
    
    # Execute multiple times to build confidence
    for _ in range(10):
        assert pattern.execute(context)
        
    # Verify confidence metrics
    assert pattern.confidence_score >= 0.65  # MVP target
    assert pattern.confidence_level in [ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH]
    
def test_parallel_pattern_resource_management():
    """Test parallel pattern resource management"""
    pattern = ParallelCoordinationPattern(
        "test_parallel",
        "Test Parallel Pattern",
        {"cpu", "memory", "network"}
    )
    
    # Test resource allocation
    assert pattern._allocate_resource("cpu")
    assert pattern._active_resources["cpu"] == 1
    
    # Test invalid resource allocation
    assert not pattern._allocate_resource("gpu")
    
    # Test resource release
    pattern._release_resource("cpu")
    assert pattern._active_resources["cpu"] == 0
    
    # Test multiple allocations
    assert pattern._allocate_resource("memory")
    assert pattern._allocate_resource("memory")
    assert pattern._active_resources["memory"] == 2
    
    pattern._release_resource("memory")
    assert pattern._active_resources["memory"] == 1

def test_parallel_pattern_error_handling():
    """Test parallel pattern error handling"""
    pattern = ParallelCoordinationPattern(
        "test_parallel",
        "Test Parallel Pattern",
        {"cpu", "memory", "network"}
    )
    
    # Test execution with invalid resources
    context = PatternContext(
        domain="test",
        agent_type="parallel",
        attributes={"required_resources": ["gpu"]}
    )
    assert not pattern.execute(context)
    
    # Test execution with missing attributes
    context = PatternContext(
        domain="test",
        agent_type="parallel"
    )
    assert not pattern.execute(context)
    
    # Verify error handling affects confidence appropriately
    assert pattern.confidence_score >= 0.0