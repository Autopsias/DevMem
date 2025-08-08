#!/usr/bin/env python3
"""
Test module for Infrastructure Domain Enhancement

Validates the enhanced infrastructure domain pattern matching
to achieve 90% accuracy target from 72% baseline.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from agent_selector import EnhancedAgentSelector, AgentMatchResult
from typing import List, Tuple


class TestInfrastructureDomainEnhancement:
    """Test infrastructure domain pattern matching improvements."""
    
    @pytest.fixture
    def selector(self):
        """Create enhanced agent selector instance."""
        return EnhancedAgentSelector()
    
    @pytest.fixture
    def infrastructure_test_cases(self) -> List[Tuple[str, float]]:
        """Infrastructure domain test cases with expected confidence scores."""
        return [
            # Core Container & Orchestration
            ("Docker container orchestration failing in production", 0.85),
            ("Kubernetes cluster scaling issues with pod networking", 0.90),
            ("Container registry security scanning setup", 0.80),
            ("Docker compose configuration for microservices", 0.85),
            ("K8s deployment rollback strategy implementation", 0.90),
            
            # Service Mesh & Networking
            ("Service mesh configuration with Istio ingress", 0.85),
            ("Load balancing configuration for containerized services", 0.80),
            ("Kubernetes networking policies and service discovery", 0.85),
            ("Ingress controller setup with nginx and TLS", 0.80),
            ("Container networking troubleshooting across clusters", 0.85),
            
            # Infrastructure as Code & Automation
            ("Terraform infrastructure provisioning for multi-cloud", 0.90),
            ("Ansible playbook automation for container deployment", 0.85),
            ("Helm chart deployment with custom configurations", 0.85),
            ("Infrastructure as code validation and testing", 0.80),
            ("DevOps pipeline integration with infrastructure automation", 0.85),
            
            # Deployment & CI/CD Integration
            ("Deployment pipeline optimization for containerized apps", 0.85),
            ("Blue-green deployment strategy for Kubernetes services", 0.90),
            ("Canary rollout configuration with progressive delivery", 0.85),
            ("CI/CD integration with infrastructure provisioning", 0.80),
            ("Container deployment automation across environments", 0.85),
            
            # Monitoring & Observability
            ("Infrastructure monitoring with Prometheus and Grafana", 0.85),
            ("Container observability and distributed tracing setup", 0.80),
            ("Kubernetes cluster monitoring and alerting configuration", 0.85),
            ("Centralized logging for microservices infrastructure", 0.80),
            ("Infrastructure metrics collection and dashboarding", 0.80),
            
            # Scaling & Performance
            ("Horizontal pod autoscaling configuration in Kubernetes", 0.90),
            ("Container resource allocation and performance tuning", 0.85),
            ("Infrastructure scaling strategies for high-load scenarios", 0.85),
            ("Cluster autoscaling policies and node management", 0.85),
            ("Performance optimization for containerized workloads", 0.80),
            
            # Cloud & Multi-Cloud
            ("Multi-cloud infrastructure deployment with Terraform", 0.90),
            ("AWS EKS cluster setup and configuration management", 0.85),
            ("GCP GKE deployment with service mesh integration", 0.85),
            ("Azure AKS infrastructure provisioning and networking", 0.85),
            ("Hybrid cloud container orchestration strategy", 0.85),
            
            # Security & Compliance
            ("Container security hardening and vulnerability scanning", 0.80),
            ("Kubernetes RBAC configuration and pod security policies", 0.85),
            ("Infrastructure security compliance and governance", 0.80),
            ("Container image security scanning and registry management", 0.80),
            ("Cluster security monitoring and threat detection", 0.80),
            
            # Storage & Persistence
            ("Persistent volume management in Kubernetes clusters", 0.85),
            ("Container storage optimization and backup strategies", 0.80),
            ("Database deployment and scaling in containerized environments", 0.80),
            ("Storage infrastructure provisioning for cloud-native apps", 0.80),
            ("Volume mounting and storage class configuration", 0.80),
            
            # Troubleshooting & Maintenance
            ("Kubernetes troubleshooting for failed pod deployments", 0.85),
            ("Container networking debugging and connectivity issues", 0.85),
            ("Infrastructure maintenance and scheduled updates", 0.80),
            ("Cluster health monitoring and diagnostic procedures", 0.80),
            ("Container runtime issues and performance debugging", 0.80),
            
            # Common Infrastructure Variations
            ("Need help with k8s deployment issues", 0.80),
            ("Docker containers not starting properly", 0.85),
            ("Infrastructure automation with ansible scripts", 0.85),
            ("Microservices orchestration problems", 0.80),
            ("DevOps pipeline infrastructure integration", 0.80),
            ("SRE practices for container infrastructure", 0.80),
            ("Cloud-native application deployment strategies", 0.80),
            ("Container platform migration and optimization", 0.80)
        ]
    
    @pytest.fixture 
    def infrastructure_edge_cases(self) -> List[Tuple[str, float]]:
        """Infrastructure domain edge cases and boundary scenarios."""
        return [
            # Cross-Domain Infrastructure Cases
            ("Docker security scanning integration", 0.70),  # Infrastructure + Security
            ("Kubernetes performance optimization", 0.75),  # Infrastructure + Performance
            ("Container testing pipeline configuration", 0.70),  # Infrastructure + Testing
            ("Infrastructure code quality improvements", 0.65),  # Infrastructure + Code Quality
            
            # Ambiguous Cases
            ("Service deployment issues", 0.60),
            ("Container problems need fixing", 0.65),
            ("Infrastructure not working correctly", 0.65),
            ("Deployment pipeline broken", 0.70),
            
            # Abbreviated Terms
            ("k8s cluster setup", 0.80),
            ("infra automation needed", 0.75),
            ("DevOps pipeline issues", 0.70),
            ("SRE troubleshooting required", 0.70),
            
            # Complex Scenarios
            ("Multi-cloud infrastructure orchestration with security compliance", 0.75),
            ("Container platform migration with zero-downtime requirements", 0.80),
            ("Kubernetes cluster federation across multiple regions", 0.85)
        ]
    
    def test_infrastructure_agent_selection_accuracy(self, selector, infrastructure_test_cases):
        """Test infrastructure domain agent selection accuracy."""
        correct_selections = 0
        total_cases = len(infrastructure_test_cases)
        confidence_scores = []
        processing_times = []
        
        for query, expected_confidence in infrastructure_test_cases:
            result = selector.select_agent(query)
            processing_times.append(result.processing_time_ms)
            confidence_scores.append(result.confidence_score)
            
            # Should select infrastructure-engineer
            if result.agent_name == 'infrastructure-engineer':
                correct_selections += 1
            
            # Should meet minimum confidence threshold
            assert result.confidence_score >= 0.4, f"Low confidence ({result.confidence_score:.2f}) for: {query}"
            
            # Should ideally meet expected confidence
            if result.confidence_score < expected_confidence * 0.8:  # Allow 20% tolerance
                print(f"Below expected confidence for '{query}': {result.confidence_score:.2f} < {expected_confidence:.2f}")
        
        accuracy = correct_selections / total_cases
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        avg_processing_time = sum(processing_times) / len(processing_times)
        
        print(f"\nInfrastructure Domain Results:")
        print(f"Accuracy: {accuracy:.1%} ({correct_selections}/{total_cases})")
        print(f"Average confidence: {avg_confidence:.2f}")
        print(f"Average processing time: {avg_processing_time:.1f}ms")
        
        # Target: 90% accuracy improvement from 72% baseline
        assert accuracy >= 0.90, f"Infrastructure domain accuracy {accuracy:.1%} below 90% target"
        assert avg_confidence >= 0.75, f"Average confidence {avg_confidence:.2f} too low"
        assert avg_processing_time < 5.0, f"Processing time {avg_processing_time:.1f}ms too slow"
    
    def test_infrastructure_pattern_matching(self, selector):
        """Test specific infrastructure pattern matching improvements."""
        pattern_tests = [
            # Container Orchestration Patterns
            ("kubernetes cluster scaling", ['kubernetes', 'cluster', 'scaling']),
            ("docker container networking", ['docker', 'container', 'networking']),
            ("service mesh configuration", ['service', 'mesh', 'configuration']),
            
            # Infrastructure as Code Patterns
            ("terraform infrastructure provisioning", ['terraform', 'infrastructure', 'provisioning']),
            ("ansible automation playbook", ['ansible', 'automation', 'playbook']),
            ("helm chart deployment", ['helm', 'chart', 'deployment']),
            
            # Cloud-Native Patterns
            ("microservices orchestration", ['microservices', 'orchestration']),
            ("cloud-native deployment", ['cloud', 'deployment']),
            ("devops pipeline integration", ['devops', 'pipeline', 'integration'])
        ]
        
        for query, expected_patterns in pattern_tests:
            result = selector.select_agent(query)
            
            # Should select infrastructure-engineer
            assert result.agent_name == 'infrastructure-engineer', f"Wrong agent for '{query}': {result.agent_name}"
            
            # Should have reasonable confidence
            assert result.confidence_score >= 0.7, f"Low confidence for '{query}': {result.confidence_score:.2f}"
            
            # Should match expected patterns (at least some)
            matched_keywords = set(result.context_keywords)
            expected_keywords = set(expected_patterns)
            overlap = matched_keywords & expected_keywords
            assert len(overlap) >= 1, f"No pattern overlap for '{query}': {matched_keywords} vs {expected_keywords}"
    
    def test_infrastructure_keyword_extraction(self, selector):
        """Test infrastructure-specific keyword extraction."""
        keyword_tests = [
            ("Kubernetes cluster deployment", ['kubernetes', 'deployment']),
            ("Docker container orchestration", ['docker', 'container', 'orchestration']),
            ("Infrastructure as code with Terraform", ['infrastructure', 'terraform']),
            ("Microservices deployment automation", ['service', 'deployment', 'automation']),
            ("K8s scaling and monitoring", ['kubernetes', 'scaling', 'monitoring']),  # k8s -> kubernetes
            ("DevOps pipeline optimization", ['infrastructure', 'deployment']),  # devops -> infrastructure, pipeline -> deployment
            ("Container registry and security", ['container', 'security']),
            ("SRE practices implementation", ['infrastructure'])  # sre -> infrastructure
        ]
        
        for query, expected_keywords in keyword_tests:
            keywords = selector.extract_keywords(query)
            
            # Should extract expected keywords
            for expected_keyword in expected_keywords:
                assert expected_keyword in keywords, f"Missing keyword '{expected_keyword}' in '{query}'"
    
    def test_infrastructure_edge_cases(self, selector, infrastructure_edge_cases):
        """Test infrastructure domain edge cases and boundary scenarios."""
        infrastructure_selections = 0
        total_cases = len(infrastructure_edge_cases)
        
        for query, min_confidence in infrastructure_edge_cases:
            result = selector.select_agent(query)
            
            # Should have minimum confidence
            assert result.confidence_score >= min_confidence * 0.8, f"Very low confidence for edge case '{query}': {result.confidence_score:.2f}"
            
            # Count infrastructure-engineer selections
            if result.agent_name == 'infrastructure-engineer':
                infrastructure_selections += 1
            
            print(f"Edge case: '{query}' -> {result.agent_name} ({result.confidence_score:.2f})")
        
        # Should handle most infrastructure edge cases correctly
        edge_accuracy = infrastructure_selections / total_cases
        assert edge_accuracy >= 0.70, f"Infrastructure edge case accuracy {edge_accuracy:.1%} too low"
    
    def test_infrastructure_vs_other_domains(self, selector):
        """Test infrastructure domain disambiguation from other domains."""
        disambiguation_tests = [
            # Infrastructure vs Testing
            ("Docker container testing framework", "test-specialist"),  # Testing context stronger
            ("Container deployment pipeline testing", "infrastructure-engineer"),  # Infrastructure context stronger
            
            # Infrastructure vs Security
            ("Container security vulnerability scanning", "security-enforcer"),  # Security context stronger
            ("Infrastructure security hardening deployment", "infrastructure-engineer"),  # Infrastructure context stronger
            
            # Infrastructure vs Performance
            ("Kubernetes performance optimization analysis", "performance-optimizer"),  # Performance context stronger
            ("Container orchestration performance tuning", "infrastructure-engineer"),  # Infrastructure context stronger
            
            # Clear Infrastructure Cases
            ("Kubernetes cluster provisioning", "infrastructure-engineer"),
            ("Docker orchestration automation", "infrastructure-engineer"),
            ("Terraform infrastructure deployment", "infrastructure-engineer")
        ]
        
        correct_disambiguations = 0
        for query, expected_agent in disambiguation_tests:
            result = selector.select_agent(query)
            
            if result.agent_name == expected_agent:
                correct_disambiguations += 1
            else:
                print(f"Disambiguation issue: '{query}' -> {result.agent_name} (expected: {expected_agent})")
        
        disambiguation_accuracy = correct_disambiguations / len(disambiguation_tests)
        print(f"\nDomain disambiguation accuracy: {disambiguation_accuracy:.1%}")
        
        # Should achieve good disambiguation
        assert disambiguation_accuracy >= 0.80, f"Domain disambiguation accuracy {disambiguation_accuracy:.1%} too low"
    
    def test_infrastructure_performance_requirements(self, selector, infrastructure_test_cases):
        """Test that infrastructure domain enhancements meet performance requirements."""
        processing_times = []
        
        # Test with larger sample for performance measurement
        test_queries = [query for query, _ in infrastructure_test_cases] * 5  # 5x repetition
        
        for query in test_queries:
            result = selector.select_agent(query)
            processing_times.append(result.processing_time_ms)
        
        avg_processing_time = sum(processing_times) / len(processing_times)
        max_processing_time = max(processing_times)
        
        print(f"\nPerformance Results:")
        print(f"Average processing time: {avg_processing_time:.2f}ms")
        print(f"Maximum processing time: {max_processing_time:.2f}ms")
        print(f"Total queries processed: {len(test_queries)}")
        
        # Performance requirements
        assert avg_processing_time < 3.0, f"Average processing time {avg_processing_time:.2f}ms too slow"
        assert max_processing_time < 10.0, f"Maximum processing time {max_processing_time:.2f}ms too slow"
    
    def test_infrastructure_comprehensive_validation(self, selector):
        """Comprehensive validation test for infrastructure domain enhancement."""
        # Test comprehensive infrastructure scenarios
        comprehensive_scenarios = [
            "Multi-cloud Kubernetes cluster deployment with Terraform and Helm",
            "Container orchestration scaling with service mesh integration", 
            "DevOps pipeline automation for microservices infrastructure",
            "Infrastructure monitoring and observability with Prometheus",
            "Container security scanning and compliance automation",
            "Kubernetes troubleshooting and performance optimization",
            "Cloud-native deployment strategies with blue-green rollouts",
            "Infrastructure as code validation and testing frameworks"
        ]
        
        infrastructure_count = 0
        high_confidence_count = 0
        
        for scenario in comprehensive_scenarios:
            result = selector.select_agent(scenario)
            
            if result.agent_name == 'infrastructure-engineer':
                infrastructure_count += 1
            
            if result.confidence_score >= 0.80:
                high_confidence_count += 1
            
            print(f"Comprehensive: '{scenario}' -> {result.agent_name} ({result.confidence_score:.2f})")
        
        comprehensive_accuracy = infrastructure_count / len(comprehensive_scenarios)
        high_confidence_rate = high_confidence_count / len(comprehensive_scenarios)
        
        print(f"\nComprehensive Infrastructure Results:")
        print(f"Infrastructure selection accuracy: {comprehensive_accuracy:.1%}")
        print(f"High confidence rate (≥0.80): {high_confidence_rate:.1%}")
        
        # Should achieve excellent results on comprehensive scenarios
        assert comprehensive_accuracy >= 0.90, f"Comprehensive accuracy {comprehensive_accuracy:.1%} below target"
        assert high_confidence_rate >= 0.75, f"High confidence rate {high_confidence_rate:.1%} too low"


if __name__ == "__main__":
    # Run specific infrastructure domain tests
    pytest.main([__file__, "-v", "-s"])
