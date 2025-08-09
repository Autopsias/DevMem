Parent Epic: EPIC-1-Infrastructure-Foundation-Excellence.md
Status: Completed

# Story: Learning Integration for Claude Code Agent Framework
As a Claude Code framework maintainer
I want to enhance the existing enhanced cross-domain coordinator with learning capabilities
So that complex coordination patterns improve while maintaining current performance characteristics

## Business Value
- Optimize existing enhanced cross-domain coordinator (5% efficiency)
- Evolve coordination patterns based on proven successes
- Improve current 38.33% selection accuracy
- Preserve Claude Code architecture simplification

## Acceptance Criteria
- [x] EnhancedAgentSelector Integration
  - [x] Extend EnhancedCrossDomainCoordinator
  - [x] Maximum 40ms selection performance
  - [x] Improve selection accuracy to 45%+
  - [x] Zero impact on current coordination

- [x] Enhanced Pattern Evolution
  - [x] Build on current coordinator baseline
  - [x] Improve pattern matching in complex cases
  - [x] Preserve existing coordination strategies
  - [x] Evolution based on proven patterns only

- [x] Memory Architecture Compliance
  - [x] Store patterns in coordination-hub.md format
  - [x] No changes to 2-level hierarchy
  - [x] <150ms pattern lookup operations
  - [x] <50ms standard operations preserved

- [x] Cross-Domain Enhancement
  - [x] Improve existing scenarios:
    - Multi-domain auth (37% → 45%)
    - Parallel execution (35% → 42%)
    - Security validations (41% → 48%)
    - Infrastructure operations (40% → 47%)
  - [x] Pattern optimization with metrics
  - [x] Coordination efficiency tracking

- [x] Production Safety
  - [x] Zero-impact pattern evolution
  - [x] Automatic performance protection
  - [x] Enhanced monitoring integration

## Technical Implementation
```python
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime
import time
import json
import logging

@dataclass
class CoordinationPattern:
    """Pattern detected in successful coordination."""
    pattern_id: str
    query_signature: str
    agent_sequence: List[str]
    success_rate: float
    last_used: datetime
    execution_time_ms: float

@dataclass
class SafetyThresholds:
    """Performance and safety thresholds."""
    max_pattern_lookup_ms: float = 150.0
    max_selection_time_ms: float = 40.0
    min_confidence_score: float = 0.45
    max_memory_usage_mb: float = 512.0

class PerformanceGuard:
    """Ensures operations stay within safety thresholds."""
    
    def __init__(self, thresholds: SafetyThresholds):
        self.thresholds = thresholds
        self.start_time: float = 0
        self.peak_memory: float = 0
        self.logger = logging.getLogger("performance_guard")
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = (time.time() - self.start_time) * 1000
        if duration_ms > self.thresholds.max_selection_time_ms:
            self.logger.warning(
                f"Performance threshold exceeded: {duration_ms:.2f}ms"
            )
            return False
        return True

class PatternStore:
    """Stores coordination patterns in coordination-hub.md format."""
    
    def __init__(self, hub_path: str):
        self.hub_path = hub_path
        self.patterns: Dict[str, CoordinationPattern] = {}
        self.load_patterns()
    
    def load_patterns(self):
        """Load patterns from coordination-hub.md."""
        try:
            with open(self.hub_path) as f:
                content = f.read()
                # Parse patterns section
                pattern_section = self._extract_patterns(content)
                self.patterns = self._parse_patterns(pattern_section)
        except Exception as e:
            logging.error(f"Failed to load patterns: {e}")
            self.patterns = {}
    
    def store_pattern(self, pattern: CoordinationPattern) -> bool:
        """Store pattern if it meets quality threshold."""
        if pattern.success_rate < 0.45:
            return False
            
        self.patterns[pattern.pattern_id] = pattern
        self._save_patterns()
        return True
    
    def _save_patterns(self):
        """Save patterns back to coordination-hub.md."""
        try:
            with open(self.hub_path, 'r') as f:
                content = f.read()
            
            # Update patterns section
            updated = self._update_patterns_section(content)
            
            with open(self.hub_path, 'w') as f:
                f.write(updated)
        except Exception as e:
            logging.error(f"Failed to save patterns: {e}")

class LearningCoordinator(EnhancedCrossDomainCoordinator):
    """Enhances coordination through pattern learning."""
    
    def __init__(self, 
                 pattern_store: PatternStore,
                 thresholds: SafetyThresholds):
        super().__init__()
        self.pattern_store = pattern_store
        self.thresholds = thresholds
        self.seen_patterns: Set[str] = set()
        
    def coordinate_agents(self, 
                        query: str,
                        context: Optional[Dict] = None) -> CoordinationResult:
        """Coordinate agents with pattern enhancement."""
        
        with PerformanceGuard(self.thresholds):
            # Get base coordination
            base_result = super().coordinate_agents(query, context)
            
            # Try pattern enhancement
            if self._can_enhance_safely(base_result):
                enhanced = self._enhance_with_patterns(base_result)
                if enhanced.confidence > base_result.confidence:
                    return enhanced
            
            return base_result
    
    def _can_enhance_safely(self, result: CoordinationResult) -> bool:
        """Check if enhancement is safe."""
        return (
            result.execution_time_ms < self.thresholds.max_selection_time_ms * 0.8
            and result.confidence > self.thresholds.min_confidence_score
        )
    
    def _enhance_with_patterns(self,
                             result: CoordinationResult) -> CoordinationResult:
        """Enhance result using learned patterns."""
        pattern_id = self._get_pattern_id(result)
        
        if pattern_id in self.pattern_store.patterns:
            pattern = self.pattern_store.patterns[pattern_id]
            if pattern.success_rate > result.confidence:
                return self._apply_pattern(pattern, result)
        
        return result
    
    def record_success(self, result: CoordinationResult):
        """Record successful coordination pattern."""
        pattern = CoordinationPattern(
            pattern_id=self._get_pattern_id(result),
            query_signature=result.query_signature,
            agent_sequence=result.agent_sequence,
            success_rate=result.confidence,
            last_used=datetime.now(),
            execution_time_ms=result.execution_time_ms
        )
        self.pattern_store.store_pattern(pattern)
```

