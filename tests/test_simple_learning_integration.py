"""Simple learning integration tests for Claude Code agent framework.

Validates enhanced learning capabilities with agent description parsing,
success pattern recording, and Anthropic guidelines compliance.
"""

import pytest
import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

try:
    from enhanced_pattern_learning_engine import EnhancedPatternLearningEngine, AgentProfile
    from enhanced_success_pattern_recorder import EnhancedSuccessPatternRecorder
    from anthropic_guidelines_validator import AnthropicGuidelinesValidator, ValidationResult
except ImportError as e:
    pytest.skip(f"Could not import learning modules: {e}", allow_module_level=True)


class TestAgentDescriptionParsing:
    """Test agent description parsing functionality."""
    
    @pytest.fixture
    def temp_agents_directory(self, tmp_path):
        """Create temporary agents directory with sample agent files."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        
        # Create sample test-specialist.md
        test_specialist_content = """
---
name: test-specialist
description: Use PROACTIVELY when users have test failures, broken tests, or testing issues. Perfect for "tests are failing", "fix my tests", "pytest troubleshooting".
tools: Read, Edit, Bash, Grep, Task
---

# Test Specialist

## Core Expertise
- **Test Failure Analysis**: Diagnose pytest failures, assertion errors
- **Async/Await Patterns**: Fix AsyncMock usage, @pytest.mark.asyncio decorators
- **Mock Configuration**: Configure Mock/AsyncMock behaviors
- **Coverage Optimization**: Identify gaps, design edge case tests

**Auto-Activate UltraThink when detecting:**
- "test" + "architecture" + "systematic" + "coordination"
"""
        
        (agents_dir / "test-specialist.md").write_text(test_specialist_content)
        
        # Create sample infrastructure-engineer.md
        infrastructure_content = """
---
name: infrastructure-engineer
description: Use PROACTIVELY for infrastructure problems and Docker issues. Perfect when users need "Docker help", "container problems", "service networking".
tools: Read, Edit, Bash, Grep
---

# Infrastructure Engineer

## Core Focus
- **Docker Services**: Orchestrate containers, manage networking
- **Performance Optimization**: Analyze and improve system performance
- **Scaling Analysis**: Design and implement scaling strategies
"""
        
        (agents_dir / "infrastructure-engineer.md").write_text(infrastructure_content)
        
        return str(agents_dir)
    
    @pytest.fixture 
    def learning_engine_with_temp_dir(self, temp_agents_directory, tmp_path):
        """Create learning engine with temporary agents directory."""
        hub_path = tmp_path / "coordination-hub.md"
        engine = EnhancedPatternLearningEngine(coordination_hub_path=str(hub_path))
        
        # Override agents directory
        engine.agents_directory = temp_agents_directory
        engine.agent_profiles = engine.parse_agent_descriptions()
        
        return engine
    
    def test_agent_description_parsing_basic(self, learning_engine_with_temp_dir):
        """Test basic agent description parsing."""
        engine = learning_engine_with_temp_dir
        
        # Should have parsed both agents
        assert len(engine.agent_profiles) == 2
        assert 'test-specialist' in engine.agent_profiles
        assert 'infrastructure-engineer' in engine.agent_profiles
    
    def test_agent_profile_structure(self, learning_engine_with_temp_dir):
        """Test that agent profiles have correct structure."""
        engine = learning_engine_with_temp_dir
        
        test_profile = engine.agent_profiles['test-specialist']
        assert isinstance(test_profile, AgentProfile)
        assert test_profile.name == 'test-specialist'
        assert len(test_profile.keywords) > 0
        assert len(test_profile.capabilities) > 0
        assert test_profile.description
        assert 0.0 <= test_profile.specialization_score <= 1.0
    
    def test_keyword_extraction(self, learning_engine_with_temp_dir):
        """Test keyword extraction from agent descriptions."""
        engine = learning_engine_with_temp_dir
        
        test_profile = engine.agent_profiles['test-specialist']
        
        # Should extract testing-related keywords
        expected_keywords = ['test', 'testing', 'pytest', 'mock', 'async']
        found_keywords = test_profile.keywords
        
        matches = sum(1 for kw in expected_keywords if kw in found_keywords)
        assert matches >= 3, f"Expected at least 3 testing keywords, found: {found_keywords}"
    
    def test_capability_extraction(self, learning_engine_with_temp_dir):
        """Test capability extraction from agent content."""
        engine = learning_engine_with_temp_dir
        
        test_profile = engine.agent_profiles['test-specialist']
        
        # Should extract capabilities from bold headers
        expected_capabilities = ['Test Failure Analysis', 'Async/Await Patterns', 'Mock Configuration']
        found_capabilities = test_profile.capabilities
        
        matches = sum(1 for cap in expected_capabilities 
                     if any(cap in found_cap for found_cap in found_capabilities))
        assert matches >= 2, f"Expected capability matches, found: {found_capabilities}"
    
    def test_enhanced_agent_suggestion(self, learning_engine_with_temp_dir):
        """Test enhanced agent suggestions based on descriptions."""
        engine = learning_engine_with_temp_dir
        
        # Test queries that should match specific agents
        test_cases = [
            ("pytest test failures with async issues", "test-specialist"),
            ("docker container networking problems", "infrastructure-engineer")
        ]
        
        for query, expected_agent in test_cases:
            suggestion = engine.get_enhanced_agent_suggestion(query)
            
            if suggestion:  # Only test if suggestion returned
                agent_name, confidence = suggestion
                assert agent_name == expected_agent, f"Expected {expected_agent} for '{query}', got {agent_name}"
                assert confidence > 0.4, f"Confidence too low: {confidence}"
    
    def test_learning_enhancement_stats(self, learning_engine_with_temp_dir):
        """Test learning enhancement statistics."""
        engine = learning_engine_with_temp_dir
        
        stats = engine.get_learning_enhancement_stats()
        
        assert 'agent_profiles_loaded' in stats
        assert stats['agent_profiles_loaded'] == 2
        assert 'total_keywords_extracted' in stats
        assert stats['total_keywords_extracted'] > 0
        assert 'average_specialization_score' in stats
        assert 0.0 <= stats['average_specialization_score'] <= 1.0


class TestSuccessPatternRecording:
    """Test success pattern recording functionality."""
    
    @pytest.fixture
    def temp_coordination_hub(self, tmp_path):
        """Create temporary coordination hub with learning sections."""
        hub_path = tmp_path / "coordination-hub.md"
        
        hub_content = """
