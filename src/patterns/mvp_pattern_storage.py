from typing import Dict, List, Optional, Set
from .mvp_base import DelegationPattern, PatternContext
from .mvp_confidence import ConfidenceLevel

class PatternStorage:
    def __init__(self):
        self._patterns: Dict[str, DelegationPattern] = {}
        self._pattern_types: Dict[str, Set[str]] = {}
        
    def store_pattern(self, pattern: DelegationPattern) -> None:
        """Store a pattern in memory"""
        # Store the pattern itself
        self._patterns[pattern.name] = pattern
        
        # Index by pattern type
        pattern_type = pattern.__class__.__name__
        if pattern_type not in self._pattern_types:
            self._pattern_types[pattern_type] = set()
        self._pattern_types[pattern_type].add(pattern.name)
        
    def get_pattern(self, name: str) -> Optional[DelegationPattern]:
        """Retrieve a pattern by name"""
        return self._patterns.get(name)
        
    def get_patterns_by_type(self, pattern_type: str) -> List[DelegationPattern]:
        """Get all patterns of a specific type"""
        if pattern_type not in self._pattern_types:
            return []
        return [self._patterns[name] for name in self._pattern_types[pattern_type]]
        
    def get_patterns_by_confidence(self, min_level: ConfidenceLevel) -> List[DelegationPattern]:
        """Get patterns meeting minimum confidence threshold"""
        result = []
        for p in self._patterns.values():
            if not p._confidence.has_minimum_executions:
                continue
            if p.confidence_level == min_level:
                result.append(p)
        return result
        
    def find_matching_patterns(self, context: PatternContext) -> List[DelegationPattern]:
        """Find all patterns matching a context"""
        return [p for p in self._patterns.values() if p.matches(context)]
        
    def remove_pattern(self, name: str) -> None:
        """Remove a pattern from memory"""
        if name in self._patterns:
            pattern = self._patterns[name]
            pattern_type = pattern.__class__.__name__
            if pattern_type in self._pattern_types:
                self._pattern_types[pattern_type].discard(name)
            del self._patterns[name]
            
    @property
    def pattern_count(self) -> int:
        """Get total number of stored patterns"""
        return len(self._patterns)
        
    @property
    def pattern_types(self) -> Set[str]:
        """Get set of all pattern types"""
        return set(self._pattern_types.keys())