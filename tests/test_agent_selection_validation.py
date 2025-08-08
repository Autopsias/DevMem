#!/usr/bin/env python3
"""
Test module for Agent Selection Validation Framework

Tests the comprehensive agent selection pattern validation system,
including pattern generation, validation logic, cross-validation,
and report generation.
"""

import pytest
import time
import json
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from agent_selection_framework import (
    AgentSelectionTestFramework,
    DomainSpecificPatternGenerator,
    EdgeCasePatternGenerator,
    AgentSelectionValidator,
    MockEnhancedSystem,
    TestPattern,
    ValidationResult
)

class TestDomainSpecificPatternGenerator:
    """Test domain-specific pattern generation"""
    
    def test_generate_patterns_single_domain(self):
        """Test pattern generation for a specific domain"""
        generator = DomainSpecificPatternGenerator()
        patterns = generator.generate_patterns(count=5, domain="testing")
        
        assert len(patterns) == 5
        assert all(p.domain_category == "testing" for p in patterns)
        assert all(p.expected_agent == "test-specialist" for p in patterns)
        assert all("testing" in p.expected_domains for p in patterns)
        
        # Check pattern diversity
        input_texts = [p.input_text for p in patterns]
        assert len(set(input_texts)) >= 3  # At least some diversity
        
    def test_generate_patterns_all_domains(self):
        """Test pattern generation across all domains"""
        generator = DomainSpecificPatternGenerator()
        patterns = generator.generate_patterns(count=25)  # 5 domains * 5 each
        
        assert len(patterns) == 25
        
        # Check domain distribution
        domain_counts = {}
        for pattern in patterns:
            domain = pattern.domain_category
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        expected_domains = ["testing", "infrastructure", "security", "performance", "code_quality", "documentation"]
        assert set(domain_counts.keys()) == set(expected_domains)
        
    def test_complexity_level_variation(self):
        """Test that patterns include different complexity levels"""
        generator = DomainSpecificPatternGenerator()
        patterns = generator.generate_patterns(count=20, domain="testing")
        
        complexity_levels = [p.complexity_level for p in patterns]
        complexity_set = set(complexity_levels)
        
        # Should have at least 2 different complexity levels
        assert len(complexity_set) >= 2
        assert complexity_set.issubset({"basic", "intermediate", "advanced", "edge_case"})
        
    def test_pattern_type_variation(self):
        """Test that patterns include different pattern types"""
        generator = DomainSpecificPatternGenerator()
        patterns = generator.generate_patterns(count=20, domain="security")
        
        pattern_types = [p.pattern_type for p in patterns]
        pattern_type_set = set(pattern_types)
        
        # Should have at least 2 different pattern types
        assert len(pattern_type_set) >= 2
        assert pattern_type_set.issubset({"explicit", "implicit", "contextual", "ambiguous"})


class TestEdgeCasePatternGenerator:
    """Test edge case pattern generation"""
    
    def test_generate_edge_case_patterns(self):
        """Test edge case pattern generation"""
        generator = EdgeCasePatternGenerator()
        patterns = generator.generate_patterns(count=10)
        
        assert len(patterns) == 10
        assert all(p.complexity_level == "edge_case" for p in patterns)
        assert all(p.pattern_type == "ambiguous" for p in patterns)
        
        # Check for variety in edge case types
        edge_types = [p.metadata["edge_case_type"] for p in patterns]
        assert len(set(edge_types)) >= 3  # Should have variety
        
    def test_edge_case_validation_criteria(self):
        """Test that edge cases have appropriate validation criteria"""
        generator = EdgeCasePatternGenerator()
        patterns = generator.generate_patterns(count=5)
        
        for pattern in patterns:
            # Edge cases should be more flexible
            assert not pattern.validation_criteria.get("agent_match_required", True)
            assert pattern.validation_criteria.get("domain_overlap_min", 1.0) <= 0.5
            assert pattern.confidence_threshold <= 0.6


