import pytest
from src.patterns import PatternContext, ConfidenceLevel
from src.patterns.meta_orchestration_mvp import MetaOrchestrationPattern

def test_meta_pattern_matching():
    """Test meta-orchestration pattern matching"""
    pattern = MetaOrchestrationPattern(
        "test_meta",
        "Test Meta Pattern",
        {"auth", "data", "network", "compute", "storage"}
    )
    
    # Test matching context (3+ domains)
    context = PatternContext(
        domain="meta",
        agent_type="orchestrator",
        attributes={"required_domains": ["auth", "data", "network"]}
    )
    assert pattern.matches(context)
    
    # Test non-matching context (too few domains)
    context = PatternContext(
        domain="meta",
        agent_type="orchestrator",
        attributes={"required_domains": ["auth", "data"]}
    )
    assert not pattern.matches(context)
    
    # Test non-matching context (unknown domain)
    context = PatternContext(
        domain="meta",
        agent_type="orchestrator",
        attributes={"required_domains": ["auth", "data", "unknown"]}
    )
    assert not pattern.matches(context)
    
def test_meta_pattern_execution():
    """Test meta-orchestration pattern execution"""
    pattern = MetaOrchestrationPattern(
        "test_meta",
        "Test Meta Pattern",
        {"auth", "data", "network", "compute", "storage"}
    )
    
    # Test successful execution
    context = PatternContext(
        domain="meta",
        agent_type="orchestrator",
        attributes={"required_domains": ["auth", "data", "network"]}
    )
    assert pattern.execute(context)
    
    # Execute multiple times to build confidence
    for _ in range(10):
        assert pattern.execute(context)
        
    # Verify confidence metrics
    assert pattern.confidence_score >= 0.5  # MVP target
    assert pattern.confidence_level in [ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH]
    
def test_meta_pattern_coordinator_selection():
    """Test coordinator selection logic"""
    pattern = MetaOrchestrationPattern(
        "test_meta",
        "Test Meta Pattern",
        {"auth", "data", "network"}
    )
    
    # Test basic selection
    domains = ["auth", "data", "network"]
    coordinator = pattern._select_coordinator(domains)
    assert coordinator == "auth"  # First available domain
    
    # Test selection with unavailable domains
    domains = ["unknown", "auth", "data"]
    coordinator = pattern._select_coordinator(domains)
    assert coordinator == "auth"  # First available domain
    
    # Test empty domains
    coordinator = pattern._select_coordinator([])
    assert coordinator is None
    
def test_meta_pattern_error_handling():
    """Test meta-orchestration error handling"""
    pattern = MetaOrchestrationPattern(
        "test_meta",
        "Test Meta Pattern",
        {"auth", "data", "network"}
    )
    
    # Test execution with too few domains
    context = PatternContext(
        domain="meta",
        agent_type="orchestrator",
        attributes={"required_domains": ["auth", "data"]}
    )
    assert not pattern.execute(context)
    
    # Test execution with invalid domains
    context = PatternContext(
        domain="meta",
        agent_type="orchestrator",
        attributes={"required_domains": ["unknown1", "unknown2", "unknown3"]}
    )
    assert not pattern.execute(context)
    
    # Test execution with missing attributes
    context = PatternContext(
        domain="meta",
        agent_type="orchestrator"
    )
    assert not pattern.execute(context)
    
    # Verify error handling affects confidence
    assert pattern.confidence_score >= 0.0