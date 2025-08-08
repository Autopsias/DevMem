"""Tests for agent pattern matching and selection performance."""

import pytest
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import re
from collections import defaultdict


@dataclass
class AgentMatchResult:
    """Result of agent pattern matching."""
    agent_name: str
    confidence_score: float
    matched_patterns: List[str]
    processing_time_ms: float
    context_keywords: List[str] = field(default_factory=list)


@dataclass
class TestQuery:
    """Test query with expected agent selection."""
    query: str
    expected_agent: str
    expected_confidence_range: Tuple[float, float]
    context_keywords: List[str] = field(default_factory=list)
    variations: List[str] = field(default_factory=list)


class CurrentPatternMatcher:
    """Current pattern matching implementation for baseline testing."""
    
    def __init__(self):
        self.agent_patterns = {
            'test-specialist': [
                r'test.*fail',
                r'pytest.*error',
                r'async.*test',
                r'mock.*config',
                r'coverage.*gap',
                r'test.*suite'
            ],
            'infrastructure-engineer': [
                r'docker.*orchestration',
                r'container.*network',
                r'service.*scaling',
                r'infrastructure.*performance',
                r'deployment.*issue'
            ],
            'security-enforcer': [
                r'security.*pattern',
                r'vulnerability.*scan',
                r'credential.*leak',
                r'authentication.*flow',
                r'security.*audit'
            ],
            'performance-optimizer': [
                r'performance.*bottleneck',
                r'latency.*optimization',
                r'resource.*usage',
                r'scaling.*performance',
                r'memory.*optimization'
            ],
            'intelligent-enhancer': [
                r'code.*refactor',
                r'variable.*naming',
                r'function.*split',
                r'type.*annotation',
                r'architecture.*improve'
            ]
        }
    
    def match_agent(self, query: str) -> AgentMatchResult:
        """Match query to best agent using current algorithm."""
        start_time = time.perf_counter()
        query_lower = query.lower()
        
        best_agent = None
        best_score = 0.0
        matched_patterns = []
        
        for agent_name, patterns in self.agent_patterns.items():
            score = 0.0
            agent_matches = []
            
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    score += 1.0
                    agent_matches.append(pattern)
            
            if score > best_score:
                best_score = score
                best_agent = agent_name
                matched_patterns = agent_matches
        
        # Fallback to intelligent-enhancer if no matches
        if best_agent is None:
            best_agent = 'intelligent-enhancer'
            best_score = 0.1
        
        processing_time = (time.perf_counter() - start_time) * 1000
        
        return AgentMatchResult(
            agent_name=best_agent,
            confidence_score=best_score,
            matched_patterns=matched_patterns,
            processing_time_ms=processing_time
        )


