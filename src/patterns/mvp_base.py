from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from enum import Enum

class ConfidenceLevel(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
        
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
        
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
        
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

@dataclass
class PatternContext:
    domain: str
    agent_type: str
    priority: int = 1
    attributes: Dict[str, Any] = None

from .mvp_confidence import ConfidenceScoring

class DelegationPattern(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._confidence = ConfidenceScoring()
        
    @property
    def confidence_score(self) -> float:
        """Get confidence score from scoring system"""
        return self._confidence.confidence_score
        
    @property
    def confidence_level(self) -> ConfidenceLevel:
        """Get confidence level from scoring system"""
        return self._confidence.confidence_level
        
    def record_execution(self, success: bool, domain: Optional[str] = None) -> None:
        """Record execution result in scoring system"""
        self._confidence.record_execution(success, domain)
            
    @abstractmethod
    def matches(self, context: PatternContext) -> bool:
        """Check if pattern matches given context"""
        pass
        
    @abstractmethod
    def execute(self, context: PatternContext) -> bool:
        """Execute pattern with given context"""
        pass
        
    def reset_stats(self) -> None:
        """Reset execution statistics"""
        self._confidence.reset_stats()