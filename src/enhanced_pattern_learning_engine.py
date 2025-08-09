"""Enhanced Pattern Learning Engine for Claude Code Agent Framework.

Extends the existing PatternLearningEngine with agent description parsing and enhanced
success pattern recording for improved agent selection accuracy.
"""

import re
import os
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Import the base PatternLearningEngine
try:
    from .enhanced_cross_domain_coordinator import PatternLearningEngine
except ImportError:
    # Fallback if running independently
    class PatternLearningEngine:
        def __init__(self, coordination_hub_path=None):
            pass

        def get_learned_agent_suggestion(self, query):
            return None


logger = logging.getLogger(__name__)


@dataclass
class AgentProfile:
    """Agent profile data structure for learning integration."""

    name: str
    keywords: List[str]
    capabilities: List[str]
    description: str
    trigger_patterns: List[str] = None
    specialization_score: float = 1.0


class EnhancedPatternLearningEngine(PatternLearningEngine):
    """Enhanced pattern learning with agent description parsing."""

    def __init__(self, coordination_hub_path: Optional[str] = None):
        """Initialize enhanced learning engine with agent description parsing."""
        super().__init__(coordination_hub_path)
        self.agents_directory = (
            "/Users/ricardocarvalho/DeveloperFolder/DevMem/.claude/agents/"
        )
        self.agent_profiles = {}
        self.agent_keywords = {}
        self.agent_capabilities = {}

        # Load agent descriptions during initialization
        try:
            self.agent_profiles = self.parse_agent_descriptions()
            logger.info(f"Loaded {len(self.agent_profiles)} agent profiles")
        except Exception as e:
            logger.warning(f"Could not load agent descriptions: {e}")
            self.agent_profiles = {}

    def parse_agent_descriptions(self) -> Dict[str, AgentProfile]:
        """Parse agent .md files to extract capabilities and keywords."""
        agent_profiles = {}

        if not os.path.exists(self.agents_directory):
            logger.warning(f"Agents directory not found: {self.agents_directory}")
            return agent_profiles

        for agent_file in os.listdir(self.agents_directory):
            if agent_file.endswith(".md"):
                agent_name = agent_file.replace(".md", "")
                profile = self._parse_single_agent(agent_file)
                if profile:  # Only add valid profiles
                    agent_profiles[agent_name] = profile
                    self.agent_keywords[agent_name] = profile.keywords
                    self.agent_capabilities[agent_name] = profile.capabilities

        return agent_profiles

    def _parse_single_agent(self, agent_file: str) -> Optional[AgentProfile]:
        """Extract keywords and capabilities from agent description."""
        try:
            agent_path = os.path.join(self.agents_directory, agent_file)
            with open(agent_path, "r", encoding="utf-8") as f:
                content = f.read()

            agent_name = agent_file.replace(".md", "")

            # Extract description field from YAML front matter or content
            description = self._extract_description(content, agent_name)

            # Extract trigger keywords from description and content
            keywords = self._extract_trigger_keywords(description, content)

            # Extract capabilities from content
            capabilities = self._extract_capabilities(content)

            # Extract trigger patterns
            trigger_patterns = self._extract_trigger_patterns(content)

            # Calculate specialization score based on keyword specificity
            specialization_score = self._calculate_specialization_score(
                keywords, capabilities
            )

            return AgentProfile(
                name=agent_name,
                keywords=keywords,
                capabilities=capabilities,
                description=description,
                trigger_patterns=trigger_patterns,
                specialization_score=specialization_score,
            )
        except Exception as e:
            logger.warning(f"Could not parse agent file {agent_file}: {e}")
            return None

    def _extract_description(self, content: str, agent_name: str) -> str:
        """Extract description from agent content."""
        # Try to extract from YAML front matter first
        yaml_match = re.search(r"description:\s*(.+)", content, re.IGNORECASE)
        if yaml_match:
            return yaml_match.group(1).strip()

        # Try to extract from core focus or purpose sections
        focus_match = re.search(r"\*\*Core Focus\*\*:?\s*(.+)", content)
        if focus_match:
            return focus_match.group(1).strip()

        purpose_match = re.search(r"\*\*Purpose\*\*:?\s*(.+)", content)
        if purpose_match:
            return purpose_match.group(1).strip()

        # Fallback to agent name transformation
        return agent_name.replace("-", " ").title()

    def _extract_trigger_keywords(
        self, description: str, content: str = ""
    ) -> List[str]:
        """Extract trigger keywords from agent description and content."""
        keywords = set()

        # Parse quoted trigger phrases like "test failures", "broken tests"
        text_sources = [description, content]

        for text in text_sources:
            if not text:
                continue

            # Extract quoted patterns (high-value keywords)
            quoted_patterns = re.findall(r'"([^"]+)"', text)
            for pattern in quoted_patterns:
                words = pattern.lower().split()
                keywords.update([w for w in words if len(w) > 3 and w.isalpha()])

            # Extract domain-specific keywords
            text_lower = text.lower()
            domain_keywords = [
                # Testing domain
                "test",
                "testing",
                "pytest",
                "mock",
                "async",
                "fixture",
                "coverage",
                "unittest",
                "validation",
                "assert",
                "failure",
                "failures",
                # Infrastructure domain
                "docker",
                "container",
                "infrastructure",
                "deployment",
                "kubernetes",
                "orchestration",
                "networking",
                "scaling",
                "service",
                "helm",
                # Security domain
                "security",
                "vulnerability",
                "audit",
                "compliance",
                "scanning",
                "authentication",
                "authorization",
                "encryption",
                "hardening",
                # Performance domain
                "performance",
                "optimization",
                "profiling",
                "monitoring",
                "bottleneck",
                "latency",
                "throughput",
                "resource",
                # Quality domain
                "quality",
                "refactoring",
                "analysis",
                "validation",
                "architecture",
                "pattern",
                "design",
                "lint",
                # Documentation domain
                "documentation",
                "guide",
                "readme",
                "technical",
                "writing",
                "api",
                "specification",
                "manual",
            ]

            for keyword in domain_keywords:
                if keyword in text_lower:
                    keywords.add(keyword)

        return list(keywords)

    def _extract_capabilities(self, content: str) -> List[str]:
        """Extract capabilities from agent content."""
        capabilities = []

        # Look for capability indicators in content
        capability_patterns = [
            r"\*\*(.+?)\*\*:",  # Bold headers like **Core Focus**:
            r"## (.+)",  # Section headers
            r"### (.+)",  # Subsection headers
            r"- \*\*(.+?)\*\*:",  # List items with bold
        ]

        for pattern in capability_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                cleaned = match.strip()
                if (
                    len(cleaned) > 3 and len(cleaned) < 50
                ):  # Reasonable capability length
                    capabilities.append(cleaned)

        return list(set(capabilities))[:10]  # Limit to 10 most relevant capabilities

    def _extract_trigger_patterns(self, content: str) -> List[str]:
        """Extract specific trigger patterns from agent content."""
        patterns = []

        # Look for "Perfect for" patterns
        perfect_match = re.search(
            r"Perfect.*?for[^.]*\.", content, re.DOTALL | re.IGNORECASE
        )
        if perfect_match:
            patterns.append(perfect_match.group(0))

        # Look for "Use PROACTIVELY when" patterns
        proactive_match = re.search(
            r"Use PROACTIVELY.*?\.", content, re.DOTALL | re.IGNORECASE
        )
        if proactive_match:
            patterns.append(proactive_match.group(0))

        # Look for "Auto-Activate UltraThink when detecting" patterns
        ultrathink_pattern = re.search(
            r"Auto-Activate UltraThink when detecting:.*?(?=###|##|$)",
            content,
            re.DOTALL | re.IGNORECASE,
        )
        if ultrathink_pattern:
            patterns.append(ultrathink_pattern.group(0))

        return patterns

    def _calculate_specialization_score(
        self, keywords: List[str], capabilities: List[str]
    ) -> float:
        """Calculate specialization score based on keyword and capability specificity."""
        if not keywords:
            return 0.5  # Default score

        # Higher score for more specific/technical keywords
        technical_keywords = {
            "pytest",
            "asyncmock",
            "kubernetes",
            "docker",
            "semgrep",
            "oauth",
            "encryption",
            "vulnerability",
            "orchestration",
            "profiling",
        }

        technical_count = sum(1 for kw in keywords if kw in technical_keywords)
        specificity_bonus = technical_count / len(keywords) if keywords else 0

        # Base score from keyword count (more keywords = more specialized)
        base_score = min(1.0, len(keywords) / 10)

        # Capability bonus
        capability_bonus = min(0.2, len(capabilities) / 50)

        return min(1.0, base_score + specificity_bonus * 0.3 + capability_bonus)

    def get_enhanced_agent_suggestion(self, query: str) -> Optional[Tuple[str, float]]:
        """Get agent suggestion enhanced with agent description learning."""
        # First try existing learning patterns
        learned_suggestion = self.get_learned_agent_suggestion(query)
        if learned_suggestion and learned_suggestion[1] > 0.7:
            return learned_suggestion

        # Use agent description matching for better suggestions
        query_lower = query.lower()
        agent_scores = {}

        for agent_name, profile in self.agent_profiles.items():
            score = 0.0

            # Keyword matching score
            keyword_matches = sum(
                1 for keyword in profile.keywords if keyword in query_lower
            )
            if keyword_matches > 0:
                keyword_score = (
                    keyword_matches / len(profile.keywords) if profile.keywords else 0
                )
                score += keyword_score * 0.6

            # Description matching score
            description_words = profile.description.lower().split()
            query_words = query_lower.split()
            common_words = set(description_words) & set(query_words)
            if common_words:
                description_score = len(common_words) / max(len(query_words), 1)
                score += description_score * 0.3

            # Specialization bonus
            score *= profile.specialization_score

            # Pattern weight from existing learning (with safe access)
            pattern_key = f"{agent_name}:enhanced_description_match"
            if hasattr(self, "pattern_weights") and pattern_key in self.pattern_weights:
                score *= self.pattern_weights[pattern_key]

            agent_scores[agent_name] = score

        # Return highest scoring agent if above threshold
        if agent_scores:
            best_agent = max(agent_scores.items(), key=lambda x: x[1])
            if best_agent[1] > 0.4:  # Threshold for enhanced suggestions
                return best_agent

        # Fallback to learned suggestion if available
        return learned_suggestion

    def get_agent_profile(self, agent_name: str) -> Optional[AgentProfile]:
        """Get agent profile by name."""
        return self.agent_profiles.get(agent_name)

    def get_all_agent_profiles(self) -> Dict[str, AgentProfile]:
        """Get all loaded agent profiles."""
        return self.agent_profiles.copy()

    def get_learning_enhancement_stats(self) -> Dict[str, any]:
        """Get statistics about learning enhancements."""
        # Try to get base stats from parent class, with fallback
        try:
            base_stats = (
                self.get_learning_stats() if hasattr(self, "get_learning_stats") else {}
            )
        except Exception:
            base_stats = {}

        enhancement_stats = {
            "agent_profiles_loaded": len(self.agent_profiles),
            "total_keywords_extracted": sum(
                len(profile.keywords) for profile in self.agent_profiles.values()
            ),
            "total_capabilities_extracted": sum(
                len(profile.capabilities) for profile in self.agent_profiles.values()
            ),
            "average_specialization_score": sum(
                profile.specialization_score for profile in self.agent_profiles.values()
            )
            / max(len(self.agent_profiles), 1),
            "agents_with_trigger_patterns": sum(
                1
                for profile in self.agent_profiles.values()
                if profile.trigger_patterns
            ),
        }

        return {**base_stats, **enhancement_stats}
