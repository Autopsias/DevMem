# Natural Delegation Pattern MVP API Reference

## Core Classes

### DelegationPattern (Abstract Base Class)
```python
class DelegationPattern:
    def __init__(self, name: str, description: str)
    
    @property
    def confidence_score(self) -> float
    
    @property
    def confidence_level(self) -> ConfidenceLevel
    
    def record_execution(self, success: bool, domain: Optional[str] = None)
    
    @abstractmethod
    def matches(self, context: PatternContext) -> bool
    
    @abstractmethod
    def execute(self, context: PatternContext) -> bool
    
    def reset_stats(self) -> None
```

### SequentialDelegationPattern
```python
class SequentialDelegationPattern(DelegationPattern):
    def __init__(self, name: str, description: str, agent_sequence: List[str])
    
    def matches(self, context: PatternContext) -> bool
    
    def execute(self, context: PatternContext) -> bool
```

### ParallelCoordinationPattern
```python
class ParallelCoordinationPattern(DelegationPattern):
    def __init__(self, name: str, description: str, resource_types: Set[str])
    
    def matches(self, context: PatternContext) -> bool
    
    def execute(self, context: PatternContext) -> bool
```

### MetaOrchestrationPattern
```python
class MetaOrchestrationPattern(DelegationPattern):
    def __init__(self, name: str, description: str, domains: Set[str])
    
    def matches(self, context: PatternContext) -> bool
    
    def execute(self, context: PatternContext) -> bool
```

## Helper Classes

### PatternContext
```python
@dataclass
class PatternContext:
    domain: str
    agent_type: str
    priority: int = 1
    attributes: Dict[str, Any] = None
```

### ConfidenceScoring
```python
class ConfidenceScoring:
    def __init__(self, thresholds: Optional[ConfidenceThresholds] = None)
    
    @property
    def confidence_score(self) -> float
    
    @property
    def confidence_level(self) -> ConfidenceLevel
    
    def record_execution(self, success: bool, domain: Optional[str] = None)
    
    def get_domain_confidence(self, domain: str) -> float
    
    def reset_stats(self) -> None
```

### PatternStorage
```python
class PatternStorage:
    def store_pattern(self, pattern: DelegationPattern) -> None
    
    def get_pattern(self, name: str) -> Optional[DelegationPattern]
    
    def get_patterns_by_type(self, pattern_type: str) -> List[DelegationPattern]
    
    def get_patterns_by_confidence(self, min_level: ConfidenceLevel) -> List[DelegationPattern]
    
    def find_matching_patterns(self, context: PatternContext) -> List[DelegationPattern]
    
    def remove_pattern(self, name: str) -> None
```

## Enums

### ConfidenceLevel
```python
class ConfidenceLevel(Enum):
    LOW = 0     # <0.5
    MEDIUM = 1  # 0.5-0.69
    HIGH = 2    # ≥0.7
```

## Usage Examples

### Sequential Pattern
```python
# Create sequential pattern
seq_pattern = SequentialDelegationPattern(
    "validation_flow",
    "Sequential validation workflow",
    ["validate", "process", "store"]
)

# Execute with context
context = PatternContext(
    domain="data",
    agent_type="sequential",
    attributes={"required_steps": ["validate", "store"]}
)
success = seq_pattern.execute(context)
```

### Parallel Pattern
```python
# Create parallel pattern
parallel_pattern = ParallelCoordinationPattern(
    "resource_manager",
    "Resource-based parallel execution",
    {"cpu", "memory", "network"}
)

# Execute with context
context = PatternContext(
    domain="system",
    agent_type="parallel",
    attributes={"required_resources": ["cpu", "memory"]}
)
success = parallel_pattern.execute(context)
```

### Meta-orchestration Pattern
```python
# Create meta pattern
meta_pattern = MetaOrchestrationPattern(
    "domain_coordinator",
    "Cross-domain orchestration",
    {"auth", "data", "network", "compute"}
)

# Execute with context
context = PatternContext(
    domain="system",
    agent_type="orchestrator",
    attributes={"required_domains": ["auth", "data", "network"]}
)
success = meta_pattern.execute(context)
```