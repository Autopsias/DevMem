"""Enhanced Cross-Domain Integration Coordinator for Claude Code Framework.

This module provides specialized boundary detection and conflict resolution
improvements for the agent selection and coordination system.

Author: Pattern Analyzer Agent
Purpose: Cross-domain integration pattern analysis and specialized boundary detection
"""

import re
import time
from typing import Dict, List, Tuple, Optional, Set, NamedTuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, Counter
import logging

logger = logging.getLogger(__name__)


class DomainType(Enum):
    """Domain types for enhanced classification."""
    TESTING = "testing"
    INFRASTRUCTURE = "infrastructure" 
    SECURITY = "security"
    PERFORMANCE = "performance"
    CODE_QUALITY = "code_quality"
    DOCUMENTATION = "documentation"
    DATA_PROCESSING = "data_processing"
    API_INTEGRATION = "api_integration"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"


class ConflictType(Enum):
    """Types of cross-domain conflicts."""
    RESOURCE_COMPETITION = "resource_competition"
    APPROACH_CONTRADICTION = "approach_contradiction"
    PRIORITY_MISMATCH = "priority_mismatch"
    TIMING_CONFLICT = "timing_conflict"
    DEPENDENCY_CONFLICT = "dependency_conflict"
    SECURITY_PERFORMANCE = "security_performance"
    QUALITY_SPEED = "quality_speed"


@dataclass
class DomainBoundary:
    """Represents a detected domain boundary with confidence."""
    primary_domain: DomainType
    secondary_domains: List[DomainType]
    confidence: float
    boundary_patterns: List[str]
    overlap_indicators: List[str]
    complexity_score: float


@dataclass
class ConflictDetection:
    """Represents a detected conflict between domains."""
    conflict_type: ConflictType
    involved_domains: List[DomainType]
    severity: float  # 0.0 to 1.0
    description: str
    resolution_strategies: List[str]
    affected_agents: List[str]


@dataclass
class CrossDomainAnalysis:
    """Complete cross-domain analysis results."""
    query: str
    detected_boundaries: List[DomainBoundary]
    potential_conflicts: List[ConflictDetection]
    recommended_coordination: str
    agent_suggestions: List[Tuple[str, float]]  # (agent_name, confidence)
    integration_complexity: float
    processing_time_ms: float


