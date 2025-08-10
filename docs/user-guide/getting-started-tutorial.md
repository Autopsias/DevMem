# Getting Started with Natural Delegation Framework

## Welcome to Natural Delegation!

This tutorial will guide you through your first steps with the Natural Delegation Framework in 15 minutes. By the end, you'll have created and executed your first intelligent delegation pattern.

## What You'll Learn

- Set up your first delegation pattern
- Execute a simple workflow
- Monitor pattern performance
- Configure confidence scoring

## Prerequisites

- Python 3.8+ installed
- Basic understanding of Python
- 15 minutes of your time

## Step 1: Installation and Setup (3 minutes)

### Install the Framework

```bash
# Install from your project directory
cd /path/to/DevMem
pip install -e .

# Verify installation
python -c "from patterns import PatternRegistry; print('✅ Installation successful!')"
```

### Project Structure

After installation, your project should have:
```
your_project/
├── src/patterns/          # Core pattern implementations
├── docs/                  # Documentation (you're here!)
├── .claude/               # Claude Code integration
└── tests/                 # Test suite
```

## Step 2: Your First Pattern (5 minutes)

Let's create a simple "Hello World" workflow pattern:

### Create the Pattern

```python
# save as: tutorial_example.py

from patterns import (
    PatternRegistry, 
    PatternExecutor, 
    SequentialDelegationPattern,
    PatternContext
)

# 1. Initialize the framework
print("🚀 Initializing Natural Delegation Framework...")
registry = PatternRegistry()
executor = PatternExecutor(registry)

# 2. Create your first pattern
hello_pattern = SequentialDelegationPattern(
    name="hello_world_workflow",
    description="A simple introduction to delegation patterns",
    steps=[
        "greet_user",
        "show_capabilities", 
        "demonstrate_learning"
    ]
)

print(f"✅ Created pattern: {hello_pattern.name}")
print(f"📝 Description: {hello_pattern.description}")
print(f"🔢 Steps: {len(hello_pattern.steps)} steps defined")
```

### Register and Execute

```python
# 3. Register the pattern
registry.register_pattern(hello_pattern)
print(f"📋 Pattern registered successfully!")

# 4. Create execution context
context = PatternContext(
    domain="tutorial",
    agent_type="learning_assistant",
    priority=1,
    attributes={
        "user_level": "beginner",
        "tutorial_step": "first_pattern"
    }
)

print(f"🎯 Context created for domain: {context.domain}")

# 5. Execute the pattern
print("\n🎬 Executing your first pattern...")
try:
    result = executor.execute("hello_world_workflow", context)
    
    if result:
        print("✅ Pattern executed successfully!")
        print("🎉 Congratulations! You've completed your first delegation pattern.")
    else:
        print("❌ Pattern execution failed - but that's okay for learning!")
        
except Exception as e:
    print(f"ℹ️  Expected behavior: {e}")
    print("💡 This is normal for a tutorial - we haven't implemented the actual workflow steps yet")
```

### Run Your Example

```bash
python tutorial_example.py
```

**Expected Output:**
```
🚀 Initializing Natural Delegation Framework...
✅ Created pattern: hello_world_workflow
📝 Description: A simple introduction to delegation patterns
🔢 Steps: 3 steps defined
📋 Pattern registered successfully!
🎯 Context created for domain: tutorial
🎬 Executing your first pattern...
ℹ️  Expected behavior: NotImplementedError
💡 This is normal for a tutorial - we haven't implemented the actual workflow steps yet
```

## Step 3: Understanding Confidence Scoring (3 minutes)

Every pattern learns from execution results:

```python
# Add this to your tutorial_example.py

# Check initial confidence (will be low for new patterns)
print(f"\n📊 Pattern Analytics:")
print(f"   Confidence Score: {hello_pattern.confidence_score:.2f}")
print(f"   Confidence Level: {hello_pattern.confidence_level.name}")

# Simulate some learning by recording execution results
print(f"\n🧠 Simulating pattern learning...")

# Record successful executions
for i in range(5):
    hello_pattern.record_execution(success=True, domain="tutorial")
    print(f"   ✅ Execution {i+1} recorded as successful")

# Check improved confidence
print(f"\n📈 Updated Analytics:")
print(f"   Confidence Score: {hello_pattern.confidence_score:.2f}")
print(f"   Confidence Level: {hello_pattern.confidence_level.name}")
print(f"   Learning Progress: Pattern is getting smarter! 🎓")
```

## Step 4: Real-World Example (4 minutes)

Let's create a practical pattern for a common workflow:

```python
# Add this as: practical_example.py

from patterns import (
    PatternRegistry,
    PatternExecutor, 
    SequentialDelegationPattern,
    PatternContext
)

# Realistic workflow: Code Review Process
code_review_pattern = SequentialDelegationPattern(
    name="code_review_workflow",
    description="Automated code review and validation process",
    steps=[
        "static_analysis",      # Run linting and static analysis
        "security_scan",        # Check for security vulnerabilities  
        "test_execution",       # Run test suite
        "coverage_analysis",    # Analyze test coverage
        "approval_workflow"     # Route for human approval
    ]
)

# Initialize system
registry = PatternRegistry()
executor = PatternExecutor(registry)
registry.register_pattern(code_review_pattern)

# Create realistic context
context = PatternContext(
    domain="software_development",
    agent_type="code_reviewer",
    priority=2,
    attributes={
        "language": "python",
        "project_type": "web_api",
        "complexity": "medium",
        "security_level": "standard"
    }
)

print("🔍 Code Review Pattern Created")
print(f"📋 Pattern: {code_review_pattern.name}")
print(f"🎯 Domain: {context.domain}")
print(f"👥 Agent Type: {context.agent_type}")
print(f"🏷️  Attributes: {context.attributes}")

# This would integrate with actual tools in production
print("\n💼 In production, this pattern would:")
print("   • Run ruff/black for code formatting")
print("   • Execute security scanners") 
print("   • Run pytest with coverage")
print("   • Generate approval requests")
print("   • Track review metrics")
```

## Next Steps

### Explore More Patterns

Try different pattern types:

```python
from patterns import ParallelCoordinationPattern, MetaOrchestrationPattern

# Parallel pattern for independent tasks
parallel_pattern = ParallelCoordinationPattern(
    name="parallel_deployment", 
    description="Deploy multiple services simultaneously",
    tasks=["deploy_frontend", "deploy_backend", "deploy_database"],
    max_concurrent=3
)

# Meta-orchestration for complex scenarios
meta_pattern = MetaOrchestrationPattern(
    name="enterprise_migration",
    description="Orchestrate complex multi-phase migration",
    strategy={
        "phases": [
            {"name": "assess", "patterns": ["analysis"], "coordination": "sequential"},
            {"name": "migrate", "patterns": ["data_migration", "app_migration"], "coordination": "parallel"},
            {"name": "validate", "patterns": ["testing"], "coordination": "sequential"}
        ]
    }
)
```

### Configuration and Customization

```python
# Fine-tune pattern behavior
code_review_pattern.set_confidence_threshold(0.8)  # Require 80% confidence
code_review_pattern.set_learning_enabled(True)     # Enable continuous learning

# Global configuration
from patterns import PatternConfig
PatternConfig.set_global_confidence_threshold(0.75)
PatternConfig.set_learning_rate(0.1)
```

### Monitoring and Analytics

```python
# Monitor pattern performance
analytics = registry.get_pattern_analytics("code_review_workflow")
print(f"Success Rate: {analytics.success_rate:.2%}")
print(f"Average Response Time: {analytics.avg_response_time}ms")
print(f"Execution Count: {analytics.execution_count}")
```

## 🎯 Quick Reference Commands

```python
# Essential imports
from patterns import PatternRegistry, PatternExecutor, SequentialDelegationPattern, PatternContext

# Basic setup (2 lines)
registry = PatternRegistry()
executor = PatternExecutor(registry)

# Create pattern (4 lines)
pattern = SequentialDelegationPattern("name", "description", ["step1", "step2"])
registry.register_pattern(pattern)
context = PatternContext(domain="your_domain", agent_type="your_agent")
result = executor.execute("name", context)

# Check confidence (2 lines)
score = pattern.confidence_score
level = pattern.confidence_level
```

## Troubleshooting

### Common Issues

**Problem**: `ImportError: No module named 'patterns'`
**Solution**: Run `pip install -e .` from your project root

**Problem**: Pattern execution fails
**Solution**: This is expected in tutorial - patterns need actual implementation

**Problem**: Low confidence scores
**Solution**: Record successful executions with `pattern.record_execution(success=True)`

### Getting Help

- 📚 **Full Documentation**: `docs/user-guide/natural-delegation-complete-guide.md`
- 🔧 **API Reference**: `docs/api-reference/`
- 🐛 **Troubleshooting**: `docs/troubleshooting/`
- 💡 **Examples**: `examples/` directory

## What's Next?

1. **Complete User Guide**: Dive deeper into all pattern types and advanced features
2. **API Reference**: Detailed documentation of all classes and methods  
3. **Best Practices**: Learn optimization techniques and production patterns
4. **Custom Patterns**: Create your own specialized delegation patterns

**Congratulations! 🎉** You've completed the Natural Delegation Framework tutorial. You now understand the basics of pattern creation, execution, and learning. Ready to build intelligent workflows!