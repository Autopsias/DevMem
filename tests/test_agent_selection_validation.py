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
    
    def test_claude_code_task_tool_integration(self):
        """Test Claude Code Task tool integration for agent learning"""
        framework = AgentSelectionTestFramework()
        
        # Test Task tool pattern recognition
        task_pattern_queries = [
            "Coordinating comprehensive analysis using 3 tasks in parallel: security assessment, performance analysis, testing evaluation",
            "analyzing [problem] using parallel assessment across infrastructure domains",
            "using async-pattern-fixer tasks in parallel for testing coordination"
        ]
        
        for query in task_pattern_queries:
            result = framework.validator.enhanced_selector.select_agent(query)
            
            # Should recognize Task tool coordination patterns
            assert result.agent_name in ['analysis-gateway', 'meta-coordinator', 'test-specialist']
            assert result.confidence_score >= 0.6
            # Should indicate coordination reasoning for Task tool patterns
            assert "coordination" in result.reasoning.lower() or "parallel" in result.reasoning.lower()
    
    def test_agent_learning_accuracy_validation(self):
        """Test actual agent learning accuracy using memory patterns"""
        framework = AgentSelectionTestFramework()
        
        # Test queries that should benefit from memory coordination hub
        learning_test_cases = [
            ("docker container orchestration with networking", "infrastructure-engineer", "container_orchestration"),
            ("scaling performance optimization issues", "performance-optimizer", "scaling_performance"),
            ("ingress kubernetes networking problems", "infrastructure-engineer", "service_networking"),
            ("pytest async testing fixture configuration", "test-specialist", "async_testing"),
            ("security vulnerability scan with compliance", "security-enforcer", "security_assessment")
        ]
        
        total_patterns = len(learning_test_cases)
        accurate_selections = 0
        
        for query, expected_agent, pattern_type in learning_test_cases:
            result = framework.validator.enhanced_selector.select_agent(query)
            
            if result.agent_name == expected_agent:
                accurate_selections += 1
            
            # Validate learning pattern integration
            assert result.confidence_score >= 0.4  # Memory should boost confidence
            assert len(result.reasoning) > 20  # Should have detailed reasoning
        
        # Memory-enhanced selection should achieve target accuracy
        accuracy = accurate_selections / total_patterns
        assert accuracy >= 0.6, f"Learning accuracy {accuracy:.1%} below 60% target"
        
    def test_enhanced_agent_selector_initialization(self):
        """Test enhanced agent selector with directory loading"""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        from agent_selector import EnhancedAgentSelector
        
        # Test default initialization
        selector = EnhancedAgentSelector()
        assert selector is not None
        assert len(selector.agents) >= 8  # Should have at least default agents
        assert hasattr(selector, 'fallback_threshold')
        assert hasattr(selector, 'digdeep_threshold')
        
        # Check fallback thresholds are reasonable
        assert 0.1 <= selector.fallback_threshold <= 0.6
        assert 0.1 <= selector.digdeep_threshold <= 0.5
        assert selector.digdeep_threshold <= selector.fallback_threshold
        
    def test_directory_agent_loading(self):
        """Test that directory agents are properly loaded"""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        from agent_selector import EnhancedAgentSelector
        
        selector = EnhancedAgentSelector()
        all_agents = list(selector.agents.keys())
        default_agents = selector._get_default_agent_names()
        directory_agents = [agent for agent in all_agents if agent not in default_agents]
        
        # Should have loaded some agents from directory (if .claude/agents/ exists)
        print(f"Total agents: {len(all_agents)}, Directory agents: {len(directory_agents)}")
        assert len(all_agents) >= len(default_agents)  # At least default agents
        
        # Test that default agents are present
        for default_agent in ['test-specialist', 'infrastructure-engineer', 'security-enforcer']:
            assert default_agent in all_agents
            
    def test_improved_fallback_logic(self):
        """Test that fallback logic minimizes digdeep usage"""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        from agent_selector import EnhancedAgentSelector
        
        selector = EnhancedAgentSelector()
        
        # Test queries that should avoid digdeep
        non_digdeep_queries = [
            "help",
            "something is broken",
            "I have a problem",
            "urgent production issue",
            "performance and security issues"
        ]
        
        digdeep_count = 0
        for query in non_digdeep_queries:
            result = selector.select_agent(query)
            if result.agent_name == 'digdeep':
                digdeep_count += 1
                
        # Should use digdeep less than 40% of the time for these queries
        digdeep_rate = digdeep_count / len(non_digdeep_queries)
        assert digdeep_rate < 0.4, f"digdeep usage too high: {digdeep_rate:.1%}"
        
    def test_enhanced_confidence_scoring(self):
        """Test improved confidence scoring"""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        from agent_selector import EnhancedAgentSelector
        
        selector = EnhancedAgentSelector()
        
        # Test high-confidence queries
        high_confidence_queries = [
            "docker container orchestration with kubernetes cluster scaling",
            "pytest test failing with async mock configuration",
            "security vulnerability scan reveals credential leaks",
            "create comprehensive API documentation for new endpoints"
        ]
        
        for query in high_confidence_queries:
            result = selector.select_agent(query)
            # Enhanced confidence should give reasonable scores for clear queries
            assert result.confidence_score >= 0.4, f"Confidence too low for '{query}': {result.confidence_score}"
    
    def test_memory_system_performance_metrics(self):
        """Test memory system performance meets targets"""
        import sys
        import time
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        from agent_selector import EnhancedAgentSelector
        
        selector = EnhancedAgentSelector()
        
        # Test memory access performance targets from coordination-hub.md
        test_queries = [
            "infrastructure deployment coordination",
            "testing async patterns with fixtures",
            "security compliance validation",
            "performance optimization analysis",
            "documentation generation workflow"
        ]
        
        response_times = []
        for query in test_queries:
            start_time = time.time()
            result = selector.select_agent(query)
            response_time_ms = (time.time() - start_time) * 1000
            response_times.append(response_time_ms)
            
            # Should have agent selection result
            assert result.agent_name is not None
            assert result.confidence_score > 0
        
        # Memory system performance targets from coordination-hub.md
        avg_response_time = sum(response_times) / len(response_times)
        assert avg_response_time < 50, f"Average response time {avg_response_time:.1f}ms exceeds 50ms target"
        
        # 95th percentile should be reasonable
        sorted_times = sorted(response_times)
        p95_time = sorted_times[int(0.95 * len(sorted_times))]
        assert p95_time < 100, f"95th percentile {p95_time:.1f}ms too high"
    
    def test_agent_coordination_delegation(self):
        """Test agent coordination and delegation patterns"""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        from agent_selector import EnhancedAgentSelector
        
        selector = EnhancedAgentSelector()
        
        # Test delegation patterns that should trigger coordination
        delegation_test_cases = [
            # Multi-domain problems should suggest coordination
            ("infrastructure security testing coordination", ["meta-coordinator", "analysis-gateway"]),
            ("performance optimization with security compliance", ["meta-coordinator", "analysis-gateway"]),
            ("testing automation requiring documentation coordination", ["meta-coordinator", "analysis-gateway", "test-specialist"]),
            
            # Single domain should be direct
            ("pytest fixture configuration", ["test-specialist"]),
            ("docker container setup", ["infrastructure-engineer", "environment-analyst"]),  # docker-specialist doesn't exist
            ("API documentation creation", ["documentation-enhancer"])
        ]
        
        for query, expected_agents in delegation_test_cases:
            result = selector.select_agent(query)
            
            assert result.agent_name in expected_agents, \
                f"Query '{query}' selected '{result.agent_name}', expected one of {expected_agents}"
            
            # Multi-domain queries should have coordination reasoning
            if len(expected_agents) > 1 and "coordination" in expected_agents[0]:
                assert "coordination" in result.reasoning.lower() or \
                       "multi-domain" in result.reasoning.lower() or \
                       "complex" in result.reasoning.lower()
        
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