class EnhancedBoundaryDetector:
    """Advanced boundary detection using pattern analysis and semantic understanding."""
    
    def __init__(self):
        """Initialize the boundary detector with enhanced patterns."""
        self.domain_patterns = self._build_domain_patterns()
        self.semantic_indicators = self._build_semantic_indicators()
        self.boundary_markers = self._build_boundary_markers()
        self.context_analyzers = self._build_context_analyzers()
        
    def _build_domain_patterns(self) -> Dict[DomainType, Dict[str, List[str]]]:
        """Build enhanced domain pattern recognition."""
        return {
            DomainType.TESTING: {
                'core_patterns': [
                    r'test.{0,15}(fail|error|pass|coverage|suite|framework)',
                    r'pytest.{0,15}(fixture|mock|param|mark|config)',
                    r'async.{0,10}(test|await|mock|pattern)',
                    r'mock.{0,15}(object|patch|assert|config|spec)',
                    r'coverage.{0,15}(report|analysis|gap|threshold)',
                    r'integration.{0,10}(test|testing|validation)',
                    r'unit.{0,8}(test|testing)',
                    r'fixture.{0,15}(design|dependency|config|setup)'
                ],
                'boundary_indicators': [
                    r'test.{0,20}(infrastructure|deployment|security|performance)',
                    r'testing.{0,20}(pipeline|automation|orchestration)',
                    r'mock.{0,20}(service|api|database|infrastructure)'
                ],
                'complexity_markers': [
                    r'async.{0,15}testing.{0,15}patterns',
                    r'concurrent.{0,15}test.{0,15}execution',
                    r'cross.{0,10}service.{0,10}testing',
                    r'end.to.end.{0,15}test.{0,15}automation'
                ]
            },
            
            DomainType.INFRASTRUCTURE: {
                'core_patterns': [
                    r'docker.{0,20}(container|image|compose|swarm|registry)',
                    r'kubernetes.{0,15}(cluster|pod|service|deployment|ingress)',
                    r'infrastructure.{0,20}(code|automation|provisioning|scaling)',
                    r'orchestration.{0,15}(container|service|workload|cluster)',
                    r'deployment.{0,15}(pipeline|strategy|automation|rollout)',
                    r'service.{0,15}(mesh|discovery|registry|gateway)',
                    r'monitoring.{0,15}(infrastructure|system|resource|performance)',
                    r'scaling.{0,15}(horizontal|vertical|auto|elastic)'
                ],
                'boundary_indicators': [
                    r'infrastructure.{0,20}(testing|security|performance|monitoring)',
                    r'container.{0,20}(security|testing|performance|orchestration)',
                    r'deployment.{0,20}(testing|security|monitoring|automation)'
                ],
                'complexity_markers': [
                    r'multi.{0,10}cloud.{0,15}infrastructure',
                    r'service.{0,10}mesh.{0,15}architecture',
                    r'container.{0,15}orchestration.{0,15}platform',
                    r'infrastructure.{0,15}as.{0,5}code.{0,15}automation'
                ]
            },
            
            DomainType.SECURITY: {
                'core_patterns': [
                    r'security.{0,20}(scan|audit|assessment|hardening|compliance)',
                    r'vulnerability.{0,15}(assessment|scan|analysis|mitigation)',
                    r'authentication.{0,15}(flow|token|oauth|session|rbac)',
                    r'authorization.{0,15}(policy|access|permission|role)',
                    r'encryption.{0,15}(data|transport|key|certificate)',
                    r'compliance.{0,15}(validation|audit|standard|requirement)',
                    r'credential.{0,15}(management|rotation|leak|storage)'
                ],
                'boundary_indicators': [
                    r'security.{0,20}(testing|infrastructure|performance|monitoring)',
                    r'secure.{0,15}(deployment|infrastructure|testing|development)',
                    r'compliance.{0,20}(automation|testing|infrastructure)'
                ],
                'complexity_markers': [
                    r'zero.{0,10}trust.{0,15}architecture',
                    r'multi.{0,10}factor.{0,15}authentication',
                    r'security.{0,15}orchestration.{0,15}automation',
                    r'compliance.{0,15}as.{0,5}code'
                ]
            },
            
            DomainType.PERFORMANCE: {
                'core_patterns': [
                    r'performance.{0,20}(optimization|analysis|tuning|monitoring)',
                    r'latency.{0,15}(reduction|optimization|measurement)',
                    r'throughput.{0,15}(optimization|analysis|improvement)',
                    r'resource.{0,15}(optimization|usage|allocation|monitoring)',
                    r'bottleneck.{0,15}(analysis|identification|resolution)',
                    r'scaling.{0,15}(performance|optimization|analysis)',
                    r'load.{0,15}(testing|balancing|optimization)'
                ],
                'boundary_indicators': [
                    r'performance.{0,20}(testing|security|infrastructure|monitoring)',
                    r'optimization.{0,20}(deployment|security|testing)',
                    r'scalability.{0,20}(testing|infrastructure|deployment)'
                ],
                'complexity_markers': [
                    r'distributed.{0,15}performance.{0,15}optimization',
                    r'real.{0,10}time.{0,15}performance.{0,15}monitoring',
                    r'auto.{0,10}scaling.{0,15}performance.{0,15}tuning',
                    r'machine.{0,10}learning.{0,15}performance.{0,15}optimization'
                ]
            },
            
            DomainType.CODE_QUALITY: {
                'core_patterns': [
                    r'code.{0,15}(quality|review|analysis|refactoring|standards)',
                    r'refactoring.{0,15}(systematic|architectural|design)',
                    r'architecture.{0,15}(improvement|design|pattern|review)',
                    r'lint.{0,15}(analysis|rule|violation|enforcement)',
                    r'style.{0,15}(guide|enforcement|consistency|standard)',
                    r'technical.{0,15}(debt|improvement|modernization)'
                ],
                'boundary_indicators': [
                    r'code.{0,20}(testing|security|performance|deployment)',
                    r'quality.{0,20}(testing|security|automation|monitoring)',
                    r'refactoring.{0,20}(testing|security|performance)'
                ],
                'complexity_markers': [
                    r'large.{0,10}scale.{0,15}refactoring',
                    r'architectural.{0,15}migration',
                    r'legacy.{0,15}code.{0,15}modernization',
                    r'cross.{0,10}cutting.{0,15}concern.{0,15}refactoring'
                ]
            },
            
            DomainType.DOCUMENTATION: {
                'core_patterns': [
                    r'documentation.{0,20}(creation|improvement|automation|generation)',
                    r'technical.{0,15}(writing|documentation|guide|specification)',
                    r'api.{0,15}(documentation|reference|guide|specification)',
                    r'user.{0,15}(guide|manual|documentation|handbook)',
                    r'knowledge.{0,15}(management|base|sharing|documentation)',
                    r'content.{0,15}(creation|management|automation)'
                ],
                'boundary_indicators': [
                    r'documentation.{0,20}(testing|infrastructure|security|deployment)',
                    r'automated.{0,15}documentation.{0,15}(generation|testing|validation)',
                    r'documentation.{0,20}(pipeline|workflow|integration)'
                ],
                'complexity_markers': [
                    r'multi.{0,10}format.{0,15}documentation.{0,15}generation',
                    r'automated.{0,15}documentation.{0,15}pipeline',
                    r'interactive.{0,15}documentation.{0,15}platform',
                    r'documentation.{0,15}as.{0,5}code'
                ]
            }
        }
    
    def _build_semantic_indicators(self) -> Dict[str, List[str]]:
        """Build semantic indicators for domain relationships."""
        return {
            'integration_signals': [
                'coordinate', 'integrate', 'combine', 'merge', 'unify',
                'orchestrate', 'synchronize', 'align', 'harmonize'
            ],
            'conflict_signals': [
                'conflict', 'contradiction', 'oppose', 'compete', 'clash',
                'interfere', 'blocking', 'incompatible', 'mutual exclusive'
            ],
            'dependency_signals': [
                'depend', 'require', 'prerequisite', 'foundation', 'based on',
                'built upon', 'relies on', 'needs', 'must have'
            ],
            'parallel_signals': [
                'parallel', 'concurrent', 'simultaneous', 'together',
                'in parallel', 'at the same time', 'jointly'
            ]
        }
    
    def _build_boundary_markers(self) -> Dict[str, float]:
        """Build boundary strength indicators."""
        return {
            # Strong boundary markers (high separation)
            'vs': 0.9, 'versus': 0.9, 'against': 0.8,
            'rather than': 0.8, 'instead of': 0.7, 'not': 0.6,
            
            # Medium boundary markers (moderate separation)
            'while': 0.5, 'but': 0.5, 'however': 0.5,
            'although': 0.4, 'despite': 0.4,
            
            # Weak boundary markers (low separation)
            'and': 0.2, 'with': 0.2, 'plus': 0.3,
            'including': 0.1, 'along with': 0.1
        }
    
    def _build_context_analyzers(self) -> Dict[str, callable]:
        """Build context analysis functions."""
        return {
            'temporal_analysis': self._analyze_temporal_context,
            'priority_analysis': self._analyze_priority_context,
            'dependency_analysis': self._analyze_dependency_context,
            'complexity_analysis': self._analyze_complexity_context
        }
    
    def _get_domain_keywords(self, domain_type: DomainType) -> List[str]:
        """Get simple keywords for domain detection."""
        domain_keywords = {
            DomainType.TESTING: ['test', 'testing', 'pytest', 'mock', 'fixture', 'coverage', 'unittest', 'validation'],
            DomainType.INFRASTRUCTURE: ['docker', 'kubernetes', 'k8s', 'container', 'deploy', 'deployment', 'infrastructure', 'orchestration', 'helm', 'terraform'],
            DomainType.SECURITY: ['security', 'secure', 'vulnerability', 'authentication', 'authorization', 'encryption', 'compliance', 'audit', 'validation'],
            DomainType.PERFORMANCE: ['performance', 'optimization', 'optimize', 'latency', 'throughput', 'bottleneck', 'resource', 'memory', 'cpu'],
            DomainType.CODE_QUALITY: ['refactor', 'refactoring', 'code quality', 'quality', 'architecture', 'technical debt', 'lint', 'clean code'],
            DomainType.DOCUMENTATION: ['documentation', 'docs', 'readme', 'api doc', 'technical writing', 'guide', 'manual', 'automation'],
            DomainType.DATA_PROCESSING: ['data processing', 'pipeline', 'etl', 'batch', 'stream'],
            DomainType.API_INTEGRATION: ['api', 'integration', 'service', 'endpoint', 'rest', 'graphql'],
            DomainType.DEPLOYMENT: ['deploy', 'deployment', 'release', 'ci/cd', 'pipeline'],
            DomainType.MONITORING: ['monitoring', 'observability', 'logging', 'metrics', 'alerting']
        }
        return domain_keywords.get(domain_type, [])
    
    def detect_domain_boundaries(self, query: str) -> List[DomainBoundary]:
        """Detect domain boundaries with enhanced pattern analysis."""
        query_lower = query.lower()
        boundaries = []
        
        # Primary domain detection with confidence scoring
        domain_scores = {}
        for domain_type, patterns in self.domain_patterns.items():
            score = 0.0
            matched_patterns = []
            
            # Core pattern matching
            for pattern in patterns['core_patterns']:
                matches = re.findall(pattern, query_lower)
                if matches:
                    score += len(matches) * 2.0  # Strong weight for core patterns
                    matched_patterns.append(pattern)
            
            # Boundary indicator detection
            boundary_score = 0.0
            boundary_patterns = []
            for pattern in patterns['boundary_indicators']:
                matches = re.findall(pattern, query_lower)
                if matches:
                    boundary_score += len(matches) * 1.5
                    boundary_patterns.append(pattern)
            
            # Complexity assessment
            complexity_score = 0.0
            for pattern in patterns['complexity_markers']:
                if re.search(pattern, query_lower):
                    complexity_score += 1.0
            
            domain_scores[domain_type] = {
                'core_score': score,
                'boundary_score': boundary_score,
                'complexity_score': complexity_score,
                'matched_patterns': matched_patterns,
                'boundary_patterns': boundary_patterns
            }
        
        # Identify primary and secondary domains
        sorted_domains = sorted(domain_scores.items(), 
                               key=lambda x: x[1]['core_score'] + x[1]['boundary_score'], 
                               reverse=True)
        
        # Lower threshold for better coverage
        if sorted_domains and sorted_domains[0][1]['core_score'] > 0.3:
            primary_domain = sorted_domains[0][0]
            primary_data = sorted_domains[0][1]
            
            # Find secondary domains with lower threshold for multi-domain detection
            secondary_domains = []
            for domain, data in sorted_domains[1:]:
                if data['core_score'] > 0.2 or data['boundary_score'] > 0.3:
                    secondary_domains.append(domain)
            
            # Improved confidence calculation with better normalization
            total_score = primary_data['core_score'] + primary_data['boundary_score']
            confidence = min(1.0, max(0.3, total_score / 2.5))
            
            # Detect overlap indicators
            overlap_indicators = self._detect_overlap_indicators(query_lower, primary_domain, secondary_domains)
            
            boundary = DomainBoundary(
                primary_domain=primary_domain,
                secondary_domains=secondary_domains,
                confidence=confidence,
                boundary_patterns=primary_data['matched_patterns'] + primary_data['boundary_patterns'],
                overlap_indicators=overlap_indicators,
                complexity_score=primary_data['complexity_score']
            )
            boundaries.append(boundary)
        
        return boundaries
    
    def _detect_overlap_indicators(self, query: str, primary: DomainType, 
                                 secondary: List[DomainType]) -> List[str]:
        """Detect indicators of domain overlap."""
        overlap_indicators = []
        
        # Check for integration signals
        for signal in self.semantic_indicators['integration_signals']:
            if signal in query:
                overlap_indicators.append(f"integration_signal:{signal}")
        
        # Check for parallel processing signals
        for signal in self.semantic_indicators['parallel_signals']:
            if signal in query:
                overlap_indicators.append(f"parallel_signal:{signal}")
        
        # Check for dependency signals
        for signal in self.semantic_indicators['dependency_signals']:
            if signal in query:
                overlap_indicators.append(f"dependency_signal:{signal}")
        
        return overlap_indicators
    
    def _analyze_temporal_context(self, query: str) -> Dict[str, any]:
        """Analyze temporal aspects of the query."""
        temporal_indicators = {
            'urgent': ['urgent', 'immediate', 'now', 'asap', 'critical'],
            'sequential': ['first', 'then', 'next', 'after', 'before', 'sequence'],
            'parallel': ['parallel', 'concurrent', 'simultaneous', 'together']
        }
        
        result = {'urgency': 0.0, 'sequencing': [], 'parallelism': 0.0}
        query_lower = query.lower()
        
        # Detect urgency
        for indicator in temporal_indicators['urgent']:
            if indicator in query_lower:
                result['urgency'] += 0.2
        
        # Detect sequencing
        for indicator in temporal_indicators['sequential']:
            if indicator in query_lower:
                result['sequencing'].append(indicator)
        
        # Detect parallelism
        for indicator in temporal_indicators['parallel']:
            if indicator in query_lower:
                result['parallelism'] += 0.3
        
        return result
    
    def _analyze_priority_context(self, query: str) -> Dict[str, any]:
        """Analyze priority indicators in the query."""
        priority_indicators = {
            'high': ['critical', 'essential', 'must', 'required', 'mandatory'],
            'medium': ['should', 'important', 'preferred', 'recommended'],
            'low': ['could', 'optional', 'nice to have', 'if possible']
        }
        
        result = {'priority_level': 'medium', 'priority_score': 0.5}
        query_lower = query.lower()
        
        high_count = sum(1 for indicator in priority_indicators['high'] if indicator in query_lower)
        medium_count = sum(1 for indicator in priority_indicators['medium'] if indicator in query_lower)
        low_count = sum(1 for indicator in priority_indicators['low'] if indicator in query_lower)
        
        if high_count > 0:
            result['priority_level'] = 'high'
            result['priority_score'] = 0.8 + min(0.2, high_count * 0.1)
        elif low_count > medium_count:
            result['priority_level'] = 'low'
            result['priority_score'] = 0.2 + min(0.3, low_count * 0.1)
        
        return result
    
    def _analyze_dependency_context(self, query: str) -> Dict[str, any]:
        """Analyze dependency relationships in the query."""
        dependency_patterns = [
            r'(\w+)\s+depends?\s+on\s+(\w+)',
            r'(\w+)\s+requires?\s+(\w+)',
            r'after\s+(\w+)\s+then\s+(\w+)',
            r'before\s+(\w+)\s+must\s+(\w+)'
        ]
        
        dependencies = []
        for pattern in dependency_patterns:
            matches = re.findall(pattern, query.lower())
            dependencies.extend(matches)
        
        return {'dependencies': dependencies, 'dependency_count': len(dependencies)}
    
    def _analyze_complexity_context(self, query: str) -> Dict[str, any]:
        """Analyze complexity indicators in the query."""
        complexity_indicators = {
            'low': ['simple', 'basic', 'straightforward', 'easy'],
            'medium': ['moderate', 'standard', 'typical', 'normal'],
            'high': ['complex', 'advanced', 'sophisticated', 'intricate'],
            'very_high': ['extremely', 'highly complex', 'very sophisticated', 'enterprise-grade']
        }
        
        query_lower = query.lower()
        complexity_score = 0.3  # Default medium complexity
        complexity_level = 'medium'
        
        for level, indicators in complexity_indicators.items():
            for indicator in indicators:
                if indicator in query_lower:
                    if level == 'low':
                        complexity_score = min(complexity_score, 0.2)
                        complexity_level = 'low'
                    elif level == 'high':
                        complexity_score = max(complexity_score, 0.7)
                        complexity_level = 'high'
                    elif level == 'very_high':
                        complexity_score = max(complexity_score, 0.9)
                        complexity_level = 'very_high'
        
        # Additional complexity indicators
        multi_word_count = len(re.findall(r'\bmulti[\w-]*', query_lower))
        cross_word_count = len(re.findall(r'\bcross[\w-]*', query_lower))
        integration_word_count = len(re.findall(r'\bintegrat\w*', query_lower))
        
        if multi_word_count + cross_word_count + integration_word_count > 2:
            complexity_score = max(complexity_score, 0.8)
            complexity_level = 'high'
        
        return {
            'complexity_level': complexity_level,
            'complexity_score': complexity_score,
            'multi_indicators': multi_word_count,
            'cross_indicators': cross_word_count,
            'integration_indicators': integration_word_count
        }