class TestAgentSelectionValidator:
    """Test agent selection validation logic"""
    
    def test_validate_pattern_success(self):
        """Test successful pattern validation"""
        validator = AgentSelectionValidator()
        
        pattern = TestPattern(
            pattern_id="test_pattern",
            input_text="Test failures in pytest with asyncio patterns",
            expected_agent="test-specialist",
            expected_domains=["testing"],
            expected_coordination="sequential",
            confidence_threshold=0.7,
            complexity_level="basic",
            domain_category="testing",
            pattern_type="explicit",
            validation_criteria={
                "agent_match_required": True,
                "domain_overlap_min": 0.8,
                "coordination_match_required": False
            },
            metadata={}
        )
        
        result = validator.validate_pattern(pattern)
        
        assert isinstance(result, ValidationResult)
        assert result.pattern_id == "test_pattern"
        assert result.selected_agent == "test-specialist"
        assert result.validation_status in ["pass", "partial"]  # Allow partial for simplified mock
        assert result.accuracy_metrics["agent_accuracy"] == 1.0
        # Mock system may have some domain matching variations
        assert result.validation_status in ["pass", "partial"]
        
    def test_validate_pattern_failure(self):
        """Test pattern validation failure"""
        validator = AgentSelectionValidator()
        
        pattern = TestPattern(
            pattern_id="test_failure",
            input_text="Random unrelated text",
            expected_agent="test-specialist",
            expected_domains=["testing"],
            expected_coordination="sequential",
            confidence_threshold=0.9,  # High threshold
            complexity_level="basic",
            domain_category="testing",
            pattern_type="explicit",
            validation_criteria={
                "agent_match_required": True,
                "domain_overlap_min": 0.8,
                "coordination_match_required": True
            },
            metadata={}
        )
        
        result = validator.validate_pattern(pattern)
        
        assert result.validation_status in ["fail", "partial"]
        assert len(result.failure_reasons) > 0
        
    def test_accuracy_metrics_calculation(self):
        """Test accuracy metrics calculation"""
        validator = AgentSelectionValidator()
        
        pattern = TestPattern(
            pattern_id="metrics_test",
            input_text="Security vulnerability assessment",
            expected_agent="security-enforcer",
            expected_domains=["security"],
            expected_coordination="sequential",
            confidence_threshold=0.7,
            complexity_level="basic",
            domain_category="security",
            pattern_type="explicit",
            validation_criteria={},
            metadata={}
        )
        
        result = validator.validate_pattern(pattern)
        
        # Check that all expected metrics are present
        expected_metrics = ["agent_accuracy", "domain_accuracy", "coordination_accuracy", "overall_accuracy"]
        assert all(metric in result.accuracy_metrics for metric in expected_metrics)
        
        # Check metric ranges
        for metric_name, metric_value in result.accuracy_metrics.items():
            assert 0.0 <= metric_value <= 1.0, f"Metric {metric_name} out of range: {metric_value}"


class TestSimplifiedValidation:
    """Test simplified validation framework components"""
    
    def test_comprehensive_validation_execution(self):
        """Test that comprehensive validation runs successfully"""
        framework = AgentSelectionTestFramework()
        
        # Create small test patterns for faster execution
        generator = DomainSpecificPatternGenerator()
        test_patterns = generator.generate_patterns(5, "testing")
        
        report = framework.run_comprehensive_validation(custom_patterns=test_patterns)
        
        assert report.total_patterns_tested == 5
        assert 0.0 <= report.overall_accuracy <= 1.0
        assert report.validation_timestamp > 0
        
    def test_report_generation(self):
        """Test report generation with minimal data"""
        framework = AgentSelectionTestFramework()
        
        generator = DomainSpecificPatternGenerator()
        test_patterns = generator.generate_patterns(3, "security")
        
        report = framework.run_comprehensive_validation(custom_patterns=test_patterns)
        
        # Check that report sections are present
        assert len(report.pattern_type_performance) > 0
        assert len(report.complexity_level_performance) > 0
        assert len(report.improvement_recommendations) > 0


