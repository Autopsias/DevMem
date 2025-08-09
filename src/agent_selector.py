"""Enhanced agent selection system with improved cross-domain boundary detection.

This module provides advanced agent selection capabilities with:
- Enhanced multi-domain query detection with improved pattern recognition
- Smarter coordination between specialized agents using .claude/agents/ structure
- Improved confidence scoring for domain boundaries with calibrated thresholds  
- Enhanced handling of overlapping domains with conflict resolution strategies
- Cross-domain pattern learning with persistent storage and performance tracking
"""

import re
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import logging
import hashlib
import statistics
from typing import NamedTuple

# Import enhanced cross-domain coordinator
try:
    from .enhanced_cross_domain_coordinator import (
        get_cross_domain_coordinator,
        CrossDomainAnalysis,
        DomainType,
        ConflictType
    )
    CROSS_DOMAIN_AVAILABLE = True
except ImportError:
    CROSS_DOMAIN_AVAILABLE = False

logger = logging.getLogger(__name__)


class PatternSuccessMetrics(NamedTuple):
    """Metrics for tracking pattern success."""
    accuracy: float
    response_time: float
    context_preservation: float
    coordination_success: float
    confidence: float
    timestamp: float


class PatternSuccessTracker:
    """Enhanced pattern success tracking with adaptive learning."""
    
    def __init__(self):
        """Initialize the pattern success tracker."""
        self.success_history = defaultdict(list)  # pattern_key -> [metrics]
        self.pattern_weights = defaultdict(lambda: 1.0)  # pattern -> weight
        self.context_patterns = defaultdict(list)  # context_hash -> [successful_patterns]
        self.temporal_trends = defaultdict(list)  # pattern -> [(timestamp, success_rate)]
        self.learning_rate = 0.1
        
    def track_success(self, pattern_key: str, query: str, agent: str, metrics: PatternSuccessMetrics):
        """Track success metrics for a pattern-agent combination."""
        self.success_history[pattern_key].append(metrics)
        
        # Update pattern weights based on recent performance
        if len(self.success_history[pattern_key]) >= 3:
            recent_metrics = self.success_history[pattern_key][-5:]  # Last 5 uses
            avg_accuracy = statistics.mean(m.accuracy for m in recent_metrics)
            
            if avg_accuracy > 0.9:
                self.pattern_weights[pattern_key] = min(2.0, self.pattern_weights[pattern_key] + self.learning_rate)
            elif avg_accuracy < 0.7:
                self.pattern_weights[pattern_key] = max(0.5, self.pattern_weights[pattern_key] - self.learning_rate)
        
        # Track context patterns
        context_hash = self._generate_context_hash(query)
        self.context_patterns[context_hash].append({
            'pattern': pattern_key,
            'agent': agent,
            'success_rate': metrics.accuracy,
            'timestamp': metrics.timestamp
        })
        
        # Update temporal trends
        pattern_successes = [m.accuracy for m in self.success_history[pattern_key][-10:]]  # Last 10
        success_rate = statistics.mean(pattern_successes)
        self.temporal_trends[pattern_key].append((metrics.timestamp, success_rate))
        
        # Keep trends manageable
        if len(self.temporal_trends[pattern_key]) > 50:
            self.temporal_trends[pattern_key] = self.temporal_trends[pattern_key][-30:]
            
    def get_pattern_weight(self, pattern_key: str) -> float:
        """Get the current weight for a pattern."""
        return self.pattern_weights[pattern_key]
    
    def get_contextual_recommendations(self, query: str) -> List[Tuple[str, str, float]]:
        """Get agent recommendations based on similar contexts."""
        self._generate_context_hash(query)
        recommendations = []
        return recommendations

    def get_pattern_based_matches(self, query: str) -> List[Tuple[str, float, str]]:
        """Get pattern-based agent matches for a query with enhanced Task tool recognition."""
        pattern_matches = []
        query_lower = query.lower()
        
        # Enhanced Task tool patterns with agent name detection
        task_pattern = re.search(r'(?:task|parallel tasks?).{0,30}(?:in parallel|coordinating|comprehensive analysis)', query_lower) or \
                      re.search(r'coordinating\s+(?:tasks?|comprehensive|parallel)(?:\s+\w+)*(?:\s+using\s+tasks?)?', query_lower) or \
                      re.search(r'parallel\s+(?:tasks?|analysis|assessment|evaluation)', query_lower)
                      
        if task_pattern:
            # Check for explicit agent names in coordination patterns
            agent_coordination_patterns = {
                'analysis-gateway': r'analysis[_-]gateway\s+coordinating',
                'test-specialist': r'test[_-]specialist\s+coordinating', 
                'infrastructure-engineer': r'infrastructure[_-]engineer\s+coordinating',
                'security-enforcer': r'security[_-]enforcer\s+coordinating',
                'documentation-enhancer': r'documentation[_-]enhancer\s+coordinating',
                'performance-optimizer': r'performance[_-]optimizer\s+coordinating'
            }
            
            for agent_name, pattern in agent_coordination_patterns.items():
                if re.search(pattern, query_lower):
                    return [(agent_name, 0.95, f'Task coordination pattern with explicit agent: {agent_name}')]
            
            # Enhanced coordination context detection with numerical domain indicators
            explicit_domains = len(re.findall(r'\b(?:security|testing|performance|infrastructure|documentation)\b', query_lower))
            
            # Check for numerical domain indicators ("5 domains", "3 domains", etc.)
            numerical_domain_match = re.search(r'(\d+)\s+domains?', query_lower)
            numerical_domains = int(numerical_domain_match.group(1)) if numerical_domain_match else 0
            
            # Use the higher count between explicit and numerical indicators
            total_domain_indicators = max(explicit_domains, numerical_domains)
            
            # Strategic coordination keywords that indicate meta-coordination
            strategic_keywords = ['strategic', 'crisis', 'comprehensive', 'complex']
            has_strategic_context = any(keyword in query_lower for keyword in strategic_keywords)
            
            # Check for domain-specific coordination patterns
            domain_specific_patterns = {
                'testing': r'(?:async[_-]pattern[_-]fixer|testing|test[_-]specialist|fixture|mock).*(?:coordination|parallel)',
                'infrastructure': r'(?:docker|kubernetes|infrastructure[_-]engineer|container).*(?:coordination|parallel)',
                'security': r'(?:security[_-]enforcer|vulnerability|auth).*(?:coordination|parallel)',
                'performance': r'(?:performance[_-]optimizer|optimization|bottleneck).*(?:coordination|parallel)'
            }
            
            # Check for single-domain specialized coordination
            for domain, pattern in domain_specific_patterns.items():
                if re.search(pattern, query_lower) and total_domain_indicators <= 1:
                    domain_agent_map = {
                        'testing': 'test-specialist',
                        'infrastructure': 'infrastructure-engineer', 
                        'security': 'security-enforcer',
                        'performance': 'performance-optimizer'
                    }
                    return [(domain_agent_map[domain], 0.85, f'Task tool {domain}-specific coordination pattern')]
            
            if total_domain_indicators >= 5 or (has_strategic_context and total_domain_indicators >= 3):
                return [('meta-coordinator', 0.9, 'Task tool strategic multi-domain coordination pattern')]
            elif total_domain_indicators >= 3 or 'comprehensive' in query_lower:
                return [('meta-coordinator', 0.85, 'Task tool multi-domain coordination pattern')]
            elif total_domain_indicators == 2 or 'analysis' in query_lower:
                return [('analysis-gateway', 0.8, 'Task tool dual-domain analysis pattern')]
            else:
                return [('analysis-gateway', 0.75, 'Task tool general coordination pattern')]            
        
        # Handle analysis gateway patterns next since they are most specific
        if re.search(r'comprehensive analysis gateway coordination', query_lower) or \
           re.search(r'analysis gateway.*coordination', query_lower) or \
           re.search(r'cross.domain.*analysis gateway', query_lower):
            return [('analysis-gateway', 0.9, 'Analysis gateway pattern match')]
            
        # Handle multi-domain coordination patterns next
        if re.search(r'strategic coordination|multi.domain coordination|meta.coordination', query_lower) or \
           re.search(r'complex multi.domain', query_lower) or \
           re.search(r'strategic.*multi.domain', query_lower):
            return [('meta-coordinator', 0.9, 'Strategic coordination pattern match')]
            
        # Count distinct domain mentions
        domain_words = {
            'testing': set(['test', 'pytest', 'unittest', 'fixture', 'mock']),
            'infrastructure': set(['docker', 'kubernetes', 'container', 'deployment', 'infrastructure']),
            'security': set(['security', 'vulnerability', 'auth', 'encrypt']),
            'performance': set(['performance', 'optimization', 'speed', 'bottleneck']),
            'documentation': set(['doc', 'document', 'readme', 'api', 'reference']),
            'code_quality': set(['refactor', 'clean', 'architecture', 'quality', 'style', 'pattern'])
        }
        
        mentioned_domains = set()
        for domain, words in domain_words.items():
            if any(word in query_lower for word in words):
                mentioned_domains.add(domain)
        
        # Handle infrastructure patterns (more specific to avoid conflicts)
        if re.search(r'(docker|kubernetes).*(container|networking|service|orchestration|deploy|infrastructure|configuration)', query_lower) or \
           re.search(r'(kubernetes|docker).{0,15}(container|ingress|orchestration|deployment)', query_lower) or \
           re.search(r'container.*(orchestration|networking|infrastructure)', query_lower) or \
           re.search(r'infrastructure.*(deployment|orchestration|container)', query_lower):
            # Avoid infrastructure match if it's clearly performance-focused
            if not re.search(r'performance.*(bottleneck|optimization|scaling)(?!.*infrastructure)', query_lower):
                pattern_matches.append(('infrastructure-engineer', 0.9, 'Infrastructure pattern match'))
                return pattern_matches
        
        # Handle parallel/async test patterns
        if re.search(r'async.pattern.fixer.*parallel.*testing', query_lower) or \
           re.search(r'parallel.*testing.*coordination', query_lower):
            return [('test-specialist', 0.9, 'Parallel testing pattern')]    
        
        # Handle coordination needs based on domain count
        if len(mentioned_domains) >= 3:
            return [('meta-coordinator', 0.9, 'Multiple domain coordination required')]
        elif len(mentioned_domains) == 2:
            return [('analysis-gateway', 0.85, 'Dual-domain coordination required')]
        
        # Performance patterns with infrastructure
        if 'performance' in mentioned_domains and ('infrastructure' in mentioned_domains or 'scaling' in query_lower):
            return [('performance-optimizer', 0.85, 'Performance optimization pattern')]
        
        # Single domain patterns
        if 'testing' in mentioned_domains:
            pattern_matches.append(('test-specialist', 0.8, 'Test pattern match'))
            
        if 'infrastructure' in mentioned_domains:
            pattern_matches.append(('infrastructure-engineer', 0.8, 'Infrastructure pattern match'))
            
        if 'security' in mentioned_domains:
            pattern_matches.append(('security-enforcer', 0.8, 'Security pattern match'))
            
        if 'performance' in mentioned_domains:
            pattern_matches.append(('performance-optimizer', 0.8, 'Performance pattern match'))
            
        if 'documentation' in mentioned_domains:
            pattern_matches.append(('documentation-enhancer', 0.8, 'Documentation pattern match'))
            
        if 'code_quality' in mentioned_domains:
            pattern_matches.append(('intelligent-enhancer', 0.8, 'Code quality pattern match'))
            
        # Sort by confidence
        return sorted(pattern_matches, key=lambda x: x[1], reverse=True)
            
    def _generate_context_hash(self, query: str) -> str:
        """Generate a hash representing the query context."""
        # Extract key terms for context matching
        key_terms = re.findall(r'\b(?:test|docker|security|performance|refactor|infrastructure|deploy)\w*', query.lower())
        context_signature = '_'.join(sorted(set(key_terms)))
        return hashlib.md5(context_signature.encode()).hexdigest()[:8]
    
    def _contexts_similar(self, query: str, context_hash: str) -> bool:
        """Check if query context is similar to stored context."""
        query_hash = self._generate_context_hash(query)
        # Simple similarity check - same first 4 chars of hash
        return query_hash[:4] == context_hash[:4]