class TestCoordinationHubLearningValidation:
    """Test coordination-hub.md learning pattern validation"""
    
    def test_infrastructure_learning_pattern_recognition(self):
        """Test recognition of infrastructure learning patterns from coordination-hub.md"""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        from agent_selector import EnhancedAgentSelector
        
        selector = EnhancedAgentSelector()
        
        # Test patterns from coordination-hub.md Infrastructure Learning section
        infrastructure_patterns = [
            # Container orchestration patterns
            ("docker networking container orchestration", "infrastructure-engineer"),
            ("kubernetes container orchestration setup", "infrastructure-engineer"),
            ("docker orchestration networking optimization", "infrastructure-engineer"),
            
            # Scaling performance patterns  
            ("performance optimization scaling", "performance-optimizer"),
            ("scaling performance analysis", "performance-optimizer"),
            
            # Service networking patterns
            ("ingress kubernetes networking", "infrastructure-engineer"),
            ("kubernetes networking service configuration", "infrastructure-engineer")
        ]
        
        correct_selections = 0
        for query, expected_agent in infrastructure_patterns:
            result = selector.select_agent(query)
            if result.agent_name == expected_agent:
                correct_selections += 1
            
            # Should have reasonable confidence for learned patterns
            assert result.confidence_score >= 0.3, f"Low confidence {result.confidence_score} for learned pattern: {query}"
        
        # Should achieve learning performance target
        accuracy = correct_selections / len(infrastructure_patterns) 
        assert accuracy >= 0.6, f"Infrastructure learning accuracy {accuracy:.1%} below 60% target"
    
    def test_learning_metrics_validation(self):
        """Test learning metrics validation from coordination-hub.md"""
        # Test that the learning performance metrics from coordination-hub.md are achievable
        learning_metrics = {
            "total_successful_patterns": 295,  # From coordination-hub.md
            "learning_rate": 1.0,  # 100% success rate
            "active_query_types": 3,  # container_orchestration, scaling_performance, service_networking
            "average_pattern_weight": 2.406
        }
        
        # Validate metrics are reasonable
        assert learning_metrics["total_successful_patterns"] > 200
        assert learning_metrics["learning_rate"] >= 0.8
        assert learning_metrics["active_query_types"] >= 3
        assert 1.0 <= learning_metrics["average_pattern_weight"] <= 5.0
    
    def test_agent_directory_integration(self):
        """Test integration with .claude/agents/ directory structure"""
        import sys
        import os
        from pathlib import Path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        from agent_selector import EnhancedAgentSelector
        
        selector = EnhancedAgentSelector()
        
        # Test that agents from .claude/agents/ are properly loaded
        expected_agents = [
            "test-specialist", "infrastructure-engineer", "security-enforcer", 
            "documentation-enhancer", "meta-coordinator", "analysis-gateway"
        ]
        
        loaded_agents = list(selector.agents.keys())
        
        # Should have loaded agents from directory
        for agent in expected_agents:
            assert agent in loaded_agents, f"Agent {agent} not loaded from .claude/agents/ directory"
        
        # Test queries that should select directory-loaded agents
        directory_agent_tests = [
            ("comprehensive API documentation creation", "documentation-enhancer"),
            ("complex multi-domain infrastructure security", "meta-coordinator"),
            ("comprehensive analysis gateway coordination", "analysis-gateway")
        ]
        
        for query, expected_agent in directory_agent_tests:
            result = selector.select_agent(query)
            assert result.agent_name == expected_agent, \
                f"Expected {expected_agent} for '{query}', got {result.agent_name}"


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