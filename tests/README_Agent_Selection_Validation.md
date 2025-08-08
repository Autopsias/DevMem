# Agent Selection Validation Test Framework

A comprehensive test framework for validating agent selection patterns, measuring accuracy metrics, and providing detailed performance analysis.

## Overview

The Agent Selection Validation Framework provides:

1. **Pattern Accuracy Measurement** - Statistical validation of agent selection decisions
2. **Domain Coverage Validation** - Testing across all agent domains (testing, security, infrastructure, performance, code quality)
3. **Cross-validation Framework** - Robust validation with stratified sampling
4. **Performance Benchmarking** - Detailed metrics on response time and efficiency
5. **Edge Case Detection** - Validation of handling unusual or boundary conditions

## Framework Components

### Core Classes

- **`AgentSelectionTestFramework`** - Main framework orchestrating all validation
- **`DomainSpecificPatternGenerator`** - Generates realistic test patterns per domain
- **`EdgeCasePatternGenerator`** - Creates challenging edge case scenarios
- **`AgentSelectionValidator`** - Validates individual patterns and calculates metrics
- **`MockEnhancedSystem`** - Mock implementation for testing when actual system unavailable

### Data Structures

- **`TestPattern`** - Represents a test case with expected outcomes
- **`ValidationResult`** - Results from validating a single pattern
- **`ComprehensiveValidationReport`** - Complete analysis with recommendations

## Usage Examples

### Basic Framework Usage

```python
from tests.agent_selection_framework import AgentSelectionTestFramework

# Initialize framework
framework = AgentSelectionTestFramework()

# Run comprehensive validation
report = framework.run_comprehensive_validation()

# Print summary
framework.print_validation_summary(report)

# Save detailed report
framework.save_validation_report(report)
```

### Custom Pattern Testing

```python
from tests.agent_selection_framework import DomainSpecificPatternGenerator

# Generate specific domain patterns
generator = DomainSpecificPatternGenerator()
testing_patterns = generator.generate_patterns(count=10, domain="testing")

# Run validation on custom patterns
report = framework.run_comprehensive_validation(custom_patterns=testing_patterns)
```

### Running Demo Scripts

```bash
# Basic demonstration
python tests/run_agent_validation_demo.py --mode basic

# Performance benchmarking
python tests/run_agent_validation_demo.py --mode performance

# Edge case analysis
python tests/run_agent_validation_demo.py --mode edge-cases

# Detailed analysis with full reporting
python tests/run_agent_validation_demo.py --mode detailed
```

## Test Framework Features

### Pattern Generation

The framework generates diverse test patterns across:

- **5 Domain Categories**: testing, infrastructure, security, performance, code_quality
- **4 Complexity Levels**: basic, intermediate, advanced, edge_case  
- **4 Pattern Types**: explicit, implicit, contextual, ambiguous
- **Realistic Scenarios**: Based on actual development scenarios

### Validation Metrics

#### Accuracy Metrics
- **Agent Accuracy**: Correctness of agent selection (0.0-1.0)
- **Domain Accuracy**: Accuracy of domain detection using Jaccard index
- **Coordination Accuracy**: Correctness of coordination pattern detection
- **Overall Accuracy**: Weighted combination (50% agent, 30% domain, 20% coordination)

#### Performance Metrics
- **Response Time**: Agent selection latency in milliseconds
- **Processing Efficiency**: Inverse response time metric
- **Confidence Scores**: System confidence in selections

#### Statistical Metrics
- **Sample Size**: Number of patterns tested
- **Confidence Intervals**: 95% confidence intervals for accuracy
- **Statistical Power**: Adequacy of sample size
- **Cross-validation Consistency**: Stability across validation folds

### Reporting Capabilities

#### Pattern Type Analysis
```
PATTERN TYPE PERFORMANCE:
  EXPLICIT:
    Count: 30
    Accuracy: 85.67%
    Pass Rate: 73.33%
    Avg Response Time: 12.5ms
```

#### Complexity Level Analysis
```
COMPLEXITY LEVEL PERFORMANCE:
  EDGE_CASE:
    Count: 15
    Accuracy: 62.33%
    Pass Rate: 40.00%
    Fail Rate: 26.67%
```

