from dataclasses import dataclass
from typing import Dict, List, Optional
from .mvp_base import ConfidenceLevel

@dataclass
class ConfidenceThresholds:
    low_threshold: float = 0.5  # Below this is LOW
    high_threshold: float = 0.7  # Above this is HIGH
    min_executions: int = 5     # Minimum executions for valid confidence
    
    def validate(self) -> None:
        """Validate threshold configuration"""
        if not 0 <= self.low_threshold <= 1:
            raise ValueError("Low threshold must be between 0 and 1")
        if not 0 <= self.high_threshold <= 1:
            raise ValueError("High threshold must be between 1")
        if self.low_threshold >= self.high_threshold:
            raise ValueError("Low threshold must be less than high threshold")
        if self.min_executions < 1:
            raise ValueError("Minimum executions must be positive")

class ConfidenceScoring:
    def __init__(self, thresholds: Optional[ConfidenceThresholds] = None):
        self.thresholds = thresholds or ConfidenceThresholds()
        self.thresholds.validate()
        self._success_count = 0
        self._total_executions = 0
        self._history: List[bool] = []
        self._domain_scores: Dict[str, float] = {}
        self._domain_history: List[str] = []
        
    @property
    def confidence_score(self) -> float:
        """Calculate confidence score based on execution history"""
        if self._total_executions < self.thresholds.min_executions:
            return 0.0
        return self._success_count / self._total_executions if self._total_executions > 0 else 0.0
        
    @property
    def confidence_level(self) -> ConfidenceLevel:
        """Get confidence level based on score thresholds"""
        score = self.confidence_score
        if score >= self.thresholds.high_threshold:
            return ConfidenceLevel.HIGH
        elif score >= self.thresholds.low_threshold:
            return ConfidenceLevel.MEDIUM
        return ConfidenceLevel.LOW
        
    def record_execution(self, success: bool, domain: Optional[str] = None) -> None:
        """Record execution result with optional domain tracking"""
        self._total_executions += 1
        if success:
            self._success_count += 1
        self._history.append(success)
        
        # Update domain-specific scores
        if domain:
            self._domain_history.append(domain)
            count = sum(1 for d in self._domain_history if d == domain)
            successes = sum(1 for i, d in enumerate(self._domain_history) 
                          if d == domain and self._history[i])
            self._domain_scores[domain] = successes / count
            
    def get_domain_confidence(self, domain: str) -> float:
        """Get confidence score for specific domain"""
        return self._domain_scores.get(domain, 0.0)
        
    def reset_stats(self) -> None:
        """Reset all confidence statistics"""
        self._success_count = 0
        self._total_executions = 0
        self._history.clear()
        self._domain_scores.clear()
        self._domain_history.clear()
        
    @property
    def has_minimum_executions(self) -> bool:
        """Check if minimum executions threshold is met"""
        return self._total_executions >= self.thresholds.min_executions
        
    @property
    def success_rate(self) -> float:
        """Get raw success rate without minimum execution check"""
        return self._success_count / self._total_executions if self._total_executions > 0 else 0.0
        
    @property
    def total_executions(self) -> int:
        """Get total number of executions"""
        return self._total_executions