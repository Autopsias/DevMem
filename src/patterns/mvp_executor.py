from typing import Optional, List, Tuple
from .mvp_base import DelegationPattern, PatternContext, ConfidenceLevel
from .mvp_registry import PatternRegistry

class PatternExecutor:
    def __init__(self, registry: PatternRegistry):
        self.registry = registry
        
    def execute_pattern(self, pattern: DelegationPattern, 
                       context: PatternContext) -> Tuple[bool, str]:
        """Execute a specific pattern"""
        try:
            success = pattern.execute(context)
            pattern.record_execution(success)
            msg = "Pattern executed successfully" if success else "Pattern execution failed"
            return success, msg
        except Exception as e:
            pattern.record_execution(False)
            return False, f"Pattern execution error: {str(e)}"
            
    def execute_best_pattern(self, context: PatternContext) -> Tuple[bool, str]:
        """Find and execute best matching pattern"""
        pattern = self.registry.find_best_pattern(context)
        if not pattern:
            return False, "No matching pattern found"
            
        if pattern.confidence_level == ConfidenceLevel.LOW:
            return False, "Best pattern has low confidence"
            
        return self.execute_pattern(pattern, context)
        
    def execute_all_matching(self, context: PatternContext,
                           min_confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
                           ) -> List[Tuple[DelegationPattern, bool, str]]:
        """Execute all matching patterns meeting confidence threshold"""
        results = []
        matches = self.registry.find_matching_patterns(context)
        
        for pattern in matches:
            if pattern.confidence_level.value >= min_confidence.value:
                success, msg = self.execute_pattern(pattern, context)
                results.append((pattern, success, msg))
                
        return results