class ConflictDetectionEngine:
    """Advanced conflict detection for cross-domain coordination."""
    
    def __init__(self):
        """Initialize conflict detection with predefined conflict patterns."""
        self.conflict_patterns = self._build_conflict_patterns()
        self.resolution_strategies = self._build_resolution_strategies()
        
    def _build_conflict_patterns(self) -> Dict[ConflictType, Dict[str, any]]:
        """Build conflict detection patterns."""
        return {
            ConflictType.SECURITY_PERFORMANCE: {
                'domain_pairs': [(DomainType.SECURITY, DomainType.PERFORMANCE)],
                'indicators': [
                    r'security.{0,20}(vs|versus|against).{0,20}performance',
                    r'performance.{0,20}(vs|versus|against).{0,20}security',
                    r'secure.{0,15}but.{0,15}slow',
                    r'fast.{0,15}but.{0,15}insecure',
                    r'encryption.{0,20}performance.{0,15}impact',
                    r'security.{0,15}overhead'
                ],
                'severity_factors': ['encryption', 'authentication', 'latency', 'throughput'],
                'base_severity': 0.7
            },
            
            ConflictType.QUALITY_SPEED: {
                'domain_pairs': [(DomainType.CODE_QUALITY, DomainType.PERFORMANCE),
                               (DomainType.TESTING, DomainType.DEPLOYMENT)],
                'indicators': [
                    r'quality.{0,20}(vs|versus|against).{0,20}speed',
                    r'thorough.{0,15}(vs|but).{0,15}fast',
                    r'comprehensive.{0,20}testing.{0,15}slow',
                    r'quick.{0,15}deployment.{0,15}quality.{0,15}risk'
                ],
                'severity_factors': ['comprehensive', 'thorough', 'detailed', 'fast', 'quick'],
                'base_severity': 0.6
            },
            
            ConflictType.RESOURCE_COMPETITION: {
                'domain_pairs': [(DomainType.TESTING, DomainType.DEPLOYMENT),
                               (DomainType.MONITORING, DomainType.PERFORMANCE)],
                'indicators': [
                    r'resource.{0,20}competition',
                    r'memory.{0,15}usage.{0,15}conflict',
                    r'cpu.{0,15}intensive.{0,15}testing',
                    r'deployment.{0,15}resource.{0,15}constraints'
                ],
                'severity_factors': ['memory', 'cpu', 'disk', 'network'],
                'base_severity': 0.5
            },
            
            ConflictType.APPROACH_CONTRADICTION: {
                'domain_pairs': [(DomainType.INFRASTRUCTURE, DomainType.SECURITY),
                               (DomainType.DEPLOYMENT, DomainType.TESTING)],
                'indicators': [
                    r'contradictory.{0,15}approaches',
                    r'conflicting.{0,15}strategies',
                    r'mutually.{0,15}exclusive',
                    r'incompatible.{0,15}methodologies'
                ],
                'severity_factors': ['exclusive', 'contradictory', 'incompatible'],
                'base_severity': 0.8
            },
            
            ConflictType.TIMING_CONFLICT: {
                'domain_pairs': [(DomainType.TESTING, DomainType.DEPLOYMENT),
                               (DomainType.SECURITY, DomainType.DEPLOYMENT)],
                'indicators': [
                    r'timing.{0,15}conflict',
                    r'sequential.{0,15}dependency.{0,15}issue',
                    r'parallel.{0,15}execution.{0,15}problem',
                    r'synchronization.{0,15}issue'
                ],
                'severity_factors': ['urgent', 'deadline', 'immediate', 'blocking'],
                'base_severity': 0.6
            },
            
            ConflictType.DEPENDENCY_CONFLICT: {
                'domain_pairs': [(DomainType.INFRASTRUCTURE, DomainType.TESTING),
                               (DomainType.SECURITY, DomainType.INFRASTRUCTURE)],
                'indicators': [
                    r'circular.{0,15}dependency',
                    r'dependency.{0,15}conflict',
                    r'prerequisite.{0,15}issue',
                    r'order.{0,15}dependency.{0,15}problem'
                ],
                'severity_factors': ['circular', 'blocking', 'prerequisite'],
                'base_severity': 0.7
            }
        }
    
    def _build_resolution_strategies(self) -> Dict[ConflictType, List[str]]:
        """Build conflict resolution strategies."""
        return {
            ConflictType.SECURITY_PERFORMANCE: [
                "Implement security measures in performance-optimized layers",
                "Use hardware acceleration for encryption operations",
                "Apply security controls selectively based on risk assessment",
                "Implement caching strategies for security validations",
                "Use asynchronous security processing where possible"
            ],
            
            ConflictType.QUALITY_SPEED: [
                "Implement parallel testing strategies to maintain quality without sacrificing speed",
                "Use risk-based testing to focus quality efforts on critical paths",
                "Implement continuous quality monitoring instead of gate-based quality checks",
                "Use automated quality tools integrated into fast deployment pipelines",
                "Apply quality standards progressively through multiple deployment stages"
            ],
            
            ConflictType.RESOURCE_COMPETITION: [
                "Implement resource scheduling and allocation strategies",
                "Use container resource limits and quotas",
                "Implement temporal resource sharing (time-based allocation)",
                "Use resource monitoring and dynamic scaling",
                "Implement priority-based resource allocation"
            ],
            
            ConflictType.APPROACH_CONTRADICTION: [
                "Identify common ground and shared objectives",
                "Implement hybrid approaches combining elements from conflicting strategies",
                "Use sequential implementation with clear handoff points",
                "Create abstraction layers that allow different approaches at different levels",
                "Implement configuration-driven approach selection"
            ],
            
            ConflictType.TIMING_CONFLICT: [
                "Implement parallel execution where dependencies allow",
                "Use asynchronous processing patterns",
                "Create clear dependency graphs and execution ordering",
                "Implement timeout and retry mechanisms",
                "Use event-driven coordination patterns"
            ],
            
            ConflictType.DEPENDENCY_CONFLICT: [
                "Break circular dependencies through interface abstractions",
                "Implement dependency injection patterns",
                "Use event-driven decoupling strategies",
                "Create clear dependency hierarchies",
                "Implement lazy initialization patterns"
            ]
        }
    
    def detect_conflicts(self, boundaries: List[DomainBoundary], query: str) -> List[ConflictDetection]:
        """Detect potential conflicts between domains."""
        conflicts = []
        query_lower = query.lower()
        
        if not boundaries:
            return conflicts
            
        primary_domain = boundaries[0].primary_domain
        secondary_domains = boundaries[0].secondary_domains
        all_domains = [primary_domain] + secondary_domains
        
        # Check for known conflict patterns
        for conflict_type, pattern_config in self.conflict_patterns.items():
            # Check if any domain pairs match this conflict type
            for domain_pair in pattern_config['domain_pairs']:
                if (domain_pair[0] in all_domains and domain_pair[1] in all_domains) or \
                   (domain_pair[1] in all_domains and domain_pair[0] in all_domains):
                    
                    # Check for conflict indicators in query
                    indicator_matches = 0
                    for indicator_pattern in pattern_config['indicators']:
                        if re.search(indicator_pattern, query_lower):
                            indicator_matches += 1
                    
                    if indicator_matches > 0:
                        # Calculate severity based on indicators and factors
                        severity = pattern_config['base_severity']
                        
                        for factor in pattern_config['severity_factors']:
                            if factor in query_lower:
                                severity = min(1.0, severity + 0.1)
                        
                        # Adjust severity based on number of indicator matches
                        severity = min(1.0, severity + (indicator_matches - 1) * 0.1)
                        
                        conflict = ConflictDetection(
                            conflict_type=conflict_type,
                            involved_domains=list(domain_pair),
                            severity=severity,
                            description=f"Detected {conflict_type.value} between {domain_pair[0].value} and {domain_pair[1].value}",
                            resolution_strategies=self.resolution_strategies[conflict_type],
                            affected_agents=self._get_affected_agents(list(domain_pair))
                        )
                        conflicts.append(conflict)
        
        # Check for resource competition conflicts
        resource_keywords = ['memory', 'cpu', 'disk', 'network', 'bandwidth', 'storage']
        resource_mentions = sum(1 for keyword in resource_keywords if keyword in query_lower)
        
        if resource_mentions >= 2 and len(all_domains) >= 2:
            conflict = ConflictDetection(
                conflict_type=ConflictType.RESOURCE_COMPETITION,
                involved_domains=all_domains[:2],  # Take first two domains
                severity=0.5 + min(0.3, resource_mentions * 0.1),
                description=f"Potential resource competition detected between {all_domains[0].value} and {all_domains[1].value}",
                resolution_strategies=self.resolution_strategies[ConflictType.RESOURCE_COMPETITION],
                affected_agents=self._get_affected_agents(all_domains[:2])
            )
            conflicts.append(conflict)
        
        return conflicts
    
    def _get_affected_agents(self, domains: List[DomainType]) -> List[str]:
        """Get agents that would be affected by conflicts in these domains."""
        domain_agent_mapping = {
            DomainType.TESTING: ['test-specialist', 'coverage-optimizer', 'fixture-design-specialist'],
            DomainType.INFRASTRUCTURE: ['infrastructure-engineer', 'docker-specialist', 'environment-analyst'],
            DomainType.SECURITY: ['security-enforcer', 'security-auditor', 'code-quality-specialist'],
            DomainType.PERFORMANCE: ['performance-optimizer', 'resource-optimizer'],
            DomainType.CODE_QUALITY: ['intelligent-enhancer', 'code-quality-specialist', 'refactoring-coordinator'],
            DomainType.DOCUMENTATION: ['documentation-enhancer'],
            DomainType.DATA_PROCESSING: ['performance-optimizer', 'intelligent-enhancer'],
            DomainType.API_INTEGRATION: ['test-specialist', 'infrastructure-engineer'],
            DomainType.DEPLOYMENT: ['infrastructure-engineer', 'ci-specialist', 'environment-analyst'],
            DomainType.MONITORING: ['infrastructure-engineer', 'performance-optimizer']
        }
        
        affected_agents = set()
        for domain in domains:
            affected_agents.update(domain_agent_mapping.get(domain, []))
        
        return list(affected_agents)
    
    def _get_conflict_keywords(self, conflict_type: ConflictType) -> List[str]:
        """Get simple keywords that indicate specific conflict types."""
        conflict_keywords = {
            ConflictType.SECURITY_PERFORMANCE: ['vs', 'versus', 'vs.', 'against', 'balance', 'trade-off', 'overhead'],
            ConflictType.QUALITY_SPEED: ['fast', 'quick', 'rapid', 'thorough', 'comprehensive', 'detailed'],
            ConflictType.RESOURCE_COMPETITION: ['memory', 'cpu', 'disk', 'network', 'bandwidth', 'resource'],
            ConflictType.APPROACH_CONTRADICTION: ['contradiction', 'conflict', 'incompatible', 'mutually exclusive'],
            ConflictType.TIMING_CONFLICT: ['timing', 'parallel', 'sequential', 'before', 'after', 'synchronization'],
            ConflictType.DEPENDENCY_CONFLICT: ['dependency', 'depends', 'requires', 'prerequisite', 'circular']
        }
        return conflict_keywords.get(conflict_type, [])