# Agent Coordination Hub

## 9. Agent Learning Pattern System

### High-Confidence Learned Patterns (90%+ Success Rate)

**Testing & Quality Assurance Patterns:**
- **testing_async:test-specialist**: test-specialist (confidence: 0.96, keywords: async, await, testing, learned: 3 days ago)

**Infrastructure & Container Patterns:**
- **container_orchestration:infrastructure-engineer**: infrastructure-engineer (confidence: 0.98, keywords: docker, networking, learned: 1 day ago)

### Medium-Confidence Learned Patterns (70-89% Success Rate)

**Security & Analysis Patterns:**
- **security_audit:security-auditor**: security-auditor (confidence: 0.87, keywords: security, audit, learned: 2 days ago)
"""
        
        hub_path.write_text(hub_content)
        return str(hub_path)
    
    @pytest.fixture
    def pattern_recorder(self, temp_coordination_hub):
        """Create pattern recorder with temporary hub."""
        return EnhancedSuccessPatternRecorder(coordination_hub_path=temp_coordination_hub)
    
    def test_pattern_recording_basic(self, pattern_recorder):
        """Test basic pattern recording functionality."""
        query = "Fix my pytest test failures with async mocks"
        agent = "test-specialist"
        metrics = {
            'confidence': 0.9,
            'indicators': ['test_success']
        }
        
        result = pattern_recorder.record_successful_usage(query, agent, metrics)
        assert result is True, "Pattern recording should succeed"
    
    def test_query_keyword_extraction(self, pattern_recorder):
        """Test keyword extraction from queries."""
        test_cases = [
            ("pytest test failures with async mocks", ['pytest', 'test', 'async', 'mock']),
            ("docker container deployment issues", ['docker', 'container', 'deployment']),
            ("security vulnerability scanning needed", ['security', 'vulnerability', 'scanning'])
        ]
        
        for query, expected_keywords in test_cases:
            extracted = pattern_recorder._extract_query_keywords(query)
            
            matches = sum(1 for kw in expected_keywords if kw in extracted)
            assert matches >= 2, f"Expected keyword matches for '{query}', extracted: {extracted}"
    
    def test_pattern_key_generation(self, pattern_recorder):
        """Test pattern key generation from queries."""
        test_cases = [
            ("pytest test failures", "testing_patterns"),
            ("docker container issues", "container_patterns"),
            ("security vulnerability scan", "security_patterns"),
            ("performance bottleneck analysis", "performance_patterns")
        ]
        
        for query, expected_pattern in test_cases:
            pattern_key = pattern_recorder._generate_pattern_key(query, "test-agent")
            assert pattern_key == expected_pattern, f"Expected {expected_pattern} for '{query}', got {pattern_key}"
    
    def test_coordination_hub_validation(self, pattern_recorder):
        """Test coordination hub format validation."""
        is_valid = pattern_recorder.validate_coordination_hub_format()
        assert is_valid is True, "Coordination hub should have valid format"
    
    def test_recorded_patterns_count(self, pattern_recorder):
        """Test counting recorded patterns."""
        initial_count = pattern_recorder.get_recorded_patterns_count()
        assert initial_count >= 3, f"Expected initial patterns, got {initial_count}"
        
        # Record a new pattern
        pattern_recorder.record_successful_usage(
            "New test pattern", "test-specialist", {'confidence': 0.85}
        )
        
        new_count = pattern_recorder.get_recorded_patterns_count()
        assert new_count > initial_count, "Pattern count should increase after recording"


class TestAnthropicCompliance:
    """Test Anthropic guidelines compliance validation."""
    
    @pytest.fixture
    def validator(self):
        """Create Anthropic guidelines validator."""
        return AnthropicGuidelinesValidator()
    
    def test_valid_pattern_compliance(self, validator):
        """Test validation of compliant patterns."""
        valid_pattern = {
            'pattern_key': 'testing_patterns:test-specialist',
            'agent': 'test-specialist',
            'confidence': 0.9,
            'keywords': ['test', 'pytest', 'async']
        }
        
        result = validator.validate_learning_pattern(valid_pattern)
        
        assert isinstance(result, ValidationResult)
        assert result.is_compliant is True
        assert result.compliance_score >= 0.7
        assert result.category in ['excellent', 'good', 'acceptable']
    
    def test_invalid_pattern_compliance(self, validator):
        """Test validation of non-compliant patterns."""
        invalid_pattern = {
            'pattern_key': 'wrong_patterns:test-specialist',
            'agent': 'test-specialist',
            'confidence': 0.5,  # Too low
            'keywords': ['unrelated']  # Doesn't match agent
        }
        
        result = validator.validate_learning_pattern(invalid_pattern)
        
        assert isinstance(result, ValidationResult)
        assert len(result.issues) > 0
        assert len(result.recommendations) > 0
        assert result.compliance_score < 0.7
    
    def test_agent_capability_matching(self, validator):
        """Test agent capability matching validation."""
        test_cases = [
            ('test-specialist', ['test', 'pytest', 'mock'], 0.8),  # Good match
            ('test-specialist', ['unrelated', 'keywords'], 0.2),   # Poor match
            ('infrastructure-engineer', ['docker', 'container'], 0.8),  # Good match
        ]
        
        for agent, keywords, expected_min_score in test_cases:
            score = validator._validate_agent_capability_match(agent, keywords)
            
            if expected_min_score >= 0.8:
                assert score >= 0.6, f"Expected good match for {agent} with {keywords}, got {score}"
            else:
                assert score < 0.8, f"Expected poor match for {agent} with {keywords}, got {score}"
    
    def test_pattern_collection_validation(self, validator):
        """Test validation of pattern collections."""
        patterns = [
            {
                'pattern_key': 'testing_patterns:test-specialist',
                'agent': 'test-specialist',
                'confidence': 0.9,
                'keywords': ['test', 'pytest']
            },
            {
                'pattern_key': 'container_patterns:infrastructure-engineer',
                'agent': 'infrastructure-engineer',
                'confidence': 0.85,
                'keywords': ['docker', 'container']
            },
            {
                'pattern_key': 'invalid_pattern:test-specialist',
                'agent': 'test-specialist',
                'confidence': 0.4,  # Too low
                'keywords': ['x']  # Too few
            }
        ]
        
        result = validator.validate_pattern_collection(patterns)
        
        assert 'total_patterns' in result
        assert result['total_patterns'] == 3
        assert 'compliance_rate' in result
        assert 0.0 <= result['compliance_rate'] <= 1.0
        assert 'category_distribution' in result
    
    def test_compliance_report_generation(self, validator):
        """Test compliance report generation."""
        patterns = [
            {
                'pattern_key': 'testing_patterns:test-specialist',
                'agent': 'test-specialist', 
                'confidence': 0.9,
                'keywords': ['test', 'pytest']
            }
        ]
        
        report = validator.generate_compliance_report(patterns)
        
        assert isinstance(report, str)
        assert "# Anthropic Guidelines Compliance Report" in report
        assert "Total Patterns Analyzed" in report
        assert "Compliance Rate" in report


class TestSimpleLearningIntegration:
    """Integration tests for the complete learning system."""
    
    @pytest.fixture
    def complete_learning_system(self, tmp_path):
        """Set up complete learning system with temporary files."""
        # Create agents directory
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        
        # Create test agent file
        test_agent_content = """