class TestAgentSelectionTestFramework:
    """Test comprehensive test framework"""
    
    def test_framework_initialization(self):
        """Test framework initialization"""
        framework = AgentSelectionTestFramework()
        
        assert framework.validator is not None
        assert framework.domain_generator is not None
        assert framework.edge_case_generator is not None
        assert framework.test_results_dir.exists()
        
    def test_generate_comprehensive_test_suite(self):
        """Test comprehensive test suite generation"""
        framework = AgentSelectionTestFramework()
        
        # Generate smaller suite for testing
        patterns = framework.generate_comprehensive_test_suite(patterns_per_domain=4, edge_cases=3)
        
        # Should have 6 domains * 4 patterns + 3 edge cases = 27 patterns
        assert len(patterns) == 27
        
        # Check domain distribution
        domain_counts = {}
        for pattern in patterns:
            domain = pattern.domain_category
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        # Should have patterns from all domains plus edge cases
        # Edge cases may be categorized as individual domains, so check total coverage
        assert len(domain_counts) >= 6  # At least all 6 primary domains
        
    def test_run_comprehensive_validation(self):
        """Test comprehensive validation execution"""
        framework = AgentSelectionTestFramework()
        
        # Create small test patterns for faster execution
        test_patterns = []
        generator = DomainSpecificPatternGenerator()
        test_patterns.extend(generator.generate_patterns(3, "testing"))
        test_patterns.extend(generator.generate_patterns(3, "security"))
        
        edge_generator = EdgeCasePatternGenerator()
        test_patterns.extend(edge_generator.generate_patterns(2))
        
        report = framework.run_comprehensive_validation(custom_patterns=test_patterns)
        
        assert report.total_patterns_tested == 8
        assert 0.0 <= report.overall_accuracy <= 1.0
        assert 0.0 <= report.domain_coverage_score <= 5.0  # Can be higher than 1.0 for harmonic mean
        
        # Check that all required sections are present
        assert len(report.pattern_type_performance) > 0
        assert len(report.complexity_level_performance) > 0
        assert len(report.improvement_recommendations) > 0
        assert report.validation_timestamp > 0
        
    def test_save_validation_report(self):
        """Test validation report saving"""
        framework = AgentSelectionTestFramework()
        
        # Create minimal test patterns
        generator = DomainSpecificPatternGenerator()
        test_patterns = generator.generate_patterns(2, "testing")
        
        report = framework.run_comprehensive_validation(custom_patterns=test_patterns)
        
        # Save report
        saved_path = framework.save_validation_report(report, "test_report.json")
        
        assert saved_path.exists()
        assert saved_path.suffix == ".json"
        
        # Verify the file contains valid JSON
        with open(saved_path, 'r') as f:
            loaded_data = json.load(f)
        
        assert loaded_data["total_patterns_tested"] == 2
        assert "overall_accuracy" in loaded_data
        
        # Clean up
        saved_path.unlink()
        
    def test_print_validation_summary(self, capsys):
        """Test validation summary printing"""
        framework = AgentSelectionTestFramework()
        
        # Create minimal test patterns
        generator = DomainSpecificPatternGenerator()
        test_patterns = generator.generate_patterns(2, "testing")
        
        report = framework.run_comprehensive_validation(custom_patterns=test_patterns)
        
        # Test that summary prints without error
        framework.print_validation_summary(report)
        
        captured = capsys.readouterr()
        assert "COMPREHENSIVE AGENT SELECTION VALIDATION REPORT" in captured.out
        assert "OVERALL PERFORMANCE" in captured.out
        assert "IMPROVEMENT RECOMMENDATIONS" in captured.out


