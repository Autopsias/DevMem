# Natural Delegation Pattern MVP Troubleshooting Guide

## Common Issues and Solutions

### 1. Pattern Matching Failures

#### Symptoms
- No matching patterns found
- Pattern execution not triggered
- Unexpected pattern selection

#### Solutions
1. Verify Context Properties
```python
# Check context attributes
print(f"Domain: {context.domain}")
print(f"Agent Type: {context.agent_type}")
print(f"Attributes: {context.attributes}")
```

2. Check Pattern Registration
```python
# Verify pattern exists
pattern = registry.get_pattern("your_pattern")
if not pattern:
    print("Pattern not registered")

# List all registered patterns
all_patterns = storage.pattern_types
print(f"Registered types: {all_patterns}")
```

3. Test Pattern Matching
```python
# Test matching directly
matches = pattern.matches(context)
if not matches:
    print("Pattern doesn't match context")
```

### 2. Confidence Scoring Issues

#### Symptoms
- Low confidence despite successes
- Unexpected confidence levels
- Pattern selection bias

#### Solutions
1. Check Execution History
```python
# Print confidence metrics
print(f"Score: {pattern.confidence_score}")
print(f"Level: {pattern.confidence_level}")
print(f"Minimum executions met: {pattern._confidence.has_minimum_executions}")
```

2. Reset Statistics
```python
# Reset pattern stats
pattern.reset_stats()

# Rebuild confidence with known successes
context = PatternContext(...)
for _ in range(10):
    pattern.execute(context)
```

3. Verify Thresholds
```python
from patterns import ConfidenceThresholds

# Check threshold configuration
thresholds = ConfidenceThresholds(
    low_threshold=0.5,
    high_threshold=0.7,
    min_executions=5
)
thresholds.validate()
```

### 3. Resource Management Problems

#### Symptoms
- Resource leaks
- Allocation failures
- Parallel execution issues

#### Solutions
1. Check Resource State
```python
# Print active resources
print(f"Active resources: {pattern._active_resources}")

# Verify resource types
print(f"Available types: {pattern.resource_types}")
```

2. Release Resources
```python
# Release specific resource
pattern._release_resource("cpu")

# Reset all resources
pattern._active_resources = {res: 0 for res in pattern.resource_types}
```

3. Monitor Allocations
```python
# Track resource allocation
before = pattern._active_resources.copy()
success = pattern.execute(context)
after = pattern._active_resources.copy()

print(f"Before: {before}")
print(f"After: {after}")
```

### 4. Memory Integration Issues

#### Symptoms
- Pattern retrieval failures
- Missing patterns
- Inconsistent state

#### Solutions
1. Verify Storage State
```python
# Check pattern count
print(f"Stored patterns: {storage.pattern_count}")

# List pattern types
print(f"Pattern types: {storage.pattern_types}")
```

2. Test Pattern Access
```python
# Try direct retrieval
pattern = storage.get_pattern("pattern_name")
if not pattern:
    print("Pattern not found in storage")

# List patterns by type
type_patterns = storage.get_patterns_by_type("PatternType")
print(f"Found {len(type_patterns)} patterns")
```

3. Check Registry Sync
```python
# Compare registry and storage
reg_pattern = registry.get_pattern("pattern_name")
stored_pattern = storage.get_pattern("pattern_name")

if reg_pattern != stored_pattern:
    print("Registry and storage out of sync")
```

## Performance Issues

### 1. Slow Pattern Lookup

#### Diagnosis
```python
from patterns.performance_measurement import PerformanceMeasurement

perf = PerformanceMeasurement()

@perf.measure("pattern_lookup")
def find_pattern(name):
    return storage.get_pattern(name)

# Check performance
perf.assert_performance("pattern_lookup", max_avg_ms=100)
```

### 2. Memory Access Delays

#### Diagnosis
```python
@perf.measure("memory_access")
def access_patterns():
    return storage.find_matching_patterns(context)

# Verify access time
perf.assert_performance("memory_access", max_avg_ms=50)
```

## Validation Issues

### 1. Pattern Validation

#### Verification Steps
```python
def validate_pattern(pattern, context):
    # Check basic properties
    assert pattern.name, "Pattern missing name"
    assert pattern.description, "Pattern missing description"
    
    # Verify matching
    assert pattern.matches(context), "Pattern doesn't match context"
    
    # Test execution
    success = pattern.execute(context)
    assert success, "Pattern execution failed"
```

### 2. Integration Validation

#### Verification Steps
```python
def validate_integration():
    # Check storage
    assert storage.pattern_count > 0, "No patterns stored"
    
    # Verify registry
    pattern = registry.get_pattern("test_pattern")
    assert pattern, "Pattern not registered"
    
    # Test confidence
    assert pattern.confidence_score >= 0, "Invalid confidence"
```

## Error Messages

### Common Error Messages

1. "Pattern {name} already registered"
   - Cause: Duplicate pattern registration
   - Solution: Use unique pattern names or unregister first

2. "No matching pattern found"
   - Cause: Context doesn't match any patterns
   - Solution: Check context attributes and pattern matching logic

3. "Pattern execution error"
   - Cause: Exception during pattern execution
   - Solution: Check pattern implementation and context validity

4. "Invalid confidence thresholds"
   - Cause: Threshold configuration error
   - Solution: Verify threshold values and ordering