class EnhancedPatternMatcher:
    """Enhanced pattern matching with improved algorithms."""
    
    def __init__(self):
        self.agent_patterns = {
            'test-specialist': {
                'primary_keywords': ['test', 'pytest', 'mock', 'coverage', 'async'],
                'context_patterns': [
                    r'test.{0,20}(fail|error|break)',
                    r'pytest.{0,15}(config|fixture|mark)',
                    r'async.{0,10}test',
                    r'mock.{0,15}(config|patch|assert)',
                    r'coverage.{0,10}(gap|report|analysis)',
                    r'integration.{0,10}test'
                ],
                'intent_indicators': ['need', 'fix', 'resolve', 'debug', 'analyze'],
                'weight_multiplier': 1.2
            },
            'infrastructure-engineer': {
                'primary_keywords': ['docker', 'container', 'service', 'infrastructure', 'deployment'],
                'context_patterns': [
                    r'docker.{0,20}(orchestration|compose|network)',
                    r'container.{0,15}(scaling|network|resource)',
                    r'service.{0,15}(mesh|discovery|communication)',
                    r'infrastructure.{0,20}(performance|scaling|architecture)',
                    r'deployment.{0,15}(pipeline|strategy|automation)'
                ],
                'intent_indicators': ['deploy', 'scale', 'orchestrate', 'optimize', 'architect'],
                'weight_multiplier': 1.1
            },
            'security-enforcer': {
                'primary_keywords': ['security', 'vulnerability', 'credential', 'authentication', 'audit'],
                'context_patterns': [
                    r'security.{0,20}(pattern|scan|audit|review)',
                    r'vulnerability.{0,15}(assessment|scan|analysis)',
                    r'credential.{0,15}(leak|management|rotation)',
                    r'authentication.{0,15}(flow|token|session)',
                    r'compliance.{0,15}(validation|audit|standard)'
                ],
                'intent_indicators': ['secure', 'audit', 'validate', 'scan', 'harden'],
                'weight_multiplier': 1.3
            },
            'performance-optimizer': {
                'primary_keywords': ['performance', 'latency', 'optimization', 'bottleneck', 'resource'],
                'context_patterns': [
                    r'performance.{0,20}(bottleneck|optimization|analysis)',
                    r'latency.{0,15}(reduction|optimization|measurement)',
                    r'resource.{0,15}(usage|allocation|optimization)',
                    r'memory.{0,15}(usage|leak|optimization)',
                    r'cpu.{0,15}(usage|optimization|profiling)'
                ],
                'intent_indicators': ['optimize', 'improve', 'reduce', 'enhance', 'accelerate'],
                'weight_multiplier': 1.0
            },
            'intelligent-enhancer': {
                'primary_keywords': ['refactor', 'variable', 'function', 'type', 'architecture'],
                'context_patterns': [
                    r'code.{0,15}(refactor|improvement|enhancement)',
                    r'variable.{0,15}(naming|renaming|improvement)',
                    r'function.{0,15}(split|extract|optimize)',
                    r'type.{0,15}(annotation|hint|system)',
                    r'architecture.{0,15}(improvement|refactoring|design)'
                ],
                'intent_indicators': ['refactor', 'improve', 'enhance', 'clean', 'restructure'],
                'weight_multiplier': 0.9
            }
        }
        
        # Build keyword index for fast lookup
        self.keyword_index = defaultdict(list)
        for agent_name, config in self.agent_patterns.items():
            for keyword in config['primary_keywords']:
                self.keyword_index[keyword].append(agent_name)
    
    def extract_keywords(self, query: str) -> List[str]:
        """Extract relevant keywords from query."""
        query_lower = query.lower()
        keywords = []
        
        # Extract primary keywords
        for keyword in self.keyword_index.keys():
            if keyword in query_lower:
                keywords.append(keyword)
        
        return keywords
    
    def calculate_semantic_similarity(self, query: str, agent_config: Dict) -> float:
        """Calculate semantic similarity score."""
        query_lower = query.lower()
        score = 0.0
        
        # Primary keyword matching with proximity boost
        for keyword in agent_config['primary_keywords']:
            if keyword in query_lower:
                base_score = 1.0
                # Boost score if keyword appears early in query
                position = query_lower.find(keyword)
                if position < len(query_lower) * 0.3:
                    base_score *= 1.2
                score += base_score
        
        # Context pattern matching
        for pattern in agent_config['context_patterns']:
            if re.search(pattern, query_lower):
                score += 1.5  # Higher weight for context patterns
        
        # Intent indicator matching
        for intent in agent_config['intent_indicators']:
            if intent in query_lower:
                score += 0.8
        
        return score * agent_config['weight_multiplier']
    
    def match_agent(self, query: str) -> AgentMatchResult:
        """Match query to best agent using enhanced algorithm."""
        start_time = time.perf_counter()
        
        # Quick keyword-based filtering
        keywords = self.extract_keywords(query)
        candidate_agents = set()
        
        for keyword in keywords:
            candidate_agents.update(self.keyword_index[keyword])
        
        # If no keyword matches, consider all agents
        if not candidate_agents:
            candidate_agents = set(self.agent_patterns.keys())
        
        best_agent = None
        best_score = 0.0
        matched_patterns = []
        
        # Calculate semantic similarity for candidate agents
        for agent_name in candidate_agents:
            agent_config = self.agent_patterns[agent_name]
            score = self.calculate_semantic_similarity(query, agent_config)
            
            if score > best_score:
                best_score = score
                best_agent = agent_name
                # Find which patterns matched
                matched_patterns = []
                for pattern in agent_config['context_patterns']:
                    if re.search(pattern, query.lower()):
                        matched_patterns.append(pattern)
        
        # Fallback with confidence penalty
        if best_agent is None or best_score < 0.5:
            best_agent = 'intelligent-enhancer'
            best_score = max(0.2, best_score)  # Minimum confidence
        
        # Normalize confidence score
        confidence_score = min(1.0, best_score / 3.0)  # Scale to 0-1 range
        
        processing_time = (time.perf_counter() - start_time) * 1000
        
        return AgentMatchResult(
            agent_name=best_agent,
            confidence_score=confidence_score,
            matched_patterns=matched_patterns,
            processing_time_ms=processing_time,
            context_keywords=keywords
        )


