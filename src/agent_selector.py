"""Enhanced agent selection system with improved pattern matching."""

import re
import time
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import logging

logger = logging.getLogger(__name__)


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
    
    def __init__(self):
        """Initialize the enhanced agent selector."""
        self.agents = self._initialize_agents()
        self.keyword_index = self._build_keyword_index()
        self.pattern_cache = {}
        self.selection_history = []
        
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
                primary_keywords=['docker', 'container', 'service', 'infrastructure', 'deployment', 'orchestration'],
                context_patterns=[
                    r'docker.{0,20}(orchestration|compose|network|swarm)',
                    r'container.{0,15}(scaling|network|resource|runtime)',
                    r'service.{0,15}(mesh|discovery|communication|registry)',
                    r'infrastructure.{0,20}(performance|scaling|architecture|automation)',
                    r'deployment.{0,15}(pipeline|strategy|automation|rollout)',
                    r'kubernetes.{0,15}(cluster|pod|service|ingress)',
                    r'orchestration.{0,15}(container|service|microservice)'
                ],
                intent_indicators=['deploy', 'scale', 'orchestrate', 'optimize', 'architect', 'provision'],
                weight_multiplier=1.1,
                description="Docker orchestration with systematic infrastructure coordination",
                specialization_areas=['docker', 'kubernetes', 'container_orchestration', 'service_mesh']
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
                primary_keywords=['ci', 'cd', 'pipeline', 'workflow', 'github', 'actions', 'automation'],
                context_patterns=[
                    r'ci.{0,15}(pipeline|workflow|automation|config)',
                    r'github.{0,15}(actions|workflow|pipeline|automation)',
                    r'pipeline.{0,15}(build|deploy|test|automation)',
                    r'workflow.{0,15}(automation|github|ci|build)',
                    r'automation.{0,15}(build|deploy|test|pipeline)'
                ],
                intent_indicators=['automate', 'build', 'deploy', 'integrate', 'pipeline'],
                weight_multiplier=1.1,
                description="CI/CD pipeline optimization and GitHub Actions expertise",
                specialization_areas=['github_actions', 'pipeline_automation', 'ci_cd']
            )
        }
    
    def _build_keyword_index(self) -> Dict[str, List[str]]:
        """Build keyword index for fast agent lookup."""
        keyword_index = defaultdict(list)
        
        for agent_name, config in self.agents.items():
            for keyword in config.primary_keywords:
                keyword_index[keyword].append(agent_name)
        
        return keyword_index
    
    def extract_keywords(self, query: str) -> List[str]:
        """Extract relevant keywords from query with stemming and variations."""
        query_lower = query.lower()
        keywords = []
        
        # Extract exact primary keywords
        for keyword in self.keyword_index.keys():
            if keyword in query_lower:
                keywords.append(keyword)
        
        # Handle common variations and stemming
        keyword_variations = {
            'testing': 'test',
            'tests': 'test',
            'tested': 'test',
            'containers': 'container',
            'containerization': 'container',
            'deployed': 'deployment',
            'deploying': 'deployment',
            'securing': 'security',
            'secured': 'security',
            'optimizing': 'optimization',
            'optimized': 'optimization',
            'refactoring': 'refactor',
            'refactored': 'refactor'
        }
        
        for variation, root in keyword_variations.items():
            if variation in query_lower and root not in keywords:
                keywords.append(root)
        
        return keywords
    
    def calculate_context_score(self, query: str, agent_config: AgentConfig) -> Tuple[float, List[str]]:
        """Calculate context-based similarity score with matched patterns."""
        query_lower = query.lower()
        score = 0.0
        matched_patterns = []
        
        # Primary keyword matching with position weighting
        for keyword in agent_config.primary_keywords:
            if keyword in query_lower:
                base_score = 1.0
                
                # Boost score for early appearance in query
                position = query_lower.find(keyword)
                if position < len(query_lower) * 0.3:
                    base_score *= 1.3
                elif position < len(query_lower) * 0.6:
                    base_score *= 1.1
                
                # Boost for word boundaries (whole word matches)
                if re.search(rf'\b{re.escape(keyword)}\b', query_lower):
                    base_score *= 1.2
                
                score += base_score
        
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
        
        # Specialization area matching
        for spec_area in agent_config.specialization_areas:
            spec_normalized = spec_area.replace('_', ' ')
            if spec_normalized in query_lower:
                score += 1.5
        
        return score * agent_config.weight_multiplier, matched_patterns
    
    def detect_multi_domain_query(self, query: str) -> List[str]:
        """Detect if query spans multiple domains and suggest coordination."""
        query_lower = query.lower()
        detected_domains = []
        
        # Check for keywords from different domains
        domain_keywords = {
            'testing': ['test', 'pytest', 'mock', 'coverage'],
            'infrastructure': ['docker', 'container', 'service', 'deployment'],
            'security': ['security', 'vulnerability', 'credential', 'audit'],
            'performance': ['performance', 'latency', 'optimization', 'bottleneck'],
            'code_quality': ['refactor', 'quality', 'lint', 'format']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_domains.append(domain)
        
        return detected_domains
    
    def select_agent(self, query: str, context: Optional[Dict] = None) -> AgentMatchResult:
        """Select the best agent for the given query with enhanced matching."""
        start_time = time.perf_counter()
        
        # Handle empty or very short queries
        if not query or len(query.strip()) < 3:
            return AgentMatchResult(
                agent_name='intelligent-enhancer',
                confidence_score=0.1,
                matched_patterns=[],
                processing_time_ms=(time.perf_counter() - start_time) * 1000,
                reasoning="Query too short or empty, defaulting to intelligent-enhancer"
            )
        
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
        
        # Select best agent or fallback
        if agent_scores and agent_scores[0]['score'] > 0.5:
            best_agent = agent_scores[0]
            confidence_score = min(1.0, best_agent['score'] / 4.0)  # Normalize to 0-1
            reasoning = f"Selected based on {len(best_agent['matched_patterns'])} pattern matches"
        else:
            # Fallback logic
            multi_domains = self.detect_multi_domain_query(query)
            if len(multi_domains) > 1:
                best_agent = {
                    'name': 'intelligent-enhancer',  # Good for multi-domain coordination
                    'matched_patterns': [],
                    'score': 0.6
                }
                confidence_score = 0.6
                reasoning = f"Multi-domain query detected ({', '.join(multi_domains)}), using intelligent-enhancer for coordination"
            else:
                best_agent = {
                    'name': 'intelligent-enhancer',
                    'matched_patterns': [],
                    'score': 0.3
                }
                confidence_score = 0.3
                reasoning = "No strong matches found, defaulting to intelligent-enhancer"
        
        processing_time = (time.perf_counter() - start_time) * 1000
        
        result = AgentMatchResult(
            agent_name=best_agent['name'],
            confidence_score=confidence_score,
            matched_patterns=best_agent['matched_patterns'],
            processing_time_ms=processing_time,
            context_keywords=keywords,
            reasoning=reasoning
        )
        
        # Store in selection history for learning
        self.selection_history.append((query, result))
        
        # Keep history to reasonable size
        if len(self.selection_history) > 1000:
            self.selection_history = self.selection_history[-500:]
        
        return result
    
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
            confidence_score = min(1.0, score / 4.0)
            
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
            return {}
        
        agent_counts = Counter(result.agent_name for _, result in self.selection_history)
        avg_confidence = sum(result.confidence_score for _, result in self.selection_history) / len(self.selection_history)
        avg_processing_time = sum(result.processing_time_ms for _, result in self.selection_history) / len(self.selection_history)
        
        return {
            'total_selections': len(self.selection_history),
            'agent_distribution': dict(agent_counts),
            'average_confidence': avg_confidence,
            'average_processing_time_ms': avg_processing_time,
            'most_selected_agent': agent_counts.most_common(1)[0] if agent_counts else None
        }


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
