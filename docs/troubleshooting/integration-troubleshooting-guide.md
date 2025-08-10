# Integration Troubleshooting Guide: Natural Delegation Framework

## Table of Contents

1. [Agent Framework Integration](#agent-framework-integration)
2. [Memory System Integration](#memory-system-integration)
3. [CI/CD Pipeline Integration](#cicd-pipeline-integration)
4. [Anthropic Compliance Issues](#anthropic-compliance-issues)
5. [Framework Compatibility Issues](#framework-compatibility-issues)
6. [Testing and Validation](#testing-and-validation)

---

## Agent Framework Integration

### Common Issues

#### Issue: Agent Selection Failures

```python
# Example error
"AgentSelectionError: Could not find suitable agent for domain 'web_development'"
```

**Troubleshooting Steps:**

1. **Verify Agent Directory Structure**
```bash
# Check agent directory structure
ls -R .claude/agents/

# Expected structure:
.claude/agents/
├── analysis-gateway.md       # Required primary agent
├── meta-coordinator.md       # Required for orchestration
├── test-specialist.md       # Testing domain agent
└── secondary/               # Optional secondary agents
```

2. **Validate Agent Configuration**
```python
from patterns import AgentValidator

validator = AgentValidator()
validation_result = validator.validate_agent_integration()

# Example validation
if not validation_result.is_valid:
    print("Agent validation failed:")
    for error in validation_result.errors:
        print(f"  ❌ {error.agent_name}: {error.message}")
```

3. **Check Agent Dependencies**
```python
# Verify agent dependencies
def check_agent_dependencies():
    """Check required agent dependencies."""
    
    required_agents = [
        "analysis-gateway",      # Core routing
        "meta-coordinator",      # Orchestration
        "test-specialist",       # Testing
        "code-quality"           # Quality checks
    ]
    
    missing_agents = []
    for agent in required_agents:
        if not os.path.exists(f".claude/agents/{agent}.md"):
            missing_agents.append(agent)
    
    if missing_agents:
        print("❌ Missing required agents:")
        for agent in missing_agents:
            print(f"  • {agent}")
        return False
    
    print("✅ All required agents present")
    return True
```

#### Issue: Agent Coordination Failures

```python
# Example error
"CoordinationError: Failed to maintain context across agent handoffs"
```

**Troubleshooting Steps:**

1. **Check Coordination Hub**
```python
class CoordinationHubValidator:
    """Validates coordination hub integration."""
    
    def __init__(self):
        self.hub_path = ".claude/memory/coordination-hub.md"
        
    def validate_hub(self):
        """Validate coordination hub structure and content."""
        
        if not os.path.exists(self.hub_path):
            print("❌ Coordination hub missing")
            self.create_hub_template()
            return False
        
        # Check hub sections
        required_sections = [
            "Pattern Registry",
            "Active Patterns",
            "Learning Statistics",
            "Domain Intelligence"
        ]
        
        with open(self.hub_path, 'r') as f:
            content = f.read()
            
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            print("❌ Missing required hub sections:")
            for section in missing_sections:
                print(f"  • {section}")
            return False
        
        print("✅ Coordination hub validated")
        return True
```

2. **Test Agent Communication**
```python
def test_agent_communication():
    """Test communication between agents."""
    
    from patterns import (
        AgentCommunicationTester,
        TestMessage,
        CommunicationChannel
    )
    
    tester = AgentCommunicationTester()
    
    # Test basic message passing
    test_message = TestMessage(
        source="analysis-gateway",
        target="test-specialist",
        content="test_request",
        priority=1
    )
    
    channel = CommunicationChannel()
    result = tester.test_message_delivery(test_message, channel)
    
    if result.delivered:
        print(f"✅ Message delivered: {result.latency_ms}ms")
    else:
        print(f"❌ Delivery failed: {result.error}")
```

3. **Monitor Context Preservation**
```python
# Context preservation monitoring
class ContextPreservationMonitor:
    """Monitors context preservation across agent handoffs."""
    
    def __init__(self):
        self.context_snapshots = {}
        
    def take_snapshot(self, agent_name: str, context: Dict):
        """Take context snapshot before agent handoff."""
        snapshot_id = str(uuid.uuid4())
        self.context_snapshots[snapshot_id] = {
            'agent': agent_name,
            'context': context.copy(),
            'timestamp': time.time()
        }
        return snapshot_id
    
    def verify_context(self, snapshot_id: str, current_context: Dict) -> bool:
        """Verify context preservation after handoff."""
        if snapshot_id not in self.context_snapshots:
            return False
            
        original = self.context_snapshots[snapshot_id]['context']
        
        # Compare critical fields
        for key in ['domain', 'priority', 'attributes']:
            if key in original and key in current_context:
                if original[key] != current_context[key]:
                    print(f"❌ Context mismatch in {key}:")
                    print(f"  Original: {original[key]}")
                    print(f"  Current:  {current_context[key]}")
                    return False
        
        return True
```

---

## Memory System Integration

### Common Issues

#### Issue: Memory Access Failures

```python
# Example error
"MemoryAccessError: Failed to read pattern data from .claude/memory/"
```

**Troubleshooting Steps:**

1. **Validate Memory System Structure**
```python
class MemorySystemValidator:
    """Validates memory system integration."""
    
    def __init__(self):
        self.memory_root = ".claude/memory"
        
    def validate_structure(self):
        """Validate memory system directory structure."""
        
        required_paths = [
            "patterns/",           # Pattern storage
            "coordination-hub.md", # Coordination hub
            "learning_data/",      # Learning history
            "performance_data/"    # Performance metrics
        ]
        
        for path in required_paths:
            full_path = os.path.join(self.memory_root, path)
            if not os.path.exists(full_path):
                print(f"❌ Missing required path: {path}")
                return False
        
        print("✅ Memory system structure validated")
        return True
```

2. **Test Memory Access**
```python
def test_memory_access():
    """Test memory system read/write operations."""
    
    from patterns import MemoryAccessTester
    
    tester = MemoryAccessTester()
    
    # Test pattern storage
    pattern_result = tester.test_pattern_storage()
    print(f"Pattern Storage: {'✅' if pattern_result.success else '❌'}")
    print(f"  Write Speed: {pattern_result.write_speed_ms}ms")
    print(f"  Read Speed: {pattern_result.read_speed_ms}ms")
    
    # Test learning data
    learning_result = tester.test_learning_storage()
    print(f"Learning Storage: {'✅' if learning_result.success else '❌'}")
    print(f"  Write Speed: {learning_result.write_speed_ms}ms")
    print(f"  Read Speed: {learning_result.read_speed_ms}ms")
```

3. **Check Memory Consistency**
```python
def check_memory_consistency():
    """Check consistency of memory system data."""
    
    from patterns import MemoryConsistencyChecker
    
    checker = MemoryConsistencyChecker()
    
    # Check pattern data consistency
    pattern_issues = checker.check_pattern_consistency()
    if pattern_issues:
        print("❌ Pattern consistency issues found:")
        for issue in pattern_issues:
            print(f"  • {issue}")
    
    # Check learning data consistency
    learning_issues = checker.check_learning_consistency()
    if learning_issues:
        print("❌ Learning data consistency issues found:")
        for issue in learning_issues:
            print(f"  • {issue}")
```

---

## CI/CD Pipeline Integration

### Common Issues

#### Issue: Pipeline Integration Failures

```python
# Example error
"PipelineError: Failed to validate pattern system in CI environment"
```

**Troubleshooting Steps:**

1. **Validate CI Configuration**
```python
class CIPipelineValidator:
    """Validates CI pipeline integration."""
    
    def validate_ci_config(self):
        """Validate CI pipeline configuration."""
        
        # Check GitHub Actions workflow
        workflow_path = ".github/workflows/pattern-validation.yml"
        if not os.path.exists(workflow_path):
            print("❌ Missing pattern validation workflow")
            return False
        
        # Validate workflow content
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
            
        required_jobs = [
            "pattern-validation",
            "memory-system-check",
            "agent-integration-test"
        ]
        
        for job in required_jobs:
            if job not in workflow['jobs']:
                print(f"❌ Missing required job: {job}")
                return False
        
        print("✅ CI pipeline configuration validated")
        return True
```

2. **Test Pipeline Steps**
```python
def test_pipeline_steps():
    """Test individual pipeline validation steps."""
    
    from patterns import PipelineTester
    
    tester = PipelineTester()
    
    # Test pattern validation
    validation_result = tester.test_pattern_validation()
    print(f"Pattern Validation: {'✅' if validation_result.success else '❌'}")
    if not validation_result.success:
        print(f"  Error: {validation_result.error}")
    
    # Test memory system check
    memory_result = tester.test_memory_system()
    print(f"Memory System: {'✅' if memory_result.success else '❌'}")
    if not memory_result.success:
        print(f"  Error: {memory_result.error}")
    
    # Test agent integration
    agent_result = tester.test_agent_integration()
    print(f"Agent Integration: {'✅' if agent_result.success else '❌'}")
    if not agent_result.success:
        print(f"  Error: {agent_result.error}")
```

3. **Monitor Pipeline Health**
```python
class PipelineHealthMonitor:
    """Monitors CI pipeline health."""
    
    def check_pipeline_health(self):
        """Check overall pipeline health."""
        
        # Get recent pipeline runs
        from patterns import GitHubAPI
        
        github = GitHubAPI()
        recent_runs = github.get_workflow_runs(limit=10)
        
        # Calculate success rate
        success_count = sum(1 for run in recent_runs if run.conclusion == 'success')
        success_rate = success_count / len(recent_runs)
        
        print(f"Pipeline Health Status:")
        print(f"  Success Rate: {success_rate:.1%}")
        print(f"  Recent Runs: {len(recent_runs)}")
        
        if success_rate < 0.8:
            print("⚠️ Pipeline success rate below 80%")
            self.analyze_failures(recent_runs)
    
    def analyze_failures(self, runs):
        """Analyze pipeline failures."""
        
        failure_patterns = {}
        for run in runs:
            if run.conclusion == 'failure':
                error = run.get_error_message()
                failure_patterns[error] = failure_patterns.get(error, 0) + 1
        
        if failure_patterns:
            print("\nCommon Failure Patterns:")
            for error, count in failure_patterns.items():
                print(f"  • {error}: {count} occurrences")
```

---

## Anthropic Compliance Issues

### Common Issues

#### Issue: Compliance Validation Failures

```python
# Example error
"ComplianceError: Pattern system violates Anthropic Claude Code guidelines"
```

**Troubleshooting Steps:**

1. **Run Compliance Check**
```python
def check_anthropic_compliance():
    """Check compliance with Anthropic guidelines."""
    
    from patterns import (
        AnthropicComplianceChecker,
        ComplianceRule,
        ValidationResult
    )
    
    checker = AnthropicComplianceChecker()
    
    # Define compliance rules
    rules = [
        ComplianceRule(
            name="agent_directory_structure",
            description="Validate agent directory structure",
            severity="critical"
        ),
        ComplianceRule(
            name="memory_integration",
            description="Check memory system integration",
            severity="critical"
        ),
        ComplianceRule(
            name="pattern_naming",
            description="Verify pattern naming conventions",
            severity="warning"
        )
    ]
    
    # Run compliance check
    results = checker.check_compliance(rules)
    
    # Report results
    critical_failures = [r for r in results if r.severity == "critical" and not r.passed]
    warnings = [r for r in results if r.severity == "warning" and not r.passed]
    
    if critical_failures:
        print("❌ Critical compliance failures:")
        for failure in critical_failures:
            print(f"  • {failure.rule_name}: {failure.message}")
            
    if warnings:
        print("⚠️ Compliance warnings:")
        for warning in warnings:
            print(f"  • {warning.rule_name}: {warning.message}")
    
    return len(critical_failures) == 0
```

2. **Validate Pattern Compliance**
```python
def validate_pattern_compliance():
    """Validate pattern compliance with Anthropic guidelines."""
    
    from patterns import PatternComplianceValidator
    
    validator = PatternComplianceValidator()
    
    # Check all patterns
    for pattern in registry.get_all_patterns():
        result = validator.validate_pattern(pattern)
        
        if not result.is_compliant:
            print(f"❌ Non-compliant pattern: {pattern.name}")
            print("  Violations:")
            for violation in result.violations:
                print(f"    • {violation}")
            
            print("  Recommendations:")
            for recommendation in result.recommendations:
                print(f"    • {recommendation}")
```

3. **Fix Common Issues**
```python
def fix_compliance_issues():
    """Fix common compliance issues."""
    
    from patterns import ComplianceFixer
    
    fixer = ComplianceFixer()
    
    # Fix directory structure
    structure_fixes = fixer.fix_directory_structure()
    if structure_fixes:
        print("✅ Fixed directory structure issues:")
        for fix in structure_fixes:
            print(f"  • {fix}")
    
    # Fix pattern naming
    naming_fixes = fixer.fix_pattern_naming()
    if naming_fixes:
        print("✅ Fixed pattern naming issues:")
        for fix in naming_fixes:
            print(f"  • {fix}")
    
    # Fix memory integration
    memory_fixes = fixer.fix_memory_integration()
    if memory_fixes:
        print("✅ Fixed memory integration issues:")
        for fix in memory_fixes:
            print(f"  • {fix}")
```

---

## Framework Compatibility Issues

### Common Issues

#### Issue: Version Compatibility

```python
# Example error
"CompatibilityError: Pattern system requires Claude Code framework version >=2.0"
```

**Troubleshooting Steps:**

1. **Check Framework Compatibility**
```python
def check_framework_compatibility():
    """Check Claude Code framework compatibility."""
    
    from patterns import FrameworkValidator
    
    validator = FrameworkValidator()
    
    # Check version compatibility
    version_check = validator.check_version_compatibility()
    if not version_check.is_compatible:
        print("❌ Framework version incompatible:")
        print(f"  Required: {version_check.required_version}")
        print(f"  Current: {version_check.current_version}")
        print("\nRecommended actions:")
        for action in version_check.recommended_actions:
            print(f"  • {action}")
        return False
    
    # Check feature compatibility
    feature_check = validator.check_feature_compatibility()
    if not feature_check.all_features_supported:
        print("⚠️ Some features not supported:")
        for feature, status in feature_check.feature_status.items():
            if not status.supported:
                print(f"  • {feature}: {status.message}")
                
    return version_check.is_compatible
```

2. **Validate Integration Points**
```python
def validate_integration_points():
    """Validate framework integration points."""
    
    from patterns import IntegrationValidator
    
    validator = IntegrationValidator()
    
    # Check required integration points
    integration_points = [
        "agent_framework",
        "memory_system",
        "pattern_registry",
        "execution_engine"
    ]
    
    for point in integration_points:
        result = validator.check_integration_point(point)
        if not result.is_valid:
            print(f"❌ Invalid integration: {point}")
            print("  Issues:")
            for issue in result.issues:
                print(f"    • {issue}")
            print("  Fix:")
            print(f"    {result.fix_instructions}")
```

3. **Test Framework Features**
```python
def test_framework_features():
    """Test required framework features."""
    
    from patterns import FeatureTester
    
    tester = FeatureTester()
    
    # Required features
    features = [
        "agent_selection",
        "pattern_learning",
        "memory_access",
        "context_preservation"
    ]
    
    for feature in features:
        result = tester.test_feature(feature)
        print(f"Testing {feature}:")
        
        if result.success:
            print(f"  ✅ Feature working")
            print(f"    Performance: {result.performance_stats}")
        else:
            print(f"  ❌ Feature failed")
            print(f"    Error: {result.error}")
            print(f"    Debug info: {result.debug_info}")
```

---

## Testing and Validation

### Integration Test Suite

```python
#!/usr/bin/env python3
# save as: integration_test_suite.py

"""
Comprehensive integration test suite for the Natural Delegation Framework.
"""

import unittest
from patterns import (
    PatternRegistry,
    PatternExecutor,
    MemorySystem,
    AgentFramework
)

class IntegrationTestSuite(unittest.TestCase):
    """Integration test suite."""
    
    def setUp(self):
        """Set up test environment."""
        self.registry = PatternRegistry()
        self.executor = PatternExecutor(self.registry)
        self.memory = MemorySystem()
        self.framework = AgentFramework()
    
    def test_end_to_end_flow(self):
        """Test complete end-to-end integration flow."""
        
        # 1. Create test pattern
        pattern = create_test_pattern()
        self.registry.register_pattern(pattern)
        
        # 2. Execute with framework
        context = create_test_context()
        result = self.executor.execute(pattern.name, context)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.execution_id)
        
        # 3. Verify memory storage
        stored_data = self.memory.get_execution_data(result.execution_id)
        self.assertIsNotNone(stored_data)
        
        # 4. Check learning update
        learning_data = pattern.get_learning_data()
        self.assertGreater(len(learning_data), 0)
        
        # 5. Validate agent integration
        agent_result = self.framework.get_agent_result(result.execution_id)
        self.assertTrue(agent_result.success)
    
    def test_error_handling(self):
        """Test error handling across integration points."""
        
        # 1. Test invalid pattern
        with self.assertRaises(ValidationError):
            self.registry.register_pattern(create_invalid_pattern())
        
        # 2. Test memory errors
        with self.assertRaises(MemoryAccessError):
            self.memory.read_invalid_path()
        
        # 3. Test framework errors
        with self.assertRaises(FrameworkError):
            self.framework.execute_invalid_request()
    
    def test_performance_requirements(self):
        """Test performance across integration points."""
        
        # 1. Pattern selection speed
        start_time = time.time()
        pattern = self.registry.get_pattern("test_pattern")
        selection_time = time.time() - start_time
        
        self.assertLess(selection_time, 0.1)  # 100ms max
        
        # 2. Memory access speed
        start_time = time.time()
        self.memory.read_test_data()
        access_time = time.time() - start_time
        
        self.assertLess(access_time, 0.025)  # 25ms max
        
        # 3. Framework overhead
        start_time = time.time()
        self.framework.execute_test_request()
        framework_time = time.time() - start_time
        
        self.assertLess(framework_time, 0.2)  # 200ms max
    
    def test_compliance_requirements(self):
        """Test compliance requirements."""
        
        # 1. Directory structure
        structure = self.framework.validate_directory_structure()
        self.assertTrue(structure.is_valid)
        
        # 2. Memory integration
        memory_compliance = self.memory.check_compliance()
        self.assertTrue(memory_compliance.is_compliant)
        
        # 3. Pattern validation
        pattern = create_test_pattern()
        validation = self.registry.validate_pattern_compliance(pattern)
        self.assertTrue(validation.is_compliant)
    
    def tearDown(self):
        """Clean up test environment."""
        self.registry.cleanup()
        self.memory.cleanup()
        self.framework.cleanup()

if __name__ == "__main__":
    unittest.main()
```

This comprehensive integration troubleshooting guide covers all major aspects of the Natural Delegation Framework's integration points, including agent framework integration, memory system integration, CI/CD pipeline integration, and compliance validation. The guide provides detailed troubleshooting steps, code examples, and validation tools for maintaining integration health and resolving common issues.