import pytest
from src.patterns import ConfidenceLevel
from src.patterns.mvp_confidence import ConfidenceScoring, ConfidenceThresholds

def test_confidence_thresholds_validation():
    """Test confidence threshold validation"""
    # Test valid thresholds
    thresholds = ConfidenceThresholds(0.4, 0.8, 5)
    thresholds.validate()  # Should not raise
    
    # Test invalid low threshold
    with pytest.raises(ValueError):
        ConfidenceThresholds(-0.1, 0.8, 5).validate()
        
    # Test invalid high threshold
    with pytest.raises(ValueError):
        ConfidenceThresholds(0.4, 1.1, 5).validate()
        
    # Test invalid threshold ordering
    with pytest.raises(ValueError):
        ConfidenceThresholds(0.8, 0.4, 5).validate()
        
    # Test invalid minimum executions
    with pytest.raises(ValueError):
        ConfidenceThresholds(0.4, 0.8, 0).validate()

def test_confidence_scoring_basic():
    """Test basic confidence scoring"""
    scoring = ConfidenceScoring()
    
    # Test initial state
    assert scoring.confidence_score == 0.0
    assert scoring.confidence_level == ConfidenceLevel.LOW
    
    # Record some executions
    for _ in range(10):
        scoring.record_execution(True)
        
    assert scoring.confidence_score == 1.0
    assert scoring.confidence_level == ConfidenceLevel.HIGH
    
    # Record some failures
    for _ in range(10):
        scoring.record_execution(False)
        
    assert scoring.confidence_score == 0.5
    assert scoring.confidence_level == ConfidenceLevel.MEDIUM

def test_confidence_minimum_executions():
    """Test minimum executions requirement"""
    thresholds = ConfidenceThresholds(low_threshold=0.5, high_threshold=0.7, min_executions=5)
    scoring = ConfidenceScoring(thresholds)
    
    # Not enough executions
    for _ in range(4):
        scoring.record_execution(True)
        
    assert scoring.confidence_score == 0.0
    assert not scoring.has_minimum_executions
    
    # Add final execution to meet minimum
    scoring.record_execution(True)
    assert scoring.confidence_score == 1.0
    assert scoring.has_minimum_executions

def test_domain_specific_confidence():
    """Test domain-specific confidence tracking"""
    scoring = ConfidenceScoring()
    
    # Record domain-specific executions
    scoring.record_execution(True, domain="auth")
    scoring.record_execution(True, domain="auth")
    scoring.record_execution(False, domain="auth")
    
    scoring.record_execution(True, domain="data")
    scoring.record_execution(False, domain="data")
    
    assert scoring.get_domain_confidence("auth") == 2/3
    assert scoring.get_domain_confidence("data") == 0.5
    assert scoring.get_domain_confidence("unknown") == 0.0

def test_confidence_reset():
    """Test confidence statistics reset"""
    scoring = ConfidenceScoring()
    
    # Record some executions
    for _ in range(10):
        scoring.record_execution(True)
        
    assert scoring.confidence_score > 0.0
    assert scoring.total_executions == 10
    
    # Reset stats
    scoring.reset_stats()
    assert scoring.confidence_score == 0.0
    assert scoring.total_executions == 0
    assert scoring.get_domain_confidence("any") == 0.0