#### Edge Case Handling
```
EDGE CASE HANDLING:
  Edge Case Count: 15
  Edge Case Accuracy: 62.33%
  Edge Case Pass Rate: 40.00%
  Edge Case Confidence Mean: 0.745
  Edge Case Response Time: 8.2ms
```

## Integration with Testing Pipeline

### Pytest Integration

The framework includes pytest fixtures and can be integrated into CI/CD pipelines:

```python
# tests/test_agent_selection_validation.py
def test_agent_selection_accuracy():
    framework = AgentSelectionTestFramework()
    report = framework.run_comprehensive_validation()
    
    # Assert minimum accuracy requirements
    assert report.overall_accuracy >= 0.90
    assert report.domain_coverage_score >= 0.85
```

### Continuous Integration

Add to CI pipeline for automated validation:

```yaml
# .github/workflows/agent-validation.yml
- name: Run Agent Selection Validation
  run: |
    python tests/run_agent_validation_demo.py --mode performance
    python -m pytest tests/test_agent_selection_validation.py -v
```

## Performance Characteristics

Based on benchmarking results:

- **Scalability**: Linear scaling with pattern count (>100k patterns/second)
- **Memory Usage**: Stable regardless of scale
- **Response Time**: Sub-millisecond per pattern validation
- **Accuracy**: 45-70% with mock system, designed for 90%+ with real system

## Validation Reports

### Generated Files

The framework generates detailed JSON reports in `tests/results/agent_selection/`:

- **comprehensive_validation_report_[timestamp].json** - Full validation results
- **demo_validation_report.json** - Demo run results

### Report Structure

```json
{
  "total_patterns_tested": 115,
  "overall_accuracy": 0.4591,
  "domain_coverage_score": 0.36,
  "pattern_type_performance": {...},
  "complexity_level_performance": {...},
  "edge_case_handling": {...},
  "performance_benchmarks": {...},
  "statistical_significance": {...},
  "improvement_recommendations": [...]
}
```

## Extension and Customization

### Adding New Domains

```python
# Extend DomainSpecificPatternGenerator
class CustomPatternGenerator(DomainSpecificPatternGenerator):
    def __init__(self):
        super().__init__()
        self.domain_templates["new_domain"] = [
            ("New domain pattern", "new-agent", ["new_domain"], "sequential"),
        ]
```

### Custom Validation Criteria

```python
# Custom validation criteria
pattern = TestPattern(
    # ... other fields ...
    validation_criteria={
        "agent_match_required": True,
        "domain_overlap_min": 0.9,  # Stricter requirement
        "coordination_match_required": True,
        "acceptable_alternatives": ["fallback-agent"]
    }
)
```

### Integration with Real Systems

```python
# Replace mock with real enhanced system
from your_system import RealEnhancedSystem

real_system = RealEnhancedSystem()
framework = AgentSelectionTestFramework(enhanced_system=real_system)
```

## Best Practices

1. **Regular Validation**: Run validation regularly during development
2. **Baseline Comparison**: Compare results against baseline metrics
3. **Edge Case Focus**: Pay special attention to edge case performance
4. **Domain Balance**: Ensure balanced testing across all domains
5. **Statistical Significance**: Use sufficient sample sizes (100+ patterns)

## Troubleshooting

### Common Issues

**Low Accuracy Scores**:
- Check pattern generation aligns with system expectations
- Verify domain mappings match system patterns
- Review validation criteria for appropriate thresholds

**Import Errors**:
- Ensure proper Python path setup
- Check dependencies are installed
- Verify test file structure

**Test Failures**:
- Review mock system behavior
- Adjust validation thresholds for testing environment
- Check pattern generation consistency

## Future Enhancements

1. **A/B Testing**: Compare different agent selection strategies
2. **Real-time Monitoring**: Integration with production monitoring
3. **Machine Learning**: Pattern learning from validation results
4. **Custom Metrics**: Domain-specific accuracy measurements
5. **Visual Reporting**: Graphical representation of results

## Contact and Support

For issues, enhancements, or questions about the Agent Selection Validation Framework, refer to the project documentation or create an issue in the repository.

---

**Note**: This framework is designed to validate agent selection patterns and provide comprehensive analysis. It includes mock implementations for testing purposes and can be extended with real systems for production validation.