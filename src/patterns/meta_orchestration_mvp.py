from typing import Dict, List, Set, Optional
from .mvp_base import DelegationPattern, PatternContext

class MetaOrchestrationPattern(DelegationPattern):
    def __init__(self, name: str, description: str, domains: Set[str]):
        super().__init__(name, description)
        self.domains = domains
        self._coordinator: Optional[str] = None
        
    def matches(self, context: PatternContext) -> bool:
        """Check if this pattern matches the context"""
        if not context.attributes:
            return False
            
        # For meta-orchestration, we need 3+ domains
        required_domains = context.attributes.get("required_domains", [])
        if len(required_domains) < 3:
            return False
            
        # Check if we can handle the required domains
        return all(domain in self.domains for domain in required_domains)
        
    def execute(self, context: PatternContext) -> bool:
        """Execute meta-orchestration pattern"""
        try:
            # Get required domains
            required_domains = context.attributes.get("required_domains", [])
            if len(required_domains) < 3:
                return False
                
            # Select coordinator domain
            self._coordinator = self._select_coordinator(required_domains)
            if not self._coordinator:
                return False
                
            # Execute meta-orchestration
            success = self._execute_orchestration(required_domains)
            
            # Record execution result for each domain and coordinator
            if self._coordinator:
                self.record_execution(success, domain=self._coordinator)
            for domain in required_domains:
                if domain != self._coordinator:
                    self.record_execution(success, domain=domain)
            return success
            
        except Exception:
            self.record_execution(False)
            return False
            
    def _select_coordinator(self, domains: List[str]) -> Optional[str]:
        """Select most suitable domain to act as coordinator"""
        if not domains:
            return None
            
        # In MVP, select domain with highest priority (first in list)
        for domain in domains:
            if domain in self.domains:
                return domain
                
        return None
        
    def _execute_orchestration(self, domains: List[str]) -> bool:
        """Execute orchestration across domains"""
        try:
            if not self._coordinator:
                return False
                
            # In MVP, verify coordinator can oversee all domains
            return all(domain in self.domains for domain in domains)
            
        except Exception:
            return False