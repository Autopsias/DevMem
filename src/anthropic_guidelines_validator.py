"""Anthropic Guidelines Validator for Claude Code Agent Framework.

Validates learning patterns against Anthropic sub-agent guidelines to ensure
compliance with recommended practices.
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of pattern validation against Anthropic guidelines."""
    is_compliant: bool
    compliance_score: float  # 0.0 to 1.0
    issues: List[str]
    recommendations: List[str]
    category: str  # compliance category


class AnthropicGuidelinesValidator:
    """Validate learning patterns against Anthropic sub-agent guidelines."""
    
    def __init__(self):
        """Initialize the guidelines validator."""
        # Anthropic sub-agent guidelines compliance criteria
        self.guidelines_criteria = {
            'sub_agent_spawning': {
                'max_parallel_agents': 10,  # From Claude Code documentation
                'proper_task_definition': True,
                'clear_context_passing': True,
                'result_synthesis': True
            },
            'agent_selection': {
                'natural_language_triggers': True,
                'appropriate_specialization': True,
                'avoid_over_coordination': True,
                'maintain_context_flow': True
            },
            'learning_patterns': {
                'based_on_success_metrics': True,
                'validate_agent_capability_match': True,
                'respect_agent_boundaries': True,
                'avoid_circular_dependencies': True
            }
        }
        
        # Known agent capabilities mapping
        self.agent_capabilities = {
            'test-specialist': ['test', 'testing', 'pytest', 'mock', 'async', 'coverage', 'fixture'],
            'infrastructure-engineer': ['docker', 'kubernetes', 'deployment', 'infrastructure', 'container', 'orchestration'],
            'security-enforcer': ['security', 'vulnerability', 'compliance', 'audit', 'scanning'],
            'performance-optimizer': ['performance', 'optimization', 'profiling', 'bottleneck', 'latency'],
            'documentation-enhancer': ['documentation', 'readme', 'guide', 'technical', 'writing', 'api'],
            'intelligent-enhancer': ['refactoring', 'code', 'quality', 'improvement', 'analysis'],
            'digdeep': ['analysis', 'root', 'cause', 'systematic', 'investigation'],
            'meta-coordinator': ['coordination', 'orchestration', 'multi-domain', 'complex']
        }
        
        # Compliance thresholds
        self.compliance_thresholds = {
            'excellent': 0.9,
            'good': 0.8,
            'acceptable': 0.7,
            'needs_improvement': 0.6
        }
    
    def validate_learning_pattern(self, pattern: Dict) -> ValidationResult:
        """Validate learning pattern against Anthropic guidelines."""
        issues = []
        recommendations = []
        compliance_score = 1.0
        
        # Extract pattern information
        agent_name = pattern.get('agent', '')
        keywords = pattern.get('keywords', [])
        confidence = pattern.get('confidence', 0.0)
        pattern_key = pattern.get('pattern_key', '')
        
        # Validation 1: Agent capability match
        capability_match_score = self._validate_agent_capability_match(agent_name, keywords)
        if capability_match_score < 0.7:
            issues.append(f"Agent {agent_name} may not be optimal for keywords: {keywords}")
            recommendations.append(f"Consider reviewing agent selection for pattern {pattern_key}")
            compliance_score -= 0.2
        
        # Validation 2: Pattern quality
        if len(keywords) < 2:
            issues.append("Insufficient context keywords for reliable pattern matching")
            recommendations.append("Add more specific keywords to improve pattern accuracy")
            compliance_score -= 0.15
        
        # Validation 3: Confidence threshold
        if confidence < 0.7:
            issues.append(f"Pattern confidence {confidence:.2f} is below recommended threshold")
            recommendations.append("Only record patterns with confidence >= 0.7 for reliable learning")
            compliance_score -= 0.1
        
        # Validation 4: Avoid over-specialization
        if len(keywords) > 8:
            issues.append("Pattern may be over-specialized with too many keywords")
            recommendations.append("Focus on 3-5 core keywords for better pattern generalization")
            compliance_score -= 0.1
        
        # Validation 5: Check for circular patterns
        if self._has_circular_dependency(pattern_key, agent_name):
            issues.append("Pattern may create circular agent dependencies")
            recommendations.append("Review coordination flow to avoid agent selection loops")
            compliance_score -= 0.25
        
        # Calculate final compliance
        compliance_score = max(0.0, min(1.0, compliance_score))
        is_compliant = compliance_score >= self.compliance_thresholds['acceptable']
        
        # Determine compliance category
        if compliance_score >= self.compliance_thresholds['excellent']:
            category = 'excellent'
        elif compliance_score >= self.compliance_thresholds['good']:
            category = 'good'
        elif compliance_score >= self.compliance_thresholds['acceptable']:
            category = 'acceptable'
        else:
            category = 'needs_improvement'
        
        return ValidationResult(
            is_compliant=is_compliant,
            compliance_score=compliance_score,
            issues=issues,
            recommendations=recommendations,
            category=category
        )
    
    def _validate_agent_capability_match(self, agent_name: str, keywords: List[str]) -> float:
        """Validate that learned pattern matches agent's actual capabilities."""
        if not agent_name or not keywords:
            return 0.0
            
        expected_capabilities = self.agent_capabilities.get(agent_name, [])
        if not expected_capabilities:
            # Unknown agent - assume moderate match
            return 0.6
        
        # Calculate keyword overlap with agent capabilities
        keyword_matches = sum(1 for keyword in keywords 
                            if any(keyword in capability or capability in keyword 
                                 for capability in expected_capabilities))
        
        if not keywords:
            return 0.0
            
        # Score based on percentage of keywords that match agent capabilities
        match_ratio = keyword_matches / len(keywords)
        
        # Bonus for having at least one strong match
        strong_matches = sum(1 for keyword in keywords 
                           if keyword in expected_capabilities)
        strong_match_bonus = 0.2 if strong_matches > 0 else 0
        
        return min(1.0, match_ratio + strong_match_bonus)
    
    def _has_circular_dependency(self, pattern_key: str, agent_name: str) -> bool:
        """Check if pattern creates circular agent dependencies."""
        # Simple heuristic: check for patterns that might cause loops
        circular_indicators = [
            'meta-coordinator:meta-coordinator',  # Meta-coordinator selecting itself
            'analysis-gateway:analysis-gateway',  # Analysis-gateway selecting itself
        ]
        
        pattern_signature = f"{agent_name}:{agent_name}"
        return pattern_signature in circular_indicators
    
    def validate_pattern_collection(self, patterns: List[Dict]) -> Dict[str, any]:
        """Validate a collection of learning patterns."""
        if not patterns:
            return {
                'total_patterns': 0,
                'compliant_patterns': 0,
                'compliance_rate': 0.0,
                'category_distribution': {},
                'common_issues': [],
                'overall_compliance': False
            }
        
        results = []
        category_counts = {'excellent': 0, 'good': 0, 'acceptable': 0, 'needs_improvement': 0}
        all_issues = []
        
        for pattern in patterns:
            result = self.validate_learning_pattern(pattern)
            results.append(result)
            category_counts[result.category] += 1
            all_issues.extend(result.issues)
        
        # Calculate overall metrics
        compliant_patterns = sum(1 for r in results if r.is_compliant)
        compliance_rate = compliant_patterns / len(patterns) if patterns else 0.0
        avg_compliance_score = sum(r.compliance_score for r in results) / len(results)
        
        # Find common issues
        issue_frequency = {}
        for issue in all_issues:
            # Normalize issue text for counting
            normalized_issue = issue.split('.')[0]  # Take first sentence
            issue_frequency[normalized_issue] = issue_frequency.get(normalized_issue, 0) + 1
        
        common_issues = sorted(issue_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_patterns': len(patterns),
            'compliant_patterns': compliant_patterns,
            'compliance_rate': compliance_rate,
            'average_compliance_score': avg_compliance_score,
            'category_distribution': category_counts,
            'common_issues': [{'issue': issue, 'frequency': freq} for issue, freq in common_issues],
            'overall_compliance': compliance_rate >= self.compliance_thresholds['acceptable'],
            'anthropic_guidelines_met': compliance_rate >= 0.8  # 80% minimum for full compliance
        }
    
    def generate_compliance_report(self, patterns: List[Dict]) -> str:
        """Generate a detailed compliance report."""
        validation_results = self.validate_pattern_collection(patterns)
        
        report = f"""# Anthropic Guidelines Compliance Report

## Summary
- **Total Patterns Analyzed**: {validation_results['total_patterns']}
- **Compliant Patterns**: {validation_results['compliant_patterns']}
- **Compliance Rate**: {validation_results['compliance_rate']:.1%}
- **Average Compliance Score**: {validation_results['average_compliance_score']:.3f}
- **Overall Compliance Status**: {"✅ COMPLIANT" if validation_results['overall_compliance'] else "❌ NEEDS IMPROVEMENT"}

## Category Distribution
"""
        
        for category, count in validation_results['category_distribution'].items():
            percentage = count / validation_results['total_patterns'] * 100 if validation_results['total_patterns'] > 0 else 0
            report += f"- **{category.title()}**: {count} patterns ({percentage:.1f}%)\n"
        
        report += "\n## Common Issues\n"
        if validation_results['common_issues']:
            for issue_data in validation_results['common_issues']:
                report += f"- {issue_data['issue']} (occurred {issue_data['frequency']} times)\n"
        else:
            report += "No common issues identified.\n"
        
        report += f"\n## Recommendations\n"
        if validation_results['compliance_rate'] < 0.8:
            report += "- Focus on improving agent-keyword matching accuracy\n"
            report += "- Increase pattern confidence thresholds to >= 0.7\n"
            report += "- Review patterns with insufficient context keywords\n"
        else:
            report += "- Current patterns show good compliance with Anthropic guidelines\n"
            report += "- Continue monitoring pattern quality and agent matching accuracy\n"
        
        return report
    
    def get_compliance_thresholds(self) -> Dict[str, float]:
        """Get current compliance thresholds."""
        return self.compliance_thresholds.copy()
    
    def update_agent_capabilities(self, agent_name: str, capabilities: List[str]) -> None:
        """Update known capabilities for an agent."""
        self.agent_capabilities[agent_name] = capabilities
        logger.info(f"Updated capabilities for agent {agent_name}: {capabilities}")
