from typing import Dict, List, Optional
from .mvp_base import DelegationPattern, PatternContext

class SequentialDelegationPattern(DelegationPattern):
    def __init__(self, name: str, description: str, agent_sequence: List[str]):
        super().__init__(name, description)
        self.agent_sequence = agent_sequence
        self._current_step = 0
        
    def matches(self, context: PatternContext) -> bool:
        """Check if this pattern matches the context"""
        # Match multi-step tasks with ordered agent types
        if not context.attributes:
            return False
            
        required_steps = context.attributes.get("required_steps", [])
        if not required_steps:
            return False
            
        # Check if our agent sequence can handle these steps
        return all(step in self.agent_sequence for step in required_steps)
        
    def execute(self, context: PatternContext) -> bool:
        """Execute the sequential delegation pattern"""
        try:
            # Reset step counter
            self._current_step = 0
            
            # Get required steps from context
            required_steps = context.attributes.get("required_steps", [])
            if not required_steps:
                return False
                
            # Verify all steps are in our sequence
            if not all(step in self.agent_sequence for step in required_steps):
                return False
                
            # Execute each step in sequence
            success = True
            for step in required_steps:
                if not self._execute_step(step, context):
                    success = False
                    break
                self._current_step += 1
                
            # Record execution result for each step domain
            for step in required_steps:
                self.record_execution(success, domain=step)
            return success
            
        except Exception:
            return False
            
    def _execute_step(self, step: str, context: PatternContext) -> bool:
        """Execute a single step in the sequence"""
        # In MVP, we just verify the step is in our sequence
        return step in self.agent_sequence