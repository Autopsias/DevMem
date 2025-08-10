from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class PatternBase(ABC):
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def validate(self, input_data: Dict[str, Any]) -> None:
        pass