class TestAgentPatternMatching:
    """Test suite for agent pattern matching performance."""
    
    @pytest.fixture
    def current_matcher(self):
        return CurrentPatternMatcher()
    
    @pytest.fixture
    def enhanced_matcher(self):
        return EnhancedPatternMatcher()
    
    @pytest.fixture
    def test_queries(self):
        return [
            TestQuery(
                query="pytest test failing with async mock configuration",
                expected_agent="test-specialist",
                expected_confidence_range=(0.7, 1.0),
                context_keywords=["test", "async", "mock"]
            ),
            TestQuery(
                query="docker orchestration issues with container networking",
                expected_agent="infrastructure-engineer", 
                expected_confidence_range=(0.7, 1.0),
                context_keywords=["docker", "container"]
            ),
            TestQuery(
                query="security vulnerability scan reveals credential leaks",
                expected_agent="security-enforcer",
                expected_confidence_range=(0.8, 1.0),
                context_keywords=["security", "vulnerability", "credential"]
            ),
            TestQuery(
                query="performance bottleneck in latency optimization",
                expected_agent="performance-optimizer",
                expected_confidence_range=(0.7, 1.0),
                context_keywords=["performance", "latency"]
            ),
            TestQuery(
                query="refactor code with better variable naming and function splitting",
                expected_agent="intelligent-enhancer",
                expected_confidence_range=(0.6, 1.0),
                context_keywords=["refactor", "variable", "function"]
            ),
            # Edge cases and variations
            TestQuery(
                query="need help with testing framework configuration",
                expected_agent="test-specialist",
                expected_confidence_range=(0.5, 0.8),
                variations=["help testing framework config", "test framework setup"]
            ),
            TestQuery(
                query="container deployment pipeline optimization",
                expected_agent="infrastructure-engineer",
                expected_confidence_range=(0.6, 0.9),
                variations=["deploy container pipeline", "container deploy optimization"]
            )
        ]
    
    def test_current_matcher_accuracy(self, current_matcher, test_queries):
        """Test accuracy of current pattern matching."""
        correct_matches = 0
        total_queries = 0
        processing_times = []
        
        for test_query in test_queries:
            result = current_matcher.match_agent(test_query.query)
            processing_times.append(result.processing_time_ms)
            
            if result.agent_name == test_query.expected_agent:
                correct_matches += 1
            total_queries += 1
            
            # Test variations
            for variation in test_query.variations:
                var_result = current_matcher.match_agent(variation)
                processing_times.append(var_result.processing_time_ms)
                if var_result.agent_name == test_query.expected_agent:
                    correct_matches += 1
                total_queries += 1
        
        accuracy = correct_matches / total_queries
        avg_processing_time = sum(processing_times) / len(processing_times)
        
        print(f"Current matcher accuracy: {accuracy:.2%}")
        print(f"Average processing time: {avg_processing_time:.2f}ms")
        
        # Baseline expectations
        assert accuracy >= 0.60, f"Current matcher accuracy too low: {accuracy:.2%}"
        assert avg_processing_time < 5.0, f"Current matcher too slow: {avg_processing_time:.2f}ms"
    
    def test_enhanced_matcher_accuracy(self, enhanced_matcher, test_queries):
        """Test accuracy of enhanced pattern matching."""
        correct_matches = 0
        total_queries = 0
        processing_times = []
        confidence_scores = []
        
        for test_query in test_queries:
            result = enhanced_matcher.match_agent(test_query.query)
            processing_times.append(result.processing_time_ms)
            confidence_scores.append(result.confidence_score)
            
            if result.agent_name == test_query.expected_agent:
                correct_matches += 1
            
            # Validate confidence range
            min_conf, max_conf = test_query.expected_confidence_range
            assert min_conf <= result.confidence_score <= max_conf, \
                f"Confidence {result.confidence_score:.2f} outside expected range [{min_conf:.2f}, {max_conf:.2f}]"
            
            total_queries += 1
            
            # Test variations
            for variation in test_query.variations:
                var_result = enhanced_matcher.match_agent(variation)
                processing_times.append(var_result.processing_time_ms)
                confidence_scores.append(var_result.confidence_score)
                if var_result.agent_name == test_query.expected_agent:
                    correct_matches += 1
                total_queries += 1
        
        accuracy = correct_matches / total_queries
        avg_processing_time = sum(processing_times) / len(processing_times)
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        
        print(f"Enhanced matcher accuracy: {accuracy:.2%}")
        print(f"Average processing time: {avg_processing_time:.2f}ms")
        print(f"Average confidence score: {avg_confidence:.2f}")
        
        # Enhanced expectations
        assert accuracy >= 0.80, f"Enhanced matcher accuracy too low: {accuracy:.2%}"
        assert avg_processing_time < 3.0, f"Enhanced matcher too slow: {avg_processing_time:.2f}ms"
        assert avg_confidence >= 0.65, f"Average confidence too low: {avg_confidence:.2f}"
    
    def test_performance_comparison(self, current_matcher, enhanced_matcher, test_queries):
        """Compare performance between current and enhanced matchers."""
        current_times = []
        enhanced_times = []
        current_accuracy = 0
        enhanced_accuracy = 0
        total_tests = 0
        
        for test_query in test_queries:
            # Test current matcher
            current_result = current_matcher.match_agent(test_query.query)
            current_times.append(current_result.processing_time_ms)
            if current_result.agent_name == test_query.expected_agent:
                current_accuracy += 1
            
            # Test enhanced matcher
            enhanced_result = enhanced_matcher.match_agent(test_query.query)
            enhanced_times.append(enhanced_result.processing_time_ms)
            if enhanced_result.agent_name == test_query.expected_agent:
                enhanced_accuracy += 1
            
            total_tests += 1
        
        current_avg_time = sum(current_times) / len(current_times)
        enhanced_avg_time = sum(enhanced_times) / len(enhanced_times)
        current_accuracy_pct = current_accuracy / total_tests
        enhanced_accuracy_pct = enhanced_accuracy / total_tests
        
        print(f"\nPerformance Comparison:")
        print(f"Current: {current_accuracy_pct:.2%} accuracy, {current_avg_time:.2f}ms avg time")
        print(f"Enhanced: {enhanced_accuracy_pct:.2%} accuracy, {enhanced_avg_time:.2f}ms avg time")
        
        accuracy_improvement = (enhanced_accuracy_pct - current_accuracy_pct) / current_accuracy_pct
        time_improvement = (current_avg_time - enhanced_avg_time) / current_avg_time
        
        print(f"Accuracy improvement: {accuracy_improvement:.1%}")
        print(f"Time improvement: {time_improvement:.1%}")
        
        # Validate improvements
        assert enhanced_accuracy_pct > current_accuracy_pct, "Enhanced matcher should be more accurate"
        # Allow enhanced matcher to be slightly slower due to more sophisticated processing
        assert enhanced_avg_time < current_avg_time * 2.0, "Enhanced matcher should not be significantly slower"
    
    def test_edge_cases(self, enhanced_matcher):
        """Test edge cases and common variations."""
        edge_cases = [
            "help with testing stuff",  # Vague request
            "security and performance issues",  # Multiple domains
            "fix broken deployment",  # Ambiguous
            "code quality problems",  # General
            "async await patterns",  # Specific technical
            "",  # Empty query
            "something is not working",  # Very vague
            "docker container networking performance security audit"  # Multiple keywords
        ]
        
        for query in edge_cases:
            result = enhanced_matcher.match_agent(query)
            
            # Should always return a result
            assert result.agent_name is not None
            assert 0.0 <= result.confidence_score <= 1.0
            assert result.processing_time_ms >= 0
            
            print(f"'{query}' -> {result.agent_name} ({result.confidence_score:.2f})")
    
    def test_keyword_extraction(self, enhanced_matcher):
        """Test keyword extraction functionality."""
        test_cases = [
            ("pytest test failing", ["test"]),
            ("docker container networking", ["docker", "container"]),
            ("security vulnerability scan", ["security", "vulnerability"]),
            ("performance bottleneck optimization", ["performance", "optimization"]),
            ("refactor variable naming", ["refactor", "variable"])
        ]
        
        for query, expected_keywords in test_cases:
            keywords = enhanced_matcher.extract_keywords(query)
            
            for expected_keyword in expected_keywords:
                assert expected_keyword in keywords, f"Missing keyword '{expected_keyword}' in '{query}'"
    
    @pytest.mark.performance
    def test_high_load_performance(self, enhanced_matcher):
        """Test performance under high load conditions."""
        queries = [
            "test failure analysis",
            "docker orchestration issues", 
            "security vulnerability assessment",
            "performance optimization needed",
            "code refactoring required"
        ] * 100  # 500 total queries
        
        start_time = time.perf_counter()
        results = [enhanced_matcher.match_agent(query) for query in queries]
        total_time = (time.perf_counter() - start_time) * 1000
        
        avg_time_per_query = total_time / len(queries)
        
        print(f"High load test: {len(queries)} queries in {total_time:.1f}ms")
        print(f"Average time per query: {avg_time_per_query:.2f}ms")
        
        # Performance requirements
        assert avg_time_per_query < 2.0, f"High load performance too slow: {avg_time_per_query:.2f}ms"
        assert all(result.agent_name is not None for result in results)
