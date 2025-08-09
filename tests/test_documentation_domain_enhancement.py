#!/usr/bin/env python3
"""
Comprehensive Test Suite for Documentation Domain Enhancement

This test suite validates the documentation domain pattern enhancements
to ensure accuracy improvement from 63% to 80%.

Test Categories:
1. Baseline compatibility tests (current 63% patterns)
2. Enhanced pattern recognition tests (target 80%)
3. Natural language documentation request tests
4. Cross-domain interference validation
5. Performance impact assessment
"""

import pytest
import time
import statistics
from src.agent_selector import EnhancedAgentSelector


class TestDocumentationDomainEnhancement:
    """Comprehensive test suite for documentation domain enhancement"""

    @pytest.fixture
    def documentation_selector(self):
        """Fixture for enhanced documentation agent selector"""
        return EnhancedAgentSelector()

    def test_baseline_compatibility(self, documentation_selector):
        """Test that current documentation patterns still work (backward compatibility)"""
        baseline_cases = [
            ("documentation update needed", 0.75),
            ("create README file", 0.80),
            ("API documentation generation", 0.82),
            ("user guide creation", 0.78),
            ("technical writing requirements", 0.85),
            ("markdown documentation", 0.76),
            ("project documentation review", 0.80),
        ]

        passed_tests = 0
        for test_input, min_confidence in baseline_cases:
            result = documentation_selector.select_agent(test_input)

            # Test passes if documentation-enhancer is selected with sufficient confidence
            if (
                result.agent_name == "documentation-enhancer"
                and result.confidence_score >= min_confidence
            ):
                passed_tests += 1
            else:
                print(
                    f"BASELINE FAIL: '{test_input}' -> {result.agent_name} ({result.confidence_score:.3f}, expected >= {min_confidence})"
                )

        accuracy = passed_tests / len(baseline_cases)
        print(
            f"Baseline Compatibility Accuracy: {accuracy:.1%} ({passed_tests}/{len(baseline_cases)})"
        )

        # Should maintain at least 75% on baseline patterns
        assert accuracy >= 0.75, f"Baseline accuracy {accuracy:.1%} below 75% threshold"

    def test_enhanced_documentation_patterns(self, documentation_selector):
        """Test enhanced documentation pattern recognition for 80% target accuracy"""
        enhanced_cases = [
            # Core Documentation Tasks
            (
                "write comprehensive documentation for new API",
                "documentation-enhancer",
                0.85,
            ),
            (
                "generate user guide for installation process",
                "documentation-enhancer",
                0.82,
            ),
            ("create technical specification document", "documentation-enhancer", 0.88),
            ("update project README with new features", "documentation-enhancer", 0.80),
            ("develop tutorial for beginners", "documentation-enhancer", 0.83),
            # API Documentation Patterns
            ("document REST API endpoints and schemas", "documentation-enhancer", 0.87),
            (
                "create API reference guide with examples",
                "documentation-enhancer",
                0.85,
            ),
            (
                "generate OpenAPI specification documentation",
                "documentation-enhancer",
                0.84,
            ),
            (
                "write API integration guide for developers",
                "documentation-enhancer",
                0.83,
            ),
            # Technical Writing Patterns
            (
                "improve technical writing quality in docs",
                "documentation-enhancer",
                0.86,
            ),
            (
                "create architecture documentation for system",
                "documentation-enhancer",
                0.82,
            ),
            (
                "write deployment guide with step-by-step instructions",
                "documentation-enhancer",
                0.84,
            ),
            (
                "develop troubleshooting guide for common issues",
                "documentation-enhancer",
                0.81,
            ),
            # Content Management Patterns
            (
                "organize knowledge base content structure",
                "documentation-enhancer",
                0.83,
            ),
            (
                "create content style guide for consistency",
                "documentation-enhancer",
                0.85,
            ),
            (
                "manage documentation versioning strategy",
                "documentation-enhancer",
                0.82,
            ),
            # Markdown and Formatting Patterns
            (
                "format documentation using markdown syntax",
                "documentation-enhancer",
                0.84,
            ),
            (
                "convert existing docs to markdown format",
                "documentation-enhancer",
                0.83,
            ),
            (
                "create markdown templates for documentation",
                "documentation-enhancer",
                0.85,
            ),
            # Documentation Automation Patterns
            (
                "automate documentation generation from code",
                "documentation-enhancer",
                0.86,
            ),
            ("set up automated docs build pipeline", "documentation-enhancer", 0.84),
            (
                "integrate documentation into CI/CD workflow",
                "documentation-enhancer",
                0.82,
            ),
            # User-Focused Documentation
            (
                "create user manual for software application",
                "documentation-enhancer",
                0.85,
            ),
            ("write FAQ section for common questions", "documentation-enhancer", 0.83),
            (
                "develop getting started guide for new users",
                "documentation-enhancer",
                0.84,
            ),
            ("create how-to guides for specific tasks", "documentation-enhancer", 0.82),
        ]

        correct_selections = 0
        confidence_scores = []

        for test_input, expected_agent, min_confidence in enhanced_cases:
            result = documentation_selector.select_agent(test_input)
            confidence_scores.append(result.confidence_score)

            # Test passes if correct agent is selected with sufficient confidence
            if (
                result.agent_name == expected_agent
                and result.confidence_score >= min_confidence
            ):
                correct_selections += 1
            else:
                print(
                    f"ENHANCED FAIL: '{test_input}' -> {result.agent_name} ({result.confidence_score:.3f}, expected {expected_agent} >= {min_confidence})"
                )

        accuracy = correct_selections / len(enhanced_cases)
        avg_confidence = statistics.mean(confidence_scores)

        print(
            f"Enhanced Documentation Patterns Accuracy: {accuracy:.1%} ({correct_selections}/{len(enhanced_cases)})"
        )
        print(f"Average Confidence Score: {avg_confidence:.3f}")

        # Should achieve target 80% accuracy on enhanced patterns
        assert accuracy >= 0.80, f"Enhanced accuracy {accuracy:.1%} below 80% target"
        assert (
            avg_confidence >= 0.75
        ), f"Average confidence {avg_confidence:.3f} too low"

    def test_natural_language_documentation_requests(self, documentation_selector):
        """Test natural language documentation requests with variations"""
        natural_cases = [
            # Conversational requests
            (
                "I need help writing documentation for my project",
                "documentation-enhancer",
            ),
            (
                "Can you create a README file for this repository?",
                "documentation-enhancer",
            ),
            ("Help me document the API endpoints properly", "documentation-enhancer"),
            ("We need better user guides for our software", "documentation-enhancer"),
            (
                "Please improve the technical writing in our docs",
                "documentation-enhancer",
            ),
            # Informal variations
            ("docs need updating badly", "documentation-enhancer"),
            ("readme is outdated and needs work", "documentation-enhancer"),
            ("api docs are missing examples", "documentation-enhancer"),
            ("users can't understand our guides", "documentation-enhancer"),
            ("technical specs are confusing", "documentation-enhancer"),
            # Action-oriented requests
            ("generate comprehensive docs from code", "documentation-enhancer"),
            ("build user manual from scratch", "documentation-enhancer"),
            ("organize scattered documentation", "documentation-enhancer"),
            ("standardize documentation format", "documentation-enhancer"),
            ("migrate docs to new platform", "documentation-enhancer"),
            # Context-rich requests
            (
                "new team members struggle with our documentation",
                "documentation-enhancer",
            ),
            ("documentation doesn't match current features", "documentation-enhancer"),
            (
                "need documentation for compliance requirements",
                "documentation-enhancer",
            ),
            (
                "stakeholders request better project documentation",
                "documentation-enhancer",
            ),
            ("documentation review revealed gaps", "documentation-enhancer"),
        ]

        correct_selections = 0
        confidence_scores = []

        for test_input, expected_agent in natural_cases:
            result = documentation_selector.select_agent(test_input)
            confidence_scores.append(result.confidence_score)

            if result.agent_name == expected_agent:
                correct_selections += 1
            else:
                print(
                    f"NATURAL FAIL: '{test_input}' -> {result.agent_name} (expected {expected_agent})"
                )

        accuracy = correct_selections / len(natural_cases)
        avg_confidence = statistics.mean(confidence_scores)

        print(
            f"Natural Language Documentation Accuracy: {accuracy:.1%} ({correct_selections}/{len(natural_cases)})"
        )
        print(f"Average Confidence Score: {avg_confidence:.3f}")

        # Should achieve good accuracy on natural language requests
        assert (
            accuracy >= 0.75
        ), f"Natural language accuracy {accuracy:.1%} below 75% threshold"

    def test_cross_domain_interference_validation(self, documentation_selector):
        """Test that documentation enhancement doesn't interfere with other domains"""
        other_domain_cases = [
            # Testing domain (should not select documentation-enhancer)
            ("pytest test failures in async code", False),
            ("mock configuration issues in tests", False),
            ("test coverage gaps analysis needed", False),
            # Infrastructure domain
            ("docker container orchestration problems", False),
            ("kubernetes cluster scaling issues", False),
            ("infrastructure deployment automation", False),
            # Security domain
            ("security vulnerability scan results", False),
            ("authentication flow validation", False),
            ("credential management security audit", False),
            # Performance domain
            ("performance bottleneck analysis", False),
            ("memory optimization requirements", False),
            ("latency reduction strategies", False),
            # Code quality domain
            ("code refactoring for better architecture", False),
            ("variable naming convention improvements", False),
            ("function complexity reduction", False),
            # Mixed cases (documentation + other domain)
            ("document API performance optimization", True),  # Documentation context
            ("create security documentation guide", True),  # Documentation context
            ("write testing strategy documentation", True),  # Documentation context
            ("API documentation update", True),  # Pure documentation
            ("security audit documentation", True),  # Documentation context
        ]

        interference_count = 0
        for test_input, should_be_documentation in other_domain_cases:
            result = documentation_selector.select_agent(test_input)
            is_documentation = result.agent_name == "documentation-enhancer"

            if should_be_documentation != is_documentation:
                interference_count += 1
                if should_be_documentation:
                    print(
                        f"MISSED DOC: '{test_input}' -> {result.agent_name} (should be documentation-enhancer)"
                    )
                else:
                    print(
                        f"INTERFERENCE: '{test_input}' -> {result.agent_name} (should NOT be documentation-enhancer)"
                    )

        accuracy = (len(other_domain_cases) - interference_count) / len(
            other_domain_cases
        )
        print(
            f"Cross-Domain Interference Validation: {accuracy:.1%} ({len(other_domain_cases) - interference_count}/{len(other_domain_cases)})"
        )

        # Should have minimal cross-domain interference
        assert (
            accuracy >= 0.85
        ), f"Cross-domain accuracy {accuracy:.1%} below 85% threshold"

    def test_performance_impact_assessment(self, documentation_selector):
        """Test performance impact of documentation enhancement"""
        test_queries = [
            "create comprehensive API documentation",
            "write user guide for new feature",
            "update project README file",
            "generate technical specification",
            "document deployment process",
        ]

        # Warm up the selector
        for query in test_queries:
            documentation_selector.select_agent(query)

        # Measure performance
        response_times = []
        for _ in range(10):
            for query in test_queries:
                start_time = time.perf_counter()
                documentation_selector.select_agent(query)
                end_time = time.perf_counter()
                response_times.append((end_time - start_time) * 1000)  # Convert to ms

        avg_response_time = statistics.mean(response_times)
        max_response_time = max(response_times)
        p95_response_time = statistics.quantiles(response_times, n=20)[
            18
        ]  # 95th percentile

        print("Documentation Enhancement Performance:")
        print(f"  Average Response Time: {avg_response_time:.2f}ms")
        print(f"  Maximum Response Time: {max_response_time:.2f}ms")
        print(f"  95th Percentile: {p95_response_time:.2f}ms")

        # Performance should remain within acceptable bounds
        assert (
            avg_response_time <= 10.0
        ), f"Average response time {avg_response_time:.2f}ms exceeds 10ms threshold"
        assert (
            max_response_time <= 50.0
        ), f"Max response time {max_response_time:.2f}ms exceeds 50ms threshold"

    def test_comprehensive_documentation_accuracy_target(self, documentation_selector):
        """Comprehensive test to validate 80% accuracy target achievement"""
        # Combine all documentation test cases
        all_documentation_cases = [
            # High-confidence exact matches
            ("documentation update", "documentation-enhancer"),
            ("create README", "documentation-enhancer"),
            ("API documentation", "documentation-enhancer"),
            ("user guide", "documentation-enhancer"),
            ("technical writing", "documentation-enhancer"),
            ("markdown guide", "documentation-enhancer"),
            ("project docs", "documentation-enhancer"),
            ("write manual", "documentation-enhancer"),
            ("generate docs", "documentation-enhancer"),
            ("documentation review", "documentation-enhancer"),
            # Medium-confidence contextual matches
            ("need better documentation for users", "documentation-enhancer"),
            ("API reference guide creation", "documentation-enhancer"),
            ("technical specification document", "documentation-enhancer"),
            ("installation guide writing", "documentation-enhancer"),
            ("troubleshooting documentation", "documentation-enhancer"),
            ("developer handbook creation", "documentation-enhancer"),
            ("knowledge base organization", "documentation-enhancer"),
            ("content management system", "documentation-enhancer"),
            ("documentation automation", "documentation-enhancer"),
            ("style guide development", "documentation-enhancer"),
            # Natural language variations
            ("help users understand the software", "documentation-enhancer"),
            ("explain how the API works", "documentation-enhancer"),
            ("create instructions for setup", "documentation-enhancer"),
            ("document the architecture", "documentation-enhancer"),
            ("write about new features", "documentation-enhancer"),
        ]

        correct_selections = 0
        total_cases = len(all_documentation_cases)

        for test_input, expected_agent in all_documentation_cases:
            result = documentation_selector.select_agent(test_input)
            if result.agent_name == expected_agent:
                correct_selections += 1
            else:
                print(
                    f"MISS: '{test_input}' -> {result.agent_name} (expected {expected_agent})"
                )

        accuracy = correct_selections / total_cases
        print(
            f"\nCOMPREHENSIVE DOCUMENTATION DOMAIN ACCURACY: {accuracy:.1%} ({correct_selections}/{total_cases})"
        )

        # Must achieve 80% accuracy target
        assert (
            accuracy >= 0.80
        ), f"Documentation domain accuracy {accuracy:.1%} below 80% target"

        print(
            f"\n✅ DOCUMENTATION DOMAIN ENHANCEMENT SUCCESSFUL: {accuracy:.1%} accuracy achieved (target: 80%)"
        )