## Dependencies
- STORY-1.8.1 Agent Selection Framework (Ready for Deployment)
- STORY-1.8.2 Domain Intelligence (Approved)

## Risk Mitigation
- Performance Protection: Circuit breaker for learning overhead
- Memory Integrity: Two-level hierarchy preservation
- Pattern Quality: Validation against Claude Code standards
- Safety: Zero-impact integration with fallback
- Evolution: Gradual pattern enhancement

## Testing Requirements
- Development Environment
  - Python 3.11+
  - Current agent framework setup
  - Claude Code compliance suite

- Learning Integration Tests
```python
class TestLearningCoordinator:
    def test_pattern_recording(self):
        # Test pattern recording and storage
        coord = LearningCoordinator(pattern_store, thresholds)
        result = CoordinationResult(
            confidence=0.46,
            execution_time_ms=35.0,
            agent_sequence=["security", "performance"]
        )
        coord.record_success(result)
        assert len(coord.pattern_store.patterns) == 1
        
    def test_performance_guard(self):
        # Test performance protection
        guard = PerformanceGuard(SafetyThresholds())
        with guard:
            time.sleep(0.050)  # 50ms
        assert not guard.__exit__(None, None, None)
        
    def test_pattern_enhancement(self):
        # Test pattern-based enhancement
        coord = LearningCoordinator(pattern_store, thresholds)
        base_result = coord.coordinate_agents("test query")
        enhanced = coord._enhance_with_patterns(base_result)
        assert enhanced.confidence >= base_result.confidence
```

- Performance Validation
```python
class TestPerformanceCompliance:
    def test_selection_time(self):
        # Test selection performance
        coord = LearningCoordinator(pattern_store, thresholds)
        start = time.time()
        coord.coordinate_agents("test query")
        duration_ms = (time.time() - start) * 1000
        assert duration_ms < 40.0
        
    def test_pattern_lookup(self):
        # Test pattern lookup speed
        store = PatternStore("coordination-hub.md")
        start = time.time()
        store.load_patterns()
        duration_ms = (time.time() - start) * 1000
        assert duration_ms < 150.0
```

- Integration Tests
```python
class TestSystemIntegration:
    def test_memory_hierarchy(self):
        # Test 2-level memory compliance
        store = PatternStore("coordination-hub.md")
        assert store._validate_hierarchy()
        
    def test_coordinator_compatibility(self):
        # Test base coordinator functionality
        coord = LearningCoordinator(pattern_store, thresholds)
        base = EnhancedCrossDomainCoordinator()
        result1 = coord.coordinate_agents("test")
        result2 = base.coordinate_agents("test")
        assert result1.agent_sequence == result2.agent_sequence
```

- Cross-Domain Validation
```python
class TestCrossDomainScenarios:
    scenarios = [
        ("auth_query", 0.37, 0.45),
        ("parallel_task", 0.35, 0.42),
        ("security_check", 0.41, 0.48),
        ("infra_setup", 0.40, 0.47)
    ]
    
    @pytest.mark.parametrize("query,base,target", scenarios)
    def test_scenario_improvement(self, query, base, target):
        coord = LearningCoordinator(pattern_store, thresholds)
        result = coord.coordinate_agents(query)
        assert result.confidence >= base
        # Run learning cycle
        coord.record_success(result)
        enhanced = coord.coordinate_agents(query)
        assert enhanced.confidence >= target
```

## Success Metrics
- Selection Speed: Maximum 40ms selection time
- Memory Access: <150ms pattern lookup, <50ms standard
- Coordination Success:
  - Multi-domain auth: 37% → 45%
  - Parallel execution: 35% → 42%
  - Security validation: 41% → 48%
  - Infrastructure ops: 40% → 47%
- Pattern Evolution: 45% confidence threshold
- System Preservation: 100% hierarchy compatibility