from typing import Dict, Any
import asyncio
from .base import PatternBase

class SequentialPattern(PatternBase):
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0.025)  # Simulate processing time
        return {"result": f"Processed {input_data['input']} sequentially"}
    
    def validate(self, input_data: Dict[str, Any]) -> None:
        if "input" not in input_data:
            raise ValueError("Sequential pattern requires 'input' field")