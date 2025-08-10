from typing import Dict, List, Set
from .mvp_base import DelegationPattern, PatternContext

class ParallelCoordinationPattern(DelegationPattern):
    def __init__(self, name: str, description: str, resource_types: Set[str]):
        super().__init__(name, description)
        self.resource_types = resource_types
        self._active_resources: Dict[str, int] = {res: 0 for res in resource_types}
        
    def matches(self, context: PatternContext) -> bool:
        """Check if this pattern matches the context"""
        if not context.attributes:
            return False
            
        # Get required resources from context
        required_resources = context.attributes.get("required_resources", [])
        if not required_resources:
            return False
            
        # Check if we can handle all required resource types
        return all(res in self.resource_types for res in required_resources)
        
    def execute(self, context: PatternContext) -> bool:
        """Execute parallel coordination pattern"""
        try:
            # Reset active resources
            self._active_resources = {res: 0 for res in self.resource_types}
            
            # Get required resources
            required_resources = context.attributes.get("required_resources", [])
            if not required_resources:
                return False
                
            # Allocate resources
            for resource in required_resources:
                if not self._allocate_resource(resource):
                    self.record_execution(False)
                    return False
                    
            # Execute parallel operations (simulated in MVP)
            success = self._execute_parallel_operations(required_resources)
            
            # Release resources
            for resource in required_resources:
                self._release_resource(resource)
                
            # Record execution result for each resource domain
            for resource in required_resources:
                self.record_execution(success, domain=resource)
            return success
            
        except Exception:
            self.record_execution(False)
            return False
            
    def _allocate_resource(self, resource: str) -> bool:
        """Allocate a resource for parallel execution"""
        if resource not in self.resource_types:
            return False
            
        self._active_resources[resource] += 1
        return True
        
    def _release_resource(self, resource: str) -> None:
        """Release an allocated resource"""
        if resource in self._active_resources:
            self._active_resources[resource] = max(0, self._active_resources[resource] - 1)
            
    def _execute_parallel_operations(self, resources: List[str]) -> bool:
        """Execute parallel operations on allocated resources"""
        # In MVP, we just verify resources are allocated
        return all(self._active_resources.get(res, 0) > 0 for res in resources)