class ContextEnrichmentEngine:
    """Enhanced context enrichment for better agent selection with improved pattern recognition."""
    
    def __init__(self):
        """Initialize the context enrichment engine."""
        self.conversation_context = []
        self.domain_momentum = defaultdict(float)  # Track domain focus over time
        self.complexity_indicators = {
            'high': ['complex', 'advanced', 'sophisticated', 'enterprise', 'large-scale', 'comprehensive', 'systematic', 'architectural'],
            'medium': ['moderate', 'standard', 'typical', 'comprehensive', 'optimize', 'enhance', 'improve'],
            'low': ['simple', 'basic', 'quick', 'straightforward', 'minimal', 'fast', 'direct']
        }
        
        # Enhanced query type patterns for better classification
        self.query_type_patterns = {
            'problem_solving': ['fix', 'resolve', 'debug', 'troubleshoot', 'issue', 'problem', 'error', 'failing', 'broken'],
            'creation': ['create', 'generate', 'build', 'develop', 'implement', 'design', 'write', 'add'],
            'analysis': ['analyze', 'evaluate', 'assess', 'review', 'examine', 'investigate', 'study'],
            'optimization': ['optimize', 'improve', 'enhance', 'refactor', 'upgrade', 'modernize', 'streamline'],
            'maintenance': ['maintain', 'update', 'sync', 'refresh', 'clean', 'organize'],
            'coordination': ['coordinate', 'orchestrate', 'manage', 'integrate', 'align']
        }
        
        # Context momentum decay rate
        self.momentum_decay = 0.1
        self.momentum_boost = 0.2
        
    def enrich_context(self, query: str, conversation_history: Optional[List[str]] = None) -> Dict[str, any]:
        """Enrich query context with conversation history, domain momentum, and enhanced pattern detection."""
        enriched = {
            'original_query': query,
            'complexity_level': self._assess_complexity(query),
            'urgency_level': self._assess_urgency(query),
            'domain_signals': self._extract_domain_signals(query),
            'coordination_hints': self._detect_coordination_hints(query),
            'context_momentum': dict(self.domain_momentum),
            'query_type': self._classify_query_type(query),
            'technical_depth': self._assess_technical_depth(query),
            'action_indicators': self._extract_action_indicators(query),
            'domain_combinations': self._detect_domain_combinations(query)
        }
        
        # Update conversation context
        if conversation_history:
            self.conversation_context.extend(conversation_history)
            self.conversation_context = self.conversation_context[-10:]  # Keep recent context
        
        self.conversation_context.append(query)
        
        # Update domain momentum
        for domain in enriched['domain_signals']:
            self.domain_momentum[domain] = min(1.0, self.domain_momentum[domain] + self.momentum_boost)
        
        # Decay other domain momentum
        for domain in list(self.domain_momentum.keys()):
            if domain not in enriched['domain_signals']:
                self.domain_momentum[domain] = max(0.0, self.domain_momentum[domain] - self.momentum_decay)
                if self.domain_momentum[domain] < 0.05:
                    del self.domain_momentum[domain]
                    
        # Boost momentum for domain combinations
        for combo in enriched['domain_combinations']:
            for domain in combo:
                if domain in self.domain_momentum:
                    self.domain_momentum[domain] = min(1.0, self.domain_momentum[domain] + 0.1)
        
        return enriched
    
    def _classify_query_type(self, query: str) -> str:
        """Classify the type of query based on intent indicators."""
        query_lower = query.lower()
        
        # Score each query type based on keyword presence
        type_scores = defaultdict(int)
        
        for query_type, indicators in self.query_type_patterns.items():
            for indicator in indicators:
                if re.search(rf'\b{re.escape(indicator)}\w*', query_lower):
                    type_scores[query_type] += 1
        
        if not type_scores:
            return 'unknown'
            
        # Return the highest scoring query type
        return max(type_scores.items(), key=lambda x: x[1])[0]
    
    def _assess_technical_depth(self, query: str) -> str:
        """Assess the technical depth required for the query."""
        query_lower = query.lower()
        
        advanced_indicators = [
            'architecture', 'design pattern', 'system design', 'scalability',
            'distributed', 'microservice', 'enterprise', 'advanced',
            'complex', 'sophisticated', 'comprehensive'
        ]
        
        intermediate_indicators = [
            'configuration', 'integration', 'optimization', 'debugging',
            'troubleshoot', 'analysis', 'implementation', 'framework'
        ]
        
        basic_indicators = [
            'setup', 'install', 'basic', 'simple', 'quick', 'help',
            'how to', 'getting started', 'tutorial'
        ]
        
        if any(indicator in query_lower for indicator in advanced_indicators):
            return 'advanced'
        elif any(indicator in query_lower for indicator in intermediate_indicators):
            return 'intermediate'
        elif any(indicator in query_lower for indicator in basic_indicators):
            return 'basic'
        else:
            return 'intermediate'  # Default
    
    def _extract_action_indicators(self, query: str) -> List[str]:
        """Extract specific action indicators from the query."""
        query_lower = query.lower()
        actions = []
        
        action_patterns = {
            'create': ['create', 'generate', 'build', 'develop', 'make', 'add', 'new'],
            'fix': ['fix', 'resolve', 'solve', 'repair', 'correct', 'debug'],
            'analyze': ['analyze', 'examine', 'investigate', 'study', 'review', 'assess'],
            'optimize': ['optimize', 'improve', 'enhance', 'boost', 'speed up'],
            'configure': ['configure', 'setup', 'set up', 'install', 'deploy'],
            'document': ['document', 'write', 'explain', 'describe', 'guide'],
            'test': ['test', 'validate', 'verify', 'check', 'ensure']
        }
        
        for action, patterns in action_patterns.items():
            if any(re.search(rf'\b{re.escape(pattern)}\w*', query_lower) for pattern in patterns):
                actions.append(action)
        
        return actions
    
    def _detect_domain_combinations(self, query: str) -> List[List[str]]:
        """Detect common domain combinations that require coordinated expertise."""
        domains = self._extract_domain_signals(query)
        
        common_combinations = [
            ['testing', 'infrastructure'],
            ['security', 'infrastructure'],
            ['performance', 'infrastructure'],
            ['testing', 'security'],
            ['documentation', 'infrastructure'],
            ['code_quality', 'testing'],
            ['performance', 'testing']
        ]
        
        found_combinations = []
        for combo in common_combinations:
            if all(domain in domains for domain in combo):
                found_combinations.append(combo)
        
        return found_combinations
    
    def _assess_complexity(self, query: str) -> str:
        """Assess the complexity level of the query with enhanced indicators."""
        query_lower = query.lower()
        
        # Check explicit complexity indicators first
        for level, indicators in self.complexity_indicators.items():
            if any(indicator in query_lower for indicator in indicators):
                return level
        
        # Enhanced technical term analysis with broader scope
        technical_terms = len(re.findall(r'\b(?:docker|kubernetes|infrastructure|security|performance|testing|deployment|orchestration|async|mock|coverage|pytest|api|documentation|refactor|architecture|configuration|networking|scaling|monitoring)\b', query_lower))
        
        # Multi-domain complexity assessment
        domain_count = len(self._extract_domain_signals(query))
        coordination_hints = self._detect_coordination_hints(query)
        
        complexity_score = 0
        complexity_score += technical_terms * 2
        complexity_score += domain_count * 3
        complexity_score += len(query.split()) * 0.5
        
        if coordination_hints.get('multi_domain', False):
            complexity_score += 5
        if coordination_hints.get('hierarchical', False):
            complexity_score += 3
            
        if complexity_score >= 15:
            return 'high'
        elif complexity_score >= 8:
            return 'medium'
        else:
            return 'low'
    
    def _assess_urgency(self, query: str) -> str:
        """Assess the urgency level of the query."""
        urgency_indicators = {
            'high': ['urgent', 'emergency', 'critical', 'immediate', 'asap', 'now', 'production', 'down'],
            'medium': ['important', 'priority', 'needed', 'required', 'should'],
            'low': ['when', 'sometime', 'eventually', 'optional', 'nice to have']
        }
        
        query_lower = query.lower()
        for level, indicators in urgency_indicators.items():
            if any(indicator in query_lower for indicator in indicators):
                return level
        
        return 'medium'  # Default
    
    def _extract_domain_signals(self, query: str) -> List[str]:
        """Extract domain signals from the query with enhanced keyword coverage."""
        domain_keywords = {
            'testing': [
                'test', 'pytest', 'mock', 'coverage', 'unittest', 'spec', 'validation',
                'async', 'fixture', 'testing', 'debug', 'failure', 'assertion', 'verify'
            ],
            'infrastructure': [
                'docker', 'kubernetes', 'k8s', 'container', 'deploy', 'infrastructure', 'orchestration',
                'service', 'networking', 'scaling', 'cluster', 'helm', 'terraform', 'ansible',
                'monitoring', 'prometheus', 'grafana', 'nginx', 'istio', 'microservice', 'devops'
            ],
            'security': [
                'security', 'vulnerability', 'auth', 'credential', 'compliance', 'audit',
                'threat', 'encryption', 'authorization', 'authentication', 'ssl', 'tls',
                'oauth', 'token', 'rbac', 'hardening', 'scanning', 'penetration'
            ],
            'performance': [
                'performance', 'optimization', 'latency', 'bottleneck', 'resource', 'memory', 'cpu',
                'throughput', 'scaling', 'caching', 'profiling', 'benchmark', 'efficiency',
                'slow', 'fast', 'speed', 'optimize', 'resource usage'
            ],
            'code_quality': [
                'refactor', 'quality', 'lint', 'architecture', 'clean', 'improve',
                'code', 'naming', 'structure', 'pattern', 'convention', 'standard',
                'maintainability', 'readability', 'complexity', 'technical debt'
            ],
            'documentation': [
                'documentation', 'docs', 'readme', 'guide', 'manual', 'api doc',
                'technical writing', 'markdown', 'wiki', 'handbook', 'reference',
                'tutorial', 'spec', 'specification', 'content', 'knowledge', 'explain'
            ]
        }
        
        detected_domains = []
        query_lower = query.lower()
        
        for domain, keywords in domain_keywords.items():
            # Use word boundary matching for better accuracy
            domain_score = 0
            for keyword in keywords:
                if re.search(rf'\b{re.escape(keyword)}\w*', query_lower):
                    domain_score += 1
            
            # Require at least one strong match or multiple weak matches
            if domain_score >= 1:
                detected_domains.append(domain)
        
        return detected_domains
    
    def _detect_coordination_hints(self, query: str) -> Dict[str, bool]:
        """Detect coordination pattern hints in the query with enhanced pattern detection."""
        query_lower = query.lower()
        
        return {
            'parallel': any(hint in query_lower for hint in [
                'parallel', 'concurrent', 'simultaneous', 'together', 'multiple', 'batch',
                'coordinated', 'synchronized', 'cross-cutting'
            ]),
            'sequential': any(hint in query_lower for hint in [
                'sequential', 'step by step', 'then', 'after', 'before', 'first',
                'phase', 'stage', 'progressive', 'incremental', 'gradual'
            ]),
            'hierarchical': any(hint in query_lower for hint in [
                'coordinate', 'orchestrate', 'manage', 'oversee', 'architect',
                'strategic', 'systematic', 'comprehensive', 'enterprise', 'governance'
            ]),
            'multi_domain': len(self._extract_domain_signals(query)) > 1,
            'integration': any(hint in query_lower for hint in [
                'integrate', 'combine', 'merge', 'unify', 'consolidate', 'align',
                'cross-domain', 'end-to-end', 'holistic'
            ])
        }


