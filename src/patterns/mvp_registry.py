from typing import Dict, List, Optional
from .mvp_base import DelegationPattern, PatternContext, ConfidenceLevel

class PatternRegistry:
    def __init__(self):
        self._patterns: Dict[str, DelegationPattern] = {}
        
    def register(self, pattern: DelegationPattern) -> None:
        """Register a new pattern"""
        if pattern.name in self._patterns:
            raise ValueError(f"Pattern {pattern.name} already registered")
        self._patterns[pattern.name] = pattern
        
    def unregister(self, name: str) -> None:
        """Unregister a pattern"""
        if name not in self._patterns:
            raise ValueError(f"Pattern {name} not found")
        del self._patterns[name]
        
    def get_pattern(self, name: str) -> DelegationPattern:
        """Get pattern by name"""
        if name not in self._patterns:
            raise ValueError(f"Pattern {name} not found")
        return self._patterns[name]
        
    def find_matching_patterns(self, context: PatternContext) -> List[DelegationPattern]:
        """Find all patterns matching given context"""
        return [p for p in self._patterns.values() if p.matches(context)]
        
    def find_best_pattern(self, context: PatternContext) -> Optional[DelegationPattern]:
        """Find best matching pattern based on confidence"""
        matches = self.find_matching_patterns(context)
        if not matches:
            return None
            
        # Sort by confidence score and return highest
        return max(matches, key=lambda p: p.confidence_score)
        
    def find_patterns_by_confidence(self, min_level: ConfidenceLevel) -> List[DelegationPattern]:
        """Find patterns meeting minimum confidence threshold"""
        return [p for p in self._patterns.values() 
                if p.confidence_level.value >= min_level.value]