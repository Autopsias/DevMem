#!/usr/bin/env python3
"""
Comprehensive Test Suite for Security Domain Enhancement

This test suite validates the security domain pattern enhancements
to ensure accuracy improvement from 65% to 85%.

Test Categories:
1. Baseline compatibility tests (current 65% patterns)
2. Enhanced pattern recognition tests (target 85%)
3. Natural language security request tests
4. Cross-domain interference validation
5. Performance impact assessment
"""

import pytest
import time
import statistics
from enhanced_security_patterns import EnhancedSecurityPatternMatcher

class TestSecurityDomainEnhancement:
    """Comprehensive test suite for security domain enhancement"""
    
    @pytest.fixture
    def security_matcher(self):
        """Fixture for enhanced security pattern matcher"""
        return EnhancedSecurityPatternMatcher()
    
    def test_baseline_compatibility(self, security_matcher):
        """Test that current security patterns still work (backward compatibility)"""
        baseline_cases = [
            ("security scan audit review", 0.80),
            ("vulnerability assessment scan", 0.85),
            ("credential leak management", 0.82),
            ("authentication flow token", 0.78),
            ("compliance validation audit", 0.83),
            ("authorization policy rbac", 0.80),
            ("encryption data transport", 0.81)
        ]
        
        passed_tests = 0
        for test_input, min_confidence in baseline_cases:
            analysis = security_matcher.analyze_security_request(test_input)
            actual_confidence = analysis["confidence_score"]
            
            # Test passes if confidence meets minimum threshold
            if actual_confidence >= min_confidence:
                passed_tests += 1
            else:
                pytest.fail(
                    f"Baseline compatibility failed for '{test_input}': "
                    f"expected >={min_confidence}, got {actual_confidence:.3f}"
                )
        
        baseline_accuracy = passed_tests / len(baseline_cases)
        assert baseline_accuracy >= 0.80, f"Baseline accuracy {baseline_accuracy:.2%} below 80% threshold"
    
    def test_enhanced_keyword_recognition(self, security_matcher):
        """Test enhanced keyword coverage (65% → 75% improvement)"""
        enhanced_keyword_cases = [
            # New threat-related keywords
            ("threat modeling analysis", "threat", 0.85),
            ("attack vector assessment", "attack", 0.83),
            ("security breach investigation", "breach", 0.87),
            ("exploit mitigation strategy", "exploit", 0.82),
            ("malware detection system", "malware", 0.85),
            ("intrusion detection setup", "intrusion", 0.84),
            
            # New compliance keywords
            ("GDPR compliance audit", "gdpr", 0.90),
            ("HIPAA data protection", "hipaa", 0.88),
            ("SOX regulatory compliance", "sox", 0.86),
            
            # New security infrastructure keywords
            ("firewall configuration review", "firewall", 0.82),
            ("penetration testing schedule", "penetration", 0.89),
            ("certificate management system", "certificate", 0.81)
        ]
        
        passed_tests = 0
        for test_input, expected_keyword, min_confidence in enhanced_keyword_cases:
            analysis = security_matcher.analyze_security_request(test_input)
            
            # Verify keyword is detected
            keyword_matches = analysis["enhancement_details"]["keyword_matches"]
            assert expected_keyword in [k.lower() for k in keyword_matches], \
                f"Expected keyword '{expected_keyword}' not detected in '{test_input}'"
            
            # Verify confidence meets threshold
            actual_confidence = analysis["confidence_score"]
            if actual_confidence >= min_confidence:
                passed_tests += 1
            else:
                pytest.fail(
                    f"Enhanced keyword test failed for '{test_input}': "
                    f"expected >={min_confidence}, got {actual_confidence:.3f}"
                )
        
        keyword_accuracy = passed_tests / len(enhanced_keyword_cases)
        assert keyword_accuracy >= 0.75, f"Enhanced keyword accuracy {keyword_accuracy:.2%} below 75% target"
    
    def test_tier_1_high_confidence_patterns(self, security_matcher):
        """Test Tier 1 high-confidence security patterns (95%+ accuracy)"""
        tier_1_cases = [
            # Threat Analysis & Attack Vectors
            ("threat modeling analysis for microservices", "tier_1", 0.90),
            ("attack surface assessment required", "tier_1", 0.88),
            ("penetration testing on web application", "tier_1", 0.92),
            ("red team exercise planning", "tier_1", 0.89),
            
            # Security Architecture & Design
            ("security architecture framework design", "tier_1", 0.91),
            ("secure coding development practices", "tier_1", 0.87),
            ("defense in depth strategy implementation", "tier_1", 0.90),
            ("zero trust architecture model", "tier_1", 0.93),
            
            # Advanced Authentication & Authorization
            ("multi factor authentication setup", "tier_1", 0.89),
            ("single sign on integration", "tier_1", 0.86),
            ("oauth 2.0 implementation security", "tier_1", 0.88),
            ("jwt token validation process", "tier_1", 0.85),
            
            # Compliance & Governance
            ("GDPR compliance audit requirements", "tier_1", 0.92),
            ("data protection governance framework", "tier_1", 0.88),
            ("regulatory compliance audit standard", "tier_1", 0.87),
            
            # Encryption & Cryptography
            ("encryption at rest implementation", "tier_1", 0.86),
            ("cryptography key management", "tier_1", 0.84),
            ("TLS certificate configuration", "tier_1", 0.83)
        ]
        
        passed_tests = 0
        for test_input, expected_tier, min_confidence in tier_1_cases:
            analysis = security_matcher.analyze_security_request(test_input)
            
            # Verify tier classification
            pattern_tier = analysis.get("pattern_tier")
            assert pattern_tier == expected_tier, \
                f"Expected tier '{expected_tier}' but got '{pattern_tier}' for '{test_input}'"
            
            # Verify high confidence
            actual_confidence = analysis["confidence_score"]
            if actual_confidence >= min_confidence:
                passed_tests += 1
            else:
                pytest.fail(
                    f"Tier 1 pattern test failed for '{test_input}': "
                    f"expected >={min_confidence}, got {actual_confidence:.3f}"
                )
        
        tier_1_accuracy = passed_tests / len(tier_1_cases)
        assert tier_1_accuracy >= 0.85, f"Tier 1 accuracy {tier_1_accuracy:.2%} below 85% target"
    
    def test_tier_2_context_enhanced_patterns(self, security_matcher):
        """Test Tier 2 context-enhanced security patterns (85%+ accuracy)"""
        tier_2_cases = [
            # Security Operations
            ("security incident response monitoring", "tier_2", 0.85),
            ("vulnerability management scanning process", "tier_2", 0.87),
            ("security testing validation requirements", "tier_2", 0.83),
            
            # Application Security
            ("application security hardening guide", "tier_2", 0.86),
            ("web application firewall protection", "tier_2", 0.84),
            ("API security authentication setup", "tier_2", 0.88),
            ("input validation security filtering", "tier_2", 0.82),
            
            # Infrastructure Security
            ("container security scanning tools", "tier_2", 0.85),
            ("cloud security configuration review", "tier_2", 0.87),
            ("network security segmentation plan", "tier_2", 0.83),
            ("endpoint security detection system", "tier_2", 0.84),
            
            # Security Monitoring & Response
            ("security monitoring alerting dashboard", "tier_2", 0.86),
            ("incident response handling procedures", "tier_2", 0.85),
            ("digital forensics investigation tools", "tier_2", 0.81)
        ]
        
        passed_tests = 0
        for test_input, expected_tier, min_confidence in tier_2_cases:
            analysis = security_matcher.analyze_security_request(test_input)
            
            # Verify appropriate tier (tier_2 or higher)
            pattern_tier = analysis.get("pattern_tier")
            assert pattern_tier in ["tier_1", "tier_2"], \
                f"Expected tier 1 or 2 but got '{pattern_tier}' for '{test_input}'"
            
            # Verify confidence meets threshold
            actual_confidence = analysis["confidence_score"]
            if actual_confidence >= min_confidence:
                passed_tests += 1
            else:
                pytest.fail(
                    f"Tier 2 pattern test failed for '{test_input}': "
                    f"expected >={min_confidence}, got {actual_confidence:.3f}"
                )
        
        tier_2_accuracy = passed_tests / len(tier_2_cases)
        assert tier_2_accuracy >= 0.80, f"Tier 2 accuracy {tier_2_accuracy:.2%} below 80% target"
    
    def test_natural_language_security_patterns(self, security_matcher):
        """Test natural language security pattern recognition (75%+ accuracy)"""
        natural_language_cases = [
            # Common security concerns in natural language
            ("check our application security", "tier_3", 0.75),
            ("verify system security setup", "tier_3", 0.78),
            ("ensure data security compliance", "tier_3", 0.80),
            ("make our API more secure", "tier_3", 0.76),
            ("protect against potential attacks", "tier_3", 0.79),
            ("harden our infrastructure security", "tier_3", 0.77),
            
            # Security concerns and issues
            ("we have security issues to resolve", "tier_3", 0.75),
            ("security problems in our system", "tier_3", 0.78),
            ("concerned about security risks", "tier_3", 0.76),
            ("our system might be vulnerable", "tier_3", 0.74),
            ("suspicious activity detected", "tier_3", 0.77),
            
            # Security-related actions
            ("scan for security vulnerabilities", "tier_3", 0.79),
            ("test our security measures", "tier_3", 0.76),
            ("audit security permissions", "tier_3", 0.80),
            ("review security configuration", "tier_3", 0.78),
            ("prevent security breaches", "tier_3", 0.77),
            ("detect security threats early", "tier_3", 0.75),
            ("mitigate attack vectors", "tier_3", 0.79),
            ("find security vulnerabilities", "tier_3", 0.76)
        ]
        
        passed_tests = 0
        for test_input, expected_tier_min, min_confidence in natural_language_cases:
            analysis = security_matcher.analyze_security_request(test_input)
            
            # Verify domain match is detected
            assert analysis["domain_match"], f"Domain not detected for natural language input: '{test_input}'"
            
            # Verify confidence meets threshold
            actual_confidence = analysis["confidence_score"]
            if actual_confidence >= min_confidence:
                passed_tests += 1
            else:
                pytest.fail(
                    f"Natural language test failed for '{test_input}': "
                    f"expected >={min_confidence}, got {actual_confidence:.3f}"
                )
        
        natural_language_accuracy = passed_tests / len(natural_language_cases)
        assert natural_language_accuracy >= 0.75, f"Natural language accuracy {natural_language_accuracy:.2%} below 75% target"
    
    def test_security_complexity_detection(self, security_matcher):
        """Test security complexity level detection and agent recommendation"""
        complexity_cases = [
            # Basic security
            ("password security policy", "basic_security", "security-enforcer"),
            ("basic authentication setup", "basic_security", "security-enforcer"),
            ("simple encryption implementation", "basic_security", "security-enforcer"),
            
            # Intermediate security
            ("vulnerability assessment process", "intermediate_security", "security-enforcer"),
            ("security hardening procedures", "intermediate_security", "security-enforcer"),
            ("compliance audit requirements", "intermediate_security", "security-enforcer"),
            ("penetration testing methodology", "intermediate_security", "security-enforcer"),
            ("threat modeling approach", "intermediate_security", "security-enforcer"),
            
            # Advanced security (should escalate to security-auditor)
            ("zero trust architecture implementation", "advanced_security", "security-auditor"),
            ("advanced threat detection system", "advanced_security", "security-auditor"),
            ("security orchestration platform", "advanced_security", "security-auditor"),
            ("threat intelligence integration", "advanced_security", "security-auditor"),
            ("multi-domain security coordination", "advanced_security", "security-auditor")
        ]
        
        for test_input, expected_complexity, expected_agent in complexity_cases:
            analysis = security_matcher.analyze_security_request(test_input)
            
            actual_complexity = analysis["complexity_level"]
            actual_agent = analysis["agent_recommendation"]
            
            assert actual_complexity == expected_complexity, \
                f"Expected complexity '{expected_complexity}' but got '{actual_complexity}' for '{test_input}'"
            
            assert actual_agent == expected_agent, \
                f"Expected agent '{expected_agent}' but got '{actual_agent}' for '{test_input}'"
    
    def test_enhanced_intent_indicators(self, security_matcher):
        """Test enhanced intent indicator recognition (185% increase)"""
        intent_cases = [
            # Current intent indicators (preserved)
            ("secure our application", "secure"),
            ("audit security permissions", "audit"),
            ("validate security setup", "validate"),
            ("scan for vulnerabilities", "scan"),
            ("harden system security", "harden"),
            ("protect against attacks", "protect"),
            ("encrypt sensitive data", "encrypt"),
            
            # New intent indicators
            ("assess security risks", "assess"),
            ("test security measures", "test"),
            ("review security policies", "review"),
            ("monitor security events", "monitor"),
            ("detect security threats", "detect"),
            ("prevent security breaches", "prevent"),
            ("mitigate attack vectors", "mitigate"),
            ("investigate security incident", "investigate"),
            ("analyze security posture", "analyze"),
            ("verify security compliance", "verify"),
            ("certify security standards", "certify"),
            ("authorize security access", "authorize"),
            ("authenticate user identity", "authenticate")
        ]
        
        for test_input, expected_intent in intent_cases:
            analysis = security_matcher.analyze_security_request(test_input)
            
            intent_matches = analysis["enhancement_details"]["intent_matches"]
            assert expected_intent in [i.lower() for i in intent_matches], \
                f"Expected intent '{expected_intent}' not detected in '{test_input}'"
            
            # Verify domain is matched
            assert analysis["domain_match"], f"Domain not detected for intent test: '{test_input}'"
    
    def test_performance_impact(self, security_matcher):
        """Test performance impact of enhanced patterns"""
        test_inputs = [
            "security vulnerability assessment",
            "threat modeling analysis",
            "GDPR compliance audit",
            "penetration testing schedule",
            "zero trust architecture"
        ]
        
        response_times = []
        
        for test_input in test_inputs:
            start_time = time.time()
            analysis = security_matcher.analyze_security_request(test_input)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            response_times.append(response_time)
            
            # Verify analysis is successful
            assert analysis["domain_match"], f"Failed to analyze: '{test_input}'"
        
        avg_response_time = statistics.mean(response_times)
        max_response_time = max(response_times)
        
        # Performance requirements: average <100ms, max <500ms
        assert avg_response_time < 100, f"Average response time {avg_response_time:.2f}ms exceeds 100ms limit"
        assert max_response_time < 500, f"Maximum response time {max_response_time:.2f}ms exceeds 500ms limit"
    
    def test_cross_domain_interference(self, security_matcher):
        """Test that security enhancements don't interfere with other domains"""
        non_security_cases = [
            ("test pytest configuration", False),  # Testing domain
            ("docker container orchestration", False),  # Infrastructure domain
            ("performance optimization analysis", False),  # Performance domain
            ("code refactoring improvements", False),  # Code quality domain
            ("API documentation update", False)  # Documentation domain
        ]
        
        for test_input, should_match_security in non_security_cases:
            analysis = security_matcher.analyze_security_request(test_input)
            
            if should_match_security:
                assert analysis["domain_match"], f"Expected security match for: '{test_input}'"
            else:
                # Should have low confidence for non-security domains
                confidence = analysis["confidence_score"]
                assert confidence < 0.70, \
                    f"Security confidence too high ({confidence:.3f}) for non-security input: '{test_input}'"
    
    def test_comprehensive_accuracy_target(self, security_matcher):
        """Test overall accuracy target of 85%"""
        # Comprehensive test suite covering all enhancement aspects
        comprehensive_cases = [
            # Baseline compatibility (10 cases)
            ("security scan audit", 0.80),
            ("vulnerability assessment", 0.85),
            ("credential management", 0.82),
            ("authentication flow", 0.78),
            ("compliance validation", 0.83),
            ("authorization policy", 0.80),
            ("encryption data", 0.81),
            ("security hardening", 0.84),
            ("audit requirements", 0.79),
            ("access control", 0.77),
            
            # Enhanced patterns (15 cases)
            ("threat modeling analysis", 0.88),
            ("attack vector assessment", 0.85),
            ("penetration testing", 0.92),
            ("GDPR compliance audit", 0.90),
            ("zero trust architecture", 0.89),
            ("multi factor authentication", 0.87),
            ("security incident response", 0.86),
            ("vulnerability management", 0.84),
            ("application security testing", 0.85),
            ("network security monitoring", 0.83),
            ("cloud security hardening", 0.87),
            ("encryption key management", 0.82),
            ("security orchestration", 0.88),
            ("threat intelligence", 0.85),
            ("security governance", 0.84),
            
            # Natural language (10 cases)
            ("make our system secure", 0.78),
            ("check for security issues", 0.80),
            ("protect against attacks", 0.76),
            ("ensure security compliance", 0.82),
            ("verify system security", 0.79),
            ("scan for vulnerabilities", 0.81),
            ("review security setup", 0.77),
            ("improve security posture", 0.78),
            ("prevent security breaches", 0.80),
            ("detect security threats", 0.76)
        ]
        
        passed_tests = 0
        total_tests = len(comprehensive_cases)
        
        for test_input, min_confidence in comprehensive_cases:
            analysis = security_matcher.analyze_security_request(test_input)
            actual_confidence = analysis["confidence_score"]
            
            if actual_confidence >= min_confidence:
                passed_tests += 1
        
        overall_accuracy = passed_tests / total_tests
        
        # Target: 85% accuracy
        assert overall_accuracy >= 0.85, \
            f"Overall accuracy {overall_accuracy:.2%} below 85% target ({passed_tests}/{total_tests} passed)"
    
    def test_enhanced_configuration_metadata(self, security_matcher):
        """Test enhanced configuration metadata"""
        config = security_matcher.get_enhanced_agent_config()
        
        # Verify enhanced counts
        assert len(config['primary_keywords']) >= 15, "Should have at least 15 primary keywords"
        assert len(config['context_patterns']) >= 50, "Should have at least 50 context patterns"
        assert len(config['intent_indicators']) >= 20, "Should have at least 20 intent indicators"
        
        # Verify enhancement metadata
        metadata = config['enhancement_metadata']
        assert metadata['version'] == '2.0_enhanced', "Version should indicate enhancement"
        assert metadata['accuracy_target'] == '85%', "Target accuracy should be 85%"
        
        # Verify specialization areas are expanded
        specialization_areas = config['specialization_areas']
        expected_areas = [
            'vulnerability_scanning', 'compliance', 'authentication', 'encryption',
            'threat_modeling', 'penetration_testing', 'security_architecture',
            'incident_response', 'risk_assessment', 'security_governance'
        ]
        
        for area in expected_areas:
            assert area in specialization_areas, f"Missing specialization area: {area}"