@dataclass
class AgentMatchResult:
    """Result of agent pattern matching."""
    agent_name: str
    confidence_score: float
    matched_patterns: List[str]
    processing_time_ms: float
    context_keywords: List[str] = field(default_factory=list)
    reasoning: str = ""


@dataclass
class AgentConfig:
    """Configuration for an agent with matching criteria."""
    name: str
    primary_keywords: List[str]
    context_patterns: List[str]
    intent_indicators: List[str]
    weight_multiplier: float
    description: str = ""
    specialization_areas: List[str] = field(default_factory=list)


class EnhancedAgentSelector:
    """Enhanced agent selection with improved pattern matching algorithms."""
    
    def __init__(self, agents_dir: Optional[str] = None):
        """Initialize the enhanced agent selector with .claude/agents/ directory integration."""
        self.agents_dir = agents_dir or self._get_agents_directory()
        self.agents = self._initialize_agents()
        self.agents.update(self._load_agents_from_directory())  # Load from .claude/agents/
        self.keyword_index = self._build_keyword_index()
        self.pattern_cache = {}
        self.selection_history = []
        self.cross_domain_coordinator = get_cross_domain_coordinator() if CROSS_DOMAIN_AVAILABLE else None
        
        # Enhanced pattern learning components
        self.pattern_success_tracker = PatternSuccessTracker()
        self.context_enrichment_engine = ContextEnrichmentEngine()
        self.adaptive_learning_enabled = True
        
        # Improved pattern matching with fallback strategy
        self.fallback_threshold = 0.4  # Lower threshold before falling back to digdeep
        self.digdeep_threshold = 0.3   # Only use digdeep for truly ambiguous queries
        
    def _get_agents_directory(self) -> str:
        """Get the .claude/agents/ directory path."""
        from pathlib import Path
        current_dir = Path.cwd()
        agents_dir = current_dir / '.claude' / 'agents'
        return str(agents_dir)
    
    def _load_agents_from_directory(self) -> Dict[str, AgentConfig]:
        """Load agent configurations from .claude/agents/ directory."""
        from pathlib import Path
        
        agents = {}
        agents_path = Path(self.agents_dir)
        
        if not agents_path.exists():
            logger.warning(f"Agents directory not found: {agents_path}")
            return agents
        
        for agent_file in agents_path.glob('*.md'):
            try:
                agent_name = agent_file.stem
                with open(agent_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract agent configuration from frontmatter and content
                agent_config = self._parse_agent_file(agent_name, content)
                if agent_config:
                    agents[agent_name] = agent_config
                    logger.debug(f"Loaded agent: {agent_name}")
            except Exception as e:
                logger.warning(f"Failed to load agent from {agent_file}: {e}")
        
        logger.info(f"Loaded {len(agents)} agents from {agents_path}")
        return agents
    
    def _parse_agent_file(self, agent_name: str, content: str) -> Optional[AgentConfig]:
        """Parse agent configuration from markdown file."""
        import re
        
        # Extract frontmatter description
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.MULTILINE | re.DOTALL)
        description = ""
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            desc_match = re.search(r'description:\s*(.+)', frontmatter, re.MULTILINE)
            if desc_match:
                description = desc_match.group(1).strip()
        
        # Extract keywords from description and content
        keywords = self._extract_keywords_from_content(description + " " + content, agent_name)
        
        # Generate context patterns
        context_patterns = self._generate_context_patterns_from_content(content, agent_name)
        
        # Extract intent indicators
        intent_indicators = self._extract_intent_indicators(description, agent_name)
        
        return AgentConfig(
            name=agent_name,
            primary_keywords=keywords,
            context_patterns=context_patterns,
            intent_indicators=intent_indicators,
            weight_multiplier=1.0,  # Default weight
            description=description,
            specialization_areas=self._extract_specialization_areas(agent_name, content)
        )
    
    def _extract_keywords_from_content(self, content: str, agent_name: str) -> List[str]:
        """Extract keywords from agent content."""
        import re
        
        content_lower = content.lower()
        keywords = set()
        
        # Add agent name variations
        name_parts = agent_name.replace('-', ' ').split()
        keywords.update(name_parts)
        
        # Common keyword patterns by agent type
        keyword_patterns = {
            'test': ['test', 'testing', 'pytest', 'mock', 'fixture', 'coverage', 'unit', 'integration'],
            'infrastructure': ['docker', 'container', 'kubernetes', 'k8s', 'deployment', 'service', 'infrastructure', 'orchestration'],
            'security': ['security', 'vulnerability', 'authentication', 'authorization', 'compliance', 'audit', 'threat'],
            'performance': ['performance', 'optimization', 'latency', 'throughput', 'bottleneck', 'resource', 'memory', 'cpu'],
            'documentation': ['documentation', 'docs', 'readme', 'guide', 'manual', 'api', 'technical', 'writing'],
            'quality': ['quality', 'refactor', 'lint', 'format', 'clean', 'architecture', 'code']
        }
        
        # Extract keywords based on agent type
        for category, category_keywords in keyword_patterns.items():
            if category in agent_name or any(kw in content_lower for kw in category_keywords[:3]):
                keywords.update(category_keywords)
        
        # Extract keywords mentioned in content
        word_pattern = re.compile(r'\b[a-z]{3,15}\b')
        content_words = word_pattern.findall(content_lower)
        word_freq = {}
        for word in content_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Add frequently mentioned words
        frequent_words = [word for word, freq in word_freq.items() if freq >= 3 and len(word) >= 4]
        keywords.update(frequent_words[:10])  # Top 10 frequent words
        
        return list(keywords)
    
    def _generate_context_patterns_from_content(self, content: str, agent_name: str) -> List[str]:
        """Generate context patterns from agent content."""
        patterns = []
        content_lower = content.lower()
        
        # Agent-specific pattern generation
        if 'test' in agent_name:
            patterns.extend([
                r'test.{0,20}(fail|error|break|issue)',
                r'pytest.{0,15}(config|fixture|mark)',
                r'mock.{0,15}(config|patch|assert)',
                r'coverage.{0,15}(gap|report|analysis)'
            ])
        elif 'infrastructure' in agent_name:
            patterns.extend([
                r'docker.{0,20}(orchestration|compose|network)',
                r'container.{0,15}(scaling|network|resource)',
                r'kubernetes.{0,15}(cluster|pod|service|deployment)',
                r'service.{0,15}(mesh|discovery|communication)'
            ])
        elif 'security' in agent_name:
            patterns.extend([
                r'security.{0,20}(scan|audit|assessment)',
                r'vulnerability.{0,15}(assessment|scan|analysis)',
                r'authentication.{0,15}(flow|token|oauth)',
                r'compliance.{0,15}(validation|audit|standard)'
            ])
        elif 'documentation' in agent_name:
            patterns.extend([
                r'documentation.{0,20}(creation|improvement|automation)',
                r'api.{0,15}(documentation|reference|guide)',
                r'readme.{0,15}(creation|update|generation)',
                r'technical.{0,15}(writing|documentation|guide)'
            ])
        
        # Extract patterns from content descriptions
        if 'orchestration' in content_lower:
            patterns.append(r'orchestrat\w*.{0,15}(container|service|cluster)')
        if 'optimization' in content_lower:
            patterns.append(r'optim\w*.{0,15}(performance|resource|latency)')
        
        return patterns
    
    def _extract_intent_indicators(self, description: str, agent_name: str) -> List[str]:
        """Extract intent indicators from agent description."""
        indicators = ['need', 'fix', 'resolve', 'analyze', 'improve', 'create', 'implement']
        
        # Agent-specific indicators
        if 'test' in agent_name:
            indicators.extend(['test', 'validate', 'verify', 'debug'])
        elif 'infrastructure' in agent_name:
            indicators.extend(['deploy', 'scale', 'orchestrate', 'configure', 'monitor'])
        elif 'security' in agent_name:
            indicators.extend(['secure', 'audit', 'scan', 'protect', 'encrypt'])
        elif 'documentation' in agent_name:
            indicators.extend(['document', 'write', 'generate', 'explain', 'guide'])
        
        return indicators
    
    def _extract_specialization_areas(self, agent_name: str, content: str) -> List[str]:
        """Extract specialization areas from agent content."""
        areas = []
        content_lower = content.lower()
        
        # Common specialization mappings
        specializations = {
            'test': ['pytest', 'async_testing', 'mocking', 'coverage_analysis'],
            'infrastructure': ['docker', 'kubernetes', 'container_orchestration', 'service_mesh'],
            'security': ['vulnerability_scanning', 'compliance', 'authentication', 'encryption'],
            'documentation': ['technical_writing', 'api_documentation', 'user_guides', 'markdown_formatting'],
            'performance': ['performance_analysis', 'resource_optimization', 'latency_reduction']
        }
        
        for category, spec_areas in specializations.items():
            if category in agent_name or category in content_lower:
                areas.extend(spec_areas)
        
        return areas
    
    def _initialize_agents(self) -> Dict[str, AgentConfig]:
        """Initialize agent configurations with enhanced patterns."""
        return {
            'test-specialist': AgentConfig(
                name='test-specialist',
                primary_keywords=['test', 'pytest', 'mock', 'coverage', 'async', 'fixture'],
                context_patterns=[
                    r'test.{0,20}(fail|error|break|issue)',
                    r'pytest.{0,15}(config|fixture|mark|param)',
                    r'async.{0,10}(test|await|mock)',
                    r'mock.{0,15}(config|patch|assert|spec)',
                    r'coverage.{0,10}(gap|report|analysis|improve)',
                    r'integration.{0,10}test',
                    r'unit.{0,10}test',
                    r'fixture.{0,15}(design|config|dependency)'
                ],
                intent_indicators=['need', 'fix', 'resolve', 'debug', 'analyze', 'improve', 'validate'],
                weight_multiplier=1.2,
                description="Testing expertise with async/await patterns and coverage optimization",
                specialization_areas=['pytest', 'async_testing', 'mocking', 'coverage_analysis']
            ),
            
            'infrastructure-engineer': AgentConfig(
                name='infrastructure-engineer',
                primary_keywords=['docker', 'container', 'service', 'infrastructure', 'deployment', 'orchestration', 'kubernetes', 'k8s', 'helm', 'terraform', 'ansible', 'monitoring', 'scaling', 'networking', 'cluster', 'automation', 'provision', 'microservices', 'rollout', 'canary', 'istio', 'prometheus', 'grafana', 'metrics', 'dashboarding', 'alerting', 'ingress', 'nginx', 'progressive', 'blue', 'green'],
                context_patterns=[
                    # Core Container & Orchestration Patterns
                    r'docker.{0,20}(orchestration|compose|network|swarm|registry|build)',
                    r'container.{0,15}(scaling|network|resource|runtime|registry|security)',
                    r'kubernetes.{0,15}(cluster|pod|service|ingress|deployment|configmap|secret)',
                    r'k8s.{0,15}(cluster|pod|service|ingress|deployment|namespace)',
                    r'orchestration.{0,15}(container|service|microservice|cluster|workload)',
                    
                    # Service Mesh & Networking
                    r'service.{0,15}(mesh|discovery|communication|registry|gateway|proxy)',
                    r'networking.{0,15}(container|kubernetes|service|mesh|ingress|egress)',
                    r'load.?balancing.{0,15}(kubernetes|container|service|nginx|haproxy)',
                    r'ingress.{0,15}(controller|nginx|traefik|gateway|routing)',
                    
                    # Infrastructure as Code & Automation
                    r'infrastructure.{0,20}(code|automation|provisioning|scaling|architecture|deployment)',
                    r'terraform.{0,15}(plan|apply|infrastructure|provisioning|modules)',
                    r'ansible.{0,15}(playbook|automation|provisioning|configuration)',
                    r'helm.{0,15}(chart|deployment|kubernetes|package|release)',
                    
                    # Deployment & CI/CD Integration
                    r'deployment.{0,15}(pipeline|strategy|automation|rollout|canary|blue.?green)',
                    r'pipeline.{0,15}(deployment|infrastructure|container|kubernetes)',
                    r'rollout.{0,15}(strategy|deployment|canary|blue.?green|progressive)',
                    
                    # Monitoring & Observability
                    r'monitoring.{0,15}(infrastructure|container|kubernetes|prometheus|grafana)',
                    r'observability.{0,15}(infrastructure|distributed|microservice|tracing)',
                    r'logging.{0,15}(infrastructure|container|kubernetes|centralized)',
                    r'metrics.{0,15}(collection|infrastructure|monitoring|prometheus)',
                    r'dashboarding.{0,15}(infrastructure|monitoring|grafana|metrics)',
                    r'alerting.{0,15}(infrastructure|monitoring|prometheus|notification)',
                    
                    # Scaling & Performance
                    r'scaling.{0,15}(horizontal|vertical|auto|kubernetes|container)',
                    r'autoscaling.{0,15}(horizontal|vertical|kubernetes|cluster)',
                    r'performance.{0,15}(infrastructure|container|kubernetes|optimization)',
                    
                    # Cloud & Multi-Cloud
                    r'cloud.{0,15}(infrastructure|deployment|multi.?cloud|hybrid|migration)',
                    r'aws.{0,15}(infrastructure|eks|ecs|deployment|container)',
                    r'gcp.{0,15}(infrastructure|gke|deployment|container)',
                    r'azure.{0,15}(infrastructure|aks|deployment|container)',
                    
                    # Security & Compliance
                    r'container.{0,15}(security|scanning|hardening|compliance)',
                    r'infrastructure.{0,15}(security|hardening|compliance|governance)',
                    r'cluster.{0,15}(security|rbac|network.?policy|pod.?security)',
                    
                    # Storage & Persistence
                    r'storage.{0,15}(persistent|volume|infrastructure|container)',
                    r'volume.{0,15}(persistent|storage|mounting|kubernetes)',
                    r'database.{0,15}(infrastructure|deployment|scaling|container)',
                    
                    # Troubleshooting & Maintenance
                    r'troubleshoot.{0,15}(infrastructure|deployment|container|kubernetes)',
                    r'debugging.{0,15}(infrastructure|container|kubernetes|networking)',
                    r'maintenance.{0,15}(infrastructure|cluster|container|scheduled)',
                    
                    # Additional Infrastructure Patterns
                    r'rollout.{0,15}(canary|blue.?green|progressive|deployment)',
                    r'progressive.{0,15}(delivery|rollout|deployment)',
                    r'canary.{0,15}(deployment|rollout|release)',
                    r'blue.?green.{0,15}(deployment|strategy|rollout)',
                    r'istio.{0,15}(service.?mesh|ingress|configuration)',
                    r'prometheus.{0,15}(monitoring|metrics|alerting)',
                    r'grafana.{0,15}(dashboard|monitoring|visualization)',
                    r'nginx.{0,15}(ingress|load.?balancer|proxy)',
                    r'traefik.{0,15}(ingress|routing|load.?balancer)',
                    r'haproxy.{0,15}(load.?balancer|proxy|routing)'
                ],
                intent_indicators=['deploy', 'scale', 'orchestrate', 'optimize', 'architect', 'provision', 'automate', 'monitor', 'troubleshoot', 'configure', 'migrate', 'upgrade'],
                weight_multiplier=1.2,
                description="Comprehensive infrastructure orchestration with cloud-native expertise and systematic coordination",
                specialization_areas=['docker', 'kubernetes', 'container_orchestration', 'service_mesh', 'infrastructure_as_code', 'cloud_native', 'deployment_automation', 'monitoring', 'scaling']
            ),
            
            'security-enforcer': AgentConfig(
                name='security-enforcer',
                primary_keywords=['security', 'vulnerability', 'credential', 'authentication', 'audit', 'compliance'],
                context_patterns=[
                    r'security.{0,20}(pattern|scan|audit|review|hardening)',
                    r'vulnerability.{0,15}(assessment|scan|analysis|mitigation)',
                    r'credential.{0,15}(leak|management|rotation|storage)',
                    r'authentication.{0,15}(flow|token|session|oauth)',
                    r'compliance.{0,15}(validation|audit|standard|requirement)',
                    r'authorization.{0,15}(policy|rbac|access|permission)',
                    r'encryption.{0,15}(data|transport|rest|key)'
                ],
                intent_indicators=['secure', 'audit', 'validate', 'scan', 'harden', 'protect', 'encrypt'],
                weight_multiplier=1.3,
                description="Fast security pattern detection and workspace validation",
                specialization_areas=['vulnerability_scanning', 'compliance', 'authentication', 'encryption']
            ),
            
            'performance-optimizer': AgentConfig(
                name='performance-optimizer',
                primary_keywords=['performance', 'latency', 'optimization', 'bottleneck', 'resource', 'memory', 'cpu'],
                context_patterns=[
                    r'performance.{0,20}(bottleneck|optimization|analysis|tuning)',
                    r'latency.{0,15}(reduction|optimization|measurement|analysis)',
                    r'resource.{0,15}(usage|allocation|optimization|monitoring)',
                    r'memory.{0,15}(usage|leak|optimization|profiling)',
                    r'cpu.{0,15}(usage|optimization|profiling|utilization)',
                    r'throughput.{0,15}(optimization|analysis|improvement)',
                    r'scaling.{0,15}(performance|horizontal|vertical)'
                ],
                intent_indicators=['optimize', 'improve', 'reduce', 'enhance', 'accelerate', 'tune', 'profile'],
                weight_multiplier=1.0,
                description="System performance optimization and bottleneck analysis",
                specialization_areas=['performance_analysis', 'resource_optimization', 'latency_reduction']
            ),
            
            'intelligent-enhancer': AgentConfig(
                name='intelligent-enhancer',
                primary_keywords=['refactor', 'variable', 'function', 'type', 'architecture', 'code', 'quality'],
                context_patterns=[
                    r'code.{0,15}(refactor|improvement|enhancement|quality)',
                    r'variable.{0,15}(naming|renaming|improvement|convention)',
                    r'function.{0,15}(split|extract|optimize|simplify)',
                    r'type.{0,15}(annotation|hint|system|checking)',
                    r'architecture.{0,15}(improvement|refactoring|design|pattern)',
                    r'refactoring.{0,15}(systematic|architectural|code|design)',
                    r'enhancement.{0,15}(code|pattern|design|structure)'
                ],
                intent_indicators=['refactor', 'improve', 'enhance', 'clean', 'restructure', 'simplify', 'modernize'],
                weight_multiplier=0.9,
                description="AI-powered code improvements with intelligent refactoring",
                specialization_areas=['code_refactoring', 'naming_conventions', 'type_annotations', 'architecture_improvement']
            ),
            
            'code-quality-specialist': AgentConfig(
                name='code-quality-specialist',
                primary_keywords=['quality', 'lint', 'format', 'style', 'convention', 'standard'],
                context_patterns=[
                    r'code.{0,15}(quality|style|standard|convention)',
                    r'lint.{0,15}(error|warning|rule|config)',
                    r'format.{0,15}(code|style|consistent|automatic)',
                    r'style.{0,15}(guide|check|enforcement|violation)',
                    r'standard.{0,15}(coding|style|compliance|enforcement)'
                ],
                intent_indicators=['lint', 'format', 'standardize', 'clean', 'enforce', 'validate'],
                weight_multiplier=1.0,
                description="Code quality analysis and style enforcement",
                specialization_areas=['linting', 'code_formatting', 'style_enforcement']
            ),
            
            'ci-specialist': AgentConfig(
                name='ci-specialist',
                primary_keywords=['ci/cd', 'github actions', 'build pipeline', 'deployment pipeline', 'continuous integration'],
                context_patterns=[
                    r'ci\s*/\s*cd.{0,15}(pipeline|workflow|automation)',
                    r'github\s+actions.{0,15}(workflow|pipeline|yaml)',
                    r'build\s+pipeline.{0,15}(configuration|setup|automation)',
                    r'deployment\s+pipeline.{0,15}(automation|workflow)',
                    r'continuous\s+integration.{0,15}(setup|configuration)'
                ],
                intent_indicators=['ci/cd pipeline', 'github actions workflow', 'build automation', 'continuous integration'],
                weight_multiplier=0.7,  # Much more selective
                description="CI/CD pipeline optimization and GitHub Actions expertise",
                specialization_areas=['github_actions', 'pipeline_automation', 'ci_cd']
            ),
            
            'documentation-enhancer': AgentConfig(
                name='documentation-enhancer',
                primary_keywords=['documentation', 'docs', 'readme', 'markdown', 'md', 'api', 'guide', 'tutorial', 'manual', 'specification', 'wiki', 'handbook', 'knowledge', 'reference', 'howto', 'faq', 'write', 'create', 'generate', 'develop', 'content', 'explain', 'describe', 'document'],
                context_patterns=[
                    # Core Documentation Patterns
                    r'documentation.{0,20}(update|create|improve|generate|write|enhance)',
                    r'docs.{0,15}(generation|creation|update|improvement|writing)',
                    r'readme.{0,15}(file|creation|update|improvement|generation)',
                    r'markdown.{0,15}(documentation|file|generation|formatting)',
                    r'api.{0,15}(documentation|docs|reference|specification|guide)',
                    
                    # Technical Writing Patterns
                    r'technical.{0,15}(writing|documentation|guide|manual|specification)',
                    r'user.{0,15}(guide|manual|documentation|handbook)',
                    r'developer.{0,15}(documentation|guide|reference|handbook)',
                    r'installation.{0,15}(guide|instructions|documentation|manual)',
                    r'setup.{0,15}(guide|documentation|instructions|manual)',
                    
                    # Content Management Patterns
                    r'content.{0,15}(creation|management|documentation|writing)',
                    r'knowledge.{0,15}(base|documentation|management|sharing)',
                    r'information.{0,15}(architecture|documentation|management)',
                    r'specification.{0,15}(documentation|writing|creation|update)',
                    
                    # Documentation Generation Patterns
                    r'generate.{0,15}(documentation|docs|readme|guide|manual)',
                    r'create.{0,15}(documentation|docs|readme|guide|manual)',
                    r'write.{0,15}(documentation|docs|readme|guide|manual)',
                    r'document.{0,15}(code|api|process|workflow|architecture)',
                    
                    # Documentation Types and Formats
                    r'tutorial.{0,15}(creation|writing|documentation|guide)',
                    r'develop.{0,15}(tutorial|guide|documentation|manual)',
                    r'howto.{0,15}(guide|documentation|instruction|manual)',
                    r'faq.{0,15}(documentation|creation|update|management|section)',
                    r'wiki.{0,15}(documentation|content|management|creation)',
                    r'handbook.{0,15}(creation|update|documentation|writing)',
                    r'troubleshooting.{0,15}(guide|documentation|manual)',
                    r'getting.?started.{0,15}(guide|documentation|tutorial)',
                    r'beginners?.{0,15}(guide|tutorial|documentation|manual)',
                    
                    # Documentation Quality and Standards
                    r'documentation.{0,15}(quality|standards|review|audit)',
                    r'docs.{0,15}(quality|standards|consistency|validation)',
                    r'content.{0,15}(quality|standards|review|validation)',
                    r'writing.{0,15}(standards|quality|style|guidelines)',
                    
                    # Documentation Integration and Automation
                    r'documentation.{0,15}(automation|integration|pipeline|workflow)',
                    r'docs.{0,15}(automation|generation|pipeline|build)',
                    r'automatic.{0,15}(documentation|docs|generation)',
                    r'automate.{0,15}(documentation|docs|generation)',
                    r'documentation.{0,15}(site|portal|platform|system)',
                    r'integrate.{0,15}(documentation|docs).{0,15}(ci|cd|pipeline)',
                    r'ci.?cd.{0,15}(documentation|docs)',
                    r'pipeline.{0,15}(documentation|docs)',
                    
                    # Code Documentation Patterns
                    r'code.{0,15}(documentation|commenting|annotation)',
                    r'inline.{0,15}(documentation|comments|docs)',
                    r'docstring.{0,15}(generation|creation|improvement)',
                    r'comment.{0,15}(documentation|generation|improvement)',
                    
                    # Project Documentation Patterns
                    r'project.{0,15}(documentation|docs|readme|guide)',
                    r'repository.{0,15}(documentation|readme|wiki)',
                    r'codebase.{0,15}(documentation|guide|reference)',
                    r'architecture.{0,15}(documentation|guide|specification)',
                    
                    # Documentation Maintenance Patterns
                    r'documentation.{0,15}(maintenance|update|synchronization)',
                    r'docs.{0,15}(maintenance|sync|update|refresh)',
                    r'outdated.{0,15}(documentation|docs|guide)',
                    r'documentation.{0,15}(versioning|migration|upgrade)'
                ],
                intent_indicators=['document', 'write', 'create', 'generate', 'explain', 'describe', 'guide', 'instruct', 'specify', 'clarify', 'elaborate', 'detail'],
                weight_multiplier=1.3,
                description="Comprehensive documentation creation, enhancement, and technical writing expertise",
                specialization_areas=['technical_writing', 'api_documentation', 'user_guides', 'readme_generation', 'markdown_formatting', 'content_management', 'documentation_automation', 'knowledge_management']
            )
        }
    
    def _build_keyword_index(self) -> Dict[str, List[str]]:
        """Build keyword index for fast agent lookup."""
        keyword_index = defaultdict(list)
        
        for agent_name, config in self.agents.items():
            for keyword in config.primary_keywords:
                keyword_index[keyword].append(agent_name)
        
        return keyword_index
    
    def _extract_context_keywords(self, query: str) -> List[str]:
        """Extract keywords from query with pattern matching."""
        query_lower = query.lower()
        keywords = []
        
        # Keyword patterns by domain
        domain_patterns = {
            # Testing patterns
            'test': [r'\b(?:test|pytest|mock|coverage|fixture|async)\w*'],
            
            # Infrastructure patterns
            'infrastructure': [r'\b(?:docker|container|service|deployment|kubernetes|orchestration)\w*'],
            
            # Security patterns
            'security': [r'\b(?:security|auth|vulnerability|audit|compliance)\w*'],
            
            # Performance patterns
            'performance': [r'\b(?:performance|optimization|latency|bottleneck|throughput)\w*'],
            
            # Documentation patterns
            'documentation': [r'\b(?:documentation|docs?|readme|api|guide|tutorial)\w*'],
            
            # Code quality patterns
            'quality': [r'\b(?:lint|format|refactor|clean|quality|style)\w*']
        }
        
        # Extract keywords using patterns
        for domain, patterns in domain_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, query_lower)
                if matches:
                    keywords.extend(matches)
                    keywords.append(domain)  # Add domain as keyword
        
        return list(set(keywords))  # Remove duplicates
    
    def calculate_context_score(self, query: str, agent_config: AgentConfig) -> Tuple[float, List[str]]:
        """Calculate context-based similarity score with enhanced pattern matching."""
        query_lower = query.lower()
        score = 0.0
        matched_patterns = []
        
        # Enhanced keyword matching with semantic scoring
        for keyword in agent_config.primary_keywords:
            keyword_score = 0.0
            
            # Exact keyword match
            if keyword in query_lower:
                keyword_score = 1.0
                
                # Position weighting (earlier = better)
                position = query_lower.find(keyword)
                position_weight = 1.0
                if position < len(query_lower) * 0.2:
                    position_weight = 1.4
                elif position < len(query_lower) * 0.5:
                    position_weight = 1.2
                elif position < len(query_lower) * 0.8:
                    position_weight = 1.1
                
                keyword_score *= position_weight
                
                # Word boundary bonus (whole word matches)
                if re.search(rf'\b{re.escape(keyword)}\b', query_lower):
                    keyword_score *= 1.3
                
                # Frequency bonus (repeated keywords indicate focus)
                frequency = query_lower.count(keyword)
                if frequency > 1:
                    keyword_score *= (1.0 + (frequency - 1) * 0.2)
            
            # Semantic variations and stems
            else:
                variations = self._get_keyword_variations(keyword)
                for variation in variations:
                    if variation in query_lower:
                        keyword_score = max(keyword_score, 0.7)  # Lower score for variations
                        break
            
            score += keyword_score
        
        # Context pattern matching with higher weight
        for pattern in agent_config.context_patterns:
            match = re.search(pattern, query_lower)
            if match:
                score += 2.0  # Higher weight for context patterns
                matched_patterns.append(pattern)
        
        # Intent indicator matching
        for intent in agent_config.intent_indicators:
            if re.search(rf'\b{re.escape(intent)}\b', query_lower):
                score += 1.0
        
        # Specialization area matching with variations
        for spec_area in agent_config.specialization_areas:
            spec_normalized = spec_area.replace('_', ' ')
            if spec_normalized in query_lower:
                score += 1.5
            
            # Check for specialized area variations
            spec_variations = {
                'container_orchestration': ['orchestration', 'orchestrated', 'orchestrate'],
                'cloud_native': ['cloud-native', 'cloud native', 'cloudnative'],
                'infrastructure_as_code': ['infrastructure as code', 'iac', 'infra as code'],
                'deployment_automation': ['deployment automation', 'automated deployment', 'deploy automation'],
                'service_mesh': ['service mesh', 'servicemesh', 'mesh'],
                'technical_writing': ['technical writing', 'tech writing', 'technical documentation'],
                'api_documentation': ['api docs', 'api documentation', 'api reference', 'api guide'],
                'user_guides': ['user guide', 'user manual', 'user documentation'],
                'readme_generation': ['readme file', 'readme creation', 'readme generation'],
                'markdown_formatting': ['markdown', 'md file', 'markdown formatting'],
                'content_management': ['content management', 'content creation', 'cms'],
                'documentation_automation': ['docs automation', 'doc generation', 'automated docs'],
                'knowledge_management': ['knowledge base', 'kb', 'knowledge management']
            }
            
            if spec_area in spec_variations:
                for variation in spec_variations[spec_area]:
                    if variation in query_lower:
                        score += 1.5
                        break
        
        # Enhanced specialization area matching with context awareness
        for spec_area in agent_config.specialization_areas:
            spec_score = 0.0
            spec_normalized = spec_area.replace('_', ' ')
            
            if spec_normalized in query_lower:
                spec_score = 1.8  # Higher weight for specialization matches
            
            # Check for specialized area variations with enhanced matching
            spec_variations = self._get_specialization_variations(spec_area)
            for variation in spec_variations:
                if re.search(rf'\b{re.escape(variation)}\w*', query_lower):
                    spec_score = max(spec_score, 1.5)
            
            score += spec_score
        
        # Context momentum bonus (agent expertise builds over conversation)
        if hasattr(self, 'context_enrichment_engine'):
            agent_domain = self._get_agent_primary_domain(agent_config.name)
            if agent_domain in self.context_enrichment_engine.domain_momentum:
                momentum_bonus = self.context_enrichment_engine.domain_momentum[agent_domain] * 0.5
                score += momentum_bonus
        
        # Optimized query type alignment bonus (use cached context)
        if hasattr(self, '_context_cache') and hasattr(self, 'context_enrichment_engine'):
            cache_key = hashlib.md5(query.encode()).hexdigest()[:8]
            if cache_key in self._context_cache:
                enriched_context = self._context_cache[cache_key]
            else:
                enriched_context = self.context_enrichment_engine.enrich_context(query)
                self._context_cache[cache_key] = enriched_context
                
            if self._agent_aligns_with_query_type(agent_config, enriched_context.get('query_type')):
                score += 1.0
        
        return score * agent_config.weight_multiplier, matched_patterns
    
    def detect_multi_domain_query(self, query: str) -> List[str]:
        """Enhanced multi-domain query detection using cross-domain coordinator."""
        query_lower = query.lower()
        detected_domains = []
        
        # Use cross-domain coordinator for enhanced detection if available
        if self.cross_domain_coordinator:
            try:
                analysis = self.cross_domain_coordinator.analyze_cross_domain_integration(query)
                
                # Extract domains from boundary analysis
                for boundary in analysis.detected_boundaries:
                    detected_domains.append(boundary.primary_domain.value)
                    detected_domains.extend([d.value for d in boundary.secondary_domains])
                
                # If cross-domain analysis detected domains, use those
                if detected_domains:
                    return list(set(detected_domains))
            except Exception as e:
                logger.warning(f"Cross-domain analysis failed in multi-domain detection: {e}")
        
        # Fallback to enhanced context enrichment detection
        if hasattr(self, 'context_enrichment_engine'):
            try:
                enriched = self.context_enrichment_engine.enrich_context(query)
                detected_domains = enriched.get('domain_signals', [])
            except Exception as e:
                logger.debug(f"Context enrichment failed: {e}")
                detected_domains = []
        
        # Enhanced fallback detection with improved patterns
        if not detected_domains:
            domain_keywords = {
                'testing': [
                    'test', 'pytest', 'mock', 'coverage', 'fixture', 'async',
                    'unit test', 'integration test', 'e2e test', 'testing framework'
                ],
                'infrastructure': [
                    'docker', 'container', 'service', 'deployment', 'orchestration', 
                    'kubernetes', 'k8s', 'infrastructure', 'helm', 'terraform', 
                    'ansible', 'scaling', 'monitoring', 'networking', 'cluster',
                    'automation', 'provision', 'devops', 'sre', 'microservices',
                    'ci/cd', 'pipeline', 'container orchestration'
                ],
                'security': [
                    'security', 'vulnerability', 'credential', 'audit', 'compliance', 
                    'authentication', 'authorization', 'encryption', 'ssl', 'tls'
                ],
                'performance': [
                    'performance', 'latency', 'optimization', 'bottleneck', 'resource', 
                    'memory', 'cpu', 'throughput', 'scaling', 'load balancing'
                ],
                'code_quality': [
                    'refactor', 'quality', 'lint', 'format', 'architecture', 'variable', 
                    'function', 'clean code', 'technical debt', 'code review'
                ],
                'documentation': [
                    'documentation', 'docs', 'readme', 'markdown', 'md', 'api', 'guide', 
                    'tutorial', 'manual', 'specification', 'wiki', 'handbook', 'knowledge', 
                    'reference', 'howto', 'faq', 'technical', 'writing', 'content',
                    'api documentation', 'user guide', 'technical writing'
                ]
            }
            
            # Enhanced keyword matching with phrase detection
            for domain, keywords in domain_keywords.items():
                if any(keyword in query_lower for keyword in keywords):
                    detected_domains.append(domain)
        
        # Enhanced coordination pattern detection with better coverage
        coordination_patterns = [
            # Explicit multi-domain patterns
            'multiple domains', 'cross domain', 'multi domain', 'across domains',
            'coordinate', 'orchestrate', 'integrate', 'synchronize',
            # Analysis depth patterns  
            'comprehensive analysis', 'systematic review', 'holistic approach',
            'end-to-end', 'full stack', 'complete solution',
            # Parallel processing patterns
            'parallel', 'concurrent', 'simultaneous', 'multiple tasks',
            # Strategic patterns
            'strategic', 'enterprise', 'architecture', 'framework'
        ]
        
        coordination_detected = any(pattern in query_lower for pattern in coordination_patterns)
        
        # Enhanced multi-domain inference with smarter complementary domain selection
        if coordination_detected:
            if not detected_domains:  
                # Infer domains based on coordination context
                if any(word in query_lower for word in ['crisis', 'emergency', 'urgent']):
                    detected_domains.extend(['infrastructure', 'security', 'performance'])
                elif any(word in query_lower for word in ['analysis', 'review', 'assessment']):
                    detected_domains.extend(['testing', 'infrastructure'])
                else:
                    detected_domains.extend(['infrastructure', 'performance'])
            elif len(detected_domains) == 1:
                # Smart complementary domain mapping
                complement_map = {
                    'testing': ['infrastructure', 'security'],
                    'infrastructure': ['security', 'testing', 'performance'],
                    'security': ['infrastructure', 'testing'],
                    'performance': ['infrastructure', 'testing'],
                    'documentation': ['testing', 'infrastructure'],
                    'code_quality': ['testing', 'security']
                }
                primary_domain = detected_domains[0]
                complements = complement_map.get(primary_domain, ['infrastructure'])
                
                # Add 1-2 complements based on coordination strength
                num_complements = 2 if 'comprehensive' in query_lower or 'strategic' in query_lower else 1
                detected_domains.extend(complements[:num_complements])
        
        return list(set(detected_domains))  # Remove duplicates
    
    def select_agent(self, query: str, context: Optional[Dict] = None) -> AgentMatchResult:
        """Select the best agent based on enhanced pattern matching."""
        start_time = time.perf_counter()
        
        # Get pattern-based matches first
        pattern_matches = self.pattern_success_tracker.get_pattern_based_matches(query)
        
        if pattern_matches:
            match = pattern_matches[0]  # Take best match
            return AgentMatchResult(
                agent_name=match[0],
                confidence_score=match[1],
                matched_patterns=[match[2]],
                processing_time_ms=(time.perf_counter() - start_time) * 1000,
                reasoning=f"Pattern-based match: {match[2]}",
                context_keywords=self._extract_context_keywords(query)
            )
            
        # Fall back to test specialist as default
        return AgentMatchResult(
            agent_name="test-specialist",
            confidence_score=0.5,
            matched_patterns=["default pattern"],
            processing_time_ms=(time.perf_counter() - start_time) * 1000,
            reasoning="Pattern-based default match",
            context_keywords=self._extract_context_keywords(query)
        )
    
    def _select_agent_original(self, query: str, start_time: float) -> AgentMatchResult:
        """Original agent selection logic as fallback."""
        # Extract keywords for fast filtering
        keywords = self.extract_keywords(query)
        
        # Get candidate agents based on keywords
        candidate_agents = set()
        if keywords:
            for keyword in keywords:
                candidate_agents.update(self.keyword_index.get(keyword, []))
        
        # If no keyword matches, consider all agents
        if not candidate_agents:
            candidate_agents = set(self.agents.keys())
        
        # Calculate scores for candidate agents
        agent_scores = []
        for agent_name in candidate_agents:
            agent_config = self.agents[agent_name]
            score, matched_patterns = self.calculate_context_score(query, agent_config)
            
            agent_scores.append({
                'name': agent_name,
                'score': score,
                'matched_patterns': matched_patterns,
                'config': agent_config
            })
        
        # Sort by score descending
        agent_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Infrastructure specialization preference for docker/container queries
        query_lower = query.lower()
        if (len(agent_scores) >= 2 and 
            any(term in query_lower for term in ['docker', 'container', 'orchestration', 'deployment', 'infrastructure']) and
            'infrastructure-engineer' in [a['name'] for a in agent_scores[:2]]):
            
            infra_idx = next(i for i, a in enumerate(agent_scores) if a['name'] == 'infrastructure-engineer')
            if infra_idx == 1 and abs(agent_scores[0]['score'] - agent_scores[1]['score']) < 1.0:
                # Swap if infrastructure-engineer is close second for infrastructure queries
                agent_scores[0], agent_scores[1] = agent_scores[1], agent_scores[0]
        
        # Enhanced agent selection with cross-domain boundary detection and improved confidence scoring
        if agent_scores and agent_scores[0]['score'] > self.fallback_threshold:
            best_agent = agent_scores[0]
            
            # Improved confidence calculation with pattern-based weighting
            base_confidence = self._calculate_enhanced_confidence(
                best_agent['score'], 
                best_agent['name'], 
                len(best_agent['matched_patterns']),
                query
            )
            
            confidence_score = min(1.0, base_confidence)
            reasoning = self._generate_selection_reasoning(best_agent, agent_scores, query)
        else:
            # Enhanced fallback logic - avoid digdeep unless truly necessary
            fallback_agent, confidence_score, reasoning = self._determine_fallback_agent(query, agent_scores)
            best_agent = {
                'name': fallback_agent,
                'matched_patterns': [],
                'score': confidence_score
            }
        
        processing_time = (time.perf_counter() - start_time) * 1000
        
        return AgentMatchResult(
            agent_name=best_agent['name'],
            confidence_score=confidence_score,
            matched_patterns=best_agent['matched_patterns'],
            processing_time_ms=processing_time,
            context_keywords=keywords,
            reasoning=reasoning
        )
    
    def get_agent_suggestions(self, query: str, top_n: int = 3) -> List[AgentMatchResult]:
        """Get top N agent suggestions for a query."""
        keywords = self.extract_keywords(query)
        candidate_agents = set()
        
        if keywords:
            for keyword in keywords:
                candidate_agents.update(self.keyword_index.get(keyword, []))
        else:
            candidate_agents = set(self.agents.keys())
        
        results = []
        for agent_name in candidate_agents:
            agent_config = self.agents[agent_name]
            score, matched_patterns = self.calculate_context_score(query, agent_config)
            # Enhanced confidence calculation
            base_confidence = score / 4.5  # Slightly adjusted normalization
            if agent_name == 'infrastructure-engineer' and base_confidence > 0.4:
                base_confidence *= 1.25  # Infrastructure boost
            elif agent_name == 'documentation-enhancer' and base_confidence > 0.2:
                base_confidence *= 1.5  # Documentation boost
                if score > 1.0:
                    base_confidence = max(base_confidence, 0.75)
                elif score > 0.5:
                    base_confidence = max(base_confidence, 0.65)
            elif agent_name == 'security-enforcer' and base_confidence > 0.2:
                base_confidence *= 1.4  # Security boost
                if score > 1.0:
                    base_confidence = max(base_confidence, 0.80)
                elif score > 0.5:
                    base_confidence = max(base_confidence, 0.70)
            confidence_score = min(1.0, base_confidence)
            
            if confidence_score > 0.1:  # Filter out very low confidence
                results.append(AgentMatchResult(
                    agent_name=agent_name,
                    confidence_score=confidence_score,
                    matched_patterns=matched_patterns,
                    processing_time_ms=0.0,  # Not timed for batch operation
                    context_keywords=keywords,
                    reasoning=f"Score: {score:.2f}, Patterns: {len(matched_patterns)}"
                ))
        
        # Sort by confidence and return top N
        results.sort(key=lambda x: x.confidence_score, reverse=True)
        return results[:top_n]
    
    def get_selection_stats(self) -> Dict:
        """Get statistics about agent selection patterns."""
        if not self.selection_history:
            return {
                'total_selections': 0,
                'agent_distribution': {},
                'average_confidence': 0.0,
                'average_processing_time_ms': 0.0,
                'most_selected_agent': None,
                'cross_domain_selections': 0,
                'cross_domain_usage_rate': 0.0,
                'conflict_handling_selections': 0,
                'conflict_handling_rate': 0.0
            }
        
        # Handle both old (2-element) and new (3-element with enriched context) history format
        agent_counts = Counter()
        confidence_scores = []
        processing_times = []
        
        for selection_data in self.selection_history:
            if len(selection_data) == 2:
                # Old format: (query, result)
                _, result = selection_data
            else:
                # New format: (query, result, enriched_context)
                _, result, _ = selection_data
            
            agent_counts[result.agent_name] += 1
            confidence_scores.append(result.confidence_score)
            processing_times.append(result.processing_time_ms)
        
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        avg_processing_time = sum(processing_times) / len(processing_times)
        
        # Enhanced cross-domain analysis statistics with better error handling
        cross_domain_stats = {}
        learning_insights = {}
        
        if self.cross_domain_coordinator:
            try:
                cross_domain_stats = self.cross_domain_coordinator.get_analysis_stats()
                learning_insights = self.cross_domain_coordinator.get_learning_insights()
            except Exception as e:
                logger.warning(f"Failed to get cross-domain coordinator stats: {e}")
                cross_domain_stats = {'error': f'Cross-domain stats unavailable: {str(e)}'}
                learning_insights = {'error': f'Learning insights unavailable: {str(e)}'}
        
        # Enhanced base statistics with cross-domain context
        cross_domain_selections = len([h for h in self.selection_history 
                                     if len(h) > 2 and h[2].get('cross_domain_used', False)])
        conflict_handling_selections = len([h for h in self.selection_history 
                                          if len(h) > 2 and h[2].get('has_conflicts', False)])
        
        base_stats = {
            'total_selections': len(self.selection_history),
            'agent_distribution': dict(agent_counts),
            'average_confidence': avg_confidence,
            'average_processing_time_ms': avg_processing_time,
            'most_selected_agent': agent_counts.most_common(1)[0] if agent_counts else None,
            'cross_domain_selections': cross_domain_selections,
            'cross_domain_usage_rate': cross_domain_selections / max(len(self.selection_history), 1),
            'conflict_handling_selections': conflict_handling_selections,
            'conflict_handling_rate': conflict_handling_selections / max(len(self.selection_history), 1)
        }
        
        # Integrate cross-domain statistics and learning insights
        if cross_domain_stats and 'error' not in cross_domain_stats:
            base_stats['cross_domain_analysis'] = cross_domain_stats
            
        if learning_insights and 'error' not in learning_insights:
            base_stats['learning_insights'] = learning_insights
        
        return base_stats
    
    def _generate_pattern_key(self, query: str, agent: str, enriched_context: Dict[str, any]) -> str:
        """Generate a unique pattern key for tracking."""
        # Create pattern key based on query characteristics
        domain_signals = '_'.join(sorted(enriched_context.get('domain_signals', [])))
        complexity = enriched_context.get('complexity_level', 'medium')
        urgency = enriched_context.get('urgency_level', 'medium')
        
        pattern_signature = f"{domain_signals}_{complexity}_{urgency}_{agent}"
        return hashlib.md5(pattern_signature.encode()).hexdigest()[:12]
    
    def _calculate_enhanced_confidence(self, score: float, agent_name: str, 
                                      pattern_count: int, query: str) -> float:
        """Calculate enhanced confidence score with better normalization."""
        # Base confidence with improved normalization
        base_confidence = score / 4.5
        
        # Pattern count bonus (more patterns = higher confidence)
        pattern_bonus = min(0.2, pattern_count * 0.05)
        base_confidence += pattern_bonus
        
        # Agent-specific confidence boosts
        agent_boosts = {
            'infrastructure-engineer': {
                'multiplier': 1.4,  # Higher boost for infrastructure
                'min_threshold': 0.3,  # Lower threshold
                'keywords': ['docker', 'kubernetes', 'container', 'service', 'deployment', 'orchestration', 'infrastructure']
            },
            'documentation-enhancer': {
                'multiplier': 1.5,
                'min_threshold': 0.2,
                'keywords': ['documentation', 'docs', 'readme', 'guide', 'api']
            },
            'security-enforcer': {
                'multiplier': 1.4,
                'min_threshold': 0.2,
                'keywords': ['security', 'vulnerability', 'audit', 'compliance']
            },
            'test-specialist': {
                'multiplier': 1.3,
                'min_threshold': 0.3,
                'keywords': ['test', 'pytest', 'mock', 'coverage']
            }
        }
        
        if agent_name in agent_boosts:
            boost_config = agent_boosts[agent_name]
            if base_confidence > boost_config['min_threshold']:
                # Additional boost if query contains relevant keywords
                query_lower = query.lower()
                keyword_matches = sum(1 for kw in boost_config['keywords'] if kw in query_lower)
                keyword_multiplier = 1.0 + (keyword_matches * 0.1)
                
                base_confidence *= boost_config['multiplier'] * keyword_multiplier
                
                # Set minimum confidence for strong matches
                if score > 2.0:
                    min_confidence = 0.6 if agent_name == 'infrastructure-engineer' else 0.65
                    base_confidence = max(base_confidence, min_confidence)
        
        return base_confidence
    
    def _get_keyword_variations(self, keyword: str) -> List[str]:
        """Get semantic variations of a keyword for enhanced matching."""
        variations_map = {
            'test': ['testing', 'tests', 'tested', 'pytest', 'unittest', 'spec', 'verify'],
            'docker': ['container', 'containerize', 'containerized', 'orchestration'],
            'kubernetes': ['k8s', 'kube', 'orchestration', 'cluster'],
            'security': ['secure', 'secured', 'securing', 'safety', 'protection'],
            'performance': ['optimize', 'optimization', 'speed', 'efficiency', 'benchmark'],
            'infrastructure': ['infra', 'devops', 'deployment', 'provisioning'],
            'documentation': ['docs', 'document', 'documenting', 'guide', 'manual'],
            'refactor': ['refactoring', 'restructure', 'redesign', 'cleanup'],
            'configuration': ['config', 'configure', 'setup', 'setting'],
            'monitoring': ['monitor', 'observability', 'metrics', 'logging']
        }
        
        return variations_map.get(keyword, [])
    
    def _get_specialization_variations(self, spec_area: str) -> List[str]:
        """Get variations for specialization areas with enhanced coverage."""
        spec_variations = {
            'container_orchestration': ['orchestration', 'orchestrated', 'orchestrate', 'docker swarm', 'kubernetes'],
            'cloud_native': ['cloud-native', 'cloud native', 'cloudnative', 'microservices', 'distributed'],
            'infrastructure_as_code': ['infrastructure as code', 'iac', 'infra as code', 'terraform', 'ansible'],
            'deployment_automation': ['deployment automation', 'automated deployment', 'deploy automation', 'ci/cd'],
            'service_mesh': ['service mesh', 'servicemesh', 'mesh', 'istio', 'linkerd'],
            'technical_writing': ['technical writing', 'tech writing', 'technical documentation', 'content creation'],
            'api_documentation': ['api docs', 'api documentation', 'api reference', 'api guide', 'openapi', 'swagger'],
            'user_guides': ['user guide', 'user manual', 'user documentation', 'how-to', 'tutorial'],
            'readme_generation': ['readme file', 'readme creation', 'readme generation', 'project documentation'],
            'markdown_formatting': ['markdown', 'md file', 'markdown formatting', 'markup'],
            'content_management': ['content management', 'content creation', 'cms', 'knowledge base'],
            'documentation_automation': ['docs automation', 'doc generation', 'automated docs', 'doc pipeline'],
            'knowledge_management': ['knowledge base', 'kb', 'knowledge management', 'wiki'],
            'async_testing': ['async test', 'asyncio test', 'async mock', 'await test'],
            'mocking': ['mock', 'mocking', 'test double', 'stub', 'spy'],
            'coverage_analysis': ['test coverage', 'code coverage', 'coverage report', 'coverage gap'],
            'vulnerability_scanning': ['vuln scan', 'security scan', 'security audit', 'penetration test'],
            'compliance': ['compliance check', 'regulatory', 'audit', 'governance'],
            'performance_analysis': ['perf analysis', 'performance profiling', 'benchmark', 'optimization']
        }
        
        return spec_variations.get(spec_area, [spec_area.replace('_', ' ')])
    
    def _get_agent_primary_domain(self, agent_name: str) -> str:
        """Get the primary domain for an agent."""
        domain_mapping = {
            'test-specialist': 'testing',
            'infrastructure-engineer': 'infrastructure', 
            'security-enforcer': 'security',
            'performance-optimizer': 'performance',
            'intelligent-enhancer': 'code_quality',
            'code-quality-specialist': 'code_quality',
            'ci-specialist': 'infrastructure',
            'documentation-enhancer': 'documentation'
        }
        return domain_mapping.get(agent_name, 'general')
    
    def _agent_aligns_with_query_type(self, agent_config: AgentConfig, query_type: str) -> bool:
        """Check if agent aligns with the query type."""
        if not query_type:
            return False
            
        agent_query_alignment = {
            'test-specialist': ['problem_solving', 'analysis', 'maintenance'],
            'infrastructure-engineer': ['creation', 'optimization', 'coordination', 'maintenance'],
            'security-enforcer': ['analysis', 'problem_solving', 'maintenance'],
            'performance-optimizer': ['optimization', 'analysis', 'problem_solving'],
            'intelligent-enhancer': ['optimization', 'creation', 'maintenance'],
            'code-quality-specialist': ['optimization', 'analysis', 'maintenance'],
            'ci-specialist': ['creation', 'optimization', 'coordination'],
            'documentation-enhancer': ['creation', 'maintenance', 'analysis']
        }
        
        aligned_types = agent_query_alignment.get(agent_config.name, [])
        return query_type in aligned_types
    
    def _generate_selection_reasoning(self, best_agent: Dict, all_scores: List[Dict], query: str) -> str:
        """Generate detailed reasoning for agent selection with Task tool pattern recognition."""
        pattern_count = len(best_agent['matched_patterns'])
        score = best_agent['score']
        query_lower = query.lower()
        
        # Enhanced Task tool coordination pattern detection
        task_patterns = [
            "coordinating" in query_lower and "tasks" in query_lower and "parallel" in query_lower,
            "using" in query_lower and "tasks" in query_lower and "parallel" in query_lower,
            "analyzing" in query_lower and "parallel" in query_lower,
            "coordination" in query_lower and ("analysis" in query_lower or "assessment" in query_lower),
            "comprehensive" in query_lower and "parallel" in query_lower,
            "coordinating" in query_lower and "parallel" in query_lower  # Additional coordination pattern
        ]
        
        # Enhanced multi-domain coordination detection
        domains_in_query = sum(1 for domain in ['security', 'testing', 'performance', 'infrastructure', 'documentation'] 
                              if domain in query_lower)
        
        # Check for explicit agent coordination patterns
        explicit_agent_coordination = any(agent_name in query_lower for agent_name in 
                                        ['analysis-gateway', 'test-specialist', 'infrastructure-engineer', 
                                         'security-enforcer', 'documentation-enhancer', 'performance-optimizer'])
        
        if any(task_patterns):
            if explicit_agent_coordination and best_agent['name'] != 'meta-coordinator':
                reason = f"Task coordination with explicit agent selection: {best_agent['name']} (score: {score:.2f})"
                if domains_in_query >= 2:
                    reason += f" coordinating {domains_in_query} domains"
            elif best_agent['name'] in ['analysis-gateway', 'meta-coordinator']:
                coordination_type = 'multi-domain' if domains_in_query >= 3 else 'dual-domain' if domains_in_query == 2 else 'coordination'
                reason = f"Task tool {coordination_type} parallel coordination pattern (score: {score:.2f})"
                if domains_in_query >= 2:
                    reason += f" integrating {domains_in_query} domains"
            else:
                reason = f"Task coordination pattern, specialized agent selected: {best_agent['name']} (score: {score:.2f})"
        elif domains_in_query >= 2 and best_agent['name'] in ['analysis-gateway', 'meta-coordinator']:
            reason = f"Multi-domain coordination required ({domains_in_query} domains, score: {score:.2f})"
        elif pattern_count > 3:
            reason = f"Strong pattern match: {pattern_count} patterns matched (score: {score:.2f})"
        elif pattern_count > 1:
            reason = f"Good pattern match: {pattern_count} patterns matched (score: {score:.2f})"
        else:
            reason = f"Basic pattern match (score: {score:.2f})"
        
        # Add competitive analysis if multiple good options
        if len(all_scores) > 1 and all_scores[1]['score'] > 1.0:
            second_best = all_scores[1]
            score_diff = best_agent['score'] - second_best['score']
            if score_diff < 0.5:
                reason += f"; closely competing with {second_best['name']}"
        
        return reason
    
    def _determine_fallback_agent(self, query: str, agent_scores: List[Dict]) -> Tuple[str, float, str]:
        """Determine fallback agent with enhanced logic to minimize digdeep usage."""
        query_lower = query.lower()
        
        # Check if any agent had a reasonable score (above digdeep threshold)
        if agent_scores:
            best_score = agent_scores[0]['score']
            best_agent = agent_scores[0]['name']
            
            if best_score > self.digdeep_threshold:
                # Use the best scoring agent even if below fallback threshold
                confidence = max(0.4, best_score / 4.5)
                reason = f"Best available match: {best_agent} (score: {best_score:.2f})"
                return best_agent, confidence, reason
        
        # Multi-domain detection for coordination agents
        multi_domains = self.detect_multi_domain_query(query)
        if len(multi_domains) > 2:
            return 'meta-coordinator', 0.65, f"Multi-domain coordination needed: {', '.join(multi_domains)}"
        elif len(multi_domains) == 2:
            return 'analysis-gateway', 0.6, f"Dual-domain analysis: {', '.join(multi_domains)}"
        
        # Check for specific fallback patterns
        fallback_patterns = {
            'urgent': ('meta-coordinator', 0.7, "Crisis coordination needed"),
            'emergency': ('meta-coordinator', 0.7, "Emergency response coordination"),
            'help': ('intelligent-enhancer', 0.5, "General assistance request"),
            'problem': ('intelligent-enhancer', 0.5, "General problem-solving"),
            'issue': ('intelligent-enhancer', 0.5, "General issue resolution"),
        }
        
        for pattern, (agent, confidence, reason) in fallback_patterns.items():
            if pattern in query_lower:
                return agent, confidence, reason
        
        # Last resort - only use digdeep for truly vague queries
        if len(query.strip()) < 10 or not any(char.isalpha() for char in query):
            return 'digdeep', 0.4, "Query too vague - deep analysis needed"
        
        # Default to intelligent-enhancer instead of digdeep
        return 'intelligent-enhancer', 0.45, "No specific patterns detected - general enhancement"
    
    def get_learning_insights(self) -> Dict[str, any]:
        """Enhanced insights from the learning system with cross-domain coordination statistics."""
        if not hasattr(self, 'pattern_success_tracker'):
            return {'message': 'Pattern success tracker not available'}
        
        # Base learning insights
        insights = {
            'total_patterns_tracked': len(self.pattern_success_tracker.success_history),
            'active_pattern_weights': len(self.pattern_success_tracker.pattern_weights),
            'context_patterns_learned': len(self.pattern_success_tracker.context_patterns),
            'domain_momentum': dict(self.context_enrichment_engine.domain_momentum),
            'adaptive_learning_enabled': self.adaptive_learning_enabled,
            'agents_loaded_from_directory': len([agent for agent in self.agents if agent not in self._get_default_agent_names()]),
            'fallback_threshold': self.fallback_threshold,
            'digdeep_threshold': self.digdeep_threshold
        }
        
        # Enhanced pattern analysis
        if self.pattern_success_tracker.pattern_weights:
            sorted_patterns = sorted(
                self.pattern_success_tracker.pattern_weights.items(),
                key=lambda x: x[1],
                reverse=True
            )
            insights['top_performing_patterns'] = sorted_patterns[:8]  # More patterns for analysis
            insights['pattern_weight_distribution'] = {
                'high_weight': len([w for w in self.pattern_success_tracker.pattern_weights.values() if w > 1.5]),
                'medium_weight': len([w for w in self.pattern_success_tracker.pattern_weights.values() if 0.8 <= w <= 1.5]),
                'low_weight': len([w for w in self.pattern_success_tracker.pattern_weights.values() if w < 0.8])
            }
        
        # Cross-domain coordination insights
        if self.cross_domain_coordinator:
            try:
                cross_domain_insights = self.cross_domain_coordinator.get_learning_insights()
                insights['cross_domain_learning'] = cross_domain_insights
            except Exception as e:
                insights['cross_domain_learning'] = {'error': str(e)}
        
        # Selection history insights
        if self.selection_history:
            recent_history = self.selection_history[-50:]  # Last 50 selections
            cross_domain_usage = len([h for h in recent_history 
                                    if len(h) > 2 and h[2].get('cross_domain_used', False)])
            insights['recent_cross_domain_usage_rate'] = cross_domain_usage / len(recent_history)
            
            avg_confidence_recent = sum(h[1].confidence_score for h in recent_history) / len(recent_history)
            insights['recent_average_confidence'] = avg_confidence_recent
        
        return insights
    
    def _get_default_agent_names(self) -> List[str]:
        """Get list of default agent names (those not loaded from directory)."""
        return [
            'test-specialist', 'infrastructure-engineer', 'security-enforcer',
            'performance-optimizer', 'intelligent-enhancer', 'code-quality-specialist',
            'ci-specialist', 'documentation-enhancer'
        ]
        
    def record_feedback(self, query: str, selected_agent: str, confidence: float, 
                       user_feedback: Optional[bool] = None, expected_agent: Optional[str] = None,
                       task_success: Optional[bool] = None, performance_metrics: Optional[Dict] = None):
        """Enhanced user feedback recording with cross-domain learning and performance tracking."""
        # Enhanced feedback recording with additional context
        if self.cross_domain_coordinator:
            try:
                self.cross_domain_coordinator.record_selection_feedback(
                    query, selected_agent, confidence, user_feedback, expected_agent, task_success
                )
            except Exception as e:
                logger.warning(f"Failed to record feedback in cross-domain coordinator: {e}")
        
        # Enhanced pattern success tracking with performance metrics integration
        if self.adaptive_learning_enabled and hasattr(self, 'pattern_success_tracker'):
            try:
                enriched_context = self.context_enrichment_engine.enrich_context(query)
                pattern_key = self._generate_pattern_key(query, selected_agent, enriched_context)
                
                # Enhanced pattern weight updates with performance consideration
                if user_feedback is True or task_success is True:
                    # Boost pattern weight for positive feedback with performance bonus
                    current_weight = self.pattern_success_tracker.get_pattern_weight(pattern_key)
                    base_increase = 0.2 if user_feedback is True else 0.15
                    
                    # Performance metrics bonus
                    performance_bonus = 0.0
                    if performance_metrics:
                        if performance_metrics.get('response_time_ms', 1000) < 500:
                            performance_bonus += 0.05  # Fast response bonus
                        if performance_metrics.get('accuracy', 0.5) > 0.8:
                            performance_bonus += 0.05  # High accuracy bonus
                    
                    total_increase = base_increase + performance_bonus
                    self.pattern_success_tracker.pattern_weights[pattern_key] = min(2.5, current_weight + total_increase)
                    
                elif user_feedback is False or task_success is False:
                    # Reduce pattern weight for negative feedback with severity consideration
                    current_weight = self.pattern_success_tracker.get_pattern_weight(pattern_key)
                    base_decrease = 0.3 if user_feedback is False else 0.2
                    
                    # Severity adjustment based on expected agent mismatch
                    if expected_agent and expected_agent != selected_agent:
                        base_decrease += 0.1  # Additional penalty for wrong agent
                    
                    self.pattern_success_tracker.pattern_weights[pattern_key] = max(0.2, current_weight - base_decrease)
                
                logger.info(f"Updated pattern weight for {pattern_key}: {self.pattern_success_tracker.get_pattern_weight(pattern_key):.3f}")
            except Exception as e:
                logger.warning(f"Failed to record enhanced feedback in pattern success tracker: {e}")
    
    def get_cross_domain_analysis(self, query: str) -> Optional[Dict]:
        """Get detailed cross-domain analysis for a query."""
        if not self.cross_domain_coordinator:
            return None
        
        try:
            analysis = self.cross_domain_coordinator.analyze_cross_domain_integration(query)
            return {
                'detected_boundaries': [
                    {
                        'primary_domain': boundary.primary_domain.value,
                        'secondary_domains': [d.value for d in boundary.secondary_domains],
                        'confidence': boundary.confidence,
                        'complexity_score': boundary.complexity_score,
                        'overlap_indicators': boundary.overlap_indicators
                    }
                    for boundary in analysis.detected_boundaries
                ],
                'potential_conflicts': [
                    {
                        'conflict_type': conflict.conflict_type.value,
                        'involved_domains': [d.value for d in conflict.involved_domains],
                        'severity': conflict.severity,
                        'description': conflict.description,
                        'resolution_strategies': conflict.resolution_strategies,
                        'affected_agents': conflict.affected_agents
                    }
                    for conflict in analysis.potential_conflicts
                ],
                'recommended_coordination': analysis.recommended_coordination,
                'agent_suggestions': analysis.agent_suggestions,
                'integration_complexity': analysis.integration_complexity,
                'processing_time_ms': analysis.processing_time_ms
            }
        except Exception as e:
            logger.error(f"Cross-domain analysis failed: {e}")
            return None


# Global instance for easy access
_agent_selector = None


def get_agent_selector() -> EnhancedAgentSelector:
    """Get the global agent selector instance."""
    global _agent_selector
    if _agent_selector is None:
        _agent_selector = EnhancedAgentSelector()
    return _agent_selector


def select_best_agent(query: str, context: Optional[Dict] = None) -> AgentMatchResult:
    """Convenience function to select the best agent for a query."""
    return get_agent_selector().select_agent(query, context)
