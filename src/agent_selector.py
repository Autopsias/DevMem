"""Enhanced agent selection system with improved pattern matching."""

import re
import time
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import logging

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
        self.cross_domain_coordinator = get_cross_domain_coordinator() if CROSS_DOMAIN_AVAILABLE else None
        
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
            'containerized': 'container',
            'deployed': 'deployment',
            'deploying': 'deployment',
            'deploy': 'deployment',
            'securing': 'security',
            'secured': 'security',
            'optimizing': 'optimization',
            'optimized': 'optimization',
            'refactoring': 'refactor',
            'refactored': 'refactor',
            # Infrastructure-specific variations
            'orchestrated': 'orchestration',
            'orchestrating': 'orchestration',
            'orchestrate': 'orchestration',
            'scaled': 'scale',
            'scaling': 'scale',
            'provisioned': 'provision',
            'provisioning': 'provision',
            'automated': 'automation',
            'automating': 'automation',
            'monitoring': 'monitor',
            'monitored': 'monitor',
            'configured': 'configuration',
            'configuring': 'configuration',
            'k8s': 'kubernetes',
            'kube': 'kubernetes',
            'infra': 'infrastructure',
            'devops': 'infrastructure',
            'sre': 'infrastructure',
            'microservices': 'service',
            'micro-services': 'service',
            'ci/cd': 'deployment',
            'cicd': 'deployment',
            # Documentation-specific variations
            'document': 'documentation',
            'documenting': 'documentation',
            'documented': 'documentation',
            'doc': 'docs',
            'documents': 'documentation',
            'writing': 'write',
            'written': 'write',
            'guides': 'guide',
            'tutorials': 'tutorial',
            'manuals': 'manual',
            'specifications': 'specification',
            'spec': 'specification',
            'specs': 'specification',
            'handbooks': 'handbook',
            'references': 'reference',
            'ref': 'reference',
            'refs': 'reference',
            'technical writing': 'technical',
            'tech writing': 'technical',
            'content creation': 'content',
            'content management': 'content',
            'knowledge base': 'knowledge',
            'kb': 'knowledge',
            'how-to': 'howto',
            'how to': 'howto'
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
        
        return score * agent_config.weight_multiplier, matched_patterns
    
    def detect_multi_domain_query(self, query: str) -> List[str]:
        """Detect if query spans multiple domains and suggest coordination."""
        query_lower = query.lower()
        detected_domains = []
        
        # Check for keywords from different domains
        domain_keywords = {
            'testing': ['test', 'pytest', 'mock', 'coverage', 'fixture', 'async'],
            'infrastructure': [
                'docker', 'container', 'service', 'deployment', 'orchestration', 
                'kubernetes', 'k8s', 'infrastructure', 'helm', 'terraform', 
                'ansible', 'scaling', 'monitoring', 'networking', 'cluster',
                'automation', 'provision', 'devops', 'sre', 'microservices'
            ],
            'security': ['security', 'vulnerability', 'credential', 'audit', 'compliance', 'authentication'],
            'performance': ['performance', 'latency', 'optimization', 'bottleneck', 'resource', 'memory', 'cpu'],
            'code_quality': ['refactor', 'quality', 'lint', 'format', 'architecture', 'variable', 'function'],
            'documentation': ['documentation', 'docs', 'readme', 'markdown', 'md', 'api', 'guide', 'tutorial', 'manual', 'specification', 'wiki', 'handbook', 'knowledge', 'reference', 'howto', 'faq', 'technical', 'writing', 'content']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_domains.append(domain)
        
        return detected_domains
    
    def select_agent(self, query: str, context: Optional[Dict] = None) -> AgentMatchResult:
        """Select the best agent for the given query with enhanced cross-domain analysis."""
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
        
        # Get original agent selection first
        original_result = self._select_agent_original(query, start_time)
        
        # Enhanced cross-domain analysis with learning integration if available
        cross_domain_analysis = None
        if self.cross_domain_coordinator:
            try:
                cross_domain_analysis = self.cross_domain_coordinator.analyze_cross_domain_integration(query)
                
                # Record the original selection for learning feedback
                if cross_domain_analysis and cross_domain_analysis.agent_suggestions:
                    # Auto-learn from high-confidence selections for infrastructure domain
                    best_suggestion = cross_domain_analysis.agent_suggestions[0]
                    if (best_suggestion[1] > 0.8 and 
                        any(boundary.primary_domain.value == 'infrastructure' 
                            for boundary in cross_domain_analysis.detected_boundaries)):
                        self.cross_domain_coordinator.record_selection_feedback(
                            query, best_suggestion[0], best_suggestion[1], user_feedback=None
                        )
                        
            except Exception as e:
                logger.warning(f"Cross-domain analysis failed: {e}")
        
        # Use cross-domain analysis if it provides better confidence or for infrastructure queries
        use_cross_domain = False
        if (cross_domain_analysis and 
            cross_domain_analysis.agent_suggestions):
            
            best_agent_name, cross_domain_confidence = cross_domain_analysis.agent_suggestions[0]
            
            # Prioritize cross-domain for infrastructure queries or higher confidence
            if (cross_domain_confidence > original_result.confidence_score or
                (cross_domain_confidence > 0.7 and 
                 any(boundary.primary_domain.value == 'infrastructure' 
                     for boundary in cross_domain_analysis.detected_boundaries))):
                use_cross_domain = True
        
        if use_cross_domain:
            best_agent_name, cross_domain_confidence = cross_domain_analysis.agent_suggestions[0]
            
            # Get additional reasoning from cross-domain analysis
            reasoning_parts = []
            
            if cross_domain_analysis.detected_boundaries:
                boundary = cross_domain_analysis.detected_boundaries[0]
                reasoning_parts.append(
                    f"Cross-domain analysis: {boundary.primary_domain.value} domain with "
                    f"{len(boundary.secondary_domains)} secondary domains"
                )
            
            if cross_domain_analysis.potential_conflicts:
                high_severity_conflicts = [c for c in cross_domain_analysis.potential_conflicts if c.severity >= 0.7]
                if high_severity_conflicts:
                    reasoning_parts.append(f"{len(high_severity_conflicts)} high-severity conflicts detected")
            
            if cross_domain_analysis.integration_complexity >= 0.7:
                reasoning_parts.append("High integration complexity detected")
            
            reasoning = "; ".join(reasoning_parts) if reasoning_parts else "Cross-domain analysis selection"
            
            # Handle coordination recommendations
            if 'meta-coordination' in cross_domain_analysis.recommended_coordination.lower():
                best_agent_name = 'meta-coordinator'
                cross_domain_confidence = min(1.0, cross_domain_confidence * 1.2)
                reasoning += " - meta-coordination recommended"
            elif 'parallel coordination' in cross_domain_analysis.recommended_coordination.lower():
                # Check if analysis-gateway is suggested
                analysis_gateway_suggestions = [s for s in cross_domain_analysis.agent_suggestions if s[0] == 'analysis-gateway']
                if analysis_gateway_suggestions:
                    best_agent_name = 'analysis-gateway'
                    cross_domain_confidence = analysis_gateway_suggestions[0][1]
                    reasoning += " - parallel coordination recommended"
            
            result = AgentMatchResult(
                agent_name=best_agent_name,
                confidence_score=min(1.0, cross_domain_confidence),
                matched_patterns=[f"cross_domain_{boundary.primary_domain.value}" for boundary in cross_domain_analysis.detected_boundaries],
                processing_time_ms=(time.perf_counter() - start_time) * 1000,
                context_keywords=self.extract_keywords(query),
                reasoning=reasoning
            )
        else:
            # Use the original domain-specific result (already calculated)
            result = original_result
        
        # Store in selection history for learning
        self.selection_history.append((query, result))
        
        # Keep history to reasonable size
        if len(self.selection_history) > 1000:
            self.selection_history = self.selection_history[-500:]
        
        return result
    
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
        
        # Select best agent or fallback
        if agent_scores and agent_scores[0]['score'] > 0.5:
            best_agent = agent_scores[0]
            # Improved confidence score calculation for better domain handling
            base_confidence = best_agent['score'] / 4.5  # Better normalization for complex patterns
            
            # Boost confidence for infrastructure-engineer due to complex patterns
            if best_agent['name'] == 'infrastructure-engineer':
                if base_confidence > 0.4:  # Lower threshold for boost
                    base_confidence *= 1.25  # 25% boost for infrastructure complexity
                # Ensure minimum confidence for infrastructure matches
                base_confidence = max(base_confidence, 0.5) if best_agent['score'] > 2.0 else base_confidence
            
            # Boost confidence for documentation-enhancer with strong patterns
            elif best_agent['name'] == 'documentation-enhancer':
                if base_confidence > 0.2:  # Lower threshold for documentation boost
                    base_confidence *= 1.5  # 50% boost for documentation patterns
                # Ensure high minimum confidence for documentation matches
                if best_agent['score'] > 1.0:
                    base_confidence = max(base_confidence, 0.75)  # Higher minimum confidence
                elif best_agent['score'] > 0.5:
                    base_confidence = max(base_confidence, 0.65)  # Medium minimum confidence
            
            # Boost confidence for security-enforcer with strong patterns
            elif best_agent['name'] == 'security-enforcer':
                if base_confidence > 0.2:  # Lower threshold for security boost
                    base_confidence *= 1.4  # 40% boost for security patterns
                # Ensure high minimum confidence for security matches
                if best_agent['score'] > 1.0:
                    base_confidence = max(base_confidence, 0.80)  # Higher minimum confidence
                elif best_agent['score'] > 0.5:
                    base_confidence = max(base_confidence, 0.70)  # Medium minimum confidence
                
            confidence_score = min(1.0, base_confidence)
            reasoning = f"Pattern-based selection: {len(best_agent['matched_patterns'])} pattern matches"
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
            return {}
        
        agent_counts = Counter(result.agent_name for _, result in self.selection_history)
        avg_confidence = sum(result.confidence_score for _, result in self.selection_history) / len(self.selection_history)
        avg_processing_time = sum(result.processing_time_ms for _, result in self.selection_history) / len(self.selection_history)
        
        # Cross-domain analysis statistics
        cross_domain_stats = {}
        if self.cross_domain_coordinator:
            try:
                cross_domain_stats = self.cross_domain_coordinator.get_analysis_stats()
            except Exception as e:
                logger.warning(f"Failed to get cross-domain stats: {e}")
        
        base_stats = {
            'total_selections': len(self.selection_history),
            'agent_distribution': dict(agent_counts),
            'average_confidence': avg_confidence,
            'average_processing_time_ms': avg_processing_time,
            'most_selected_agent': agent_counts.most_common(1)[0] if agent_counts else None
        }
        
        if cross_domain_stats:
            base_stats['cross_domain_analysis'] = cross_domain_stats
            
        # Add learning insights if available
        if self.cross_domain_coordinator:
            try:
                learning_insights = self.cross_domain_coordinator.get_learning_insights()
                if learning_insights:
                    base_stats['learning_insights'] = learning_insights
            except Exception as e:
                logger.warning(f"Failed to get learning insights: {e}")
        
        return base_stats
        
    def record_feedback(self, query: str, selected_agent: str, confidence: float, 
                       user_feedback: Optional[bool] = None, expected_agent: Optional[str] = None):
        """Record user feedback for learning improvement."""
        if self.cross_domain_coordinator:
            try:
                self.cross_domain_coordinator.record_selection_feedback(
                    query, selected_agent, confidence, user_feedback, expected_agent
                )
            except Exception as e:
                logger.warning(f"Failed to record feedback: {e}")
    
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