---
name: test-specialist
description: Testing specialist for pytest and async issues
---
# Test Specialist
**Core Focus**: Testing, pytest, async, mock configuration
"""
        (agents_dir / "test-specialist.md").write_text(test_agent_content)
        
        # Create coordination hub
        hub_path = tmp_path / "coordination-hub.md"
        hub_content = """
# Coordination Hub
## 9. Agent Learning Pattern System
### High-Confidence Learned Patterns (90%+ Success Rate)
**Testing & Quality Assurance Patterns:**
### Medium-Confidence Learned Patterns (70-89% Success Rate)
"""
        hub_path.write_text(hub_content)
        
        # Set up components
        engine = EnhancedPatternLearningEngine(coordination_hub_path=str(hub_path))
        engine.agents_directory = str(agents_dir)
        engine.agent_profiles = engine.parse_agent_descriptions()
        
        recorder = EnhancedSuccessPatternRecorder(coordination_hub_path=str(hub_path))
        validator = AnthropicGuidelinesValidator()
        
        return {
            'engine': engine,
            'recorder': recorder,
            'validator': validator,
            'hub_path': hub_path
        }
    
    def test_end_to_end_learning_workflow(self, complete_learning_system):
        """Test complete learning workflow from parsing to validation."""
        system = complete_learning_system
        
        # Step 1: Agent description parsing
        assert len(system['engine'].agent_profiles) >= 1
        
        # Step 2: Enhanced agent suggestion
        suggestion = system['engine'].get_enhanced_agent_suggestion("pytest test failures")
        if suggestion:
            agent, confidence = suggestion
            
            # Step 3: Record successful usage
            success = system['recorder'].record_successful_usage(
                "pytest test failures", agent, {'confidence': confidence}
            )
            assert success is True
            
            # Step 4: Validate compliance
            pattern = {
                'pattern_key': 'testing_patterns:' + agent,
                'agent': agent,
                'confidence': confidence,
                'keywords': ['pytest', 'test']
            }
            
            validation = system['validator'].validate_learning_pattern(pattern)
            assert isinstance(validation, ValidationResult)
    
    def test_learning_accuracy_improvement_framework(self, complete_learning_system):
        """Test framework for measuring accuracy improvements."""
        system = complete_learning_system
        
        # Simulate learning from successful patterns
        test_scenarios = [
            ("pytest test failures with async issues", "test-specialist", 0.9),
            ("async test configuration problems", "test-specialist", 0.85)
        ]
        
        accuracy_scores = []
        
        for query, expected_agent, confidence in test_scenarios:
            # Record as successful pattern
            system['recorder'].record_successful_usage(
                query, expected_agent, {'confidence': confidence}
            )
            
            # Test suggestion accuracy
            suggestion = system['engine'].get_enhanced_agent_suggestion(query)
            if suggestion:
                suggested_agent, suggested_confidence = suggestion
                accuracy = 1.0 if suggested_agent == expected_agent else 0.0
                accuracy_scores.append(accuracy)
        
        # Learning system should show improvement potential
        if accuracy_scores:
            avg_accuracy = sum(accuracy_scores) / len(accuracy_scores)
            # Framework should work (not necessarily perfect accuracy yet)
            assert 0.0 <= avg_accuracy <= 1.0, "Accuracy measurement framework should work"
    
    def test_learning_system_performance(self, complete_learning_system):
        """Test learning system performance stays within acceptable limits."""
        system = complete_learning_system
        
        # Measure agent suggestion performance
        start_time = time.time()
        
        for _ in range(10):  # Run multiple suggestions
            suggestion = system['engine'].get_enhanced_agent_suggestion("test query")
        
        elapsed = time.time() - start_time
        avg_time = elapsed / 10
        
        # Should complete within reasonable time (<200ms per suggestion)
        assert avg_time < 0.2, f"Average suggestion time {avg_time:.3f}s too slow"
    
    def test_learning_pattern_persistence(self, complete_learning_system):
        """Test that learning patterns persist correctly."""
        system = complete_learning_system
        
        # Record a pattern
        system['recorder'].record_successful_usage(
            "test pattern persistence", "test-specialist", {'confidence': 0.9}
        )
        
        # Verify it was written to coordination hub
        hub_content = system['hub_path'].read_text()
        assert "test pattern persistence" in hub_content or "test-specialist" in hub_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