class TestDocumentationPatternDetails:
    """Detailed pattern testing for documentation domain"""

    @pytest.fixture
    def selector(self):
        return EnhancedAgentSelector()

    def test_documentation_keyword_extraction(self, selector):
        """Test documentation-specific keyword extraction"""
        test_cases = [
            ("create API documentation", ["api", "documentation"]),
            ("write user guide", ["guide"]),
            ("README file generation", ["readme"]),
            ("technical writing improvement", ["technical"]),
            ("markdown formatting", ["markdown"]),
            ("knowledge base management", ["knowledge"]),
            ("how-to guide creation", ["howto", "guide"]),
        ]

        for query, expected_keywords in test_cases:
            keywords = selector.extract_keywords(query)
            for expected in expected_keywords:
                assert (
                    expected in keywords
                ), f"Missing keyword '{expected}' from '{query}'"

    def test_documentation_context_patterns(self, selector):
        """Test documentation context pattern matching"""
        doc_agent = selector.agents["documentation-enhancer"]

        test_patterns = [
            "documentation update needed",
            "create comprehensive docs",
            "API reference guide",
            "user manual creation",
            "technical specification writing",
            "knowledge base organization",
            "content management requirements",
        ]

        for pattern in test_patterns:
            score, matched = selector.calculate_context_score(pattern, doc_agent)
            assert score > 0, f"No score for documentation pattern: {pattern}"
            print(f"Pattern '{pattern}': score={score:.2f}, matches={len(matched)}")

    def test_documentation_specialization_areas(self, selector):
        """Test documentation specialization area matching"""
        specializations = [
            ("technical writing", "technical_writing"),
            ("API documentation", "api_documentation"),
            ("user guide", "user_guides"),
            ("README generation", "readme_generation"),
            ("markdown formatting", "markdown_formatting"),
            ("content management", "content_management"),
            ("documentation automation", "documentation_automation"),
            ("knowledge management", "knowledge_management"),
        ]

        doc_agent = selector.agents["documentation-enhancer"]

        for test_input, expected_spec in specializations:
            score, matched = selector.calculate_context_score(test_input, doc_agent)
            assert score >= 1.5, f"Insufficient score for '{test_input}': {score}"
            print(
                f"Specialization '{test_input}' -> {expected_spec}: score={score:.2f}"
            )


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v", "--tb=short"])