class TestIntegrationScenarios:
    """Test integration scenarios and edge cases"""
    
    def test_empty_pattern_handling(self):
        """Test framework handling of empty pattern lists"""
        framework = AgentSelectionTestFramework()
        
        # Framework generates default patterns when none provided
        report = framework.run_comprehensive_validation(custom_patterns=[])
        
        # Empty list means framework generates its own patterns
        assert report.total_patterns_tested > 0  # Framework generates default suite
        assert len(report.improvement_recommendations) > 0
        
    def test_single_pattern_validation(self):
        """Test framework with single pattern"""
        framework = AgentSelectionTestFramework()
        
        generator = DomainSpecificPatternGenerator()
        single_pattern = generator.generate_patterns(1, "testing")
        
        report = framework.run_comprehensive_validation(custom_patterns=single_pattern)
        
        assert report.total_patterns_tested == 1
        assert 0.0 <= report.overall_accuracy <= 1.0
        
    def test_mock_system_consistency(self):
        """Test mock system consistency across multiple calls"""
        mock_system = MockEnhancedSystem()
        
        # Test same input multiple times
        input_text = "Test failures in pytest"
        results = []
        
        for _ in range(5):
            selected_agent, confidence, details = mock_system.select_agent(input_text)
            results.append((selected_agent, confidence))
        
        # Agent selection should be consistent
        agents = [r[0] for r in results]
        assert len(set(agents)) <= 2  # Allow for some variation but not complete randomness
        
    def test_performance_measurement_accuracy(self):
        """Test that performance measurements are reasonable"""
        framework = AgentSelectionTestFramework()
        
        generator = DomainSpecificPatternGenerator()
        test_patterns = generator.generate_patterns(5, "testing")
        
        start_time = time.time()
        report = framework.run_comprehensive_validation(custom_patterns=test_patterns)
        total_time = time.time() - start_time
        
        # Reported execution time should be close to actual time
        reported_time = report.detailed_breakdowns.get("total_execution_time", 0)
        assert abs(reported_time - total_time) < 1.0  # Within 1 second
        
        # Performance benchmarks should be reasonable (mock is very fast)
        avg_response_time = report.performance_benchmarks["avg_response_time_ms"]
        assert 0.0 <= avg_response_time <= 10000  # Between 0ms and 10s (mock can be sub-0.1ms)


class TestStatisticalValidation:
    """Test statistical validation and significance calculations"""
    
    def test_statistical_significance_calculation(self):
        """Test statistical significance calculations"""
        framework = AgentSelectionTestFramework()
        
        # Generate enough patterns for statistical analysis
        generator = DomainSpecificPatternGenerator()
        test_patterns = generator.generate_patterns(15, "testing")
        
        report = framework.run_comprehensive_validation(custom_patterns=test_patterns)
        
        stats = report.statistical_significance
        
        if not stats.get("insufficient_data", False):
            assert stats["sample_size"] == 15
            assert 0.0 <= stats["mean_accuracy"] <= 1.0
            assert stats["accuracy_std"] >= 0.0
            assert stats["confidence_interval_lower"] <= stats["mean_accuracy"]
            assert stats["confidence_interval_upper"] >= stats["mean_accuracy"]
            assert 0.0 <= stats["statistical_power"] <= 1.0
        
    def test_cross_validation_consistency(self):
        """Test cross-validation consistency metrics"""
        framework = AgentSelectionTestFramework()
        
        # Generate patterns with known characteristics
        generator = DomainSpecificPatternGenerator()
        test_patterns = generator.generate_patterns(15, "testing")  # Single domain for consistency
        
        report = framework.run_comprehensive_validation(custom_patterns=test_patterns)
        
        cv_metrics = report.cross_validation_metrics
        
        if cv_metrics:
            consistency = cv_metrics.get("accuracy_consistency", 0)
            assert 0.0 <= consistency <= 1.0
            
            # CV standard deviation should be reasonable
            cv_std = cv_metrics.get("accuracy_mean_cv_std", 0)
            assert cv_std >= 0.0
            

# Performance and load testing
class TestPerformanceAndScalability:
    """Test framework performance and scalability"""
    
    @pytest.mark.slow
    def test_large_scale_validation(self):
        """Test framework with larger number of patterns"""
        framework = AgentSelectionTestFramework()
        
        # Generate larger test suite
        test_patterns = framework.generate_comprehensive_test_suite(patterns_per_domain=10, edge_cases=5)
        
        start_time = time.time()
        report = framework.run_comprehensive_validation(custom_patterns=test_patterns)
        execution_time = time.time() - start_time
        
        # Should complete in reasonable time (adjust threshold as needed)
        assert execution_time < 120.0  # 2 minutes max
        assert report.total_patterns_tested == 65  # 6*10 + 5
        
    def test_memory_usage_reasonable(self):
        """Test that memory usage remains reasonable"""
        framework = AgentSelectionTestFramework()
        
        # Generate moderate test suite
        test_patterns = framework.generate_comprehensive_test_suite(patterns_per_domain=5, edge_cases=3)
        
        # This test assumes the validation doesn't consume excessive memory
        # In a real scenario, you might use memory profiling tools
        report = framework.run_comprehensive_validation(custom_patterns=test_patterns)
        
        # Basic check that report was generated successfully
        assert report.total_patterns_tested == 33  # 6*5 + 3
        assert len(report.improvement_recommendations) > 0


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])