# Integration test with existing agent selection framework
def test_integration_with_agent_selector():
    """Test integration with existing agent selector"""
    matcher = EnhancedSecurityPatternMatcher()
    config = matcher.get_enhanced_agent_config()
    
    # Verify configuration format matches expected agent config structure
    required_fields = ['name', 'primary_keywords', 'context_patterns', 'intent_indicators', 
                      'weight_multiplier', 'description', 'specialization_areas']
    
    for field in required_fields:
        assert field in config, f"Missing required field: {field}"
    
    # Verify backward compatibility with current structure
    assert config['name'] == 'security-enforcer', "Agent name should remain consistent"
    assert isinstance(config['weight_multiplier'], (int, float)), "Weight multiplier should be numeric"
    assert len(config['description']) > 0, "Description should not be empty"

if __name__ == "__main__":
    # Run comprehensive validation when script is executed directly
    
    matcher = EnhancedSecurityPatternMatcher()
    
    print("Running Enhanced Security Domain Validation...")
    print("=" * 60)
    
    # Test configuration
    config = matcher.get_enhanced_agent_config()
    print("Enhanced Configuration:")
    print(f"  Primary Keywords: {len(config['primary_keywords'])} (baseline: 6)")
    print(f"  Context Patterns: {len(config['context_patterns'])} (baseline: 7)")
    print(f"  Intent Indicators: {len(config['intent_indicators'])} (baseline: 7)")
    print(f"  Target Accuracy: {config['enhancement_metadata']['accuracy_target']}")
    print()
    
    # Run sample tests
    test_cases = [
        "security vulnerability assessment",
        "threat modeling analysis",
        "GDPR compliance audit",
        "make our API secure",
        "zero trust architecture"
    ]
    
    print("Sample Test Results:")
    print(f"{'Input':<35} {'Confidence':<10} {'Tier':<8} {'Agent':<16}")
    print("-" * 70)
    
    for test_input in test_cases:
        analysis = matcher.analyze_security_request(test_input)
        confidence = analysis['confidence_score']
        tier = analysis.get('pattern_tier', 'N/A')
        agent = analysis['agent_recommendation']
        
        print(f"{test_input:<35} {confidence:<10.3f} {tier:<8} {agent:<16}")
    
    print("\nTo run complete test suite:")
    print("  pytest test_security_domain_enhancement.py -v")
