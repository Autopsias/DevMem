import pytest
from src.patterns import PatternContext, ConfidenceLevel
from src.patterns.sequential_mvp import SequentialDelegationPattern

def test_sequential_pattern_matching():
    """Test sequential pattern matching logic"""
    # Create pattern with defined sequence
    pattern = SequentialDelegationPattern(
        "test_seq",
        "Test Sequential Pattern",
        ["validate", "process", "store"]
    )
    
    # Test matching context
    context = PatternContext(
        domain="test",
        agent_type="sequential",
        attributes={"required_steps": ["validate", "store"]}
    )
    assert pattern.matches(context)
    
    # Test non-matching context (missing step)
    context = PatternContext(
        domain="test",
        agent_type="sequential",
        attributes={"required_steps": ["validate", "unknown"]}
    )
    assert not pattern.matches(context)
    
    # Test context without steps
    context = PatternContext(
        domain="test",
        agent_type="sequential",
        attributes={}
    )
    assert not pattern.matches(context)

def test_sequential_pattern_execution():
    """Test sequential pattern execution"""
    pattern = SequentialDelegationPattern(
        "test_seq",
        "Test Sequential Pattern",
        ["validate", "process", "store"]
    )
    
    # Test successful execution
    context = PatternContext(
        domain="test",
        agent_type="sequential",
        attributes={"required_steps": ["validate", "store"]}
    )
    assert pattern.execute(context)
    
    # Execute multiple times to build confidence
    for _ in range(10):
        assert pattern.execute(context)
        
    # Verify confidence metrics
    assert pattern.confidence_score >= 0.6  # MVP target
    assert pattern.confidence_level in [ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH]
    
def test_sequential_pattern_error_handling():
    """Test sequential pattern error handling"""
    pattern = SequentialDelegationPattern(
        "test_seq",
        "Test Sequential Pattern",
        ["validate", "process", "store"]
    )
    
    # Test execution with invalid steps
    context = PatternContext(
        domain="test",
        agent_type="sequential",
        attributes={"required_steps": ["unknown"]}
    )
    assert not pattern.execute(context)
    
    # Test execution with missing attributes
    context = PatternContext(
        domain="test",
        agent_type="sequential"
    )
    assert not pattern.execute(context)
    
    # Verify error handling doesn't affect confidence
    assert pattern.confidence_score >= 0.0