class PatternLearningEngine:
    """Learning engine for infrastructure task patterns."""
    
    def __init__(self):
        """Initialize the pattern learning engine."""
        self.successful_patterns = defaultdict(list)  # query_type -> [(pattern, success_rate)]
        self.failed_patterns = defaultdict(list)  # query_type -> [(pattern, reasons)]
        self.infrastructure_keywords = self._build_infrastructure_learning_keywords()
        self.learning_threshold = 0.75  # Minimum success rate to consider pattern successful
        self.pattern_weights = defaultdict(float)  # pattern -> weight
        
    def _build_infrastructure_learning_keywords(self) -> Dict[str, List[str]]:
        """Build infrastructure-specific learning keywords."""
        return {
            'container_orchestration': [
                'docker', 'container', 'kubernetes', 'k8s', 'orchestration',
                'pod', 'service', 'deployment', 'helm', 'compose'
            ],
            'infrastructure_automation': [
                'terraform', 'ansible', 'infrastructure', 'provisioning',
                'iac', 'automation', 'ci/cd', 'pipeline', 'devops'
            ],
            'service_networking': [
                'networking', 'service mesh', 'ingress', 'load balancer',
                'proxy', 'routing', 'dns', 'discovery'
            ],
            'monitoring_observability': [
                'monitoring', 'observability', 'metrics', 'logging',
                'alerting', 'tracing', 'prometheus', 'grafana'
            ],
            'scaling_performance': [
                'scaling', 'autoscaling', 'performance', 'optimization',
                'resource', 'capacity', 'throughput', 'latency'
            ]
        }
    
    def learn_from_success(self, query: str, selected_agent: str, confidence: float, 
                          user_feedback: Optional[bool] = None):
        """Learn from successful agent selections."""
        if confidence >= self.learning_threshold:
            query_type = self._classify_infrastructure_query(query)
            if query_type:
                pattern_key = f"{query_type}:{selected_agent}"
                self.successful_patterns[query_type].append({
                    'pattern': pattern_key,
                    'agent': selected_agent,
                    'confidence': confidence,
                    'query_keywords': self._extract_keywords(query),
                    'timestamp': time.time(),
                    'user_feedback': user_feedback
                })
                
                # Update pattern weight
                self.pattern_weights[pattern_key] += 0.1 if user_feedback is True else 0.05
                
    def learn_from_failure(self, query: str, selected_agent: str, expected_agent: str, 
                          reasons: List[str]):
        """Learn from failed agent selections."""
        query_type = self._classify_infrastructure_query(query)
        if query_type:
            failure_pattern = {
                'selected_agent': selected_agent,
                'expected_agent': expected_agent,
                'reasons': reasons,
                'query_keywords': self._extract_keywords(query),
                'timestamp': time.time()
            }
            self.failed_patterns[query_type].append(failure_pattern)
            
            # Reduce weight for failed pattern
            failed_pattern_key = f"{query_type}:{selected_agent}"
            self.pattern_weights[failed_pattern_key] -= 0.1
            
    def _classify_infrastructure_query(self, query: str) -> Optional[str]:
        """Classify infrastructure query type."""
        query_lower = query.lower()
        
        for query_type, keywords in self.infrastructure_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in query_lower)
            if matches >= 2:  # Need at least 2 keyword matches
                return query_type
        
        # Fallback classification based on single strong keywords
        strong_keywords = {
            'docker': 'container_orchestration',
            'kubernetes': 'container_orchestration', 
            'k8s': 'container_orchestration',
            'terraform': 'infrastructure_automation',
            'ansible': 'infrastructure_automation',
            'prometheus': 'monitoring_observability',
            'grafana': 'monitoring_observability'
        }
        
        for keyword, query_type in strong_keywords.items():
            if keyword in query_lower:
                return query_type
                
        return None
        
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract keywords from query for learning."""
        query_lower = query.lower()
        keywords = []
        
        for keyword_list in self.infrastructure_keywords.values():
            keywords.extend([kw for kw in keyword_list if kw in query_lower])
            
        return list(set(keywords))
        
    def get_learned_agent_suggestion(self, query: str) -> Optional[Tuple[str, float]]:
        """Get agent suggestion based on learned patterns."""
        query_type = self._classify_infrastructure_query(query)
        if not query_type or query_type not in self.successful_patterns:
            return None
            
        successful_patterns = self.successful_patterns[query_type]
        if not successful_patterns:
            return None
            
        # Score patterns based on keyword overlap and success rate
        query_keywords = set(self._extract_keywords(query))
        pattern_scores = []
        
        for pattern in successful_patterns:
            pattern_keywords = set(pattern['query_keywords'])
            keyword_overlap = len(query_keywords.intersection(pattern_keywords))
            
            if keyword_overlap > 0:
                # Calculate score based on overlap, confidence, and learned weights
                pattern_key = pattern['pattern']
                base_score = pattern['confidence'] * (keyword_overlap / max(len(query_keywords), 1))
                weight_boost = self.pattern_weights.get(pattern_key, 0.0)
                
                # Time decay factor (recent patterns matter more)
                time_factor = max(0.5, 1.0 - (time.time() - pattern['timestamp']) / (30 * 24 * 3600))  # 30 days decay
                
                final_score = base_score + weight_boost * time_factor
                pattern_scores.append((pattern['agent'], final_score))
                
        if pattern_scores:
            # Return highest scoring agent
            pattern_scores.sort(key=lambda x: x[1], reverse=True)
            return pattern_scores[0]
            
        return None
        
    def get_learning_stats(self) -> Dict[str, any]:
        """Get learning engine statistics."""
        total_successes = sum(len(patterns) for patterns in self.successful_patterns.values())
        total_failures = sum(len(patterns) for patterns in self.failed_patterns.values())
        
        return {
            'total_successful_patterns': total_successes,
            'total_failed_patterns': total_failures,
            'learning_rate': total_successes / (total_successes + total_failures) if (total_successes + total_failures) > 0 else 0.0,
            'infrastructure_query_types': list(self.successful_patterns.keys()),
            'pattern_weights_count': len(self.pattern_weights),
            'average_pattern_weight': sum(self.pattern_weights.values()) / len(self.pattern_weights) if self.pattern_weights else 0.0
        }


class EnhancedCrossDomainCoordinator:
    """Main coordinator for enhanced cross-domain integration with learning capabilities."""
    
    def __init__(self):
        """Initialize the enhanced coordinator with learning engine."""
        self.boundary_detector = EnhancedBoundaryDetector()
        self.conflict_engine = ConflictDetectionEngine()
        self.pattern_learning_engine = PatternLearningEngine()
        self.analysis_history = []
        
    def analyze_cross_domain_integration(self, query: str) -> CrossDomainAnalysis:
        """Perform comprehensive cross-domain analysis with learning integration."""
        start_time = time.perf_counter()
        
        # Step 1: Check learned patterns first for infrastructure queries
        learned_suggestion = self.pattern_learning_engine.get_learned_agent_suggestion(query)
        
        # Step 2: Detect domain boundaries
        boundaries = self.boundary_detector.detect_domain_boundaries(query)
        
        # Step 3: Detect potential conflicts
        conflicts = self.conflict_engine.detect_conflicts(boundaries, query)
        
        # Step 4: Generate coordination recommendations
        coordination_recommendation = self._generate_coordination_recommendation(boundaries, conflicts)
        
        # Step 5: Generate agent suggestions with conflict awareness and learning integration
        agent_suggestions = self._generate_agent_suggestions_with_learning(boundaries, conflicts, learned_suggestion)
        
        # Step 6: Calculate integration complexity
        integration_complexity = self._calculate_integration_complexity(boundaries, conflicts)
        
        processing_time = (time.perf_counter() - start_time) * 1000
        
        analysis = CrossDomainAnalysis(
            query=query,
            detected_boundaries=boundaries,
            potential_conflicts=conflicts,
            recommended_coordination=coordination_recommendation,
            agent_suggestions=agent_suggestions,
            integration_complexity=integration_complexity,
            processing_time_ms=processing_time
        )
        
        # Store analysis for learning
        self.analysis_history.append(analysis)
        if len(self.analysis_history) > 1000:
            self.analysis_history = self.analysis_history[-500:]
            # Force garbage collection to ensure cleanup
            import gc
            gc.collect()
        
        return analysis
    
    def _generate_coordination_recommendation(self, boundaries: List[DomainBoundary], 
                                            conflicts: List[ConflictDetection]) -> str:
        """Generate coordination recommendations based on analysis."""
        if not boundaries:
            return "Single-domain analysis - no cross-domain coordination required"
        
        boundary = boundaries[0]  # Take primary boundary
        
        if not boundary.secondary_domains:
            return f"Primary domain: {boundary.primary_domain.value} - single-agent approach recommended"
        
        coordination_strategies = []
        
        # Base coordination strategy
        if len(boundary.secondary_domains) == 1:
            coordination_strategies.append("Dual-domain coordination")
        elif len(boundary.secondary_domains) <= 3:
            coordination_strategies.append("Multi-domain parallel coordination")
        else:
            coordination_strategies.append("Strategic meta-coordination")
        
        # Add conflict-specific strategies
        if conflicts:
            high_severity_conflicts = [c for c in conflicts if c.severity >= 0.7]
            if high_severity_conflicts:
                coordination_strategies.append("High-priority conflict resolution required")
            
            for conflict in conflicts:
                if conflict.conflict_type == ConflictType.TIMING_CONFLICT:
                    coordination_strategies.append("Sequential coordination with timing management")
                elif conflict.conflict_type == ConflictType.RESOURCE_COMPETITION:
                    coordination_strategies.append("Resource-aware coordination scheduling")
        
        # Add complexity-based strategies
        if boundary.complexity_score >= 2.0:
            coordination_strategies.append("Complex integration patterns required")
        
        return " + ".join(coordination_strategies)
    
    def _generate_agent_suggestions_with_learning(self, boundaries: List[DomainBoundary], 
                                                 conflicts: List[ConflictDetection],
                                                 learned_suggestion: Optional[Tuple[str, float]]) -> List[Tuple[str, float]]:
        """Generate agent suggestions with learning integration and conflict awareness."""
        if not boundaries:
            # Check for learned patterns even without boundaries
            if learned_suggestion and learned_suggestion[1] > 0.7:
                return [learned_suggestion]
            return [('intelligent-enhancer', 0.5)]
        
        boundary = boundaries[0]
        suggestions = []
        
        # Use learned suggestion if it has high confidence and matches infrastructure domain
        if (learned_suggestion and learned_suggestion[1] > 0.75 and 
            boundary.primary_domain == DomainType.INFRASTRUCTURE):
            suggestions.append(learned_suggestion)
        else:
            # Primary domain agent
            primary_agent, primary_confidence = self._get_domain_agent(boundary.primary_domain)
            
            # Apply infrastructure learning boost
            if boundary.primary_domain == DomainType.INFRASTRUCTURE and learned_suggestion:
                if learned_suggestion[0] == primary_agent:
                    primary_confidence = min(1.0, primary_confidence + 0.2)  # Boost confidence
                elif learned_suggestion[1] > 0.6:  # Consider learned agent if confidence is reasonable
                    suggestions.append(learned_suggestion)
                    
            suggestions.append((primary_agent, primary_confidence * boundary.confidence))
        
        # Secondary domain agents (with learning awareness)
        for secondary_domain in boundary.secondary_domains:
            agent, confidence = self._get_domain_agent(secondary_domain)
            
            # Apply learning boost for infrastructure secondary domains
            if (secondary_domain == DomainType.INFRASTRUCTURE and learned_suggestion and 
                learned_suggestion[0] == agent and learned_suggestion[1] > 0.6):
                confidence = min(1.0, confidence + 0.15)
                
            adjusted_confidence = confidence * 0.8 * boundary.confidence
            suggestions.append((agent, adjusted_confidence))
        
        # Add coordination agents if needed
        if len(boundary.secondary_domains) >= 2:
            suggestions.append(('analysis-gateway', 0.7))
        
        if len(boundary.secondary_domains) >= 4 or any(c.severity >= 0.8 for c in conflicts):
            suggestions.append(('meta-coordinator', 0.8))
        
        # Add conflict resolution specialists
        if conflicts:
            security_performance_conflicts = [c for c in conflicts 
                                            if c.conflict_type == ConflictType.SECURITY_PERFORMANCE]
            if security_performance_conflicts:
                suggestions.append(('security-auditor', 0.75))
                suggestions.append(('performance-optimizer', 0.75))
        
        # Sort by confidence and remove duplicates
        unique_suggestions = {}
        for agent, confidence in suggestions:
            if agent not in unique_suggestions or confidence > unique_suggestions[agent]:
                unique_suggestions[agent] = confidence
        
        return sorted(unique_suggestions.items(), key=lambda x: x[1], reverse=True)
    
    def _generate_agent_suggestions(self, boundaries: List[DomainBoundary], 
                                  conflicts: List[ConflictDetection]) -> List[Tuple[str, float]]:
        """Legacy method - redirects to learning-enhanced version."""
        return self._generate_agent_suggestions_with_learning(boundaries, conflicts, None)
        
    def record_selection_feedback(self, query: str, selected_agent: str, confidence: float,
                                user_feedback: Optional[bool] = None, expected_agent: Optional[str] = None):
        """Record feedback for learning improvement."""
        if user_feedback is False and expected_agent:
            # Learn from failure
            reasons = ["User feedback indicated incorrect selection"]
            self.pattern_learning_engine.learn_from_failure(query, selected_agent, expected_agent, reasons)
        elif user_feedback is True or confidence > 0.8:
            # Learn from success
            self.pattern_learning_engine.learn_from_success(query, selected_agent, confidence, user_feedback)
            
    def get_learning_insights(self) -> Dict[str, any]:
        """Get insights from the learning engine."""
        return self.pattern_learning_engine.get_learning_stats()
    
    def _get_domain_agent(self, domain: DomainType) -> Tuple[str, float]:
        """Get the primary agent for a domain."""
        domain_agents = {
            DomainType.TESTING: ('test-specialist', 0.9),
            DomainType.INFRASTRUCTURE: ('infrastructure-engineer', 0.9),
            DomainType.SECURITY: ('security-enforcer', 0.85),
            DomainType.PERFORMANCE: ('performance-optimizer', 0.85),
            DomainType.CODE_QUALITY: ('intelligent-enhancer', 0.8),
            DomainType.DOCUMENTATION: ('documentation-enhancer', 0.9),
            DomainType.DATA_PROCESSING: ('performance-optimizer', 0.75),
            DomainType.API_INTEGRATION: ('infrastructure-engineer', 0.8),
            DomainType.DEPLOYMENT: ('infrastructure-engineer', 0.85),
            DomainType.MONITORING: ('infrastructure-engineer', 0.8)
        }
        
        return domain_agents.get(domain, ('intelligent-enhancer', 0.6))
    
    def _calculate_integration_complexity(self, boundaries: List[DomainBoundary], 
                                        conflicts: List[ConflictDetection]) -> float:
        """Calculate overall integration complexity score."""
        if not boundaries:
            return 0.1
        
        boundary = boundaries[0]
        complexity = 0.3  # Base complexity
        
        # Domain count factor
        domain_count = 1 + len(boundary.secondary_domains)
        complexity += min(0.4, domain_count * 0.1)
        
        # Boundary complexity factor
        complexity += min(0.2, boundary.complexity_score * 0.1)
        
        # Conflict complexity factor
        if conflicts:
            avg_conflict_severity = sum(c.severity for c in conflicts) / len(conflicts)
            complexity += min(0.3, avg_conflict_severity * 0.3)
        
        # Overlap complexity factor
        overlap_count = len(boundary.overlap_indicators)
        complexity += min(0.2, overlap_count * 0.05)
        
        return min(1.0, complexity)
    
    def get_analysis_stats(self) -> Dict[str, any]:
        """Get statistics about cross-domain analysis patterns."""
        if not self.analysis_history:
            return {}
        
        # Domain frequency analysis
        domain_frequency = Counter()
        conflict_frequency = Counter()
        complexity_scores = []
        
        for analysis in self.analysis_history:
            for boundary in analysis.detected_boundaries:
                domain_frequency[boundary.primary_domain.value] += 1
                for secondary in boundary.secondary_domains:
                    domain_frequency[secondary.value] += 1
            
            for conflict in analysis.potential_conflicts:
                conflict_frequency[conflict.conflict_type.value] += 1
            
            complexity_scores.append(analysis.integration_complexity)
        
        avg_complexity = sum(complexity_scores) / len(complexity_scores) if complexity_scores else 0.0
        avg_processing_time = sum(a.processing_time_ms for a in self.analysis_history) / len(self.analysis_history)
        
        return {
            'total_analyses': len(self.analysis_history),
            'domain_frequency': dict(domain_frequency.most_common()),
            'conflict_frequency': dict(conflict_frequency.most_common()),
            'average_complexity': avg_complexity,
            'average_processing_time_ms': avg_processing_time,
            'conflict_detection_rate': len([a for a in self.analysis_history if a.potential_conflicts]) / len(self.analysis_history)
        }


# Global instance for easy access
_cross_domain_coordinator = None


def get_cross_domain_coordinator() -> EnhancedCrossDomainCoordinator:
    """Get the global cross-domain coordinator instance."""
    global _cross_domain_coordinator
    if _cross_domain_coordinator is None:
        _cross_domain_coordinator = EnhancedCrossDomainCoordinator()
    return _cross_domain_coordinator


def analyze_cross_domain_query(query: str) -> CrossDomainAnalysis:
    """Convenience function to analyze cross-domain integration for a query."""
    return get_cross_domain_coordinator().analyze_cross_domain_integration(query)
