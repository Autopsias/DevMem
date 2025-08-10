import pytest
from src.patterns import PatternContext, ConfidenceLevel
from src.patterns.sequential_mvp import SequentialDelegationPattern
from src.patterns.parallel_mvp import ParallelCoordinationPattern
from src.patterns.meta_orchestration_mvp import MetaOrchestrationPattern
from src.patterns.mvp_pattern_storage import PatternStorage

def test_pattern_storage_basic():
    """Test basic pattern storage operations"""
    storage = PatternStorage()
    
    # Store patterns
    seq_pattern = SequentialDelegationPattern(
        "test_seq",
        "Test Sequential Pattern",
        ["validate", "process", "store"]
    )
    storage.store_pattern(seq_pattern)
    
    parallel_pattern = ParallelCoordinationPattern(
        "test_parallel",
        "Test Parallel Pattern",
        {"cpu", "memory", "network"}
    )
    storage.store_pattern(parallel_pattern)
    
    # Retrieve patterns
    assert storage.get_pattern("test_seq") == seq_pattern
    assert storage.get_pattern("test_parallel") == parallel_pattern
    assert storage.get_pattern("unknown") is None
    
    # Remove pattern
    storage.remove_pattern("test_seq")
    assert storage.get_pattern("test_seq") is None
    assert storage.pattern_count == 1

def test_pattern_type_indexing():
    """Test pattern type indexing"""
    storage = PatternStorage()
    
    # Store patterns
    seq_pattern = SequentialDelegationPattern(
        "test_seq",
        "Test Sequential Pattern",
        ["validate", "process", "store"]
    )
    storage.store_pattern(seq_pattern)
    
    parallel_pattern = ParallelCoordinationPattern(
        "test_parallel",
        "Test Parallel Pattern",
        {"cpu", "memory", "network"}
    )
    storage.store_pattern(parallel_pattern)
    
    # Get patterns by type
    seq_patterns = storage.get_patterns_by_type("SequentialDelegationPattern")
    assert len(seq_patterns) == 1
    assert seq_patterns[0] == seq_pattern
    
    parallel_patterns = storage.get_patterns_by_type("ParallelCoordinationPattern")
    assert len(parallel_patterns) == 1
    assert parallel_patterns[0] == parallel_pattern
    
    # Check unknown type
    assert not storage.get_patterns_by_type("UnknownType")
    
    # Check pattern types
    assert storage.pattern_types == {"SequentialDelegationPattern", "ParallelCoordinationPattern"}

def test_pattern_confidence_filtering():
    """Test pattern filtering by confidence"""
    storage = PatternStorage()
    
    # Create patterns
    seq_pattern = SequentialDelegationPattern(
        "test_seq",
        "Test Sequential Pattern",
        ["validate", "process", "store"]
    )
    parallel_pattern = ParallelCoordinationPattern(
        "test_parallel",
        "Test Parallel Pattern",
        {"cpu", "memory", "network"}
    )
    meta_pattern = MetaOrchestrationPattern(
        "test_meta",
        "Test Meta Pattern",
        {"auth", "data", "network"}
    )
    
    # Build different confidence levels
    seq_context = PatternContext(
        domain="test",
        agent_type="test",
        attributes={"required_steps": ["validate", "store"]}
    )
    
    # High confidence pattern (10 successes)
    for _ in range(10):
        seq_pattern.execute(seq_context)
        
    parallel_context = PatternContext(
        domain="test",
        agent_type="test",
        attributes={"required_resources": ["cpu"]}
    )
    
    # Medium confidence pattern (6 successes, 4 failures)
    for i in range(10):
        success = i < 6  # 60% success rate
        if success:
            parallel_pattern.execute(parallel_context)
        else:
            parallel_pattern.record_execution(False)
            
    # Low confidence pattern (no executions)
    # meta_pattern stays at 0% confidence
    
    # Store patterns (order matters for testing)
    storage.store_pattern(seq_pattern)      # High confidence
    storage.store_pattern(parallel_pattern)  # Medium confidence
    storage.store_pattern(meta_pattern)      # Low confidence
    
    # Filter by confidence
    high_conf = storage.get_patterns_by_confidence(ConfidenceLevel.HIGH)
    assert len(high_conf) == 1
    assert high_conf[0] == seq_pattern
    
    medium_conf = storage.get_patterns_by_confidence(ConfidenceLevel.MEDIUM)
    assert len(medium_conf) == 1
    assert parallel_pattern in medium_conf

def test_pattern_context_matching():
    """Test pattern matching by context"""
    storage = PatternStorage()
    
    # Store patterns
    seq_pattern = SequentialDelegationPattern(
        "test_seq",
        "Test Sequential Pattern",
        ["validate", "process", "store"]
    )
    storage.store_pattern(seq_pattern)
    
    parallel_pattern = ParallelCoordinationPattern(
        "test_parallel",
        "Test Parallel Pattern",
        {"cpu", "memory", "network"}
    )
    storage.store_pattern(parallel_pattern)
    
    # Test sequential context
    context = PatternContext(
        domain="test",
        agent_type="test",
        attributes={"required_steps": ["validate", "store"]}
    )
    matches = storage.find_matching_patterns(context)
    assert len(matches) == 1
    assert matches[0] == seq_pattern
    
    # Test parallel context
    context = PatternContext(
        domain="test",
        agent_type="test",
        attributes={"required_resources": ["cpu", "memory"]}
    )
    matches = storage.find_matching_patterns(context)
    assert len(matches) == 1
    assert matches[0] == parallel_pattern
    
    # Test non-matching context
    context = PatternContext(
        domain="test",
        agent_type="test",
        attributes={"required_steps": ["unknown"]}
    )
    matches = storage.find_matching_patterns(context)
    assert not matches